#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, r'c:\Users\rsade\Desktop\Yeni klasör\EnvanterQR\EnvanterQR')

from order_system import get_order_db

# MySQL bağlantısını al
conn = get_order_db()
cursor = conn.cursor()

# Test: Durum güncelleme
order_id = 49  # İlk order
new_status = 'Kısmi'
received_qty = 10
notes = 'Test notası'

print(f"Durum güncelleme test: Order ID {order_id}")

try:
    cursor.execute("""
        UPDATE order_list
        SET status = %s,
            received_quantity = %s,
            notes = %s,
            status_updated_date = NOW()
        WHERE id = %s
    """, (new_status, received_qty, notes, order_id))
    
    conn.commit()
    print("✅ Güncelleme başarılı")
    
    # Kontrol et
    cursor.execute("SELECT id, part_code, status, received_quantity, notes FROM order_list WHERE id = %s", (order_id,))
    result = cursor.fetchone()
    if result:
        print(f"Güncellenmiş sipariş: {result}")
    
except Exception as e:
    print(f"❌ Hata: {e}")
finally:
    conn.close()
    print("✓ Bağlantı kapatıldı")
