#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, r'c:\Users\rsade\Desktop\Yeni klasör\EnvanterQR\EnvanterQR')

from order_system import get_order_db

# MySQL bağlantısını al
conn = get_order_db()
cursor = conn.cursor()

# Örnek parça kodları al
cursor.execute('SELECT id, part_code, part_name, status, ordered_quantity, received_quantity FROM order_list LIMIT 5')
rows = cursor.fetchall()
print("Veritabanı sonuçları:")
for i, row in enumerate(rows):
    # row dict olabilir
    if isinstance(row, dict):
        print(f"{i+1}. ID: {row['id']}, Parça: {row['part_code']}, Durum: {row['status']}")
    else:
        print(f"{i+1}. ID: {row[0]}, Parça: {row[1]}, Durum: {row[3]}")

conn.close()
print("\n✓ Veritabanı bağlantısı başarılı!")
