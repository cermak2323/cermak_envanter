#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final orphan QR cleanup - remove all NULL and invalid part_code_id entries
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
    
    # Step 1: Check what we have
    print("[CHECK] Current state of qr_codes table:")
    cursor.execute("SELECT COUNT(*) as cnt FROM qr_codes")
    print(f"  Total: {cursor.fetchone()['cnt']}")
    
    cursor.execute("SELECT COUNT(*) as cnt FROM qr_codes WHERE part_code_id IS NULL")
    null_count = cursor.fetchone()['cnt']
    print(f"  With NULL part_code_id: {null_count}")
    
    cursor.execute("""
        SELECT COUNT(*) as cnt 
        FROM qr_codes q 
        WHERE part_code_id NOT IN (SELECT id FROM part_codes)
        AND part_code_id IS NOT NULL
    """)
    invalid_count = cursor.fetchone()['cnt']
    print(f"  With invalid part_code_id: {invalid_count}")
    
    # Step 2: Delete ALL orphans (NULL and invalid)
    print("\n[DELETE] Removing all orphan QR codes...")
    
    # First: Set foreign_key_checks OFF temporarily
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    
    cursor.execute("""
        DELETE FROM qr_codes
        WHERE part_code_id IS NULL OR part_code_id NOT IN (SELECT id FROM part_codes)
    """)
    deleted = cursor.rowcount
    conn.commit()
    print(f"  Deleted: {deleted} rows")
    
    # Re-enable checks
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
    
    # Step 3: Now add foreign key back
    print("\n[FK] Adding foreign key constraint...")
    cursor.execute("""
        ALTER TABLE qr_codes 
        ADD CONSTRAINT fk_qr_part 
        FOREIGN KEY (part_code_id) 
        REFERENCES part_codes(id) 
        ON DELETE RESTRICT 
        ON UPDATE RESTRICT
    """)
    conn.commit()
    print("  Foreign key added successfully")
    
    # Step 4: Final verification
    print("\n[VERIFY] Final state:")
    cursor.execute("SELECT COUNT(*) as cnt FROM qr_codes")
    total = cursor.fetchone()['cnt']
    print(f"  Total QR codes: {total}")
    
    cursor.execute("""
        SELECT COUNT(*) as orphan_count
        FROM qr_codes q
        LEFT JOIN part_codes p ON q.part_code_id = p.id
        WHERE p.id IS NULL
    """)
    orphan_count = cursor.fetchone()['orphan_count']
    print(f"  Orphan QR codes: {orphan_count}")
    
    if orphan_count == 0:
        print("\n[SUCCESS] All orphan QR codes removed and foreign key protected!")
    else:
        print(f"\n[WARNING] Still {orphan_count} orphans remain")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
