#!/usr/bin/env python3
"""
EnvanterQR - PostgreSQL Veri Göçü Rehberi
SQLite'dan PostgreSQL'e (Neon) veri aktarma işlemi

DURUM: ✅ Başarıyla tamamlandı
TARİH: 24 Kasım 2025
"""

"""
GÖÇÜRÜLEN VERİLER:
- 602 QR Kod (qr_codes tablosu)
- 64 Taranan QR Kaydı (scanned_qr tablosu)

ALTYAPI:
- Kaynak: SQLite (local, instance/envanter_local.db)
- Hedef: PostgreSQL Neon (ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech)
- Veritabanı: neondb

VERİ TÜRETÖRÜ:
PostgreSQL'den başka tarafında zaten mevcut olan veriler:
- Part Codes: 3832 kayıt ✓
- Count Sessions: 7 oturum ✓
- Envanter Users: 3 kullanıcı ✓

KOMUTLAR:

1. Göçü Tekrar Çalıştırmak (Tüm Verileri Sil ve Yeniden Göçür):
   $ python migrate_qr_data.py

   Çıktı:
   ======================================================================
   SQLite to PostgreSQL QR Data Migration
   ======================================================================

   1. Connecting to SQLite...
      OK - SQLite connected

   2. Connecting to PostgreSQL...
      OK - PostgreSQL connected

   3. Migrating QR codes...
      Found 602 QR codes in SQLite
      Clearing PostgreSQL qr_codes table...
      OK - Inserted 602 QR codes into PostgreSQL

   4. Migrating scanned QR records...
      Found 64 scanned QR records in SQLite
      Clearing PostgreSQL scanned_qr table...
      OK - Inserted 64 scanned QR records into PostgreSQL

   5. Verifying migration...
      PostgreSQL qr_codes: 602 records
      PostgreSQL scanned_qr: 64 records
      OK - Migration successful!

   6. Cleaning up...
      OK - Connections closed

   ======================================================================
   MIGRATION COMPLETE
   ======================================================================

2. İşleme Kaydı Kontrol Etme:

   $ python -c "
   from app import app, db
   from models import QRCode, CountSession, ScannedQR
   
   with app.app_context():
       print(f'QR Codes: {db.session.query(QRCode).count()}')
       print(f'Count Sessions: {db.session.query(CountSession).count()}')
       print(f'Scanned QRs: {db.session.query(ScannedQR).count()}')
   "

   Çıktı:
   QR Codes: 602
   Count Sessions: 7
   Scanned QRs: 64

3. PostgreSQL Web Konsolu (Neon):
   https://console.neon.tech/
   
   Burada doğrudan sorgu çalıştırabilirsiniz:
   SELECT COUNT(*) FROM qr_codes;    -- 602
   SELECT COUNT(*) FROM scanned_qr;  -- 64

DASHBOARD İSTATİSTİKLERİ:

API Endpoint: GET /api/dashboard_stats

Yanıt:
{
  "total_qr_codes": 602,
  "total_reports": 7,
  "active_counts": 0,
  "completed_counts": 7,
  "last_count_date": "2025-11-22T13:09:52.290207"
}

KONFIGÜRASYON:

.env dosyasında bu ayarlar kontrol edin:
- USE_POSTGRESQL=True           ✓ (PostgreSQL kullanıyor)
- DATABASE_URL=postgresql://... ✓ (Neon bağlantı dizesi)
- FLASK_ENV=development         ✓ (Geliştirme ortamı)

SORUN GIDERME:

❌ "PostgreSQL connection failed" hatası:
   → DATABASE_URL çevre değişkenini kontrol et
   → .env dosyasında doğru ayarlandığından emin ol
   → Neon konsolunda veritabanının çalıştığını doğrula

❌ "INSERT failed" hatası:
   → Bağlantı havuzu yapılandırmasını kontrol et
   → db_config.py dosyasında bağlantı parametrelerini kontrol et

❌ "Record count mismatch" uyarısı:
   → Veri çakışması olabilir (tekrarlı göçü çalıştırırken)
   → Çözüm: PostgreSQL'de tabloları temizle ve tekrar çalıştır

BAKIYE VE DESTEK:

Neon Dashboard:
→ https://console.neon.tech/
→ neondb veritabanı
→ SQL Editor'da doğrudan sorgu çalıştırabilir

PostgreSQL Ayarları (db_config.py):
→ Connection pooling: 5 bağlantı
→ Max overflow: 10 ek bağlantı
→ Pool recycle: 3600 saniye (1 saat)
→ SSL: Required (Neon gereksinimi)

---
Göç dosyası: migrate_qr_data.py
İstatistikler: /api/dashboard_stats endpoint'i
Test tarihi: 24 Kasım 2025 02:23:28 UTC
"""
