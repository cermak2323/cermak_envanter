#!/usr/bin/env python3
"""Check ATAŞMAN package"""

import pymysql

conn = pymysql.connect(
    host='192.168.0.57',
    port=3306,
    user='flaskuser',
    password='FlaskSifre123!',
    database='flaskdb',
    charset='utf8mb4'
)

cursor = conn.cursor()

# Check ATAŞMAN
print("[CHECK] Looking for ATAŞMAN packages...")
cursor.execute("""
    SELECT id, part_code, part_name, is_package, 
           CHAR_LENGTH(package_items) as items_len
    FROM part_codes 
    WHERE part_code LIKE '%ATAŞMAN%' OR part_code LIKE '%ATASМАН%'
    OR part_name LIKE '%ATAŞMAN%' OR part_name LIKE '%ATASМАН%'
""")

results = cursor.fetchall()
print(f"Found {len(results)} ATAŞMAN records:")
for row in results:
    print(f"  ID: {row[0]:5} | part_code: {row[1]:20} | is_package: {row[3]} | items_len: {row[4]}")

conn.close()
