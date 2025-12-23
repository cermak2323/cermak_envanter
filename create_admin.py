import sqlite3
from werkzeug.security import generate_password_hash

# Şifre ve parametreler
admin_password = "@R9t$L7e!xP2w"
password_hash = generate_password_hash(admin_password)

# Database bağlantısı
conn = sqlite3.connect('instance/envanter_local.db')
cursor = conn.cursor()

# Admin user'ını kontrol et
cursor.execute('SELECT id FROM envanter_users WHERE username = ?', ('admin',))
if cursor.fetchone():
    # Var, güncelle
    cursor.execute('UPDATE envanter_users SET password_hash = ? WHERE username = ?', (password_hash, 'admin'))
    print('✅ Admin user şifresi güncellendi')
else:
    # Yok, oluştur
    cursor.execute('''
        INSERT INTO envanter_users (username, full_name, password_hash, role, is_active_user, first_login_completed)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('admin', 'Sistem Administratörü', password_hash, 'admin', True, True))
    print('✅ Admin user oluşturuldu')

conn.commit()

# Doğrulama
cursor.execute('SELECT id, username, role FROM envanter_users WHERE username = ?', ('admin',))
user = cursor.fetchone()
print(f'✅ User ID: {user[0]}, Username: {user[1]}, Role: {user[2]}')

conn.close()
