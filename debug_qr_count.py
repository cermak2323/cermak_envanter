#!/usr/bin/env python3
# QR sayılarının doğru gelip gelmediğini kontrol et

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
    
    # ORM kodu ile aynı SQL
    cursor.execute("""
        SELECT 
            pc.id,
            pc.part_code,
            pc.part_name,
            pc.description,
            pc.created_at,
            COUNT(q.qr_id) as qr_count
        FROM part_codes pc
        LEFT JOIN qr_codes q ON pc.id = q.part_code_id
        GROUP BY pc.id
        ORDER BY pc.created_at DESC
        LIMIT 20
    """)
    
    results = cursor.fetchall()
    
    print(f"✅ {len(results)} parça döndü\n")
    
    for i, row in enumerate(results[:20]):
        print(f"{i+1}. {row['part_code']}: {row['part_name'][:30]:30s} | QR: {row['qr_count']}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
