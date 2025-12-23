#!/usr/bin/env python3
"""
Check if specific QR codes exist in database
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, execute_query, get_db

with app.app_context():
    conn = get_db()
    cursor = conn.cursor()
    
    print("\nVeritabanında aranacak kodlar:\n")
    
    codes = [
        'Y129150-48811',
        'Y129150-49811',
        'Y129150',
    ]
    
    for code in codes:
        cursor = execute_query(cursor, 'SELECT part_code FROM part_codes WHERE part_code LIKE %s LIMIT 5', (f'%{code}%',))
        results = cursor.fetchall()
        
        print(f"Kod: '{code}'")
        if results:
            print(f"  Bulundu: {len(results)} sonuç")
            for row in results:
                print(f"    - {row[0]}")
        else:
            print(f"  Bulunamadı")
        print()
