#!/usr/bin/env python3
"""Direct test without Flask"""

import sqlite3
import os

db_path = os.path.join('instance', 'envanter_local.db')
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Test direct SQL
part_code = '11111-11111'
cursor.execute("SELECT part_code, description FROM part_codes WHERE part_code = ?", (part_code,))
result = cursor.fetchone()

print(f"Direct query for '{part_code}':")
print(f"  Result: {result}")

if result:
    print(f"  ✓ SUCCESS - Part code found!")
else:
    print(f"  ✗ NOT FOUND")

conn.close()
