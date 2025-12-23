#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
from pathlib import Path
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# DATABASE_URL'den bilgileri çek
db_url = os.getenv('DATABASE_URL')
parsed = urlparse(db_url)

# PostgreSQL bağlantısı
conn = psycopg2.connect(
    host=parsed.hostname,
    port=parsed.port or 5432,
    database=parsed.path[1:],  # Remove leading /
    user=parsed.username,
    password=parsed.password,
    sslmode='require'
)

cursor = conn.cursor()

# Tüm part_code'ları al
cursor.execute('SELECT part_code, part_name, is_package FROM part_codes ORDER BY part_code')
parts = cursor.fetchall()

qr_dir = Path('static/qr_codes')
missing = []
found = []

for part_code, part_name, is_package in parts:
    # QR dosyası klasör içinde: static/qr_codes/PART_CODE/PART_CODE_1.png
    qr_folder = qr_dir / part_code
    
    # Klasör yoksa veya klasör içinde PNG dosyası yoksa
    if not qr_folder.exists():
        missing.append((part_code, part_name, is_package))
    else:
        png_files = list(qr_folder.glob('*.png'))
        if png_files:
            found.append(part_code)
        else:
            missing.append((part_code, part_name, is_package))

print("\n" + "="*70)
print("QR DOSYA KONTROLÜ")
print("="*70)
print(f"Veritabanında kayıtlı: {len(parts)} adet part_code")
print(f"QR dosyası var: {len(found)} adet")
print(f"QR dosyası YOK: {len(missing)} adet")
print("="*70)

if missing:
    print("\nQR DOSYASI OLMAYAN PARÇALAR:")
    print("-"*70)
    for part_code, part_name, is_package in missing[:20]:  # İlk 20 tanesi
        pkg_label = "[PAKET]" if is_package else ""
        print(f"  {part_code:20} {part_name[:40]:40} {pkg_label}")
    
    if len(missing) > 20:
        print(f"\n  ... ve {len(missing) - 20} adet daha")

cursor.close()
conn.close()
