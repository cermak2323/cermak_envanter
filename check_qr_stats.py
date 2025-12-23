#!/usr/bin/env python3
# QR kod sayısını kontrol et

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
    
    # Toplam QR kod
    cursor.execute("SELECT COUNT(*) as cnt FROM qr_codes")
    total_qr = cursor.fetchone()['cnt']
    print(f"✅ Toplam QR kod: {total_qr}")
    
    # QR kodu olan parçalar
    cursor.execute("SELECT COUNT(DISTINCT part_code_id) as cnt FROM qr_codes")
    qr_parts = cursor.fetchone()['cnt']
    print(f"✅ QR kodu olan parça sayısı: {qr_parts}")
    
    # QR kodu olmayan parçalar
    cursor.execute("""
        SELECT COUNT(*) as cnt FROM part_codes
        WHERE id NOT IN (SELECT DISTINCT part_code_id FROM qr_codes)
    """)
    no_qr_parts = cursor.fetchone()['cnt']
    print(f"✅ QR kodu OLMAYAN parça sayısı: {no_qr_parts}")
    
    # Top 10 parça - QR sayıları
    print("\n📊 Top 10 - QR sayıları:")
    cursor.execute("""
        SELECT pc.part_code, pc.part_name, COUNT(q.qr_id) as qr_count
        FROM part_codes pc
        LEFT JOIN qr_codes q ON pc.id = q.part_code_id
        GROUP BY pc.id
        ORDER BY qr_count DESC
        LIMIT 10
    """)
    
    top = cursor.fetchall()
    for row in top:
        print(f"  {row['part_code']}: {row['qr_count']} QR")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
