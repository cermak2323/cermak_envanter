#!/usr/bin/env python3
"""Debug JCB package"""

import pymysql
import json

conn = pymysql.connect(
    host='192.168.0.57',
    port=3306,
    user='flaskuser',
    password='FlaskSifre123!',
    database='flaskdb',
    charset='utf8mb4'
)

cursor = conn.cursor()

# Check all JCB-related records
print("[CHECK] Looking for JCB package...")
cursor.execute("""
    SELECT id, part_code, part_name, is_package, package_items, 
           CHAR_LENGTH(package_items) as items_len
    FROM part_codes 
    WHERE part_code = 'JCB'
""")

results = cursor.fetchall()
print(f"Found {len(results)} JCB records:")
for row in results:
    pkg_items = row[4]
    print(f"\n  ID: {row[0]}")
    print(f"  part_code: {row[1]}")
    print(f"  part_name: {row[2]}")
    print(f"  is_package: {row[3]}")
    print(f"  package_items: {pkg_items if pkg_items else 'NULL/EMPTY'}")
    print(f"  items_length: {row[5]}")

# Check if there are any JCB-related QR codes
print("\n\n[CHECK] Looking for JCB-related QR codes...")
cursor.execute("""
    SELECT id, qr_code, part_code 
    FROM qr_codes 
    WHERE part_code LIKE '%JCB%'
    LIMIT 10
""")

qr_results = cursor.fetchall()
print(f"Found {cursor.rowcount} JCB QR codes:")
for row in qr_results:
    print(f"  QR: {row[1]} → {row[2]}")

# Check other working packages for comparison
print("\n\n[COMPARE] Checking a working package (SCHAFFER)...")
cursor.execute("""
    SELECT id, part_code, part_name, is_package, 
           CHAR_LENGTH(package_items) as items_len
    FROM part_codes 
    WHERE part_code = 'SCHAFFER'
""")

result = cursor.fetchone()
if result:
    print(f"  part_code: {result[1]}")
    print(f"  part_name: {result[2]}")
    print(f"  is_package: {result[3]}")
    print(f"  items_length: {result[4]} bytes")

conn.close()
