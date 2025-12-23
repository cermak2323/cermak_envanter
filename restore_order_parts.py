#!/usr/bin/env python3
# order_system_stock'taki parçaları part_codes'a geri yükle

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
    
    # order_system_stock'tan parçaları al ve part_codes'a ekle/güncelle
    cursor.execute("""
        SELECT DISTINCT part_code, part_name, supplier as description
        FROM order_system_stock
        ORDER BY part_code
    """)
    
    stock_parts = cursor.fetchall()
    
    inserted = 0
    updated = 0
    
    for part in stock_parts:
        # Mevcut kontrolü yap
        cursor.execute("SELECT id FROM part_codes WHERE part_code = %s", (part['part_code'],))
        exists = cursor.fetchone()
        
        if exists:
            # Varsa güncelle
            cursor.execute("""
                UPDATE part_codes 
                SET part_name = %s, description = %s
                WHERE part_code = %s
            """, (part['part_name'], part['description'], part['part_code']))
            updated += cursor.rowcount
        else:
            # Yoksa ekle
            cursor.execute("""
                INSERT INTO part_codes (part_code, part_number, part_name, description, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            """, (part['part_code'], part['part_code'], part['part_name'], part['description']))
            inserted += cursor.rowcount
    
    conn.commit()
    
    print(f"✅ Tamamlandı:")
    print(f"   - Eklenen: {inserted} parça")
    print(f"   - Güncellenen: {updated} parça")
    
    # Kontrol et
    cursor.execute("SELECT COUNT(*) as cnt FROM part_codes")
    total = cursor.fetchone()
    print(f"   - Toplam part_codes: {total['cnt']} parça")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
