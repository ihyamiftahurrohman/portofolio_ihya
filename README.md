# 🚀 Web Portofolio Dinamis — Flask

Aplikasi web portofolio pribadi yang dibangun dengan **Python Flask**, lengkap dengan panel admin untuk mengelola project, profil, dan pesan dari pengunjung — tanpa perlu menyentuh database secara manual.

---

## ✨ Fitur Utama

### 👤 Halaman Publik (Frontend)
| Halaman | Route | Deskripsi |
|---|---|---|
| Home | `/` | Landing page dengan 3 project terbaru |
| About | `/about` | Profil lengkap pemilik portofolio |
| Portfolio | `/portfolio` | Daftar semua project |
| Detail Project | `/project/<id>` | Halaman detail satu project |
| Contact | `/contact` | Form kirim pesan untuk pengunjung |

### 🔒 Panel Admin (Butuh Login)
| Halaman | Route | Deskripsi |
|---|---|---|
| Dashboard | `/dashboard` | Statistik ringkas (total project, pesan, pesan belum dibaca) |
| Kelola Project | `/dashboard/projects` | CRUD project (tambah, edit, hapus) |
| Kotak Masuk | `/dashboard/messages` | Baca & hapus pesan dari pengunjung |
| Edit Profil | `/dashboard/profile` | Edit info pribadi, skills, sosial media, foto profil |

---

## 🛠️ Tech Stack

| Komponen | Teknologi |
|---|---|
| Backend Framework | [Flask 3.1.1](https://flask.palletsprojects.com/) |
| Database ORM | [Flask-SQLAlchemy 3.1.1](https://flask-sqlalchemy.palletsprojects.com/) |
| Autentikasi | [Flask-Login 0.6.3](https://flask-login.readthedocs.io/) |
| Password Hashing | [Werkzeug 3.1.3](https://werkzeug.palletsprojects.com/) |
| Database | SQLite (`portfolio.db`) |
| Frontend | HTML, CSS, Jinja2 Templating |

---

## 📁 Struktur Project

```
portfolio-flask/
├── app.py               # Entry point — semua route dan konfigurasi app
├── config.py            # Konfigurasi (database, upload, secret key)
├── models.py            # Model database (User, Project, Message)
├── requirements.txt     # Daftar dependency Python
├── portfolio.db         # File database SQLite (auto-generated)
├── static/
│   └── uploads/         # Folder penyimpanan gambar yang diupload
└── templates/
    ├── base.html        # Layout dasar (navbar, footer)
    ├── index.html       # Halaman Home
    ├── about.html       # Halaman About
    ├── portfolio.html   # Halaman Portfolio
    ├── project_detail.html
    ├── contact.html
    └── dashboard/
        ├── login.html
        ├── index.html   # Dashboard utama
        ├── projects.html
        ├── add_project.html
        ├── edit_project.html
        ├── messages.html
        └── profile.html
```

---

## ⚙️ Cara Menjalankan

### 1. Clone / Download Project

```bash
git clone https://github.com/username/portfolio-flask.git
cd portfolio-flask
```

### 2. Buat Virtual Environment *(opsional tapi disarankan)*

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependency

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
python app.py
```

Buka browser dan akses: **http://127.0.0.1:5000**

---

## 🔑 Akun Admin Default

Saat pertama kali dijalankan, aplikasi otomatis membuat akun admin:

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `admin123` |

> ⚠️ **Penting:** Segera ubah password melalui halaman profil setelah login pertama kali, terutama sebelum di-deploy ke server publik.

Akses halaman login admin di: **http://127.0.0.1:5000/login**

---

## 📸 Upload Gambar

- **Format yang didukung:** `jpg`, `jpeg`, `png`, `gif`
- **Ukuran maksimal:** 2 MB per file
- File tersimpan di folder `static/uploads/`

---

## 🗄️ Model Database

### `User` — Data pemilik portofolio & admin
- `username`, `password` (hashed), `name`, `bio`, `photo`
- `email`, `phone`, `address`, `skills`
- `site_name` — nama brand di navbar
- `github`, `linkedin`, `instagram`

### `Project` — Data karya/project
- `title`, `description`, `image`
- `tech_stack`, `demo_link`, `github_link`
- `created_at`, `user_id` (foreign key ke User)

### `Message` — Pesan dari pengunjung
- `name`, `email`, `subject`, `body`
- `is_read` (status baca), `created_at`

---

## 🌐 Variabel Lingkungan *(Opsional)*

Untuk keamanan di lingkungan produksi, buat file `.env` atau set environment variable:

```bash
SECRET_KEY=ganti-dengan-kunci-rahasia-yang-kuat
```

Jika tidak diset, aplikasi akan menggunakan nilai default (`kunci-rahasia-default`).

---

## 📝 Lisensi

Project ini dibuat untuk keperluan tugas akademik. Bebas digunakan dan dimodifikasi untuk keperluan belajar.

---

> Dibuat dengan ❤️ menggunakan Python & Flask
