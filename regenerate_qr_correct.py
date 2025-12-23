#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MySQL'deki QR kodlar için dosyaları DOĞRU YAPIYLA yeniden oluştur
Yapı: qr_codes/<part_code>/<qr_id>.png
"""

import os
import shutil
import qrcode
import pymysql

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

# Önce yanlış oluşturulan dosyaları temizle (kök dizindeki .png dosyaları)
print("[1/3] Yanlış yapıdaki dosyalar temizleniyor...")
if os.path.exists(TARGET_DIR):
    for item in os.listdir(TARGET_DIR):
        item_path = os.path.join(TARGET_DIR, item)
        if item.endswith('.png') and os.path.isfile(item_path):
            os.remove(item_path)
    print("  Kök dizindeki PNG dosyalar silindi")
else:
    os.makedirs(TARGET_DIR)
    print(f"  Klasör oluşturuldu: {TARGET_DIR}")

# Tüm QR kodları al (parça kodu ile birlikte)
print("\n[2/3] Veritabanından QR kayıtları alınıyor...")
cur.execute('''
    SELECT q.qr_id, p.part_code
    FROM qr_codes q 
    JOIN part_codes p ON q.part_code_id = p.id
    WHERE q.qr_id IS NOT NULL
''')
qr_records = cur.fetchall()
print(f"  Toplam QR kayıt: {len(qr_records)}")

# QR kodları doğru yapıyla oluştur
print("\n[3/3] QR dosyaları oluşturuluyor...")
created = 0
skipped = 0
errors = 0

for qr_id, part_code in qr_records:
    # Parça için klasör oluştur
    part_dir = os.path.join(TARGET_DIR, part_code)
    if not os.path.exists(part_dir):
        os.makedirs(part_dir)
    
    # Dosya yolu
    filename = f"{qr_id}.png"
    filepath = os.path.join(part_dir, filename)
    
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
        qr.add_data(qr_id)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filepath)
        created += 1
        
        if created % 100 == 0:
            print(f"  [PROGRESS] {created} QR dosyası oluşturuldu...")
            
    except Exception as e:
        errors += 1
        print(f"  [ERROR] {qr_id}: {e}")

conn.close()

# Oluşturulan klasör sayısını kontrol et
folder_count = len([d for d in os.listdir(TARGET_DIR) if os.path.isdir(os.path.join(TARGET_DIR, d))])

print(f"\n{'='*60}")
print(f"[TAMAMLANDI]")
print(f"  Oluşturulan QR: {created}")
print(f"  Atlanan (var): {skipped}")
print(f"  Hata: {errors}")
print(f"  Parça klasörü: {folder_count}")
print(f"  Hedef: {TARGET_DIR}")
print(f"{'='*60}")
print(f"\nYapı örneği:")
print(f"  {TARGET_DIR}\\<part_code>\\<qr_id>.png")
