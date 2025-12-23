#!/usr/bin/env python3
"""Test JCB package scanning"""

import requests
import json

BASE_URL = "http://127.0.0.1:5002"

print("=" * 60)
print("TEST: JCB Package Scanning")
print("=" * 60)

# Test scanning JCB
print("\n[TEST] Scanning JCB QR code...")
response = requests.post(
    f"{BASE_URL}/api/scan_qr",
    json={"qr_id": "JCB", "session_id": "test_session_jcb"},
    headers={"Content-Type": "application/json"}
)

print(f"Status Code: {response.status_code}")
data = response.json()
print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")

if data.get('success'):
    print("\n✓ JCB PACKAGE RECOGNIZED AND SCANNED!")
    if 'items' in data:
        items = data.get('items', [])
        print(f"✓ Total items in package: {len(items)}")
        if len(items) > 0:
            print(f"  Sample items:")
            for item in items[:5]:
                print(f"    - {item.get('part_code', '?')}: qty {item.get('quantity', 0)}")
else:
    print("\n✗ JCB PACKAGE NOT RECOGNIZED!")
    print(f"Error: {data.get('message', 'Unknown error')}")

print("\n" + "=" * 60)
