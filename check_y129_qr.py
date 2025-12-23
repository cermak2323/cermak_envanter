#!/usr/bin/env python3
import pymysql
conn = pymysql.connect(host='192.168.0.57', user='flaskuser', password='FlaskSifre123!', database='flaskdb', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

# Y129A00-55730_1 gibi QR ID'leri ara
cursor.execute("SELECT COUNT(*) as cnt FROM qr_codes WHERE qr_id LIKE %s", ('Y129A00-55730_%',))
result = cursor.fetchone()
print(f"DB'de Y129A00-55730 ile ilgili QR: {result['cnt']}")

# İlk 5'ini göster
cursor.execute("SELECT qr_id FROM qr_codes WHERE qr_id LIKE %s LIMIT 5", ('Y129A00-55730_%',))
for row in cursor.fetchall():
    print(f"  - {row['qr_id']}")

cursor.close()
conn.close()
