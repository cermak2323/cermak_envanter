#!/usr/bin/env python3
"""
Direct test of the search API to verify the fix works
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Disable SQLAlchemy query caching for this test
import os
os.environ['SQLALCHEMY_ECHO'] = 'false'

from app import app
import json

print("\n" + "="*70)
print("DIRECT SEARCH API TEST")
print("="*70 + "\n")

with app.test_client() as client:
    # Test 1: Search for part code
    print("[TEST 1] Search for part code 'Y129150'")
    response = client.get('/api/search_parts?q=Y129150')
    print(f"Status: {response.status_code}")
    data = response.get_json()
    print(f"Results: {len(data) if data else 0} items found")
    if data:
        print(f"First result: {data[0] if data else 'None'}")
    
    # Test 2: Search with LIKE pattern
    print("\n[TEST 2] Search for pattern 'Y12'")
    response = client.get('/api/search_parts?q=Y12')
    print(f"Status: {response.status_code}")
    data = response.get_json()
    print(f"Results: {len(data) if data else 0} items found")
    if data and len(data) > 0:
        print(f"First 3 results: {data[:3]}")
    
    # Test 3: Empty search
    print("\n[TEST 3] Empty search")
    response = client.get('/api/search_parts?q=')
    print(f"Status: {response.status_code}")
    data = response.get_json()
    print(f"Results: {len(data) if data else 0} items found")

print("\n" + "="*70)
print("SEARCH API TEST COMPLETE")
print("="*70 + "\n")
