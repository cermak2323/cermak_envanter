#!/usr/bin/env python3
"""
Kontrol: 03593-07400 parçasının database'deki verisi nedir?
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
    
    print("=" * 80)
    print(f"KONTROL: {part_code} parçasının verisi")
    print("=" * 80)
    
    cursor.execute("""
        SELECT 
            part_code,
            part_name,
            stock,
            supplier,
            sale_price_eur,
            replacement_code,
            build_out
        FROM parts_info
        WHERE part_code = %s
    """, (part_code,))
    
    result = cursor.fetchone()
    
    if result:
        print(f"\nPart Code:         {result[0]}")
        print(f"Part Name:         {result[1]}")
        print(f"Stock:             {result[2]}")
        print(f"Supplier:          {result[3]}")
        print(f"Sale Price EUR:    {result[4]}")
        print(f"Replacement Code:  {result[5]}")
        print(f"Build Out:         {result[6]}")
    else:
        print(f"\n✗ Part {part_code} database'de bulunmadı!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"✗ Error: {e}")
