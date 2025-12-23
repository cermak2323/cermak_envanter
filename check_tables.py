import psycopg2
from werkzeug.security import generate_password_hash

conn = psycopg2.connect('postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require')
cur = conn.cursor()

# Mevcut admin kullanıcısını kontrol et
cur.execute("SELECT id, username, password_hash FROM envanter_users WHERE username = 'admin'")
admin = cur.fetchone()
print(f"Mevcut admin: {admin}")

# Yeni şifreyi oluştur
new_password = "@R9t$L7e!xP2w"
new_hash = generate_password_hash(new_password)
print(f"Yeni hash: {new_hash}")

# Şifreyi güncelle
cur.execute("UPDATE envanter_users SET password_hash = %s WHERE username = 'admin'", (new_hash,))
conn.commit()
print("Admin şifresi güncellendi!")

conn.close()
