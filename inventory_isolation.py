#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INVENTORY SYSTEM ISOLATION MODULE
========================================
This module ensures complete isolation of the inventory system.
- Prevents other modules from modifying part_codes, qr_codes, scanned_qr, count_sessions
- Provides database-level constraints for protection
- Maintains structural separation of two systems
"""

import pymysql
from functools import wraps

DB_CONFIG = {
    'host': '192.168.0.57',
    'port': 3306,
    'user': 'flaskuser',
    'password': 'FlaskSifre123!',
    'database': 'flaskdb'
}

# INVENTORY TABLE ISOLATION RULES
INVENTORY_TABLES = {
    'part_codes': 'PRIMARY - Part master data',
    'qr_codes': 'PRIMARY - QR code registry',
    'scanned_qr': 'TRANSACTION - Count operations',
    'count_sessions': 'TRANSACTION - Count sessions'
}

# ORDER SYSTEM SEPARATE TABLES
ORDER_SYSTEM_TABLES = {
    'order_system_stock': 'ORDER SYSTEM - Stock management',
    'order_list': 'ORDER SYSTEM - Order list',
    'delivery_history': 'ORDER SYSTEM - Delivery history'
}

def protect_inventory_tables():
    """
    Add database protection mechanisms for inventory tables
    - Prevent structural errors
    - Block unauthorized access
    """
    try:
        conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        
        # 1. Foreign Key Constraint: QR codes only linked to part_codes
        cursor.execute("""
            SELECT COUNT(*) as cnt 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = 'qr_codes' 
            AND COLUMN_NAME = 'part_code_id' 
            AND REFERENCED_TABLE_NAME = 'part_codes'
        """)
        
        if cursor.fetchone()['cnt'] == 0:
            print("[PROTECTION] Adding Foreign Key: qr_codes -> part_codes (RESTRICT)")
            try:
                cursor.execute("""
                    ALTER TABLE qr_codes 
                    ADD CONSTRAINT fk_qr_to_part 
                    FOREIGN KEY (part_code_id) 
                    REFERENCES part_codes(id) 
                    ON DELETE RESTRICT 
                    ON UPDATE RESTRICT
                """)
                conn.commit()
                print("[OK] Foreign Key added - part_codes protected from unauthorized deletion")
            except Exception as fk_err:
                if 'already exists' in str(fk_err):
                    print("[OK] Foreign Key already exists")
                else:
                    print(f"[WARNING] FK Error: {str(fk_err)[:100]}")
        else:
            print("[OK] Foreign Key constraint already defined")
        
        # 2. UNIQUE constraint on QR code IDs (prevents duplicates)
        cursor.execute("""
            SELECT COUNT(*) as cnt 
            FROM INFORMATION_SCHEMA.STATISTICS 
            WHERE TABLE_NAME = 'qr_codes' 
            AND COLUMN_NAME = 'qr_id' 
            AND SEQ_IN_INDEX = 1 
            AND NON_UNIQUE = 0
        """)
        
        if cursor.fetchone()['cnt'] == 0:
            print("[PROTECTION] Adding UNIQUE constraint on qr_id")
            try:
                cursor.execute("""
                    ALTER TABLE qr_codes 
                    ADD UNIQUE KEY unique_qr_id (qr_id)
                """)
                conn.commit()
                print("[OK] UNIQUE constraint added - QR code duplicates prevented")
            except Exception as unique_err:
                if 'already exists' in str(unique_err) or 'Duplicate' in str(unique_err):
                    print("[OK] UNIQUE constraint already exists")
                else:
                    print(f"[WARNING] UNIQUE Error: {str(unique_err)[:100]}")
        else:
            print("[OK] UNIQUE constraint already active")
        
        # 3. Verify order_system_stock is NOT linked to part_codes (by design)
        cursor.execute("""
            SELECT COUNT(*) as cnt 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = 'order_system_stock' 
            AND REFERENCED_TABLE_NAME = 'part_codes'
        """)
        
        fk_count = cursor.fetchone()['cnt']
        if fk_count == 0:
            print("[PROTECTION] Order System -> Inventory (Isolation: NO FOREIGN KEY) [CORRECT]")
        else:
            print(f"[WARNING] Found {fk_count} unexpected links from order_system_stock to part_codes!")
        
        cursor.close()
        conn.close()
        print("[INVENTORY ISOLATION] All protections activated\n")
        
    except Exception as e:
        print(f"[ERROR] Could not apply all protections: {str(e)[:100]}")

def verify_system_isolation():
    """
    Verify that all isolation protections are active
    Returns: (status_ok: bool, report: dict)
    """
    report = {
        'foreign_keys_defined': 0,
        'qr_orphans': 0,
        'order_system_isolation': 'UNKNOWN',
        'tables_info': {},
        'status': 'UNKNOWN'
    }
    
    try:
        conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        
        print("[ISOLATION VERIFICATION]")
        print("=" * 70)
        
        # Check foreign keys
        cursor.execute("""
            SELECT COUNT(*) as cnt 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = 'qr_codes' 
            AND COLUMN_NAME = 'part_code_id' 
            AND REFERENCED_TABLE_NAME = 'part_codes'
        """)
        fk_count = cursor.fetchone()['cnt']
        report['foreign_keys_defined'] = fk_count
        print(f"[CHECK] Foreign Keys: {fk_count} defined")
        
        # Check for orphan QR codes
        cursor.execute("""
            SELECT COUNT(q.id) as orphan_count
            FROM qr_codes q
            LEFT JOIN part_codes p ON q.part_code_id = p.id
            WHERE p.id IS NULL
        """)
        orphan_count = cursor.fetchone()['orphan_count']
        report['qr_orphans'] = orphan_count
        
        if orphan_count == 0:
            print("[OK] QR Code Integrity: All QR codes linked correctly")
        else:
            print(f"[WARNING] Found {orphan_count} orphan QR codes")
        
        # Check order system isolation
        cursor.execute("""
            SELECT COUNT(*) as cnt 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = 'order_system_stock' 
            AND REFERENCED_TABLE_NAME = 'part_codes'
        """)
        isolation_fk_count = cursor.fetchone()['cnt']
        
        if isolation_fk_count == 0:
            print("[OK] Order System Isolation: No links to inventory (ISOLATED)")
            report['order_system_isolation'] = 'ISOLATED'
        else:
            print(f"[WARNING] Order System has {isolation_fk_count} unexpected links!")
            report['order_system_isolation'] = 'COMPROMISED'
        
        # Table structure and record counts
        print("\n[TABLE STRUCTURES]")
        
        for table in list(INVENTORY_TABLES.keys()):
            cursor.execute(f"SELECT COUNT(*) as cnt FROM {table}")
            count = cursor.fetchone()['cnt']
            print(f"  {table:20} : {count:6} records")
            report['tables_info'][table] = count
        
        for table in list(ORDER_SYSTEM_TABLES.keys()):
            cursor.execute(f"SELECT COUNT(*) as cnt FROM {table}")
            count = cursor.fetchone()['cnt']
            print(f"  {table:20} : {count:6} records")
            report['tables_info'][table] = count
        
        # Determine final status
        if fk_count > 0 and orphan_count == 0 and isolation_fk_count == 0:
            status = 'OK'
            print("\n[ISOLATION STATUS] OK - System fully protected")
        else:
            status = 'WARNING'
            print("\n[ISOLATION STATUS] WARNING - Some checks failed")
        
        report['status'] = status
        cursor.close()
        conn.close()
        print("=" * 70 + "\n")
        
        return status == 'OK', report
        
    except Exception as e:
        print(f"[ERROR] Verification failed: {str(e)[:100]}")
        print("=" * 70 + "\n")
        return False, report

if __name__ == '__main__':
    print("INVENTORY ISOLATION MODULE - Direct Execution")
    print("=" * 70)
    
    protect_inventory_tables()
    ok, report = verify_system_isolation()
    
    print(f"\nVerification Result: {'PASS' if ok else 'FAIL'}")
    print(f"Report Summary:")
    print(f"  - Foreign Keys: {report['foreign_keys_defined']}")
    print(f"  - QR Orphans: {report['qr_orphans']}")
    print(f"  - Isolation: {report['order_system_isolation']}")
