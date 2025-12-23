import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash

db_url = 'postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require'
conn = psycopg2.connect(db_url)
cursor = conn.cursor()

# Mevcut admin'i kontrol et
cursor.execute('SELECT id, username, password_hash FROM envanter_users WHERE username = %s', ('admin',))
user = cursor.fetchone()
print(f'Mevcut admin ID: {user[0]}, username: {user[1]}')
print(f'Mevcut hash: {user[2][:50]}...')

# Yeni sifre hash'i olustur
new_password = '@R9t$L7e!xP2w'
new_hash = generate_password_hash(new_password)
print(f'Yeni hash: {new_hash[:50]}...')

# Sifreyi guncelle
cursor.execute('UPDATE envanter_users SET password_hash = %s WHERE username = %s', (new_hash, 'admin'))
conn.commit()
print('Admin sifresi guncellendi!')

# Dogrula
cursor.execute('SELECT password_hash FROM envanter_users WHERE username = %s', ('admin',))
updated_hash = cursor.fetchone()[0]
result = check_password_hash(updated_hash, new_password)
print(f'Dogrulama: {result}')

conn.close()
print('Tamamlandi!')
