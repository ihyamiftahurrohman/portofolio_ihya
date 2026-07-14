"""
models.py - Perancangan Struktur Database
==========================================
File ini berisi definisi dari tabel-tabel yang akan
dibuat di dalam database. Kita menggunakan SQLAlchemy 
(ORM - Object Relational Mapper) agar kita tidak perlu 
menulis kueri SQL (seperti CREATE TABLE) secara manual.

Sebagai gantinya, setiap tabel direpresentasikan sebagai 
sebuah Class Python.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Membuat object db SQLAlchemy. 
# Object ini akan di-import ke app.py untuk dihubungkan dengan Flask
db = SQLAlchemy()

# -------------------------------------------------------------------
# TABEL 1: User (Pemilik Portofolio / Admin)
# -------------------------------------------------------------------
# UserMixin menambahkan fungsionalitas khusus untuk sistem login 
# (seperti is_authenticated, is_active, dll).
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    # nullable=True artinya kolom ini boleh kosong saat pertama kali dibuat
    bio = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    
    # Skills disimpan sebagai satu string panjang (contoh: "HTML, CSS, Python")
    skills = db.Column(db.Text, nullable=True)
    
    # Link Sosial Media
    github = db.Column(db.String(200), nullable=True)
    linkedin = db.Column(db.String(200), nullable=True)
    instagram = db.Column(db.String(200), nullable=True)
    
    # Relasi Database (One-to-Many)
    # Satu User memiliki banyak Project. 
    # backref='owner' membuat kita bisa mengakses pemilik suatu project 
    # lewat variabel 'owner' (contoh: project_ku.owner.name)
    projects = db.relationship('Project', backref='owner', lazy=True)

# -------------------------------------------------------------------
# TABEL 2: Project (Karya/Portofolio yang ditampilkan)
# -------------------------------------------------------------------
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    
    # Teknologi yang digunakan (contoh: "Flask, Bootstrap 5")
    tech_stack = db.Column(db.String(300), nullable=True)
    
    # Link terkait project
    demo_link = db.Column(db.String(300), nullable=True)
    github_link = db.Column(db.String(300), nullable=True)
    
    # default=datetime.now akan otomatis mengisi waktu saat data disimpan
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Foreign Key: Menyambungkan project ini dengan User tertentu (pemiliknya)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# -------------------------------------------------------------------
# TABEL 3: Message (Pesan dari pengunjung di form Contact)
# -------------------------------------------------------------------
# Tabel ini berdiri sendiri dan tidak memiliki Foreign Key, karena
# pesan dikirim oleh pengunjung umum yang tidak memiliki akun di website.
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    
    # is_read digunakan untuk menandai apakah admin sudah membaca pesan ini
    # default=False artinya pesan baru dianggap "belum dibaca"
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
