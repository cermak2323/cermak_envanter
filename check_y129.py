#!/usr/bin/env python3
import pymysql
conn = pymysql.connect(host='192.168.0.57', user='flaskuser', password='FlaskSifre123!', database='flaskdb', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
cursor.execute("SELECT id, part_code, part_name FROM part_codes WHERE part_code LIKE %s", ('%Y129A00-55730%',))
for row in cursor.fetchall():
    print(f"{row['part_code']}: {row['part_name']}")
cursor.close()
conn.close()
