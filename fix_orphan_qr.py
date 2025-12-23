#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find and remove orphan QR codes in MySQL database
"""

import pymysql

DB_CONFIG = {
    'host': '192.168.0.57',
    'port': 3306,
    'user': 'flaskuser',
    'password': 'FlaskSifre123!',
    'database': 'flaskdb'
}

try:
    print("[INFO] Connecting to database...")
    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    
    # Find orphan QR codes
    print("\n[SEARCH] Finding orphan QR codes...\n")
    cursor.execute("""
        SELECT q.id, q.qr_id, q.part_code_id, q.created_at, q.used_count
        FROM qr_codes q
        LEFT JOIN part_codes p ON q.part_code_id = p.id
        WHERE p.id IS NULL
        ORDER BY q.id
    """)
    
    orphans = cursor.fetchall()
    print(f"[FOUND] {len(orphans)} orphan QR code(s):\n")
    
    for idx, qr in enumerate(orphans, 1):
        print(f"{idx}. QR ID: {qr['qr_id']}")
        print(f"   Database ID: {qr['id']}")
        print(f"   Part Code ID: {qr['part_code_id']} (MISSING)")
        print(f"   Created: {qr['created_at']}")
        print(f"   Used: {qr['used_count']} times")
        
        # Check if part_code_id exists in part_codes table
        cursor.execute("""
            SELECT id, part_code FROM part_codes WHERE id = %s
        """, (qr['part_code_id'],))
        
        result = cursor.fetchone()
        if result:
            print(f"   Part Code: {result['part_code']} (EXISTS in other system?)")
        else:
            print(f"   Part Code ID {qr['part_code_id']}: NOT FOUND - ORPHAN")
    
    if len(orphans) > 0:
        print(f"\n[ACTION] Deleting {len(orphans)} orphan QR code(s)...")
        cursor.execute("""
            DELETE FROM qr_codes
            WHERE part_code_id NOT IN (SELECT id FROM part_codes)
        """)
        conn.commit()
        print(f"[SUCCESS] Deleted {cursor.rowcount} orphan QR codes")
        
        # Verify
        cursor.execute("""
            SELECT COUNT(*) as orphan_count
            FROM qr_codes q
            LEFT JOIN part_codes p ON q.part_code_id = p.id
            WHERE p.id IS NULL
        """)
        remaining = cursor.fetchone()['orphan_count']
        print(f"[VERIFY] Remaining orphans: {remaining}")
    
    cursor.close()
    conn.close()
    print("\n[OK] Done!")
    
except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
