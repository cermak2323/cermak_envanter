#!/usr/bin/env python3
# Eski sipariş metinlerini part_codes tablosundan temizle

import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='cermak',
        database='flaskdb',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    cursor = conn.cursor()
    
    # Sipariş metinlerini içeren açıklamaları temizle
    cursor.execute("""
        UPDATE part_codes 
        SET description = '' 
        WHERE description LIKE '%sipariş%' 
           OR description LIKE '%takeuchi%' 
           OR description LIKE '%Takeuchi%'
           OR description LIKE '%tr sipariş%'
           OR description LIKE '%Gelmedi%'
    """)
    
    rows_updated = cursor.rowcount
    conn.commit()
    
    print(f"✅ {rows_updated} satır temizlendi")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Hata: {e}")
