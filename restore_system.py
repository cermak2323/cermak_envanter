#!/usr/bin/env python3
# Silinen parçaları geri yükle, ama description boş bırak

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
    
    print("1️⃣ order_system_stock'taki parçaları part_codes'a yüklüyorum...")
    
    # order_system_stock'tan parçaları al
    cursor.execute("""
        SELECT DISTINCT part_code, part_name
        FROM order_system_stock
        ORDER BY part_code
    """)
    
    stock_parts = cursor.fetchall()
    
    inserted = 0
    already_exists = 0
    
    for part in stock_parts:
        # Mevcut kontrolü yap
        cursor.execute("SELECT id FROM part_codes WHERE part_code = %s", (part['part_code'],))
        exists = cursor.fetchone()
        
        if not exists:
            # Yoksa ekle (description boş!)
            try:
                cursor.execute("""
                    INSERT INTO part_codes (part_code, part_number, part_name, description, created_at)
                    VALUES (%s, %s, %s, '', NOW())
                """, (part['part_code'], part['part_code'], part['part_name']))
                inserted += 1
            except Exception as e:
                if 'Duplicate' not in str(e):
                    print(f"  ⚠️ {part['part_code']}: {e}")
        else:
            already_exists += 1
    
    conn.commit()
    
    print(f"\n✅ Tamamlandı:")
    print(f"   - Eklenen yeni: {inserted}")
    print(f"   - Zaten mevcut: {already_exists}")
    
    # Kontrol
    cursor.execute("SELECT COUNT(*) as cnt FROM part_codes")
    total = cursor.fetchone()['cnt']
    print(f"   - part_codes TOPLAM: {total}")
    
    # Description'da TAKEUCHI vb kalanlı temizle
    print("\n2️⃣ Eski açıklamaları temizliyorum...")
    cursor.execute("""
        UPDATE part_codes 
        SET description = '' 
        WHERE description IS NOT NULL 
        AND description != ''
        AND (description LIKE '%takeuchi%' OR description LIKE '%Takeuchi%' 
             OR description LIKE '%sipariş%' OR description LIKE '%TR%')
    """)
    
    cleaned = cursor.rowcount
    conn.commit()
    print(f"   ✅ {cleaned} açıklama temizlendi")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Sistem restore edildi - İki sistem bağımsız!")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
