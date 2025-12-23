#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find and fix orphan QR codes
"""

import pymysql

DB_CONFIG = {
    'host': '192.168.0.57',
    'port': 3306,
    'user': 'flaskuser',
    'password': 'FlaskSifre123!',
    'database': 'flaskdb'
}

conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

# Find orphan QR codes
print("Finding orphan QR codes...")
cursor.execute("""
    SELECT q.id, q.qr_id, q.part_code_id, q.created_at, q.used_count
    FROM qr_codes q
    LEFT JOIN part_codes p ON q.part_code_id = p.id
    WHERE p.id IS NULL
    ORDER BY q.id
""")

orphans = cursor.fetchall()
print(f"\nFound {len(orphans)} orphan QR code(s):\n")

for qr in orphans:
    print(f"ID: {qr['id']}, QR_ID: {qr['qr_id']}, part_code_id: {qr['part_code_id']}")
    print(f"  Created: {qr['created_at']}, Used: {qr['used_count']} times")
    
    # Check if we can find the part_code in the filesystem or by similar name
    print(f"  Status: ORPHAN - part_code_id {qr['part_code_id']} doesn't exist")
    
    # Option: Delete or mark for review
    delete_choice = input(f"  Delete this orphan QR? (y/n): ").strip().lower()
    if delete_choice == 'y':
        cursor.execute("DELETE FROM qr_codes WHERE id = %s", (qr['id'],))
        conn.commit()
        print(f"  --> DELETED")
    else:
        print(f"  --> KEPT")

cursor.close()
conn.close()

print("\nDone!")
