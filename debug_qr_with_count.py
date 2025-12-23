#!/usr/bin/env python3
# QR sayısı olan parçaları göster

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
    
    # QR sayısı > 0 olan parçalar
    cursor.execute("""
        SELECT 
            pc.id,
            pc.part_code,
            pc.part_name,
            COUNT(q.qr_id) as qr_count
        FROM part_codes pc
        LEFT JOIN qr_codes q ON pc.id = q.part_code_id
        GROUP BY pc.id
        HAVING COUNT(q.qr_id) > 0
        ORDER BY qr_count DESC
        LIMIT 20
    """)
    
    results = cursor.fetchall()
    
    print(f"✅ QR kodu olan {len(results)} parça\n")
    
    for i, row in enumerate(results[:20]):
        print(f"{i+1}. {row['part_code']:20s} | {row['part_name'][:30]:30s} | QR: {row['qr_count']}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Hata: {e}")
