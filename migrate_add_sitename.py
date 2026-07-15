"""Script migrasi: tambah kolom site_name ke tabel user"""
import sqlite3

conn = sqlite3.connect('portfolio.db')
try:
    conn.execute("ALTER TABLE user ADD COLUMN site_name VARCHAR(100) DEFAULT '<Portofolio />'")
    conn.commit()
    print("Kolom site_name berhasil ditambahkan!")
except sqlite3.OperationalError as e:
    if "duplicate column" in str(e):
        print("Kolom site_name sudah ada, skip.")
    else:
        raise
finally:
    conn.close()
