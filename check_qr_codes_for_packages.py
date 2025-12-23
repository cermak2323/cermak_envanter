#!/usr/bin/env python3
"""Check QR codes for JCB and ATAŞMAN"""

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

# Check QR codes for JCB
print("[CHECK] QR codes for JCB...")
cursor.execute("""
    SELECT qr_code, part_code
    FROM qr_codes
    WHERE part_code = 'JCB'
""")

jcb_qrs = cursor.fetchall()
print(f"  Found {len(jcb_qrs)} QR codes for part_code='JCB':")
for qr_code, part_code in jcb_qrs[:5]:
    print(f"    - {qr_code} → {part_code}")
if len(jcb_qrs) > 5:
    print(f"    ... and {len(jcb_qrs) - 5} more")

# Check QR codes for JCB PAKETİ
print("\n[CHECK] QR codes for JCB PAKETİ...")
cursor.execute("""
    SELECT qr_code, part_code
    FROM qr_codes
    WHERE part_code = 'JCB PAKETİ'
""")

jcb_pkg_qrs = cursor.fetchall()
print(f"  Found {len(jcb_pkg_qrs)} QR codes for part_code='JCB PAKETİ':")
for qr_code, part_code in jcb_pkg_qrs[:5]:
    print(f"    - {qr_code} → {part_code}")
if len(jcb_pkg_qrs) > 5:
    print(f"    ... and {len(jcb_pkg_qrs) - 5} more")

# Check QR codes for ATAŞMAN
print("\n[CHECK] QR codes for ATAŞMAN...")
cursor.execute("""
    SELECT qr_code, part_code
    FROM qr_codes
    WHERE part_code = 'ATAŞMAN'
""")

atasман_qrs = cursor.fetchall()
print(f"  Found {len(atasман_qrs)} QR codes for part_code='ATAŞMAN':")
for qr_code, part_code in atasман_qrs[:5]:
    print(f"    - {qr_code} → {part_code}")
if len(atasман_qrs) > 5:
    print(f"    ... and {len(atasман_qrs) - 5} more")

conn.close()
