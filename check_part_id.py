#!/usr/bin/env python3
import pymysql
conn = pymysql.connect(host='192.168.0.57', user='flaskuser', password='FlaskSifre123!', database='flaskdb', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

cursor.execute('SELECT COUNT(DISTINCT part_code_id) as cnt FROM qr_codes WHERE qr_id LIKE "Y129A00-55730_%"')
print('part_code_id sayısı:', cursor.fetchone()['cnt'])

cursor.execute('SELECT DISTINCT part_code_id FROM qr_codes WHERE qr_id LIKE "Y129A00-55730_%" LIMIT 1')
result = cursor.fetchone()
if result:
    part_id = result['part_code_id']
    print(f"QR'ların part_code_id: {part_id}")
    cursor.execute('SELECT part_code FROM part_codes WHERE id = %s', (part_id,))
    part = cursor.fetchone()
    print('part_code:', part['part_code'] if part else 'NOT FOUND')

cursor.close()
conn.close()
