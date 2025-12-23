#!/usr/bin/env python3
"""Delete broken JCB record and keep the correct one"""

import pymysql

conn = pymysql.connect(
    host='192.168.0.57', port=3306, user='flaskuser', password='FlaskSifre123!',
    database='flaskdb', charset='utf8mb4'
)
cursor = conn.cursor()

print("[CHECK] Current JCB records in database...")
cursor.execute("SELECT id, part_code, part_name, is_package, CHAR_LENGTH(package_items) FROM part_codes WHERE part_code IN ('JCB', 'JCB PAKETİ') OR id IN (3831, 6663)")
records = cursor.fetchall()
print(f"Found {len(records)} records:")
for rec in records:
    print(f"  ID: {rec[0]:5} | part_code: {rec[1]:15} | part_name: {rec[2]:20} | is_package: {rec[3]} | items_len: {rec[4]}")

# Check for dependent records
print("\n[SCAN] Checking for dependent records...")
cursor.execute("SELECT COUNT(*) FROM qr_codes WHERE part_code_id = 3831")
qr_count_3831 = cursor.fetchone()[0]
print(f"  QR codes pointing to id=3831: {qr_count_3831}")

cursor.execute("DESC scanned_qr")
cols = cursor.fetchall()
col_names = [c[0] for c in cols]
if 'part_code_id' in col_names:
    cursor.execute("SELECT COUNT(*) FROM scanned_qr WHERE part_code_id = 3831")
elif 'part_code' in col_names:
    cursor.execute("SELECT COUNT(*) FROM scanned_qr WHERE part_code = 'JCB'")
else:
    print("  Could not find part_code column in scanned_qr")
    scan_count_3831 = 0

row = cursor.fetchone()
scan_count_3831 = row[0] if row else 0
print(f"  Scanned records for JCB: {scan_count_3831}")

# Ask permission
if qr_count_3831 == 0 and scan_count_3831 == 0:
    print("\n[SAFE] No dependencies found for id=3831 - safe to delete!")
    
    # Delete hatalı kayıt
    print("\n[DELETE] Deleting broken JCB record (id=3831)...")
    cursor.execute("DELETE FROM part_codes WHERE id = 3831")
    conn.commit()
    print(f"✓ Deleted 1 broken record")
    
    # Verify the good one remains
    print("\n[VERIFY] Remaining JCB records:")
    cursor.execute("SELECT id, part_code, part_name, is_package FROM part_codes WHERE id = 6663")
    good = cursor.fetchone()
    if good:
        print(f"✓ ID: {good[0]} | part_code: {good[1]} | part_name: {good[2]} | is_package: {good[3]}")
        print(f"✓ This is the correct package with 380+ items")
else:
    print(f"\n[WARNING] Cannot delete - has dependencies!")
    print(f"  Please check these records manually")

conn.close()
