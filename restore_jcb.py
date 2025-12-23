#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import os

# Add app's config to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Get MySQL connection details from environment
import pymysql

conn = pymysql.connect(
    host='192.168.0.57',
    user='root',
    password='2564',
    database='flaskdb',
    charset='utf8mb4'
)
cursor = conn.cursor()

print("[RESTORE] JCB paketini yedekten geri yükle...")

# Read backup
try:
    with open('jcb_backup.json', 'r', encoding='utf-8') as f:
        backup = json.load(f)
    package_items = backup['package_items']
    print(f"  ✓ Yedek okundu: {len(package_items)} bytes")
except FileNotFoundError:
    print("  ✗ Yedek dosyası bulunamadı!")
    sys.exit(1)

# Create new clean record
print("\n[CREATE] Yeni JCB paketesi oluştur...")
cursor.execute('''
    INSERT INTO part_codes (part_code, part_number, part_name, is_package, package_items)
    VALUES (%s, %s, %s, %s, %s)
''', (
    'JCB',
    'JCB',
    'JCB PAKETİ',
    True,
    package_items
))
conn.commit()
new_id = cursor.lastrowid
print(f"  ✓ Paket oluşturuldu - ID: {new_id}")

# Create QR code
print("\n[CREATE] QR kodunu oluştur...")
cursor.execute('''
    INSERT INTO qr_codes (qr_code, part_code_id, qr_id)
    VALUES (%s, %s, %s)
''', (
    'JCB',
    new_id,
    'JCB'
))
conn.commit()
print(f"  ✓ QR kodu oluşturuldu")

# Verify
print("\n[VERIFY] Sonucu doğrula...")
cursor.execute('SELECT id, part_code, part_name, is_package, LENGTH(package_items) FROM part_codes WHERE part_code = %s', ('JCB',))
result = cursor.fetchone()
if result:
    print(f"  ✓ ID: {result[0]}")
    print(f"  ✓ Part Code: {result[1]}")
    print(f"  ✓ Name: {result[2]}")
    print(f"  ✓ Is Package: {result[3]}")
    print(f"  ✓ Size: {result[4]} bytes")
else:
    print("  ✗ Doğrulama başarısız!")

cursor.close()
conn.close()
print("\n✅ JCB PAKETİ BAŞARIYLA YENIDEN OLUŞTURULDU!")
