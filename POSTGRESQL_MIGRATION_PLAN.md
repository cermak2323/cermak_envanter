# PostgreSQL Geçiş Planı (Migration Plan)

**Başlangıç Tarihi**: 2025-11-23
**Hedef**: SQLite'den Neon PostgreSQL'e veri geçişi
**Durum**: Hazırlık Tamamlandı ✅

---

## 📋 Hazırlık Kontrol Listesi

### ✅ Tamamlanan Adımlar

1. **Sistem Yedeklemesi**
   - Tam yedek oluşturuldu: `FULL_BACKUP_20251123_141034`
   - Tüm dosyalar dahil (instance/, templates/, static/, models.py, app.py, vb.)
   - Şu anda SQLite veritabanı burada güvende: `FULL_BACKUP_20251123_141034/instance/envanter_local.db`

2. **PostgreSQL Kurulum**
   - Neon hesabı oluşturuldu
   - PostgreSQL bağlantı stringi hazırlandı:
     ```
     postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
     ```

3. **Sistem Yapılandırması**
   - `.env` dosyası oluşturuldu
   - `db_config.py` dual-mode desteği ile güncellendi
   - PostgreSQL ve SQLite için optimize connection pools yapılandırıldı

4. **Geçiş Betikleri**
   - `migrate_to_postgresql.py` oluşturuldu ve test edildi
   - URL encoding tüm rotalar için uygulandı (7 route)
   - Sistem stabilite kontrolleri geçildi

---

## 🚀 Geçiş Adımları

### ADIM 1: PostgreSQL Tablolarını Oluştur

Neon'da tablolar şu anda boş. SQLAlchemy otomatik oluşturacak.

```bash
# Tüm bağlantıları kontrol et
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✅ Tablolar oluşturuldu')"
```

**Beklenen Çıktı:**
```
[DB] PostgreSQL (Neon) kullanılacak
✅ Tablolar oluşturuldu
```

**Ne olur?**
- 5 tablo PostgreSQL'de oluşturulacak:
  - `envanter_users`
  - `part_codes`
  - `qr_codes`
  - `count_sessions`
  - `scanned_qr`
  - `count_passwords` (varsa)

---

### ADIM 2: Veri Geçişini Başlat

```bash
python migrate_to_postgresql.py
```

**Beklenen Çıktı:**
```
✅ SQLite bağlantısı kuruldu: instance/envanter_local.db
✅ PostgreSQL (Neon) bağlantısı kuruldu
📊 Bulunan tablolar: envanter_users, part_codes, qr_codes, count_sessions, scanned_qr, ...
   ✅ envanter_users: X satır geçişi tamamlandı
   ✅ part_codes: Y satır geçişi tamamlandı
   ✅ qr_codes: Z satır geçişi tamamlandı
   ... (diğer tablolar)

📊 Geçiş İstatistikleri:
   - Toplam tablolar: 6
   - Geçilen tablolar: 6
   - Toplam satırlar: ABC
   - Geçiş Süresi: X saniye
   ✅ VERİ GEÇİŞİ BAŞARILI
```

---

### ADIM 3: Veri Doğrulama

```bash
python verify_postgresql_data.py
```

Bu komut kontrol eder:
- Her tablo kaç satır içeriyor?
- Kritik veriler var mı (admin kullanıcı, QR kodlar)?
- Foreign key ilişkileri bozuk mu?

**Beklenen Çıktı:**
```
📊 PostgreSQL Veri Doğrulaması:
   envanter_users: 5 satır
   part_codes: 150 satır
   qr_codes: 1500 satır
   count_sessions: 45 satır
   scanned_qr: 8000 satır
   
✅ Tüm veriler başarıyla geçişi yapıldı
✅ Foreign key ilişkileri OK
✅ Admin kullanıcı kontrol edildi: CERMAK SERVIS
```

---

### ADIM 4: PostgreSQL Modunu Etkinleştir

`.env` dosyasında güncelleyin:

```env
USE_POSTGRESQL=True
DATABASE_URL=postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

---

### ADIM 5: Uygulamayı Başlat ve Test Et

```bash
# Geliştirme ortamında test
python app.py

# Ya da production
gunicorn -c gunicorn.conf.py app:app
```

**Test Kontrol Listesi:**
- [ ] Login sayfası yükleniyor
- [ ] Admin kullanıcı ile giriş yapabiliyor
- [ ] Parça kodları görüntüleniyor
- [ ] Yeni parça kodu eklenebiliyor
- [ ] QR kod oluşturulabiliyor
- [ ] Sayım oturumu başlatılabiliyor
- [ ] Raporlar oluşturulabiliyor
- [ ] `/parts/948/756` gibi `/` içeren kodlar çalışabiliyor

---

## 🔄 Rollback Planı (Geri Alma)

Eğer sorun çıkarsa:

### Plan A: SQLite'ye Geri Dön (Hızlı)
```bash
# .env dosyasını düzenle
USE_POSTGRESQL=False

# Uygulamayı yeniden başlat
python app.py
```

Sistem otomatik olarak SQLite'ye dönecek. Tüm veriler orijinal backup'te güvendedir.

### Plan B: Full Restore (Eğer Gerekirse)
```powershell
# Backup'ten geri yükle
Remove-Item -Recurse instance/
Copy-Item "FULL_BACKUP_20251123_141034\instance" -Destination "instance" -Recurse
Copy-Item "FULL_BACKUP_20251123_141034\app.py" -Destination "app.py" -Force
```

---

## ⚠️ Önemli Notlar

1. **Bağlantı Havuzu Ayarları**
   - SQLite: pool_size=20, max_overflow=30
   - PostgreSQL: pool_size=5, max_overflow=10 (Neon sınırlaması)
   - SSL: PostgreSQL'de zorunlu (`sslmode=require`)

2. **Veri Türü Uyumluluğu**
   - SQLite: Boolean → PostgreSQL: boolean (SQLAlchemy otomatik dönüştürür)
   - SQLite: TEXT → PostgreSQL: text (OK)
   - SQLite: DATETIME → PostgreSQL: timestamp (OK)

3. **Performans**
   - PostgreSQL ilk kez yavaş olabilir (cold start)
   - Connection pooling nedeniyle sonraki istekler hızlı
   - Neon'un "auto-suspend" özelliği inaktif DB'leri donduruyor olabilir

4. **Backup Stratejisi**
   - Neon otomatik backup yapıyor (3 gün)
   - Manual backup: `pg_dump` komutunu kullanabilirsiniz
   - SQLite backup: `FULL_BACKUP_20251123_141034` dizininde korumaya alındı

---

## 📞 Sorun Giderme

### Sorun: "Bağlantı timeout"
```
Çözüm: 
1. Neon dashboard'a gidin ve DB durumunu kontrol edin
2. Connection pool ayarlarını kontrol edin (db_config.py)
3. Network connectivity kontrol edin
```

### Sorun: "no such table" hatası
```
Çözüm:
1. ADIM 1'i çalıştırdığınızdan emin olun (CREATE TABLES)
2. USE_POSTGRESQL=True olup olmadığını kontrol edin
3. DATABASE_URL doğru mu kontrol edin
```

### Sorun: "SSL error"
```
Çözüm:
1. sslmode=require DATABASE_URL'de var mı kontrol edin
2. Neon sertifikaları güncel mi kontrol edin
3. Firewall/antivirus SSL portunu engellemiyor mu kontrol edin
```

---

## ✅ Son Kontrol Listesi Geçiş Öncesi

- [ ] Tam yedek alındı: `FULL_BACKUP_20251123_141034`
- [ ] PostgreSQL veritabanı Neon'da oluşturuldu
- [ ] `.env` dosyası yapılandırıldı
- [ ] `db_config.py` güncellenmiş
- [ ] `migrate_to_postgresql.py` hazır
- [ ] Test ortamında hızlı kontrol yapılacak
- [ ] Production'a geçiş yapılacak

---

**Önerilen Sıra:**
1. ADIM 1: PostgreSQL tablolarını oluştur
2. ADIM 2: Veri geçişini başlat
3. ADIM 3: Veri doğrulama
4. ADIM 4: PostgreSQL modunu etkinleştir
5. ADIM 5: Tam test
6. ✅ Live!

**Tahmini Süre:** 5-10 dakika
**Risk Seviyesi:** DÜŞÜK (Full rollback stratejisi var)

---

*Son Güncelleme: 2025-11-23*
*Hazırlanmış: GitHub Copilot Assistant*
