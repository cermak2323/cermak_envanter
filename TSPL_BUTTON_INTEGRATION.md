# TSPL Entegrasyon - Parça Sayfasına Buton

## ✅ Eklenen Özellikler

### Parts Detail Page (`/parts/<part_code>`)
- ✅ QR kod üretme seçeneğinde **TSPL Termal Yazıcıdan Yazdır** checkbox'ı
- ✅ Yazıcı durumu göstergesi (Hazır/Bağlı Değil/Kapalı)
- ✅ QR üretimi sırasında otomatik TSPL yazdırması
- ✅ TSPL sonuç bilgilendirmesi

### Özellikler
1. **TSPL Checkbox**: QR üretme sırasında checkbox işaretlerseniz:
   - PNG dosya oluşturulur (hep)
   - TSPL yazıcıya otomatik gönderilir (eğer etkinse ve bağlıysa)
   - Sonuç alert'te gösterilir

2. **Yazıcı Status Göstergesi**:
   - 🟢 **Yazıcı hazır** - Checkbox etkin, yazdırabilirsin
   - 🟡 **Yazıcı bağlı değil** - Checkbox devre dışı
   - ⚫ **Yazıcı kapalı** - Checkbox devre dışı

3. **Otomatik İşlem**:
   - Checkbox işaretler
   - Adet gir (1-500)
   - "QR Kod Üret" butonuna tıkla
   - PNG + TSPL yazdırması otomatik olur

---

## 🚀 Kullanım

### Adım 1: Parça Sayfasına Git
```
URL: http://192.168.10.27:5002/parts/05686-26600
```

### Adım 2: QR Üret Bölümüne Git
- "QR Kod Üret" kartını göreceksin

### Adım 3: TSPL Seçeneğini Kullan
```
1. Quantity'yi gir (örn. 10)
2. "TSPL Termal Yazıcıdan Yazdır" checkbox'ını işaretle
3. "QR Kod Üret" butonuna tıkla
```

### Adım 4: Sonuç
- PNG dosyalar otomatik oluşturulur (shared folder)
- TSPL yazıcıya gönderilir (eğer etkinse)
- Alert mesajı gösterilir

---

## 📋 Önemli Notlar

✅ **PNG Hep Oluşturulur**
- TSPL kapalı olsa bile PNG dosya kaydedilir
- Bu fallback ve dokümantasyon için gerekli

✅ **Checkbox Devre Dışı Durumları**
- Yazıcı kapalı (TSPL_ENABLED=false)
- Yazıcı bağlı değil (CONNECTION_FAILED)
- Yazıcı IP/Port yanlış

✅ **Admin Panel Ayrı Kalmıştır**
- `/admin/tspl` - Yazıcı konfigürasyonu
- `/parts` - QR üretim ve yazdırma

---

## 🔧 Backend Ayarları

### app.py
- ✅ `/generate_qr/<part_code>` route'u `print_to_tspl` parametresini alıyor
- ✅ TSPL yazıcıya gönderme logic'i eklendi
- ✅ TSPL sonuçları response'a ekleniyor

### part_detail.html
- ✅ TSPL checkbox'ı eklendi
- ✅ Status göstergesi eklendi
- ✅ JavaScript fonksiyonu eklendi
- ✅ TSPL helper script'i linked

### parts.html
- ✅ TSPL helper script'i linked

---

## 📝 Teknik Detaylar

### Frontend Flow
```javascript
// User tıklar
1. Page yüklenir
2. TSPL status kontrol edilir
3. Checkbox enable/disable edilir
4. User checkbox işaretler
5. Quantity girer
6. Button tıklar
7. POST request gönderilir (print_to_tspl: true)
8. Backend response'ı gönderir
9. Alert + Modal gösterilir
```

### Backend Flow
```python
# POST /generate_qr/<part_code>
1. Quantity parametresi alınır
2. print_to_tspl parametresi alınır
3. QR kodlar oluşturulur
4. PNG dosyalar kaydedilir
5. Eğer print_to_tspl=true:
   - Her QR için TSPL yazıcıya gönderilir
   - Sonuçlar tspl_results array'ine eklenir
6. Response'ta tspl_results döndürülür
7. Frontend'de sonuçlar gösterilir
```

---

## ✨ Senaryo Örnekleri

### Senaryo 1: Yazıcı Hazır
```
1. URL: /parts/05686-26600
2. TSPL indicator: 🟢 Yazıcı hazır
3. Checkbox: Etkin ✓
4. 10 QR üret → TSPL'ye yazdırılır
5. Alert: ✓ 10/10 QR kod TSPL yazıcıya gönderildi
```

### Senaryo 2: Yazıcı Kapalı
```
1. TSPL indicator: ⚫ Yazıcı kapalı
2. Checkbox: Devre dışı
3. 10 QR üret → Sadece PNG oluşturulur
4. TSPL sonucu yok
```

### Senaryo 3: Yazıcı Kapalıyken Yeniden Aç
```
1. TSPL_ENABLED=true yapıldı
2. App restart'landı
3. Page refresh'lendiğinde
4. Status kontrol yapılıyor
5. Checkbox tekrar aktif oluyor
```

---

## 🎯 Checklist

- [x] Part detail page'inde TSPL checkbox'ı
- [x] Yazıcı status göstergesi
- [x] Frontend TSPL helper integration
- [x] Backend TSPL yazdırma logic'i
- [x] Response'ta TSPL sonuçları
- [x] Alert mesajları
- [x] Admin panel ayrı (konfigürasyon için)

---

## 📞 Sorun Giderme

### Checkbox Devre Dışı?
- .env'de TSPL_ENABLED=true olduğunu kontrol et
- App'i restart et
- Page'i refresh et

### TSPL Yazıcı Kontrol Hatası?
- API health check et: `/api/tspl/status`
- Host/Port ayarlarını kontrol et
- Firewall kurallarını kontrol et

### Yazdırma Başarısız?
- Logs'u kontrol et: `logs/app.log`
- Admin panelinden test print yap
- Yazıcı driver'ını kontrol et

---

**Tamamlandı!** ✓ 

Sistem hazır - parts sayfasında direkt buton olarak TSPL entegrasyonu var.
