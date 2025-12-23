#!/usr/bin/env python3
"""Check what part codes exist in database"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app

print("\n" + "="*70)
print("Checking Part Codes in Database")
print("="*70 + "\n")

with app.test_client() as client:
    # Use /api/search_parts to find any codes
    response = client.get('/api/search_parts?q=%')
    
    if response.status_code == 200:
        data = response.get_json()
        print(f"Found {len(data)} parts\n")
        
        if len(data) > 0:
            print("First 10 parts:")
            for i, part in enumerate(data[:10], 1):
                desc = part.get('description') or 'N/A'
                desc = desc[:40] if desc else 'N/A'
                print(f"  {i}. {part.get('part_code')} - {desc}")
            
            # Test the first code with /api/part_details
            first_code = data[0]['part_code']
            print(f"\n[TEST] GET /api/part_details/{first_code}")
            response2 = client.get(f'/api/part_details/{first_code}')
            print(f"  Status: {response2.status_code}")
            if response2.status_code == 200:
                print(f"  SUCCESS ✓")
        else:
            print("No parts found in database!")
    else:
        print(f"Search failed: {response.status_code}")

print("\n" + "="*70 + "\n")
