#!/usr/bin/env python3
"""Sync SQLite part_codes to PostgreSQL"""

import sys
import os
import sqlite3
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from models import PartCode
from datetime import datetime

print("\n" + "="*70)
print("SYNCING SQLite Data to PostgreSQL (Neon)")
print("="*70 + "\n")

# Connect to SQLite
db_path = os.path.join('instance', 'envanter_local.db')
sqlite_conn = sqlite3.connect(db_path)
sqlite_conn.row_factory = sqlite3.Row
sqlite_cursor = sqlite_conn.cursor()

# Get all parts from SQLite
sqlite_cursor.execute("""
    SELECT part_code, part_name, description, photo_path, catalog_image,
           used_in_machines, specifications, stock_location, supplier,
           unit_price, critical_stock_level, notes, last_updated, updated_by
    FROM part_codes
""")

all_parts = sqlite_cursor.fetchall()
print(f"Found {len(all_parts)} parts in SQLite\n")

# Start sync
with app.app_context():
    try:
        # Clear PostgreSQL - cascade delete
        print("[1] Clearing PostgreSQL part_codes (cascade)...")
        
        # Delete QR codes first to avoid foreign key constraint
        print("    - Deleting QR codes...")
        db.session.execute(db.text("DELETE FROM scanned_qr"))
        db.session.execute(db.text("DELETE FROM qr_codes"))
        db.session.commit()
        
        # Now delete part codes
        print("    - Deleting part codes...")
        db.session.query(PartCode).delete()
        db.session.commit()
        print("    ✓ Cleared\n")
        
        # Insert all parts
        print("[2] Inserting parts into PostgreSQL...")
        inserted = 0
        for i, row in enumerate(all_parts, 1):
            try:
                part = PartCode(
                    part_code=row['part_code'],
                    part_name=row['part_name'],
                    description=row['description'],
                    # Note: photo_path and catalog_image not in PartCode model
                    # is_package and package_items can be NULL
                    created_at=row['last_updated'] or datetime.now()
                )
                db.session.add(part)
                inserted += 1
                
                if i % 500 == 0:
                    print(f"    {i}/{len(all_parts)} inserted...")
            except Exception as e:
                print(f"    Error on row {i} ({row['part_code']}): {e}")
                continue
        
        db.session.commit()
        print(f"    ✓ {inserted} parts inserted\n")
        
        # Verify
        print("[3] Verification...")
        count = db.session.query(PartCode).count()
        print(f"    Total parts in PostgreSQL: {count}\n")
        
        if count > 0:
            # Test specific parts
            test_codes = ['11111-11111', 'Y129150-49811', '00010-90002']
            for code in test_codes:
                part = db.session.query(PartCode).filter_by(part_code=code).first()
                if part:
                    print(f"    ✓ {code}: Found")
                else:
                    print(f"    ✗ {code}: NOT FOUND")
        
        print("\n" + "="*70)
        print("SYNC COMPLETE!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        db.session.rollback()
        sys.exit(1)

sqlite_conn.close()
