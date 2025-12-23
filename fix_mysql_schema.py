#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MySQL tablosu duzeltmeleri - models.py ile uyumlu hale getir"""

import pymysql

conn = pymysql.connect(
    host='192.168.0.57',
    port=3306,
    user='flaskuser',
    password='FlaskSifre123!',
    database='flaskdb'
)
cur = conn.cursor()

# 1. qr_codes - qr_id sutununu ekle
print('=== qr_codes duzeltmeleri ===')
try:
    cur.execute('ALTER TABLE qr_codes ADD COLUMN qr_id VARCHAR(100)')
    print('qr_id eklendi')
except Exception as e:
    if 'Duplicate' in str(e):
        print('qr_id zaten var')
    else:
        print(f'qr_id: {e}')

try:
    cur.execute('ALTER TABLE qr_codes ADD COLUMN used_count INT DEFAULT 0')
    print('used_count eklendi')
except Exception as e:
    if 'Duplicate' in str(e):
        print('used_count zaten var')

try:
    cur.execute('ALTER TABLE qr_codes ADD COLUMN first_used_at TIMESTAMP NULL')
    print('first_used_at eklendi')
except Exception as e:
    if 'Duplicate' in str(e):
        print('first_used_at zaten var')

try:
    cur.execute('ALTER TABLE qr_codes ADD COLUMN last_used_at TIMESTAMP NULL')
    print('last_used_at eklendi')
except Exception as e:
    if 'Duplicate' in str(e):
        print('last_used_at zaten var')

try:
    cur.execute('ALTER TABLE qr_codes ADD COLUMN is_active TINYINT(1) DEFAULT 1')
    print('is_active eklendi')
except Exception as e:
    if 'Duplicate' in str(e):
        print('is_active zaten var')

# qr_id = qr_code olarak set et
cur.execute("UPDATE qr_codes SET qr_id = qr_code WHERE qr_id IS NULL OR qr_id = ''")
print(f'qr_id guncellendi: {cur.rowcount}')

# 2. count_sessions - eksik sutunlar
print('\n=== count_sessions duzeltmeleri ===')
cols = [
    ('is_active', 'TINYINT(1) DEFAULT 1'),
    ('ended_at', 'TIMESTAMP NULL'),
    ('created_by', 'INT'),
    ('session_password', 'VARCHAR(255)'),
    ('description', 'TEXT')
]
for col, dtype in cols:
    try:
        cur.execute(f'ALTER TABLE count_sessions ADD COLUMN {col} {dtype}')
        print(f'{col} eklendi')
    except Exception as e:
        if 'Duplicate' in str(e):
            print(f'{col} zaten var')
        else:
            print(f'{col}: {e}')

# ended_at = finished_at kopyala
cur.execute('UPDATE count_sessions SET ended_at = finished_at WHERE ended_at IS NULL AND finished_at IS NOT NULL')
print(f'ended_at guncellendi: {cur.rowcount}')

# 3. scanned_qr - qr_id ve part_code ekle
print('\n=== scanned_qr duzeltmeleri ===')
cols = [
    ('qr_id', 'VARCHAR(255)'),
    ('part_code', 'VARCHAR(255)'),
    ('scanned_by', 'INT')
]
for col, dtype in cols:
    try:
        cur.execute(f'ALTER TABLE scanned_qr ADD COLUMN {col} {dtype}')
        print(f'{col} eklendi')
    except Exception as e:
        if 'Duplicate' in str(e):
            print(f'{col} zaten var')
        else:
            print(f'{col}: {e}')

# qr_id = qr_code, part_code = part_number
cur.execute("UPDATE scanned_qr SET qr_id = qr_code WHERE qr_id IS NULL OR qr_id = ''")
print(f'qr_id guncellendi: {cur.rowcount}')
cur.execute("UPDATE scanned_qr SET part_code = part_number WHERE part_code IS NULL OR part_code = ''")
print(f'part_code guncellendi: {cur.rowcount}')

# 4. count_passwords - session_id ve created_by ekle
print('\n=== count_passwords duzeltmeleri ===')
cols = [
    ('session_id', 'INT'),
    ('password', 'VARCHAR(255)'),
    ('created_by', 'INT')
]
for col, dtype in cols:
    try:
        cur.execute(f'ALTER TABLE count_passwords ADD COLUMN {col} {dtype}')
        print(f'{col} eklendi')
    except Exception as e:
        if 'Duplicate' in str(e):
            print(f'{col} zaten var')
        else:
            print(f'{col}: {e}')

conn.commit()

# Sonuc kontrolu
print('\n=== SONUC ===')
for t in ['qr_codes', 'part_codes', 'count_sessions', 'scanned_qr']:
    cur.execute(f'SELECT COUNT(*) FROM {t}')
    print(f'{t}: {cur.fetchone()[0]} kayit')

conn.close()
print('\nTAMAMLANDI!')
