#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JFIF logosunu ICO formatına çevir - Exe simgesi için
"""

from PIL import Image
import os
from pathlib import Path

app_dir = Path(__file__).parent.resolve()

print("""
╔════════════════════════════════════════════════════════════════════╗
║        LOGO DONUSUM - JFIF -> ICO                                 ║
╚════════════════════════════════════════════════════════════════════╝
""")

# Logo dosyası
logo_path = app_dir / "cermaktakeuchi_logo.jfif"
ico_path = app_dir / "cermaktakeuchi_logo.ico"

print(f"[1] Logo Dosyası Kontrol Ediliyor...")
if not logo_path.exists():
    print(f"[!] HATA: {logo_path} bulunamadı")
    exit(1)

print(f"[✓] Logo Bulundu: {logo_path}")
print(f"    Boyut: {logo_path.stat().st_size / 1024:.1f} KB")

print(f"\n[2] Logo Yükleniyor...")
try:
    img = Image.open(logo_path)
    print(f"[✓] Logo Yüklendi")
    print(f"    Orijinal Boyut: {img.size}")
    print(f"    Format: {img.format}")
except Exception as e:
    print(f"[!] HATA: {e}")
    exit(1)

print(f"\n[3] ICO Formatına Çevriliyor...")
try:
    # CMYK ise RGB'ye çevir
    if img.mode == 'CMYK':
        print(f"    [*] CMYK formatından RGB'ye çevriliyor...")
        img = img.convert('RGB')
    
    # ICO için resize (256x256 ideal)
    size = (256, 256)
    img_resized = img.resize(size, Image.Resampling.LANCZOS)
    
    # ICO olarak kaydet
    img_resized.save(ico_path, format='ICO')
    
    print(f"[✓] ICO Oluşturuldu")
    print(f"    Yeni Boyut: {img_resized.size}")
    print(f"    Dosya: {ico_path}")
    print(f"    Boyut: {ico_path.stat().st_size / 1024:.1f} KB")
except Exception as e:
    print(f"[!] HATA: {e}")
    exit(1)

print(f"""
╔════════════════════════════════════════════════════════════════════╗
║                    DONUSUM TAMAMLANDI                             ║
║                                                                    ║
║  ICO Dosyası Hazır: {ico_path.name}
║                                                                    ║
║  PyInstaller için kullanılacak:                                  ║
║  --icon=cermaktakeuchi_logo.ico                                   ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")
