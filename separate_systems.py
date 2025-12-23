#!/usr/bin/env python3
# QR kodu olan parçaları part_codes'ta tut, order_system_stock parçalarını sil

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
    
    print("1️⃣ QR kodu olan parçaları buluyorum...")
    # QR kodu olan parçaların part_code_id'lerini al
    cursor.execute("""
        SELECT DISTINCT pc.id, pc.part_code
        FROM part_codes pc
        INNER JOIN qr_codes q ON pc.id = q.part_code_id
    """)
    
    qr_parts = cursor.fetchall()
    qr_part_codes = [p['part_code'] for p in qr_parts]
    
    print(f"   ✅ {len(qr_part_codes)} parça QR kodlu bulundu")
    
    print("\n2️⃣ Order sistem parçalarını siliyorum...")
    # Order_system_stock'ta olan parçaları part_codes'tan sil
    cursor.execute("""
        SELECT DISTINCT part_code FROM order_system_stock
    """)
    
    order_parts = cursor.fetchall()
    order_part_codes = [p['part_code'] for p in order_parts]
    
    # Silinecekler = order parçaları - QR parçaları
    to_delete = [p for p in order_part_codes if p not in qr_part_codes]
    
    if to_delete:
        placeholders = ','.join(['%s'] * len(to_delete))
        cursor.execute(f"DELETE FROM part_codes WHERE part_code IN ({placeholders})", to_delete)
        deleted = cursor.rowcount
        print(f"   ✅ {deleted} order sistemi parçası silindi")
    else:
        print(f"   ✅ Silinecek order parçası yok")
    
    conn.commit()
    
    print("\n3️⃣ Kontrol:")
    cursor.execute("SELECT COUNT(*) as cnt FROM part_codes")
    total_parts = cursor.fetchone()['cnt']
    print(f"   - part_codes toplam: {total_parts}")
    
    cursor.execute("SELECT COUNT(*) as cnt FROM order_system_stock")
    order_total = cursor.fetchone()['cnt']
    print(f"   - order_system_stock toplam: {order_total}")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Tamamlandı - İki sistem ayrıldı!")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
