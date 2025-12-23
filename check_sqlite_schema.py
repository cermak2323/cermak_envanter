#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('instance/envanter_local.db')
cursor = conn.cursor()

tables = ['part_codes', 'envanter_users', 'qr_codes', 'count_sessions', 'scanned_qr', 'count_passwords']

for table in tables:
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    if columns:
        print(f'\n{table}:')
        for col in columns:
            col_id, col_name, col_type, notnull, default, pk = col
            print(f'  - {col_name}: {col_type}')
    else:
        print(f'\n{table}: (empty or not found)')

conn.close()
