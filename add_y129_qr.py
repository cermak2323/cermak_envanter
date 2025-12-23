#!/usr/bin/env python3
# Y129A00-55730 QR kodlarını folder'dan al ve DB'ye ekle

import os
import pymysql

shared_folder = r"\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\static\qr_codes"
y_folder = os.path.join(shared_folder, "Y129A00-55730")

if not os.path.exists(y_folder):
    print(f"❌ Folder yok: {y_folder}")
    exit(1)

# Folder'daki QR dosyalarını al
qr_files = [f for f in os.listdir(y_folder) if f.endswith('.png') or f.endswith('.jpg')]
print(f"📁 Folder'da {len(qr_files)} QR kod dosyası bulundu")

try:
    conn = pymysql.connect(host='192.168.0.57', user='flaskuser', password='FlaskSifre123!', database='flaskdb', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    
    # Y129A00-55730 parçasının ID'sini bul
    cursor.execute("SELECT id FROM part_codes WHERE part_code = %s", ('Y129A00-55730',))
    part = cursor.fetchone()
    
    if not part:
        print("❌ Y129A00-55730 part_codes'ta YOK")
        exit(1)
    
    part_id = part['id']
    
    # QR kodlarını ekle
    added = 0
    skipped = 0
    
    for qr_file in qr_files:
        qr_id = qr_file.replace('.png', '').replace('.jpg', '')
        
        cursor.execute("SELECT id FROM qr_codes WHERE qr_id = %s", (qr_id,))
        exists = cursor.fetchone()
        
        if exists:
            skipped += 1
        else:
            cursor.execute("""
                INSERT INTO qr_codes (qr_id, part_code_id, is_used, used_count)
                VALUES (%s, %s, FALSE, 0)
            """, (qr_id, part_id))
            added += 1
    
    conn.commit()
    
    print(f"\n✅ Eklendi: {added} QR kod")
    print(f"⏭️  Zaten var: {skipped} QR kod")
    
    # Kontrol et
    cursor.execute("SELECT COUNT(*) as cnt FROM qr_codes WHERE part_code_id = %s", (part_id,))
    total = cursor.fetchone()['cnt']
    print(f"✅ Toplam DB'de: {total} QR kod")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
