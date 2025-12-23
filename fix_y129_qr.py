#!/usr/bin/env python3
# Y129A00-55730 QR kodlarının part_code_id'sini düzelt

import pymysql

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
    
    # Y129A00-55730'ün doğru ID'sini bul
    cursor.execute("SELECT id FROM part_codes WHERE part_code = %s", ('Y129A00-55730',))
    correct_part = cursor.fetchone()
    
    if not correct_part:
        print("❌ Y129A00-55730 part_codes'ta YOK")
        exit(1)
    
    correct_id = correct_part['id']
    print(f"✅ Y129A00-55730 doğru part_code_id: {correct_id}")
    
    # Yanlış ID ile bağlı QR kodları bul
    cursor.execute("""
        SELECT COUNT(*) as cnt FROM qr_codes 
        WHERE qr_id LIKE %s 
        AND part_code_id != %s
    """, ('Y129A00-55730_%', correct_id))
    
    wrong_count = cursor.fetchone()['cnt']
    print(f"⚠️ Yanlış ID ile {wrong_count} QR kod bulundu")
    
    # Düzelt
    if wrong_count > 0:
        cursor.execute("""
            UPDATE qr_codes 
            SET part_code_id = %s
            WHERE qr_id LIKE %s
            AND part_code_id != %s
        """, (correct_id, 'Y129A00-55730_%', correct_id))
        
        updated = cursor.rowcount
        conn.commit()
        print(f"✅ {updated} QR kod düzeltildi")
    
    # Kontrol et
    cursor.execute("""
        SELECT COUNT(*) as cnt FROM qr_codes 
        WHERE qr_id LIKE %s
        AND part_code_id = %s
    """, ('Y129A00-55730_%', correct_id))
    
    final_count = cursor.fetchone()['cnt']
    print(f"✅ Toplam düzeltilen QR: {final_count}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
