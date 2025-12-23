#!/usr/bin/env python3
"""
Debug the execute_query function to see what's being returned
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, execute_query, get_db

print("\n" + "="*70)
print("DEBUG: execute_query function")
print("="*70 + "\n")

with app.app_context():
    conn = get_db()
    cursor = conn.cursor()
    
    # Test a direct query
    print("[TEST 1] Simple SELECT query")
    result = execute_query(cursor, 'SELECT COUNT(*) FROM part_codes', None)
    print(f"  Result type: {type(result)}")
    print(f"  Result._rows type: {type(result._rows)}")
    print(f"  Result._rows length: {len(result._rows)}")
    
    row = result.fetchone()
    print(f"  First row: {row}")
    if row:
        print(f"  Count: {row[0]}")
    
    # Test with parameter
    print("\n[TEST 2] SELECT with parameter")
    result = execute_query(cursor, 'SELECT part_code, part_name FROM part_codes WHERE part_code = %s LIMIT 1', ('11111-11111',))
    print(f"  Result type: {type(result)}")
    print(f"  Result._rows: {result._rows}")
    
    rows = result.fetchall()
    print(f"  Rows length: {len(rows)}")
    if rows:
        print(f"  First row: {rows[0]}")
    
    # Test with LIKE
    print("\n[TEST 3] SELECT LIKE with parameters")
    result = execute_query(cursor, 'SELECT part_code, part_name FROM part_codes WHERE part_code LIKE %s OR part_name LIKE %s LIMIT 5', ('%11111%', '%11111%'))
    print(f"  Result type: {type(result)}")
    print(f"  Result._rows length: {len(result._rows)}")
    
    rows = result.fetchall()
    print(f"  Rows: {rows}")

print("\n" + "="*70 + "\n")
