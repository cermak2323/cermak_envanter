#!/usr/bin/env python3
# Shared folder'daki QR kodlarını veritabanıyla karşılaştır

import os
import re
from pathlib import Path

# Shared folder path
shared_folder = r"\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\static\qr_codes"

print(f"📁 Kontrol ediliyor: {shared_folder}\n")

# Folder'da olan QR kodları bul
if not os.path.exists(shared_folder):
    print(f"❌ Folder bulunamadı: {shared_folder}")
    exit(1)

qr_files = []
for file in os.listdir(shared_folder):
    if file.endswith('.png') or file.endswith('.jpg'):
        # QR kod dosya adından part_code'u al
        # Format: part_code_qr_id.png
        qr_id = file.replace('.png', '').replace('.jpg', '')
        qr_files.append(qr_id)

print(f"✅ Folder'da {len(qr_files)} QR kod dosyası bulundu\n")

# Y129A00-55730 ile ilgili QR kodları göster
y_codes = [q for q in qr_files if 'Y129A00-55730' in q or '129A00-55730' in q]
print(f"📊 Y129A00-55730 / 129A00-55730 QR kodları (Folder):")
for code in y_codes[:10]:
    print(f"  - {code}")

if len(y_codes) > 10:
    print(f"  ... ve {len(y_codes) - 10} daha")

print(f"\n✅ Toplam: {len(y_codes)} QR kod dosyası")

# DB'de ne var kontrol et
import pymysql

try:
    conn = pymysql.connect(
        host='192.168.0.57',
        port=3306,
        user='flaskuser',
        password='FlaskSifre123!',
        database='flaskdb',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    cursor = conn.cursor()
    
    # Y129A00-55730 parçasının ID'sini bul
    cursor.execute("SELECT id FROM part_codes WHERE part_code = %s", ('Y129A00-55730',))
    part = cursor.fetchone()
    
    if part:
        part_id = part['id']
        cursor.execute("SELECT COUNT(*) as cnt FROM qr_codes WHERE part_code_id = %s", (part_id,))
        db_count = cursor.fetchone()['cnt']
        print(f"\n📊 Y129A00-55730 QR kodları (DATABASE):")
        print(f"   DB'de {db_count} QR kod kayıtlı")
        
        # Bazı QR kodları göster
        cursor.execute("""
            SELECT qr_id FROM qr_codes 
            WHERE part_code_id = %s 
            LIMIT 10
        """, (part_id,))
        
        db_qrs = cursor.fetchall()
        for qr in db_qrs:
            print(f"  - {qr['qr_id']}")
    else:
        print(f"\n❌ Y129A00-55730 part_codes'ta bulunamadı!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ DB Hatası: {e}")
    import traceback
    traceback.print_exc()
