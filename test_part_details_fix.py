#!/usr/bin/env python3
"""Test /api/part_details endpoint after placeholder fix"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app

print("\n" + "="*70)
print("Testing /api/part_details Endpoint After Fix")
print("="*70 + "\n")

with app.test_client() as client:
    test_codes = ['Y129150-49811', 'Y129150-49100', 'Y129150', '00010-90002']
    
    for code in test_codes:
        print(f"\n[TEST] GET /api/part_details/{code}")
        response = client.get(f'/api/part_details/{code}')
        
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"  Result: SUCCESS [OK]")
            print(f"    - Part Code: {data.get('part_code')}")
            print(f"    - Description: {data.get('description', 'N/A')[:50]}")
        elif response.status_code == 404:
            print(f"  Result: NOT FOUND")
        else:
            print(f"  Result: ERROR")
            print(f"    Response: {response.data}")

print("\n" + "="*70 + "\n")
