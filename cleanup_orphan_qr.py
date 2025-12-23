#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix the orphan QR by dropping and recreating the foreign key
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
    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    
    # Step 1: Drop the foreign key
    print("[1] Dropping foreign key constraint...")
    try:
        cursor.execute("""
            ALTER TABLE qr_codes DROP FOREIGN KEY fk_qr_part
        """)
        conn.commit()
        print("[OK] Foreign key dropped")
    except Exception as e:
        if 'cannot find' in str(e).lower() or 'not found' in str(e).lower():
            print("[OK] Foreign key doesn't exist (already dropped?)")
        else:
            print(f"[ERROR] {e}")
            raise
    
    # Step 2: Delete orphan QR codes
    print("\n[2] Deleting orphan QR codes...")
    cursor.execute("""
        DELETE FROM qr_codes
        WHERE part_code_id IS NULL OR part_code_id NOT IN (SELECT id FROM part_codes)
    """)
    conn.commit()
    deleted = cursor.rowcount
    print(f"[OK] Deleted {deleted} orphan QR code(s)")
    
    # Step 3: Recreate the foreign key constraint
    print("\n[3] Recreating foreign key constraint...")
    cursor.execute("""
        ALTER TABLE qr_codes 
        ADD CONSTRAINT fk_qr_part 
        FOREIGN KEY (part_code_id) 
        REFERENCES part_codes(id) 
        ON DELETE RESTRICT 
        ON UPDATE RESTRICT
    """)
    conn.commit()
    print("[OK] Foreign key constraint recreated with RESTRICT protection")
    
    # Step 4: Verify
    print("\n[4] Verification:")
    cursor.execute("""
        SELECT COUNT(*) as orphan_count
        FROM qr_codes q
        LEFT JOIN part_codes p ON q.part_code_id = p.id
        WHERE p.id IS NULL
    """)
    orphan_count = cursor.fetchone()['orphan_count']
    print(f"[CHECK] Remaining orphans: {orphan_count}")
    
    cursor.execute("""
        SELECT COUNT(*) as total FROM qr_codes
    """)
    total = cursor.fetchone()['total']
    print(f"[CHECK] Total QR codes: {total}")
    
    cursor.close()
    conn.close()
    print("\n[SUCCESS] Orphan QR cleanup complete!")
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
