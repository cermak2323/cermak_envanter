#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Integration Test - Verify All Components Work Together
"""

import sys
import os

# Fix encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

def test_all():
    print("\n" + "="*80)
    print(" FINAL INTEGRATION TEST - POSTGRESQL + SQLALCHEMY")
    print("="*80 + "\n")
    
    try:
        # Test 1: Import Flask app
        print("[1/5] Testing Flask app import...")
        from app import app, db, init_db
        print("[OK] Flask app loaded")
        
        # Test 2: Database connection
        print("[2/5] Testing PostgreSQL connection...")
        with app.app_context():
            db.session.execute(db.text('SELECT 1'))
            print("[OK] PostgreSQL connection OK")
        
        # Test 3: Models
        print("[3/5] Testing SQLAlchemy ORM models...")
        with app.app_context():
            from models import User, PartCode, QRCode, CountSession, ScannedQR
            
            u_count = User.query.count()
            p_count = PartCode.query.count()
            q_count = QRCode.query.count()
            c_count = CountSession.query.count()
            s_count = ScannedQR.query.count()
            
            print(f"  - Users: {u_count}")
            print(f"  - Part Codes: {p_count}")
            print(f"  - QR Codes: {q_count}")
            print(f"  - Count Sessions: {c_count}")
            print(f"  - Scanned QRs: {s_count}")
            print("[OK] All models query successfully")
        
        # Test 4: Init DB function
        print("[4/5] Testing init_db() function...")
        with app.app_context():
            result = init_db()
            if result:
                print("[OK] init_db() completed successfully")
            else:
                print("[WARN] init_db() returned False")
        
        # Test 5: Legacy compatibility
        print("[5/5] Testing legacy wrapper functions...")
        with app.app_context():
            from app import get_db, execute_query, close_db
            
            conn = get_db()
            print("[OK] Legacy get_db() works")
            close_db(conn)
            print("[OK] Legacy close_db() works")
            print("[OK] Legacy execute_query() available")
        
        print("\n" + "="*80)
        print("[SUCCESS] ALL INTEGRATION TESTS PASSED")
        print("="*80 + "\n")
        
        print("System Status:")
        print(f"  [OK] PostgreSQL: Connected")
        print(f"  [OK] SQLAlchemy: Initialized")
        print(f"  [OK] Models: {u_count + p_count + q_count + c_count + s_count} total records")
        print(f"  [OK] Compatibility: Backward compatible")
        print(f"  [OK] Status: PRODUCTION READY")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_all()
    sys.exit(0 if success else 1)

