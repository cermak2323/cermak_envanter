#!/usr/bin/env python3
"""
Test PostgreSQL ORM connection
"""
import sys
sys.path.insert(0, '/root')

from app import app, db
from models import User

with app.app_context():
    print("\n" + "="*70)
    print(" TESTING POSTGRESQL SQLALCHEMY ORM CONNECTION")
    print("="*70 + "\n")
    
    try:
        # Test basic query
        user_count = User.query.count()
        print(f"✅ Connected to PostgreSQL!")
        print(f"✅ Total users in database: {user_count}")
        
        # Test admin user
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print(f"✅ Admin user exists: {admin.username}")
        else:
            print("❌ Admin user not found")
        
        # Test count sessions
        from models import CountSession
        session_count = CountSession.query.count()
        print(f"✅ Count sessions: {session_count}")
        
        # Test part codes
        from models import PartCode
        part_count = PartCode.query.count()
        print(f"✅ Part codes: {part_count}")
        
        # Test QR codes
        from models import QRCode
        qr_count = QRCode.query.count()
        print(f"✅ QR codes: {qr_count}")
        
        # Test scanned QR
        from models import ScannedQR
        scanned_count = ScannedQR.query.count()
        print(f"✅ Scanned QRs: {scanned_count}")
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED - POSTGRESQL ORM WORKING")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
