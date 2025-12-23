#!/usr/bin/env python3
# Eski sipariş metinlerini part_codes tablosundan temizle

import pymysql

try:
    conn = pymysql.connect(
        host='192.168.0.57',
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
    
    # Kontrol et - temizlenen parçaları göster
    cursor.execute("SELECT part_code, part_name, description FROM part_codes WHERE description != '' LIMIT 10")
    remaining = cursor.fetchall()
    
    if remaining:
        print("\n📋 Hala açıklama olan parçalar (örnek):")
        for p in remaining:
            print(f"  - {p['part_code']}: {p.get('description', '')[:50]}")
    else:
        print("✅ Tüm açıklamalar temizlendi!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Hata: {e}")
