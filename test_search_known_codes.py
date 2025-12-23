#!/usr/bin/env python3
"""
Test search for known part codes from the database
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app
import json

print("\n" + "="*70)
print("SEARCH TEST WITH KNOWN PART CODES")
print("="*70 + "\n")

with app.test_client() as client:
    test_cases = [
        ('11111-11111', 'Exact match test'),
        ('11111', 'Partial match test'),
        ('JPN', 'Another code test'),
        ('HLP46', 'Another code test 2'),
        ('Y129', 'Y series test'),
    ]
    
    for query, description in test_cases:
        print(f"\n[TEST] Search: '{query}' ({description})")
        response = client.get(f'/api/search_parts?q={query}')
        print(f"  Status: {response.status_code}")
        data = response.get_json()
        
        if data and len(data) > 0:
            print(f"  [OK] Found {len(data)} results:")
            for i, result in enumerate(data[:3], 1):  # Show first 3
                print(f"    {i}. {result}")
        else:
            print(f"  [FAIL] No results found")

print("\n" + "="*70 + "\n")
