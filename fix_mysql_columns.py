#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MySQL'e eksik sütunları ekle"""

import pymysql

conn = pymysql.connect(
    host='192.168.0.57', 
    port=3306, 
    user='flaskuser', 
    password='FlaskSifre123!', 
    database='flaskdb'
)
cur = conn.cursor()

# part_codes tablosuna eksik sutunlar
part_cols = [
    ('created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'),
    ('updated_at', 'TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP'),
    ('is_package', 'TINYINT(1) DEFAULT 0'),
    ('package_items', 'TEXT')
]

print('=== part_codes ===')
for col, dtype in part_cols:
    try:
        cur.execute(f'ALTER TABLE part_codes ADD COLUMN {col} {dtype}')
        print(f'  + {col} eklendi')
    except Exception as e:
        if 'Duplicate' in str(e):
            print(f'  - {col} zaten var')
        else:
            print(f'  ! {col}: {e}')

# qr_codes tablosuna eksik sutunlar
print('\n=== qr_codes ===')
qr_cols = [
    ('used_count', 'INT DEFAULT 0'),
    ('first_used_at', 'TIMESTAMP NULL'),
    ('last_used_at', 'TIMESTAMP NULL'),
    ('is_active', 'TINYINT(1) DEFAULT 1')
]
for col, dtype in qr_cols:
    try:
        cur.execute(f'ALTER TABLE qr_codes ADD COLUMN {col} {dtype}')
        print(f'  + {col} eklendi')
    except Exception as e:
        if 'Duplicate' in str(e):
            print(f'  - {col} zaten var')
        else:
            print(f'  ! {col}: {e}')

# envanter_users tablosuna eksik sutunlar
print('\n=== envanter_users ===')
user_cols = [
    ('is_active_user', 'TINYINT(1) DEFAULT 1'),
    ('created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'),
    ('last_login', 'TIMESTAMP NULL'),
    ('role', "VARCHAR(50) DEFAULT 'user'")
]
for col, dtype in user_cols:
    try:
        cur.execute(f'ALTER TABLE envanter_users ADD COLUMN {col} {dtype}')
        print(f'  + {col} eklendi')
    except Exception as e:
        if 'Duplicate' in str(e):
            print(f'  - {col} zaten var')
        else:
            print(f'  ! {col}: {e}')

conn.commit()
conn.close()
print('\n[OK] Tamamlandı!')
