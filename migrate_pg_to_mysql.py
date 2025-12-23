import psycopg2
import pymysql
from datetime import datetime

# PostgreSQL bağlantısı
pg_conn = psycopg2.connect('postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require')
pg_cur = pg_conn.cursor()

# MySQL bağlantısı
mysql_conn = pymysql.connect(
    host='192.168.0.57',
    user='flaskuser',
    password='FlaskSifre123!',
    database='flaskdb',
    port=3306,
    charset='utf8mb4'
)
mysql_cur = mysql_conn.cursor()

print("=== PostgreSQL'den MySQL'e Veri Aktarımı ===\n")

# 1. QR Codes (PostgreSQL şeması: id, qr_id, part_code_id, created_at)
print("[1/5] QR Codes aktarılıyor...")
pg_cur.execute("SELECT id, qr_id, created_at FROM qr_codes WHERE qr_id IS NOT NULL ORDER BY id")
qr_codes = pg_cur.fetchall()
count = 0
for qr in qr_codes:
    try:
        # MySQL'de qr_code kolonuna qr_id'yi yazıyoruz
        mysql_cur.execute("INSERT INTO qr_codes (id, qr_code, created_at) VALUES (%s, %s, %s)", 
                         (qr[0], qr[1], qr[2]))
        count += 1
    except Exception as e:
        if 'Duplicate' not in str(e):
            print(f"  QR Code {qr[0]} ({qr[1]}) hata: {e}")
mysql_conn.commit()
print(f"  ✅ {count} QR code aktarıldı\n")

# 2. Part Codes - QR ile ilişkilendirme
print("[2/5] Part Codes aktarılıyor...")
pg_cur.execute("""
    SELECT pc.id, qr.id as qr_code_id, pc.part_code, 1 as quantity,
           pc.photo_path, pc.catalog_image, pc.description, 
           pc.used_in_machines, pc.specifications, pc.stock_location,
           pc.supplier, pc.unit_price, pc.critical_stock_level, 
           pc.notes, pc.last_updated, pc.updated_by
    FROM part_codes pc
    LEFT JOIN qr_codes qr ON qr.part_code_id = pc.id
    WHERE pc.part_code IS NOT NULL
    ORDER BY pc.id
""")
part_codes = pg_cur.fetchall()
count = 0
for part in part_codes:
    try:
        mysql_cur.execute("""
            INSERT INTO part_codes 
            (id, qr_code_id, part_number, quantity, photo_path, catalog_image, 
             description, used_in_machines, specifications, stock_location, 
             supplier, unit_price, critical_stock_level, notes, last_updated, updated_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, part)
        count += 1
    except Exception as e:
        if 'Duplicate' not in str(e):
            print(f"  Part {part[0]} ({part[2]}) hata: {e}")
mysql_conn.commit()
print(f"  ✅ {count} part code aktarıldı\n")

# 3. Count Sessions (PostgreSQL: session_name, created_by, started_at, ended_at, finished_by, total_expected, total_scanned, report_file_path)
print("[3/5] Count Sessions aktarılıyor...")
pg_cur.execute("""
    SELECT id, session_name, started_at, ended_at, created_by, finished_by,
           total_expected, total_scanned, report_file_path
    FROM count_sessions ORDER BY id
""")
sessions = pg_cur.fetchall()
count = 0
for session in sessions:
    try:
        mysql_cur.execute("""
            INSERT INTO count_sessions 
            (id, session_name, started_at, finished_at, started_by, finished_by,
             total_expected, total_scanned, report_file_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, session)
        count += 1
    except Exception as e:
        if 'Duplicate' not in str(e):
            print(f"  Session {session[0]} hata: {e}")
mysql_conn.commit()
print(f"  ✅ {count} session aktarıldı\n")

# 4. Scanned QR (PostgreSQL: session_id, qr_id, part_code, scanned_at)
print("[4/5] Scanned QR aktarılıyor...")
pg_cur.execute("""
    SELECT id, session_id, qr_id, scanned_at, part_code, 1 as quantity
    FROM scanned_qr ORDER BY id
""")
scanned = pg_cur.fetchall()
count = 0
for scan in scanned:
    try:
        mysql_cur.execute("""
            INSERT INTO scanned_qr 
            (id, session_id, qr_code, scanned_at, part_number, quantity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, scan)
        count += 1
    except Exception as e:
        if 'Duplicate' not in str(e):
            print(f"  Scanned {scan[0]} hata: {e}")
mysql_conn.commit()
print(f"  ✅ {count} scanned QR aktarıldı\n")

# 5. Users (admin zaten var, diğerlerini ekle)
print("[5/5] Users aktarılıyor...")
pg_cur.execute("""
    SELECT id, username, password_hash, full_name, role, created_at
    FROM envanter_users WHERE username != 'admin' ORDER BY id
""")
users = pg_cur.fetchall()
for user in users:
    try:
        mysql_cur.execute("""
            INSERT INTO envanter_users 
            (id, username, password_hash, full_name, role, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, user)
    except Exception as e:
        print(f"  User {user[1]} hata: {e}")
mysql_conn.commit()
print(f"  ✅ {len(users)} kullanıcı aktarıldı\n")

# AUTO_INCREMENT değerlerini düzelt
print("AUTO_INCREMENT değerleri ayarlanıyor...")
tables = ['qr_codes', 'part_codes', 'count_sessions', 'scanned_qr', 'envanter_users']
for table in tables:
    mysql_cur.execute(f"SELECT MAX(id) FROM {table}")
    max_id = mysql_cur.fetchone()[0]
    if max_id:
        mysql_cur.execute(f"ALTER TABLE {table} AUTO_INCREMENT = {max_id + 1}")
        print(f"  ✅ {table}: {max_id + 1}")

mysql_conn.commit()

pg_conn.close()
mysql_conn.close()

print("\n✅ TÜM VERİLER MYSQL'E AKTARILDI!")
