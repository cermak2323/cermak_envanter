#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MySQL'deki QR kodlar için dosyaları yeniden oluştur
Hedef klasör: \\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\static\qr_codes
"""

import os
import qrcode
import pymysql
from datetime import datetime

# Hedef klasör
TARGET_DIR = r"\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\static\qr_codes"

# MySQL bağlantısı
conn = pymysql.connect(
    host='192.168.0.57', 
    port=3306, 
    user='flaskuser', 
    password='FlaskSifre123!', 
    database='flaskdb'
)
cur = conn.cursor()

# Klasör yoksa oluştur
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)
    print(f"[+] Klasör oluşturuldu: {TARGET_DIR}")

# Tüm QR kodları al
cur.execute('''
    SELECT q.id, q.qr_id, q.qr_code, p.part_code, p.part_name 
    FROM qr_codes q 
    LEFT JOIN part_codes p ON q.part_code_id = p.id
    WHERE q.qr_id IS NOT NULL OR q.qr_code IS NOT NULL
''')
qr_records = cur.fetchall()
print(f"[INFO] Toplam QR kayıt: {len(qr_records)}")

created = 0
skipped = 0
errors = 0

for row in qr_records:
    qr_id, qr_code_id, qr_code, part_code, part_name = row
    
    # qr_id veya qr_code kullan
    qr_value = qr_code_id or qr_code
    if not qr_value:
        skipped += 1
        continue
    
    # Dosya adı
    filename = f"{qr_value}.png"
    filepath = os.path.join(TARGET_DIR, filename)
    
    # Zaten varsa atla
    if os.path.exists(filepath):
        skipped += 1
        continue
    
    try:
        # QR kod oluştur
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_value)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filepath)
        created += 1
        
        if created % 100 == 0:
            print(f"[PROGRESS] {created} QR dosyası oluşturuldu...")
            
    except Exception as e:
        errors += 1
        print(f"[ERROR] {qr_value}: {e}")

conn.close()

print(f"\n{'='*50}")
print(f"[TAMAMLANDI]")
print(f"  Oluşturulan: {created}")
print(f"  Atlanan (var): {skipped}")
print(f"  Hata: {errors}")
print(f"  Hedef: {TARGET_DIR}")
print(f"{'='*50}")
