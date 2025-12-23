#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check the exact orphan QR structure
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
    
    # Find the exact orphan QR
    cursor.execute("""
        SELECT *
        FROM qr_codes
        WHERE qr_id = 'TEST_PAKET_131328'
    """)
    
    qr = cursor.fetchone()
    if qr:
        print("Found orphan QR:")
        for key, value in qr.items():
            print(f"  {key}: {value} (type: {type(value).__name__})")
        
        # Try to delete it directly
        print("\nDeleting it directly...")
        cursor.execute("""
            DELETE FROM qr_codes WHERE id = %s
        """, (qr['id'],))
        conn.commit()
        print(f"Deleted {cursor.rowcount} row(s)")
        
        # Verify
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM qr_codes WHERE qr_id = 'TEST_PAKET_131328'
        """)
        remaining = cursor.fetchone()['cnt']
        print(f"Remaining: {remaining}")
    else:
        print("Orphan QR not found")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
