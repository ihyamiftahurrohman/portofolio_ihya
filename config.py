"""
config.py - Konfigurasi Aplikasi Flask
=======================================
File ini menyimpan semua pengaturan (konfigurasi) yang
dibutuhkan oleh aplikasi Flask.

Mengapa konfigurasi dipisah ke file sendiri?
- Agar kode lebih rapi dan terorganisir (Separation of Concerns)
- Memudahkan perubahan konfigurasi tanpa mengubah kode utama
- Best practice dalam pengembangan aplikasi Flask
"""

import os

# Mendapatkan path absolut dari folder project ini
# Contoh: C:/Users/LENOVO/Downloads/portfolio-flask
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Class yang menyimpan semua konfigurasi aplikasi.
    
    Mengapa menggunakan class?
    - Lebih rapi daripada variabel terpisah
    - Mudah dipanggil dari app.py: app.config.from_object(Config)
    """
    
    # SECRET_KEY: Kunci rahasia untuk mengamankan session dan form
    # os.environ.get() akan mencari di environment variable terlebih dahulu,
    # jika tidak ada, gunakan nilai default 'kunci-rahasia-default'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci-rahasia-default'
    
    # SQLALCHEMY_DATABASE_URI: Lokasi file database SQLite
    # Format: sqlite:///path/ke/file.db
    # os.path.join menggabungkan basedir dengan nama file database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'portfolio.db')
    
    # SQLALCHEMY_TRACK_MODIFICATIONS: Menonaktifkan fitur tracking
    # yang tidak kita butuhkan (menghemat memori)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # UPLOAD_FOLDER: Lokasi penyimpanan file yang diupload
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    
    # MAX_CONTENT_LENGTH: Batas maksimal ukuran file upload (2 MB)
    # 2 * 1024 * 1024 = 2097152 bytes = 2 MB
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    
    # ALLOWED_EXTENSIONS: Tipe file yang diperbolehkan untuk upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
