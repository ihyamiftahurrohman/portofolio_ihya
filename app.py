"""
app.py - File Utama Aplikasi Flask
===================================
File ini adalah "pintu masuk" (entry point) dari aplikasi.
Semua konfigurasi, inisialisasi, dan route didefinisikan di sini.

Mengapa semua ada di satu file?
- Sesuai dengan struktur tugas yang diberikan dosen
- Untuk project kecil-menengah, satu file sudah cukup
- Lebih mudah dipahami oleh mahasiswa Pengantar Pemrograman

Cara menjalankan:
    python app.py
"""

from flask import Flask, render_template, request, flash, redirect, url_for
from config import Config
from models import db, User, Project, Message
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
from models import db, User, Project, Message

# Fungsi Helper untuk Validasi Ekstensi File
def allowed_file(filename):
    # Memastikan file memiliki titik (.) dan ekstensi ada dalam ALLOWED_EXTENSIONS (config.py)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ============================================
# INISIALISASI APLIKASI
# ============================================

# Membuat instance aplikasi Flask
# __name__ memberi tahu Flask lokasi folder project
app = Flask(__name__)

# Memuat konfigurasi dari class Config di config.py
app.config.from_object(Config)

# Inisialisasi object database dengan aplikasi Flask
db.init_app(app)

# Inisialisasi Flask-Login untuk mengatur sesi (session)
login_manager = LoginManager()
login_manager.init_app(app)
# Jika user belum login tapi mencoba akses halaman admin, arahkan ke route 'login'
login_manager.login_view = 'login'
login_manager.login_message = 'Silakan login terlebih dahulu untuk mengakses halaman ini.'
login_manager.login_message_category = 'warning'

# Fungsi untuk memberi tahu Flask-Login cara mengambil data user berdasarkan ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Membuat semua tabel di database jika belum ada
# app_context() diperlukan agar SQLAlchemy tahu aplikasi Flask mana yang sedang aktif
with app.app_context():
    db.create_all()
    
    # Otomatis buat akun admin jika belum ada
    if not User.query.first():
        admin = User(
            username='admin',
            password=generate_password_hash('admin123'),
            name='Administrator',
            bio='Saya adalah seorang Web Developer.',
            email='admin@portofolio.com'
        )
        db.session.add(admin)
        db.session.commit()
        print("Akun Admin default berhasil dibuat (admin / admin123)")


# ============================================
# ROUTE - HALAMAN PUBLIK (FRONTEND)
# ============================================

@app.route('/')
def index():
    """Halaman Home - Landing page utama"""
    # Mengambil data user pertama (karena ini portofolio tunggal)
    user = User.query.first()
    # Mengambil 3 project terbaru berdasarkan tanggal
    projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
    # Meneruskan variabel user dan projects ke dalam file HTML
    return render_template('index.html', user=user, projects=projects)

@app.route('/about')
def about():
    """Halaman About - Profil lengkap"""
    user = User.query.first()
    return render_template('about.html', user=user)

@app.route('/portfolio')
def portfolio():
    """Halaman Portfolio - Daftar semua project"""
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('portfolio.html', projects=projects)

@app.route('/project/<int:id>')
def project_detail(id):
    """Halaman Detail Project - Menampilkan satu project spesifik"""
    # get_or_404 akan otomatis menampilkan halaman error 404 jika ID project tidak ada di database
    project = Project.query.get_or_404(id)
    return render_template('project_detail.html', project=project)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Halaman Contact - Form kirim pesan"""
    if request.method == 'POST':
        # Mengambil data dari form HTML berdasarkan atribut 'name'
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        body = request.form.get('body')
        
        # Menyimpan data pesan baru ke database
        new_message = Message(name=name, email=email, subject=subject, body=body)
        db.session.add(new_message)
        db.session.commit()
        
        # Menampilkan pesan sukses ke pengunjung
        # Fitur flash Flask membutuhkan SECRET_KEY (sudah kita atur di config.py)
        flash('Pesan Anda berhasil dikirim! Terima kasih telah menghubungi kami.', 'success')
        
        # Redirect (pindah) kembali ke halaman contact agar form kosong kembali
        return redirect(url_for('contact'))
        
    # Jika method GET (hanya membuka halaman)
    return render_template('contact.html')


# ============================================
# ROUTE - AUTENTIKASI (LOGIN & LOGOUT)
# ============================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Halaman Login Admin"""
    # Jika user sudah login, langsung tendang ke dashboard (tidak usah login lagi)
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Mencari user di database berdasarkan username
        user = User.query.filter_by(username=username).first()
        
        # Jika user ditemukan DAN password yang di-hash cocok dengan yang diinput
        if user and check_password_hash(user.password, password):
            # Daftarkan session login user tersebut
            login_user(user)
            flash('Login berhasil! Selamat datang di Dashboard.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah.', 'danger')
            
    return render_template('dashboard/login.html')

@app.route('/logout')
@login_required
def logout():
    """Proses Logout Admin"""
    logout_user() # Menghapus sesi (session) user
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('index'))


# ============================================
# ROUTE - DASHBOARD ADMIN (TAHAP 6)
# ============================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Halaman Utama Dashboard & Statistik"""
    # Menghitung jumlah data di database menggunakan count()
    total_projects = Project.query.count()
    total_messages = Message.query.count()
    unread_messages = Message.query.filter_by(is_read=False).count()
    
    return render_template('dashboard/index.html', 
                           total_projects=total_projects,
                           total_messages=total_messages,
                           unread_messages=unread_messages)

# ============================================
# ROUTE - CRUD PROJECT (TAHAP 7)
# ============================================

@app.route('/dashboard/projects')
@login_required
def dashboard_projects():
    """Melihat daftar seluruh project (READ)"""
    # Ambil semua project, urutkan dari yang terbaru
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('dashboard/projects.html', projects=projects)

@app.route('/dashboard/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    """Menambah project baru (CREATE) beserta Upload Gambar"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tech_stack = request.form.get('tech_stack')
        demo_link = request.form.get('demo_link')
        github_link = request.form.get('github_link')
        
        # Mengelola Upload Gambar
        image_filename = None
        # Cek apakah form mengirimkan file gambar
        if 'image' in request.files:
            file = request.files['image']
            # Jika admin benar-benar memilih file (filename tidak kosong)
            if file and file.filename != '':
                # Validasi tipe file
                if allowed_file(file.filename):
                    # Amankan nama file (contoh: "Foto Keren.jpg" jadi "Foto_Keren.jpg")
                    filename = secure_filename(file.filename)
                    # Simpan ke folder statis (UPLOAD_FOLDER)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filename = filename # Simpan nama file ke variabel untuk database
                else:
                    flash('Format gambar tidak valid. Gunakan jpg, jpeg, png, atau gif.', 'danger')
                    return redirect(request.url)
        
        # Simpan seluruh data ke database
        new_project = Project(
            title=title,
            description=description,
            image=image_filename,
            tech_stack=tech_stack,
            demo_link=demo_link,
            github_link=github_link,
            user_id=current_user.id
        )
        db.session.add(new_project)
        db.session.commit()
        
        flash('Project berhasil ditambahkan!', 'success')
        return redirect(url_for('dashboard_projects'))
        
    return render_template('dashboard/add_project.html')

@app.route('/dashboard/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    """Mengedit project yang sudah ada (UPDATE) beserta Upload Gambar"""
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.tech_stack = request.form.get('tech_stack')
        project.demo_link = request.form.get('demo_link')
        project.github_link = request.form.get('github_link')
        
        # Mengelola Upload Gambar (Hanya memperbarui jika ada gambar baru yang dipilih)
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    project.image = filename # Timpa data lama dengan gambar baru
                else:
                    flash('Format gambar tidak valid. Gunakan jpg, jpeg, png, atau gif.', 'danger')
                    return redirect(request.url)
        
        db.session.commit()
        flash('Project berhasil diperbarui!', 'success')
        return redirect(url_for('dashboard_projects'))
        
    return render_template('dashboard/edit_project.html', project=project)

@app.route('/dashboard/projects/delete/<int:id>')
@login_required
def delete_project(id):
    """Menghapus project (DELETE)"""
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    
    flash('Project berhasil dihapus!', 'success')
    return redirect(url_for('dashboard_projects'))


# ROUTE DUMMY (Akan dilengkapi pada Tahap 9 dan 10)

# ============================================
# ROUTE - KOTAK MASUK / PESAN (TAHAP 10)
# ============================================

@app.route('/dashboard/messages')
@login_required
def dashboard_messages():
    """Halaman Melihat Seluruh Pesan Masuk"""
    # Mengambil semua pesan dari pengunjung, diurutkan dari yang terbaru
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('dashboard/messages.html', messages=messages)

@app.route('/dashboard/messages/read/<int:id>')
@login_required
def read_message(id):
    """Menandai pesan sebagai sudah dibaca"""
    message = Message.query.get_or_404(id)
    message.is_read = True # Ubah status dari False menjadi True
    db.session.commit()
    flash('Pesan telah ditandai sebagai sudah dibaca.', 'success')
    return redirect(url_for('dashboard_messages'))

@app.route('/dashboard/messages/delete/<int:id>')
@login_required
def delete_message(id):
    """Menghapus pesan masuk secara permanen"""
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Pesan berhasil dihapus.', 'success')
    return redirect(url_for('dashboard_messages'))

@app.route('/dashboard/profile', methods=['GET', 'POST'])
@login_required
def dashboard_profile():
    """Halaman Edit Profil Admin & Skill"""
    # Mengambil data user yang sedang login dari database
    user = User.query.get(current_user.id)
    
    if request.method == 'POST':
        # Memperbarui data teks
        user.name = request.form.get('name')
        user.bio = request.form.get('bio')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        user.address = request.form.get('address')
        user.skills = request.form.get('skills')
        user.github = request.form.get('github')
        user.linkedin = request.form.get('linkedin')
        user.instagram = request.form.get('instagram')
        
        # Cek jika ada upload foto profil baru
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Menambahkan kata 'profile_' dan ID user agar nama file unik
                    filename = f"profile_{current_user.id}_{filename}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    user.photo = filename # Timpa dengan foto baru
                else:
                    flash('Format foto tidak valid. Gunakan jpg, jpeg, png, atau gif.', 'danger')
                    return redirect(request.url)
                    
        # Simpan perubahan ke database
        db.session.commit()
        flash('Profil berhasil diperbarui!', 'success')
        return redirect(url_for('dashboard_profile'))
        
    return render_template('dashboard/profile.html', user=user)


# ============================================
# MENJALANKAN APLIKASI
# ============================================

if __name__ == '__main__':
    # debug=True agar server otomatis restart saat ada perubahan kode
    # dan menampilkan pesan error yang detail di browser
    app.run(debug=True)
