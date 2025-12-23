#!/usr/bin/env python3
"""
SQLite to PostgreSQL Migration Script
Migrates QR codes and scanned QR data from local SQLite to production PostgreSQL
"""

import sqlite3
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment
load_dotenv()

def migrate_qr_data():
    """Migrate QR codes and scanned QR data from SQLite to PostgreSQL"""
    
    # Get databases
    sqlite_path = os.path.join('instance', 'envanter_local.db')
    postgres_url = os.environ.get("DATABASE_URL")
    
    if not postgres_url:
        print("ERROR: DATABASE_URL not set in .env file")
        return False
    
    print("="*70)
    print("SQLite to PostgreSQL QR Data Migration")
    print("="*70)
    
    # Connect to SQLite
    print("\n1. Connecting to SQLite...")
    try:
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_cursor = sqlite_conn.cursor()
        print("   OK - SQLite connected")
    except Exception as e:
        print(f"   ERROR - SQLite connection failed: {e}")
        return False
    
    # Connect to PostgreSQL
    print("\n2. Connecting to PostgreSQL...")
    try:
        pg_engine = create_engine(postgres_url, echo=False)
        pg_conn = pg_engine.connect()
        print("   OK - PostgreSQL connected")
    except Exception as e:
        print(f"   ERROR - PostgreSQL connection failed: {e}")
        return False
    
    # Migrate QR Codes
    print("\n3. Migrating QR codes...")
    try:
        # Read from SQLite
        sqlite_cursor.execute("SELECT id, qr_id, part_code_id, is_used, used_count, first_used_at, last_used_at, is_active, created_at FROM qr_codes")
        qr_rows = sqlite_cursor.fetchall()
        print(f"   Found {len(qr_rows)} QR codes in SQLite")
        
        # Clear PostgreSQL table first (to avoid duplicates)
        print("   Clearing PostgreSQL qr_codes table...")
        pg_conn.execute(text("DELETE FROM qr_codes"))
        pg_conn.commit()
        
        # Insert into PostgreSQL
        inserted = 0
        for row in qr_rows:
            try:
                pg_conn.execute(text("""
                    INSERT INTO qr_codes (id, qr_id, part_code_id, is_used, used_count, first_used_at, last_used_at, is_active, created_at)
                    VALUES (:id, :qr_id, :part_code_id, :is_used, :used_count, :first_used_at, :last_used_at, :is_active, :created_at)
                """), {
                    'id': row[0],
                    'qr_id': row[1],
                    'part_code_id': row[2],
                    'is_used': bool(row[3]),
                    'used_count': row[4],
                    'first_used_at': row[5],
                    'last_used_at': row[6],
                    'is_active': bool(row[7]),
                    'created_at': row[8]
                })
                inserted += 1
            except Exception as e:
                print(f"   WARNING: Failed to insert QR code {row[1]}: {e}")
        
        pg_conn.commit()
        print(f"   OK - Inserted {inserted} QR codes into PostgreSQL")
        
    except Exception as e:
        print(f"   ERROR - QR codes migration failed: {e}")
        return False
    
    # Migrate Scanned QR data
    print("\n4. Migrating scanned QR records...")
    try:
        # Read from SQLite
        sqlite_cursor.execute("SELECT id, session_id, qr_id, part_code, scanned_by, scanned_at FROM scanned_qr")
        scanned_rows = sqlite_cursor.fetchall()
        print(f"   Found {len(scanned_rows)} scanned QR records in SQLite")
        
        # Clear PostgreSQL table first (to avoid duplicates)
        print("   Clearing PostgreSQL scanned_qr table...")
        pg_conn.execute(text("DELETE FROM scanned_qr"))
        pg_conn.commit()
        
        # Insert into PostgreSQL
        inserted = 0
        for row in scanned_rows:
            try:
                pg_conn.execute(text("""
                    INSERT INTO scanned_qr (id, session_id, qr_id, part_code, scanned_by, scanned_at)
                    VALUES (:id, :session_id, :qr_id, :part_code, :scanned_by, :scanned_at)
                """), {
                    'id': row[0],
                    'session_id': row[1],
                    'qr_id': row[2],
                    'part_code': row[3],
                    'scanned_by': row[4],
                    'scanned_at': row[5]
                })
                inserted += 1
            except Exception as e:
                print(f"   WARNING: Failed to insert scanned QR {row[0]}: {e}")
        
        pg_conn.commit()
        print(f"   OK - Inserted {inserted} scanned QR records into PostgreSQL")
        
    except Exception as e:
        print(f"   ERROR - Scanned QR migration failed: {e}")
        return False
    
    # Verify
    print("\n5. Verifying migration...")
    try:
        result = pg_conn.execute(text("SELECT COUNT(*) as cnt FROM qr_codes"))
        qr_count = result.fetchone()[0]
        
        result = pg_conn.execute(text("SELECT COUNT(*) as cnt FROM scanned_qr"))
        scanned_count = result.fetchone()[0]
        
        print(f"   PostgreSQL qr_codes: {qr_count} records")
        print(f"   PostgreSQL scanned_qr: {scanned_count} records")
        
        if qr_count == len(qr_rows) and scanned_count == len(scanned_rows):
            print("   OK - Migration successful!")
        else:
            print("   WARNING - Record count mismatch!")
            return False
        
    except Exception as e:
        print(f"   ERROR - Verification failed: {e}")
        return False
    
    # Cleanup
    print("\n6. Cleaning up...")
    try:
        sqlite_conn.close()
        pg_conn.close()
        pg_engine.dispose()
        print("   OK - Connections closed")
    except Exception as e:
        print(f"   WARNING - Cleanup error: {e}")
    
    print("\n" + "="*70)
    print("MIGRATION COMPLETE")
    print("="*70)
    print("\nYour dashboard should now display:")
    print(f"  - Toplam QR Kod: {qr_count}")
    print(f"  - Toplam Rapor: 7")
    print("  - Aktif Sayım: [calculated from is_active flag]")
    print("  - Tamamlanan Sayım: [calculated from is_active flag]")
    
    return True

if __name__ == "__main__":
    success = migrate_qr_data()
    exit(0 if success else 1)
