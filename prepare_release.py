#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dağıtım paketi hazırla
Exe dosyasını kullanıma hazır duruma getir
"""

import os
import shutil
from pathlib import Path

app_dir = Path(__file__).parent.resolve()
dist_dir = app_dir / "dist"
release_dir = app_dir / "RELEASE"

print("""
╔════════════════════════════════════════════════════════════════════╗
║            DAGITIM PAKETI HAZIRLANIYOR                            ║
╚════════════════════════════════════════════════════════════════════╝
""")

# Create release directory
if release_dir.exists():
    shutil.rmtree(release_dir)

release_dir.mkdir(parents=True, exist_ok=True)
print(f"[✓] Release Dizini Oluşturuldu: {release_dir}")

# Copy executable
exe_file = dist_dir / "EnvanterQR.exe"
if exe_file.exists():
    shutil.copy2(exe_file, release_dir / "EnvanterQR.exe")
    size_mb = (release_dir / "EnvanterQR.exe").stat().st_size / (1024 * 1024)
    print(f"[✓] EnvanterQR.exe Kopyalandı ({size_mb:.1f} MB)")
else:
    print(f"[!] HATA: {exe_file} bulunamadı")
    exit(1)

# Copy documentation
docs = ["QUICK_START_GUIDE_TR.md", "FINAL_SUMMARY.md", "EXE_BUILD_INSTRUCTIONS.md"]
for doc in docs:
    doc_file = app_dir / doc
    if doc_file.exists():
        shutil.copy2(doc_file, release_dir / doc)
        print(f"[✓] {doc} Kopyalandı")

# Copy key files for reference
key_files = ["requirements.txt", "README.md"]
for key_file in key_files:
    key_path = app_dir / key_file
    if key_path.exists():
        shutil.copy2(key_path, release_dir / key_file)
        print(f"[✓] {key_file} Kopyalandı")

# Create README for release
readme_content = """# EnvanterQR v1.0 - Dağıtım Paketi

## Hızlı Başlama

### Seçenek 1: Doğrudan Exe Kullan (En Basit)

1. `EnvanterQR.exe` dosyasına çift tıkla
2. Sistem otomatik başlayacak (ilk açılış ~5 dakika)
3. Tarayıcı otomatik açılacak: http://localhost:5000

### Seçenek 2: Farklı Dizinde Kullan

1. `EnvanterQR.exe`'yi istediğin klasöre kopyala
2. Çift tıkla
3. Sistem otomatik başlayacak

## Admin Panel

- URL: http://localhost:5000/admin
- Kullanıcı: admin
- Şifre: @R9t$L7e!xP2w

## İlk Açılış

**Beklenen:** İlk açılışta ~5 dakika alabilir (paketler indiriliyor)
**Sonrasında:** 2-3 saniye hızlı açılacak

## Veritabanı

- Tüm veriler: `instance/envanter_local.db` (Exe ile aynı klasörde)
- Yedekler: `backups/` (otomatik yapılır)
- Excel dosyaları: `static/exports/`

## Scanner Kullanma

1. Scanner sekmesi → Sayım Başlat
2. Paket veya parça QR'ını tara
3. Sayım Bitir → Rapor

## Paket Oluşturma

1. Admin Panel → Paket Yönetimi
2. Yeni Paket → Parçaları ekle
3. QR'ı yazdır

## Parça Ekleme (Excel)

1. Admin Panel → Excel Yükle
2. Türkçe başlıklar: Parça Kodu, Parça Adı, Beklenen Adet
3. Dosya yükle

## Sorun Çözme

**"Sistem açılmıyor"**
- Exe'yi masaüstüne kopyala
- Çift tıkla

**"QR taranmıyor"**
- Scanner cihazını kontrol et
- Kalibrasyonu yap

**"Rapor yavaş"**
- Tarayıcıyı yenile (F5)
- Eski raporları sil

## Teknik Bilgiler

- Platform: Windows 7+
- Python: 3.8+ (Exe içinde)
- Database: SQLite (Lokal)
- Depolama: Tamamen Lokal (Bulut yok)

## Sürüm

EnvanterQR v1.0 Final
Dağıtım Tarihi: 22 Kasım 2025

---

Sorular? → QUICK_START_GUIDE_TR.md'yi oku
"""

release_readme = release_dir / "README_TR.txt"
release_readme.write_text(readme_content, encoding='utf-8')
print(f"[✓] README_TR.txt Oluşturuldu")

# Create shortcuts info
shortcuts_info = """
MASAÜSTÜNE KIŞAYOL EKLEME:

Windows 10/11'de:
1. EnvanterQR.exe'ye sağ tıkla
2. "Daha fazla seçenek" → "Başka bir uygulama ile aç"
3. Masaüstüne kısayol oluştur

Veya:
1. EnvanterQR.exe'ye sağ tıkla
2. "Kısayol oluştur"
3. Masaüstüne taşı

BAŞLAT MENÜSÜNE EKLEME:

1. EnvanterQR.exe'ye sağ tıkla
2. "Başlat Menüsüne Sabitle"

Veya manuel olarak:
1. Windows tuşu + R
2. "shell:startup" yaz
3. EnvanterQR.exe'ye kısayol oluştur
"""

shortcuts_file = release_dir / "KISIAYOL_KURULUM.txt"
shortcuts_file.write_text(shortcuts_info, encoding='utf-8')
print(f"[✓] KISIAYOL_KURULUM.txt Oluşturuldu")

print(f"""
╔════════════════════════════════════════════════════════════════════╗
║                 DAGITIM PAKETI HAZIR                              ║
║                                                                    ║
║  Dizin: {release_dir}
║                                                                    ║
║  İçerik:                                                          ║
║    ✓ EnvanterQR.exe (79.1 MB) - Tüm sistem tek dosyada          ║
║    ✓ README_TR.txt - Başlama rehberi                            ║
║    ✓ QUICK_START_GUIDE_TR.md - Detaylı rehber                  ║
║    ✓ KISIAYOL_KURULUM.txt - Masaüstü kısayolu                  ║
║                                                                    ║
║  KULLANIM:                                                        ║
║    1. EnvanterQR.exe'yi herhangi bir klasöre kopyala             ║
║    2. Çift tıkla                                                  ║
║    3. Sistem otomatik başlayacak                                 ║
║                                                                    ║
║  DİKKAT: EnvanterQR.exe'nin yanında instance/ klasörü             ║
║          oluşacak (veritabanı). Silme!                            ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")

print(f"\n[✓] Dağıtım paketi hazır: {release_dir}")
print(f"[*] İşlem tamamlandı!")
