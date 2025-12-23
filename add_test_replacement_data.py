#!/usr/bin/env python3
"""
Test verisi ekle: replacement_code ve build_out
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
    
    print("=" * 80)
    print("TEST VERİSİ EKLENIYOR")
    print("=" * 80)
    
    # İlk 10 parçaya test verisi ekle
    cursor.execute("""
        SELECT id, part_code FROM parts_info ORDER BY id LIMIT 10
    """)
    
    rows = cursor.fetchall()
    
    for idx, (part_id, part_code) in enumerate(rows):
        if idx % 2 == 0:
            # Çift indeksliler için replacement_code ekle
            replacement = f"REPL-{part_code[-6:]}" if len(part_code) > 6 else f"REPL-{part_code}"
            cursor.execute("""
                UPDATE parts_info 
                SET replacement_code = %s 
                WHERE id = %s
            """, (replacement, part_id))
            print(f"✓ ID {part_id} ({part_code}): replacement_code = {replacement}")
        
        if idx % 3 == 0:
            # 3'e bölüne olanlar BUILD OUT
            cursor.execute("""
                UPDATE parts_info 
                SET build_out = 1 
                WHERE id = %s
            """, (part_id,))
            print(f"✓ ID {part_id} ({part_code}): build_out = 1 (discontinued)")
    
    conn.commit()
    
    print("\n" + "=" * 80)
    print("KONTROL: Yeni verileri görüntüle")
    print("=" * 80)
    
    cursor.execute("""
        SELECT part_code, replacement_code, build_out 
        FROM parts_info ORDER BY id LIMIT 10
    """)
    
    results = cursor.fetchall()
    for part_code, repl_code, build in results:
        repl = repl_code if repl_code else "NULL"
        build = "BUILD OUT" if build else "Active"
        print(f"{part_code:20} | Repl: {repl:15} | {build}")
    
    print("\n✓ Test verisi başarıyla eklendi!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"✗ Error: {e}")
