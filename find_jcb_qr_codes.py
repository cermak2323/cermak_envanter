#!/usr/bin/env python3
"""Find QR codes for JCB and ATAŞMAN packages"""

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

# Find JCB package ID
print("[LOOKUP] Looking for JCB package ID...")
cursor.execute("SELECT id, part_code, part_name, is_package FROM part_codes WHERE part_code = 'JCB'")
jcb = cursor.fetchone()
if jcb:
    jcb_id = jcb[0]
    print(f"  Found JCB: id={jcb_id}, part_code={jcb[1]}, is_package={jcb[3]}")
    
    # Find QR codes for this JCB
    cursor.execute("SELECT COUNT(*) FROM qr_codes WHERE part_code_id = %s", (jcb_id,))
    count = cursor.fetchone()[0]
    print(f"  QR codes pointing to JCB (id={jcb_id}): {count}")

# Find JCB PAKETİ package ID
print("\n[LOOKUP] Looking for JCB PAKETİ package ID...")
cursor.execute("SELECT id, part_code, part_name, is_package FROM part_codes WHERE part_code = 'JCB PAKETİ'")
jcb_pkg = cursor.fetchone()
if jcb_pkg:
    jcb_pkg_id = jcb_pkg[0]
    print(f"  Found JCB PAKETİ: id={jcb_pkg_id}, part_code={jcb_pkg[1]}, is_package={jcb_pkg[3]}")
    
    # Find QR codes for this JCB PAKETİ
    cursor.execute("SELECT COUNT(*), GROUP_CONCAT(qr_code SEPARATOR ', ') FROM qr_codes WHERE part_code_id = %s", (jcb_pkg_id,))
    row = cursor.fetchone()
    count, qr_list = row[0], row[1]
    print(f"  QR codes pointing to JCB PAKETİ (id={jcb_pkg_id}): {count}")
    if qr_list:
        qr_codes = qr_list.split(', ')[:5]
        print(f"    Examples: {', '.join(qr_codes)}")

# Find ATAŞMAN
print("\n[LOOKUP] Looking for ATAŞMAN package ID...")
cursor.execute("SELECT id, part_code, part_name, is_package FROM part_codes WHERE part_code = 'ATAŞMAN'")
atasман = cursor.fetchone()
if atasман:
    atasман_id = atasман[0]
    print(f"  Found ATAŞMAN: id={atasман_id}, part_code={atasман[1]}, is_package={atasман[3]}")
    
    # Find QR codes for this ATAŞMAN
    cursor.execute("SELECT COUNT(*), GROUP_CONCAT(qr_code SEPARATOR ', ') FROM qr_codes WHERE part_code_id = %s", (atasман_id,))
    row = cursor.fetchone()
    count, qr_list = row[0], row[1]
    print(f"  QR codes pointing to ATAŞMAN (id={atasман_id}): {count}")
    if qr_list:
        qr_codes = qr_list.split(', ')[:5]
        print(f"    Examples: {', '.join(qr_codes)}")

conn.close()
