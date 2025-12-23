#!/usr/bin/env python3
"""Fix JCB and ATAŞMAN packages that have is_package=FALSE"""

import pymysql

# Connect to MySQL
conn = pymysql.connect(
    host='192.168.0.57',
    port=3306,
    user='flaskuser',
    password='FlaskSifre123!',
    database='flaskdb',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

# Check JCB specifically
print("[DEBUG] Checking JCB package...")
cursor.execute("SELECT part_code, part_name, is_package, package_items FROM part_codes WHERE part_code = 'JCB'")
jcb = cursor.fetchone()
if jcb:
    print(f"  JCB found: is_package={jcb['is_package']}, has_items={bool(jcb['package_items'])}")
else:
    print("  JCB not found!")

# Find broken packages
print("\n[FIX] Finding all broken packages...")
cursor.execute("""
    SELECT part_code, part_name, is_package 
    FROM part_codes 
    WHERE is_package = FALSE AND package_items IS NOT NULL AND package_items != ''
""")

broken_packages = cursor.fetchall()
print(f"Found {len(broken_packages)} broken packages:")
for pkg in broken_packages:
    print(f"  - {pkg['part_code']}: {pkg['part_name']} (is_package={pkg['is_package']})")

# Fix them
if broken_packages:
    print(f"\n[ACTION] Fixing {len(broken_packages)} packages...")
    cursor.execute("""
        UPDATE part_codes 
        SET is_package = TRUE 
        WHERE is_package = FALSE AND package_items IS NOT NULL AND package_items != ''
    """)
    conn.commit()
    print(f"✓ Fixed {cursor.rowcount} packages!")
    
    # Verify
    print("\n[VERIFY] Checking fixed packages...")
    for pkg in broken_packages:
        cursor.execute("SELECT is_package FROM part_codes WHERE part_code = %s", (pkg['part_code'],))
        result = cursor.fetchone()
        status = "✓" if result and result['is_package'] else "✗"
        print(f"  {status} {pkg['part_code']}: is_package={result['is_package']}")
else:
    print("✓ No broken packages found - all OK!")

conn.close()
print("\nDone!")
