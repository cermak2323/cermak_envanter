#!/usr/bin/env python3
# order_system_stock'tan gelen parçaları part_codes'tan sil

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
    
    # order_system_stock'ta olan part_code'ları bul
    cursor.execute("SELECT DISTINCT part_code FROM order_system_stock")
    order_codes = cursor.fetchall()
    
    deleted_count = 0
    for row in order_codes:
        part_code = row['part_code']
        cursor.execute("DELETE FROM part_codes WHERE part_code = %s", (part_code,))
        deleted_count += cursor.rowcount
    
    conn.commit()
    
    print(f"✅ {deleted_count} parça silindi (order_system_stock'ta olanlar)")
    
    # Kalan parçaları göster
    cursor.execute("SELECT COUNT(*) as cnt FROM part_codes")
    remaining = cursor.fetchone()
    print(f"✅ part_codes tablosunda kalan: {remaining['cnt']} parça")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
