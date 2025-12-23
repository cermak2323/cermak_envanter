#!/usr/bin/env python3
"""Delete both JCB records and recreate as one correct package"""

import pymysql
import json

conn = pymysql.connect(
    host='192.168.0.57', port=3306, user='flaskuser', password='FlaskSifre123!',
    database='flaskdb', charset='utf8mb4'
)
cursor = conn.cursor()

print("[PLAN] İşlem planı:")
print("  1. Doğru JCB paketini (id=6663) yedekle")
print("  2. Her iki JCB kaydını sil (3831, 6663)")
print("  3. İlgili QR kodlarını sil")
print("  4. İlgili tarama kayıtlarını sil")
print("  5. Yeni temiz JCB paketini oluştur")
print()

# BACKUP: Doğru kaydı yedekle
print("[BACKUP] Doğru JCB paketini yedekle...")
cursor.execute("""
    SELECT part_code, part_name, is_package, package_items
    FROM part_codes
    WHERE id = 6663
""")
backup = cursor.fetchone()
if backup:
    part_code, part_name, is_package, package_items = backup
    print(f"  ✓ Yedeklendi: {part_code} ({part_name}) - {len(package_items) if package_items else 0} bytes")
else:
    print("  ✗ Yedeklenecek kayıt bulunamadı!")
    exit(1)

# DELETE scanned records
print("\n[DELETE] Tarama kayıtlarını sil...")
cursor.execute("DELETE FROM scanned_qr WHERE part_code = 'JCB'")
deleted_scans = cursor.rowcount
print(f"  ✓ {deleted_scans} tarama kaydı silindi")

# DELETE QR codes
print("\n[DELETE] QR kodlarını sil...")
cursor.execute("DELETE FROM qr_codes WHERE part_code_id IN (3831, 6663)")
deleted_qrs = cursor.rowcount
print(f"  ✓ {deleted_qrs} QR kodu silindi")

# DELETE part_codes
print("\n[DELETE] JCB paket kayıtlarını sil...")
cursor.execute("DELETE FROM part_codes WHERE id IN (3831, 6663)")
deleted_parts = cursor.rowcount
print(f"  ✓ {deleted_parts} paket kaydı silindi")

conn.commit()

# CREATE new clean record
print("\n[CREATE] Yeni temiz JCB paketini oluştur...")
cursor.execute("""
    INSERT INTO part_codes (part_code, part_number, part_name, is_package, package_items)
    VALUES (%s, %s, %s, %s, %s)
""", (
    'JCB',
    'JCB',  # part_number = part_code
    'JCB PAKETİ',
    True,  # is_package = TRUE
    package_items  # Yedeklenmiş items
))
conn.commit()
new_id = cursor.lastrowid
print(f"  ✓ Yeni JCB paketesi oluşturuldu - ID: {new_id}")

# CREATE QR code
print("\n[CREATE] QR kodunu oluştur...")
cursor.execute("""
    INSERT INTO qr_codes (qr_code, part_code_id, qr_id)
    VALUES (%s, %s, %s)
""", (
    'JCB',
    new_id,
    'JCB'
))
conn.commit()
print(f"  ✓ JCB QR kodu oluşturuldu")

# VERIFY
print("\n[VERIFY] Yeni JCB paketini kontrol et...")
cursor.execute("""
    SELECT pc.id, pc.part_code, pc.part_name, pc.is_package, CHAR_LENGTH(pc.package_items) as items_len,
           qr.qr_code, qr.part_code_id
    FROM part_codes pc
    LEFT JOIN qr_codes qr ON pc.id = qr.part_code_id
    WHERE pc.part_code = 'JCB'
""")
result = cursor.fetchone()
if result:
    print(f"  ✓ ID: {result[0]}")
    print(f"  ✓ part_code: {result[1]}")
    print(f"  ✓ part_name: {result[2]}")
    print(f"  ✓ is_package: {result[3]} (TRUE)")
    print(f"  ✓ items_length: {result[4]} bytes (380+ parts)")
    print(f"  ✓ QR code: {result[5]}")
    print(f"  ✓ QR points to: {result[6]}")
else:
    print("  ✗ Kayıt bulunamadı!")

conn.close()
print("\n✅ BAŞARILI - JCB paketesi yeniden oluşturuldu!")
