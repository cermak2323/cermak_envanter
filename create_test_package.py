import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('instance/envanter_local.db')
c = conn.cursor()

# Create test items
items = [
    ('11111-11111', 'Test Part 1', 2),
    ('22222-22222', 'Test Part 2', 2),
    ('33333-33333', 'Test Part 3', 2),
    ('44444-44444', 'Test Part 4', 2),
    ('55555-55555', 'Test Part 5', 2),
]

# Insert items
for part_code, part_name, qty in items:
    c.execute('''
        INSERT INTO part_codes (part_code, part_name, is_package, created_at)
        VALUES (?, ?, ?, ?)
    ''', (part_code, part_name, False, datetime.now()))

# Create package
package_items = [
    {'part_code': '11111-11111', 'quantity': 2},
    {'part_code': '22222-22222', 'quantity': 2},
    {'part_code': '33333-33333', 'quantity': 2},
    {'part_code': '44444-44444', 'quantity': 2},
    {'part_code': '55555-55555', 'quantity': 2},
]

c.execute('''
    INSERT INTO part_codes (part_code, part_name, is_package, package_items, created_at)
    VALUES (?, ?, ?, ?, ?)
''', ('JPN', 'JPN PARÇALARI', True, json.dumps(package_items), datetime.now()))

conn.commit()

# Verify
c.execute("SELECT COUNT(*) FROM part_codes")
print(f"Part codes: {c.fetchone()[0]}")

c.execute("SELECT part_code, is_package, package_items FROM part_codes WHERE part_code = 'JPN'")
jpn = c.fetchone()
print(f"\nJPN Package Created:")
print(f"  Code: {jpn[0]}")
print(f"  Is Package: {jpn[1]}")
print(f"  Items: {len(json.loads(jpn[2]))} items")
for item in json.loads(jpn[2]):
    print(f"    - {item['part_code']}: qty {item['quantity']}")

conn.close()
print("\nReady for testing!")
