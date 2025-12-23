#!/usr/bin/env python3
"""Check QR table schema"""

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

# Check QR table structure
print("[CHECK] QR codes table structure...")
cursor.execute("DESC qr_codes")

columns = cursor.fetchall()
print(f"  Columns in qr_codes table:")
for col in columns:
    print(f"    - {col[0]}: {col[1]}")

# Sample a few records
print("\n[SAMPLE] Sample QR codes:")
cursor.execute("SELECT * FROM qr_codes LIMIT 5")
sample_rows = cursor.fetchall()
for row in sample_rows:
    print(f"  {row}")

conn.close()
