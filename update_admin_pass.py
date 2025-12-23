from werkzeug.security import generate_password_hash
import psycopg2

# Yeni şifre
new_password = '@R9t$L7e!xP2w'
password_hash = generate_password_hash(new_password)

# PostgreSQL bağlantısı
conn = psycopg2.connect('postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require')
cur = conn.cursor()

# Admin şifresini güncelle
cur.execute("UPDATE envanter_users SET password_hash = %s WHERE username = 'admin'", (password_hash,))
conn.commit()

print(f'✅ Admin password updated to: {new_password}')
print(f'   New hash: {password_hash[:60]}...')

# Kontrol et
cur.execute("SELECT username, password_hash FROM envanter_users WHERE username='admin'")
row = cur.fetchone()

from werkzeug.security import check_password_hash
is_valid = check_password_hash(row[1], new_password)
print(f'   Verification: {is_valid}')

conn.close()
