#!/usr/bin/env python3
"""
Test search with exact part codes that exist in database
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app

print("\n" + "="*70)
print("PART SEARCH TEST - QR Tarama Benzetimi")
print("="*70 + "\n")

with app.test_client() as client:
    test_cases = [
        ('Y129150-48811', 'QR code test'),
        ('y129150-48811', 'Küçük harf QR code'),
        ('Y129150', 'Kısaltılmış kod (varsa)'),
    ]
    
    for query, description in test_cases:
        print(f"\n[TEST] Kod: '{query}' ({description})")
        response = client.get(f'/api/search_parts?q={query}')
        
        if response.status_code == 200:
            data = response.get_json()
            if data and len(data) > 0:
                print(f"  [OK] {len(data)} sonuç bulundu:")
                for result in data[:2]:
                    print(f"    - {result['part_code']}: {result.get('description', 'N/A')}")
            else:
                print(f"  [NO MATCH] Sonuç yok")
        else:
            print(f"  [ERROR] HTTP {response.status_code}")

print("\n" + "="*70 + "\n")
