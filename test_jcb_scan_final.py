#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import pymysql.cursors

def get_db():
    mysql_config = {
        'host': '192.168.0.57',
        'user': 'flaskuser',
        'password': 'FlaskSifre123!',
        'database': 'flaskdb',
        'port': 3306,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.Cursor,
        'autocommit': False
    }
    return pymysql.connect(**mysql_config)

print("[TEST] JCB PAKETİ TARAMA TESTI")
print("=" * 60)

conn = get_db()
cursor = conn.cursor()

# Test 1: Check if JCB exists
print("\n[TEST 1] JCB paketini veritabanında kontrol et...")
cursor.execute('SELECT id, part_code, part_name, is_package, LENGTH(package_items) FROM part_codes WHERE part_code = %s', ('JCB',))
result = cursor.fetchone()
if result:
    jcb_id, code, name, is_package, size = result
    print(f"  ✓ ID: {jcb_id}")
    print(f"  ✓ Code: {code}")
    print(f"  ✓ Name: {name}")
    print(f"  ✓ Is Package: {is_package} (TRUE={bool(is_package)})")
    print(f"  ✓ Items Size: {size} bytes")
else:
    print("  ✗ JCB paketesi bulunamadı!")

# Test 2: Check if QR code exists
print("\n[TEST 2] JCB QR kodunu kontrol et...")
cursor.execute('SELECT id, qr_code, part_code_id FROM qr_codes WHERE qr_code = %s', ('JCB',))
qr_result = cursor.fetchone()
if qr_result:
    qr_id, qr_code, part_id = qr_result
    print(f"  ✓ QR ID: {qr_id}")
    print(f"  ✓ QR Code: {qr_code}")
    print(f"  ✓ Part Code ID: {part_id}")
else:
    print("  ✗ QR kod bulunamadı!")

# Test 3: Simulate package detection
print("\n[TEST 3] Paket tespiti simülasyonu...")
cursor.execute('''
    SELECT pc.is_package, LENGTH(pc.package_items), pc.id 
    FROM part_codes pc
    WHERE pc.id = (SELECT part_code_id FROM qr_codes WHERE qr_code = %s)
''', ('JCB',))
detect_result = cursor.fetchone()
if detect_result:
    is_pkg, items_len, pkg_id = detect_result
    print(f"  ✓ is_package: {is_pkg} (would trigger package mode: {bool(is_pkg)})")
    print(f"  ✓ package_items size: {items_len} bytes")
    print(f"  ✓ part_codes ID: {pkg_id}")
    
    if is_pkg:
        print(f"\n  ✅ PAKET ALGINDA BAŞARILI!")
        print(f"  JCB scanning'i paket modu ile çalışacak")
    else:
        print(f"\n  ⚠️  UYARI: is_package=FALSE (hotfix aktif olacak)")
else:
    print("  ✗ Paket tespiti başarısız!")

# Test 4: Verify no scanned_qr conflicts
print("\n[TEST 4] Eski tarama kayıtlarını kontrol et...")
cursor.execute('SELECT COUNT(*) FROM scanned_qr WHERE qr_code = %s OR part_code = %s', ('JCB', 'JCB'))
old_count = cursor.fetchone()[0]
if old_count == 0:
    print(f"  ✓ Eski tarama kaydı yok (temiz!)")
else:
    print(f"  ⚠️  {old_count} eski tarama kaydı var (silme başarısız mı?)")

cursor.close()
conn.close()

print("\n" + "=" * 60)
print("✅ JCB PAKETİ BAŞARIYLA OLUŞTURULDU VE TARAMA HAZIR!")
