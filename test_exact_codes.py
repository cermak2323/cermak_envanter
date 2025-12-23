#!/usr/bin/env python3
"""
Test exact match for codes that definitely exist
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app

print("\n" + "="*70)
print("Exact Code Search Test")
print("="*70 + "\n")

with app.test_client() as client:
    test_cases = [
        ('Y129150-49811', 'Var olan kod (29811)'),
        ('Y129150-49100', 'Var olan kod (49100)'),
        ('Y129150-48811', 'Olmayan kod (48811) - Scanner hatası mı?'),
    ]
    
    for query, desc in test_cases:
        response = client.get(f'/api/search_parts?q={query}')
        data = response.get_json() if response.status_code == 200 else []
        
        status = f"[OK] {len(data)} sonuç" if data else "[FAIL] 0 sonuç"
        print(f"{desc}")
        print(f"  Kod: {query}")
        print(f"  Status: {status}")
        if data:
            print(f"  Bulundu: {data[0]['part_code']}")
        print()

print("="*70 + "\n")
