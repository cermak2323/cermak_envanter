#!/usr/bin/env python3
# Shared folder'daki QR kod klasörlerini DB'ye senkronize et

import os
import pymysql
from pathlib import Path

shared_folder = r"\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\static\qr_codes"

try:
    conn = pymysql.connect(
        host='192.168.0.57',
        port=3306,
        user='flaskuser',
        password='FlaskSifre123!',
        database='flaskdb',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    cursor = conn.cursor()
    
    total_qr_added = 0
    total_folders = 0
    
    # Shared folder'daki her klasörü kontrol et
    for folder in os.listdir(shared_folder):
        folder_path = os.path.join(shared_folder, folder)
        
        if not os.path.isdir(folder_path):
            continue
        
        total_folders += 1
        part_code = folder.strip()
        
        # part_code'ın DB'de olup olmadığını kontrol et
        cursor.execute("SELECT id FROM part_codes WHERE part_code = %s", (part_code,))
        part = cursor.fetchone()
        
        if not part:
            print(f"⚠️ {part_code} - part_codes'ta YOK, skip")
            continue
        
        part_id = part['id']
        
        # Bu klasördeki QR kod dosyalarını al
        qr_files = [f for f in os.listdir(folder_path) 
                   if f.endswith('.png') or f.endswith('.jpg')]
        
        added_for_part = 0
        for qr_file in qr_files:
            qr_id = qr_file.replace('.png', '').replace('.jpg', '')
            
            # Mevcut kontrolü yap
            cursor.execute("SELECT id FROM qr_codes WHERE qr_id = %s", (qr_id,))
            exists = cursor.fetchone()
            
            if not exists:
                # Yeni QR kodu ekle
                try:
                    cursor.execute("""
                        INSERT INTO qr_codes (qr_id, part_code_id, is_used, used_count)
                        VALUES (%s, %s, FALSE, 0)
                    """, (qr_id, part_id))
                    added_for_part += 1
                    total_qr_added += 1
                except pymysql.err.IntegrityError:
                    # Duplicate key, skip
                    pass
        
        if added_for_part > 0:
            print(f"✅ {part_code}: {added_for_part} QR kod eklendi")
    
    conn.commit()
    
    print(f"\n{'='*50}")
    print(f"✅ Senkronizasyon tamamlandı!")
    print(f"   - Tarama yapılan klasör: {total_folders}")
    print(f"   - Eklenen QR kod: {total_qr_added}")
    print(f"{'='*50}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
