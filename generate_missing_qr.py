#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
from pathlib import Path
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import qrcode
from PIL import Image, ImageDraw, ImageFont

load_dotenv()

# DATABASE_URL'den bilgileri çek
db_url = os.getenv('DATABASE_URL')
parsed = urlparse(db_url)

# PostgreSQL bağlantısı
conn = psycopg2.connect(
    host=parsed.hostname,
    port=parsed.port or 5432,
    database=parsed.path[1:],
    user=parsed.username,
    password=parsed.password,
    sslmode='require'
)

def generate_qr_with_logo(part_code, part_name, is_package=False):
    """QR kod oluştur - CERMAK logosu ile"""
    
    # QR klasörü
    qr_folder = Path('static/qr_codes') / part_code
    qr_folder.mkdir(parents=True, exist_ok=True)
    
    # QR kod oluştur
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(part_code)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Logo ekle
    logo_path = Path('cermaktakeuchi_logo.jfif')
    if logo_path.exists():
        logo = Image.open(logo_path)
        logo = logo.convert('RGB')
        
        # Logo boyutu (QR'ın %15'i)
        qr_width, qr_height = qr_img.size
        logo_size = int(qr_width * 0.15)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Logoyu ortaya yerleştir
        logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        qr_img.paste(logo, logo_pos)
    
    # Üst başlık (CERMAK) ve alt metin (parça adı veya paket adı)
    header_text = "CERMAK"
    footer_text = part_name[:30] if not is_package else part_name[:30]
    
    # Font ayarları
    try:
        header_font = ImageFont.truetype("arial.ttf", 40)
        footer_font = ImageFont.truetype("arial.ttf", 24)
    except:
        header_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()
    
    # Yeni canvas (başlık + QR + alt metin)
    draw_temp = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    header_bbox = draw_temp.textbbox((0, 0), header_text, font=header_font)
    footer_bbox = draw_temp.textbbox((0, 0), footer_text, font=footer_font)
    
    header_height = header_bbox[3] - header_bbox[1] + 20
    footer_height = footer_bbox[3] - footer_bbox[1] + 20
    
    total_width = max(qr_width, header_bbox[2] - header_bbox[0], footer_bbox[2] - footer_bbox[0]) + 40
    total_height = header_height + qr_height + footer_height + 40
    
    final_img = Image.new('RGB', (total_width, total_height), 'white')
    draw = ImageDraw.Draw(final_img)
    
    # Başlık (üstte ortada)
    header_x = (total_width - (header_bbox[2] - header_bbox[0])) // 2
    draw.text((header_x, 10), header_text, fill='black', font=header_font)
    
    # QR kod (ortada)
    qr_x = (total_width - qr_width) // 2
    qr_y = header_height + 10
    final_img.paste(qr_img, (qr_x, qr_y))
    
    # Alt metin (altta ortada)
    footer_x = (total_width - (footer_bbox[2] - footer_bbox[0])) // 2
    footer_y = qr_y + qr_height + 10
    draw.text((footer_x, footer_y), footer_text, fill='black', font=footer_font)
    
    # Kaydet - 2 kopya (_1.png ve _2.png)
    output_path_1 = qr_folder / f'{part_code}_1.png'
    output_path_2 = qr_folder / f'{part_code}_2.png'
    
    final_img.save(output_path_1, 'PNG', quality=95, optimize=True)
    final_img.save(output_path_2, 'PNG', quality=95, optimize=True)
    
    return True


# Eksik QR'ları bul
cursor = conn.cursor()
cursor.execute('SELECT part_code, part_name, is_package FROM part_codes ORDER BY part_code')
parts = cursor.fetchall()

qr_dir = Path('static/qr_codes')
missing = []

for part_code, part_name, is_package in parts:
    qr_folder = qr_dir / part_code
    
    if not qr_folder.exists() or not list(qr_folder.glob('*.png')):
        missing.append((part_code, part_name, is_package))

print("\n" + "="*70)
print("EKSIK QR KOD OLUŞTURMA")
print("="*70)
print(f"Toplam parça: {len(parts)}")
print(f"QR'sı eksik: {len(missing)}")
print("="*70)

if missing:
    print(f"\n{len(missing)} adet QR kod oluşturuluyor...")
    
    created = 0
    errors = 0
    
    for idx, (part_code, part_name, is_package) in enumerate(missing, 1):
        try:
            generate_qr_with_logo(part_code, part_name, is_package)
            created += 1
            
            if idx % 50 == 0:
                print(f"  [{idx}/{len(missing)}] {created} oluşturuldu, {errors} hata")
        
        except Exception as e:
            errors += 1
            print(f"  HATA: {part_code} - {e}")
    
    print("\n" + "="*70)
    print("TAMAMLANDI!")
    print("="*70)
    print(f"Oluşturulan: {created}")
    print(f"Hata: {errors}")
    print("="*70)
else:
    print("\nTüm parçaların QR kodu mevcut!")

cursor.close()
conn.close()
