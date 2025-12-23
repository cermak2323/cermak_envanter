#!/usr/bin/env python3
import pymysql

conn = pymysql.connect(
    host='192.168.0.57', port=3306, user='flaskuser', password='FlaskSifre123!',
    database='flaskdb', charset='utf8mb4'
)
cursor = conn.cursor()

# Check scanned_qr structure
print("[STRUCTURE] scanned_qr table columns:")
cursor.execute("DESC scanned_qr")
cols = cursor.fetchall()
for col in cols:
    print(f"  - {col[0]}: {col[1]}")

# Find JCB scanned records
print("\n[SCAN] Recent scanned records for 'JCB':")
cursor.execute("""
    SELECT id, qr_id, scanned_at, part_code
    FROM scanned_qr 
    WHERE qr_id LIKE '%JCB%' OR qr_id = 'JCB' OR part_code = 'JCB'
    ORDER BY scanned_at DESC 
    LIMIT 10
""")
records = cursor.fetchall()
print(f"Found {len(records)} records:")
for rec in records:
    print(f"  - ID: {rec[0]} | QR: {rec[1]} | scanned_at: {rec[2]} | part_code: {rec[3]}")

conn.close()
