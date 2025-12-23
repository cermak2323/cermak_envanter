#!/usr/bin/env python3
"""Fix JCB QR code to point to correct package"""

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

print("[FIX] Fixing JCB package QR code linkage...")

# Get the QR code that points to the wrong JCB record
cursor.execute("SELECT id, qr_code FROM qr_codes WHERE part_code_id = 3831")
qr_row = cursor.fetchone()

if qr_row:
    qr_id = qr_row[0]
    qr_code = qr_row[1]
    print(f"  Found QR code: {qr_code} (id={qr_id}) pointing to part_code_id=3831 (wrong)")
    
    # Update it to point to the correct JCB PAKETİ (id=6663)
    cursor.execute(
        "UPDATE qr_codes SET part_code_id = 6663 WHERE id = %s",
        (qr_id,)
    )
    conn.commit()
    print(f"  ✓ Updated QR code {qr_code} to point to part_code_id=6663 (JCB PAKETİ)")
    print(f"    Affected rows: {cursor.rowcount}")
else:
    print("  No QR code found pointing to JCB (id=3831)")

# Verify the fix
print("\n[VERIFY] Checking updated linkage...")
cursor.execute("""
    SELECT qr.qr_code, pc.part_code, pc.part_name, pc.is_package, CHAR_LENGTH(pc.package_items) as items_len
    FROM qr_codes qr
    JOIN part_codes pc ON qr.part_code_id = pc.id
    WHERE qr.qr_code LIKE 'JCB%'
""")

results = cursor.fetchall()
print(f"  QR codes with 'JCB' in name:")
for qr_code, part_code, part_name, is_package, items_len in results:
    print(f"    - {qr_code} → {part_code} ({part_name}) is_package={is_package} items_len={items_len}")

conn.close()
print("\nDone!")
