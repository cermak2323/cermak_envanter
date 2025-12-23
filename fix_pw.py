import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

# Şifre
password = "@R9t$L7e!xP2w"

# Hash oluştur ve test et
new_hash = generate_password_hash(password)
print(f"Şifre: {password}")
print(f"Hash: {new_hash}")
print(f"Doğrulama: {check_password_hash(new_hash, password)}")

# Veritabanına yaz
conn = psycopg2.connect('postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require')
cur = conn.cursor()

# Güncelle
cur.execute("UPDATE envanter_users SET password_hash = %s WHERE username = 'admin'", (new_hash,))
conn.commit()

# Kontrol et
cur.execute("SELECT password_hash FROM envanter_users WHERE username = 'admin'")
db_hash = cur.fetchone()[0]
print(f"\nDB Hash: {db_hash}")
print(f"DB Doğrulama: {check_password_hash(db_hash, password)}")

conn.close()
print("\nŞifre güncellendi!")
