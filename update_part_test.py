#!/usr/bin/env python3
"""
Test: 03593-07400 parçasını replacement_code ve build_out ile manuel olarak güncelle
"""

import mysql.connector

try:
    conn = mysql.connector.connect(
        host='192.168.0.57',
        user='flaskuser',
        password='FlaskSifre123!',
        database='flaskdb',
        port=3306
    )
    
    cursor = conn.cursor()
    
    part_code = '03593-07400'
    replacement_code = '03793-66006'
    build_out = 1  # "Build Out" text
    
    print("=" * 80)
    print(f"Güncellemeden önce: {part_code}")
    print("=" * 80)
    
    cursor.execute("""
        SELECT part_code, replacement_code, build_out FROM parts_info WHERE part_code = %s
    """, (part_code,))
    before = cursor.fetchone()
    print(f"Replacement Code: {before[1]}")
    print(f"Build Out: {before[2]}")
    
    # Güncelle
    print(f"\nGüncelleniyor: replacement_code={replacement_code}, build_out={build_out}")
    cursor.execute("""
        UPDATE parts_info 
        SET replacement_code = %s, build_out = %s 
        WHERE part_code = %s
    """, (replacement_code, build_out, part_code))
    
    conn.commit()
    
    # Kontrol
    print(f"\nGüncellendikten sonra: {part_code}")
    print("=" * 80)
    
    cursor.execute("""
        SELECT part_code, replacement_code, build_out FROM parts_info WHERE part_code = %s
    """, (part_code,))
    after = cursor.fetchone()
    print(f"Replacement Code: {after[1]}")
    print(f"Build Out: {after[2]}")
    
    print("\n✓ Test tamamlandı!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"✗ Error: {e}")
