#!/usr/bin/env python3
"""Check part codes in SQLite directly"""

import sqlite3
import os

db_path = os.path.join('instance', 'envanter_local.db')

if not os.path.exists(db_path):
    print(f"Database not found: {db_path}")
else:
    print(f"Database: {db_path}\n")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='part_codes'")
    if cursor.fetchone():
        # Count parts
        cursor.execute("SELECT COUNT(*) FROM part_codes")
        count = cursor.fetchone()[0]
        print(f"Total part_codes: {count}\n")
        
        if count > 0:
            # Get first 5
            cursor.execute("SELECT part_code, description FROM part_codes LIMIT 5")
            rows = cursor.fetchall()
            print("First 5 parts:")
            for i, (code, desc) in enumerate(rows, 1):
                d = (desc or 'N/A')[:40]
                print(f"  {i}. {code} - {d}")
    else:
        print("Table 'part_codes' not found!")
    
    conn.close()
