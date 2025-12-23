-- qr_codes tablosuna used_at kolonu ekle
-- Bu kolon QR kodunun ne zaman kullanıldığını takip eder

ALTER TABLE qr_codes 
ADD COLUMN IF NOT EXISTS used_at TIMESTAMP;

-- Performans için index ekle
CREATE INDEX IF NOT EXISTS idx_qr_codes_used_at ON qr_codes(used_at);

-- Mevcut is_used=true olan kayıtlar için used_at'i created_at ile doldur (opsiyonel)
UPDATE qr_codes 
SET used_at = created_at 
WHERE is_used = TRUE AND used_at IS NULL;
