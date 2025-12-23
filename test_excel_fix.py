"""
Test Excel Report Field Name Fix
Verifies that 'Parça Kodu' (with ç) is correctly parsed
"""
import json

# Simulated JSON from database (what's actually stored)
description_from_db = '''
[
    {"Parça Kodu": "Y129648-01780", "Beklenen Adet": 5},
    {"Parça Kodu": "ANTİF03", "Beklenen Adet": 10},
    {"Parça Kodu": "Y123672-01782", "Beklenen Adet": 2}
]
'''

print("=" * 60)
print("EXCEL REPORT FIELD NAME FIX TEST")
print("=" * 60)

# Parse the JSON
expected_list = json.loads(description_from_db)
print(f"\n✅ Parsed {len(expected_list)} items from JSON")

# OLD CODE (BROKEN) - This was the bug
print("\n❌ OLD CODE (BROKEN):")
expected_parts_old = {}
for item in expected_list:
    part_code = item.get('Para Kodu') or item.get('part_code')  # WRONG!
    expected_qty = item.get('Beklenen Adet') or 0
    if part_code:
        expected_parts_old[part_code] = int(expected_qty)
        
print(f"   Found {len(expected_parts_old)} parts: {list(expected_parts_old.keys())}")
if len(expected_parts_old) == 0:
    print("   🐛 BUG: No parts found because 'Para Kodu' doesn't exist!")

# NEW CODE (FIXED) - This is the fix
print("\n✅ NEW CODE (FIXED):")
expected_parts_new = {}
for item in expected_list:
    # FIX: Correct field name is 'Parça Kodu' (with ç) not 'Para Kodu'
    part_code = item.get('Parça Kodu') or item.get('Para Kodu') or item.get('part_code')
    expected_qty = item.get('Beklenen Adet') or 0
    if part_code:
        expected_parts_new[part_code] = int(expected_qty)
        
print(f"   Found {len(expected_parts_new)} parts:")
for code, qty in expected_parts_new.items():
    print(f"      {code}: {qty} expected")

# Verify the fix
print("\n" + "=" * 60)
if len(expected_parts_new) == 3 and 'ANTİF03' in expected_parts_new:
    print("✅ FIX VERIFIED: All parts correctly parsed with expected quantities!")
    print(f"   ANTİF03 expected: {expected_parts_new['ANTİF03']} (should be 10)")
else:
    print("❌ FIX FAILED: Parts not correctly parsed")
print("=" * 60)
