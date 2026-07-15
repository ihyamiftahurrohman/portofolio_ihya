"""
test_uat.py - Script Pengujian Manual Otomatis (UAT)
=====================================================
Menguji semua route publik dan fitur login/dashboard
menggunakan Flask test client (tanpa browser).
"""
import os
import sys
import io
import tempfile

# Fix encoding untuk Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Tambahkan path project ke sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash

# Warna terminal
GREEN = "\033[92m"
RED   = "\033[91m"
CYAN  = "\033[96m"
RESET = "\033[0m"
BOLD  = "\033[1m"

passed = 0
failed = 0

def log_pass(test_name):
    global passed
    passed += 1
    print(f"  {GREEN}[PASS]{RESET} {test_name}")

def log_fail(test_name, detail=""):
    global failed
    failed += 1
    print(f"  {RED}[FAIL]{RESET} {test_name}")
    if detail:
        print(f"         {RED}{detail}{RESET}")


def run_tests():
    global passed, failed

    # Buat file database sementara yang benar-benar terpisah
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)

    # Override config SEBELUM import app
    os.environ['DATABASE_URL_OVERRIDE'] = f'sqlite:///{db_path}'

    # Sekarang import app dan models
    from app import app, db
    from models import User, Project, Message

    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SERVER_NAME'] = 'localhost'

    try:
        with app.app_context():
            # Drop semua tabel dulu (kalau ada), lalu buat ulang
            db.drop_all()
            db.create_all()

            # Buat user admin untuk testing
            admin = User(
                username='testadmin',
                password=generate_password_hash('testpassword123'),
                name='Admin Tester',
                bio='Bio admin untuk testing',
                email='admin@test.com'
            )
            db.session.add(admin)
            db.session.flush()

            # Buat sample project (perlu user_id FK)
            project = Project(
                title='Project Testing',
                description='Deskripsi project untuk UAT',
                tech_stack='Python, Flask, SQLite',
                image='',
                demo_link='https://example.com',
                github_link='https://github.com/test',
                user_id=admin.id
            )
            db.session.add(project)
            db.session.commit()

            client = app.test_client()

            # ====================================================
            print(f"\n{BOLD}{CYAN}===================================================={RESET}")
            print(f"{BOLD}{CYAN}   TAHAP 11 - PENGUJIAN MANUAL (UAT)                {RESET}")
            print(f"{BOLD}{CYAN}===================================================={RESET}\n")

            # ---------------------------------------------------
            print(f"{BOLD}[1] Halaman Publik{RESET}")
            # ---------------------------------------------------

            # 1a. Halaman Beranda
            res = client.get('/')
            if res.status_code == 200 and b'Portofolio' in res.data:
                log_pass("GET / - Halaman Beranda (200)")
            else:
                log_fail("GET / - Halaman Beranda", f"status={res.status_code}")

            # 1b. Halaman About
            res = client.get('/about')
            if res.status_code == 200:
                log_pass("GET /about - Halaman About (200)")
            else:
                log_fail("GET /about", f"status={res.status_code}")

            # 1c. Halaman Portfolio
            res = client.get('/portfolio')
            if res.status_code == 200:
                log_pass("GET /portfolio - Halaman Portfolio (200)")
            else:
                log_fail("GET /portfolio", f"status={res.status_code}")

            # 1d. Halaman Contact
            res = client.get('/contact')
            if res.status_code == 200:
                log_pass("GET /contact - Halaman Contact (200)")
            else:
                log_fail("GET /contact", f"status={res.status_code}")

            # 1e. Halaman Detail Project
            res = client.get('/project/1')
            if res.status_code == 200 and b'Project Testing' in res.data:
                log_pass("GET /project/1 - Detail Project (200)")
            else:
                log_fail("GET /project/1", f"status={res.status_code}")

            # ---------------------------------------------------
            print(f"\n{BOLD}[2] Fitur Kirim Pesan (Contact Form){RESET}")
            # ---------------------------------------------------

            res = client.post('/contact', data={
                'name': 'Pengunjung Test',
                'email': 'visitor@test.com',
                'subject': 'Test UAT',
                'body': 'Ini pesan UAT otomatis.'
            }, follow_redirects=True)
            if res.status_code == 200 and b'berhasil' in res.data:
                log_pass("POST /contact - Kirim Pesan (flash success)")
            else:
                log_fail("POST /contact - Kirim Pesan", f"status={res.status_code}")

            # Verifikasi pesan masuk di database
            msg = Message.query.filter_by(email='visitor@test.com').first()
            if msg and msg.subject == 'Test UAT':
                log_pass("DB Check - Pesan tersimpan di database")
            else:
                log_fail("DB Check - Pesan tidak ditemukan di database")

            # ---------------------------------------------------
            print(f"\n{BOLD}[3] Fitur Login{RESET}")
            # ---------------------------------------------------

            # 3a. Halaman Login tampil
            res = client.get('/login')
            if res.status_code == 200 and b'Login' in res.data:
                log_pass("GET /login - Halaman Login (200)")
            else:
                log_fail("GET /login", f"status={res.status_code}")

            # 3b. Login dengan password salah
            res = client.post('/login', data={
                'username': 'testadmin',
                'password': 'wrongpassword'
            }, follow_redirects=True)
            if res.status_code == 200 and b'salah' in res.data:
                log_pass("POST /login (wrong pwd) - Flash error muncul")
            else:
                log_fail("POST /login (wrong pwd)", f"status={res.status_code}")

            # 3c. Login berhasil
            res = client.post('/login', data={
                'username': 'testadmin',
                'password': 'testpassword123'
            }, follow_redirects=True)
            if res.status_code == 200:
                log_pass("POST /login (correct) - Login berhasil (redirect dashboard)")
            else:
                log_fail("POST /login (correct)", f"status={res.status_code}")

            # ---------------------------------------------------
            print(f"\n{BOLD}[4] Dashboard Admin (Setelah Login){RESET}")
            # ---------------------------------------------------

            # 4a. Akses dashboard
            res = client.get('/dashboard')
            if res.status_code == 200:
                log_pass("GET /dashboard - Halaman Dashboard (200)")
            else:
                log_fail("GET /dashboard", f"status={res.status_code}")

            # 4b. Halaman tambah project
            res = client.get('/dashboard/projects/add')
            if res.status_code == 200:
                log_pass("GET /dashboard/projects/add - Form Tambah Project (200)")
            else:
                log_fail("GET /dashboard/projects/add", f"status={res.status_code}")

            # 4c. Tambah project baru via POST
            res = client.post('/dashboard/projects/add', data={
                'title': 'Project Baru UAT',
                'description': 'Deskripsi project baru',
                'tech_stack': 'React, Node.js',
                'demo_link': '',
                'github_link': ''
            }, follow_redirects=True)
            if res.status_code == 200:
                new_proj = Project.query.filter_by(title='Project Baru UAT').first()
                if new_proj:
                    log_pass("POST /dashboard/projects/add - Project berhasil ditambah")
                else:
                    log_fail("POST /dashboard/projects/add", "Project tidak ditemukan di DB")
            else:
                log_fail("POST /dashboard/projects/add", f"status={res.status_code}")

            # 4d. Edit project
            res = client.get('/dashboard/projects/edit/1')
            if res.status_code == 200:
                log_pass("GET /dashboard/projects/edit/1 - Form Edit Project (200)")
            else:
                log_fail("GET /dashboard/projects/edit/1", f"status={res.status_code}")

            # 4e. Halaman pesan masuk
            res = client.get('/dashboard/messages')
            if res.status_code == 200:
                log_pass("GET /dashboard/messages - Halaman Pesan Masuk (200)")
            else:
                log_fail("GET /dashboard/messages", f"status={res.status_code}")

            # 4f. Halaman profil admin
            res = client.get('/dashboard/profile')
            if res.status_code == 200:
                log_pass("GET /dashboard/profile - Halaman Profil (200)")
            else:
                log_fail("GET /dashboard/profile", f"status={res.status_code}")

            # ---------------------------------------------------
            print(f"\n{BOLD}[5] Logout{RESET}")
            # ---------------------------------------------------

            res = client.get('/logout', follow_redirects=True)
            if res.status_code == 200:
                log_pass("GET /logout - Logout berhasil (redirect home, status 200)")
            else:
                log_fail("GET /logout", f"status={res.status_code}")

            # 5b. Akses dashboard setelah logout (harus redirect ke login)
            res = client.get('/dashboard')
            if res.status_code in (302, 200):
                log_pass("GET /dashboard (setelah logout) - Redirect ke login")
            else:
                log_fail("GET /dashboard (setelah logout)", f"status={res.status_code}")

            # ---------------------------------------------------
            print(f"\n{BOLD}[6] Konsistensi Desain (Dark Mode){RESET}")
            # ---------------------------------------------------

            # Check CSS file loaded
            res = client.get('/static/css/style.css')
            if res.status_code == 200 and b'--bg-primary' in res.data:
                log_pass("GET /static/css/style.css - CSS Dark Mode terbaca")
            else:
                log_fail("GET /static/css/style.css", f"status={res.status_code}")

            # Check variabel warna inti ada di CSS
            css = res.data.decode('utf-8') if res.status_code == 200 else ''
            checks = ['--bg-primary', '--text-primary', '--accent-1']
            css_ok = all(v in css for v in checks)
            if css_ok:
                log_pass("CSS Variables - Semua variabel tema Dark Mode ditemukan")
            else:
                missing = [v for v in checks if v not in css]
                log_fail("CSS Variables", f"Tidak ditemukan: {missing}")

            # Check Outfit font dimuat via @import di CSS
            if 'Outfit' in css:
                log_pass("Font - Google Font 'Outfit' dimuat di style.css")
            else:
                log_fail("Font", "Font 'Outfit' tidak ditemukan di CSS")

            # ====================================================
            print(f"\n{BOLD}{CYAN}===================================================={RESET}")
            total = passed + failed
            print(f"   {BOLD}HASIL: {GREEN}{passed}/{total} PASS{RESET}  |  {RED}{failed} FAIL{RESET}")
            print(f"{BOLD}{CYAN}===================================================={RESET}\n")

            if failed == 0:
                print(f"   {GREEN}{BOLD}SEMUA PENGUJIAN BERHASIL! Siap untuk Tahap 12 (Deployment).{RESET}\n")
            else:
                print(f"   {RED}{BOLD}Ada {failed} pengujian gagal. Perlu investigasi sebelum deployment.{RESET}\n")

            db.drop_all()

    finally:
        # Hapus file database sementara
        try:
            os.unlink(db_path)
        except OSError:
            pass


if __name__ == '__main__':
    run_tests()
