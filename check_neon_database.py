#!/usr/bin/env python3
"""Check Neon PostgreSQL database integrity and stats"""

import os
os.environ['FLASK_ENV'] = 'production'

from app import app, db

with app.app_context():
    print('=== NEON DATABASE VERIFICATION ===\n')
    
    # 1. Table row counts
    print('📊 TABLE SIZES:')
    tables = {
        'qr_codes': 'SELECT COUNT(*) FROM qr_codes',
        'part_codes': 'SELECT COUNT(*) FROM part_codes',
        'envanter_users': 'SELECT COUNT(*) FROM envanter_users',
        'scanned_qr': 'SELECT COUNT(*) FROM scanned_qr',
        'count_sessions': 'SELECT COUNT(*) FROM count_sessions',
        'count_passwords': 'SELECT COUNT(*) FROM count_passwords',
    }
    
    total_rows = 0
    for table, query in tables.items():
        try:
            result = db.session.execute(db.text(query)).scalar()
            print(f'   {table}: {result} rows')
            total_rows += result
        except Exception as e:
            print(f'   {table}: ERROR - {str(e)[:50]}')
    
    print(f'\n   TOTAL ROWS: {total_rows}')
    
    # 2. Check schema integrity
    print('\n🔍 SCHEMA CHECK:')
    try:
        query = """
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """
        result = db.session.execute(db.text(query)).fetchall()
        print(f'   Tables found: {len(result)}')
        for row in result:
            print(f'   - {row[0]}')
    except Exception as e:
        print(f'   Schema check failed: {e}')
    
    # 3. Connection pool status
    print('\n⚙️  CONNECTION POOL:')
    try:
        pool = db.engine.pool
        print(f'   Pool size: {pool.size()}')
        print(f'   Checked out: {pool.checkedout()}')
    except Exception as e:
        print(f'   Pool info unavailable: {e}')
    
    # 4. Recent data samples
    print('\n📋 DATA SAMPLES:')
    
    try:
        users = db.session.execute(db.text('SELECT COUNT(*), role FROM envanter_users GROUP BY role')).fetchall()
        if users:
            print('   Users by role:')
            for count, role in users:
                print(f'   - {role}: {count}')
        else:
            print('   No users found')
    except Exception as e:
        print(f'   Error fetching users: {e}')
    
    try:
        qr_used = db.session.execute(db.text('SELECT COUNT(*) as used FROM qr_codes WHERE is_used = true')).scalar()
        qr_total = db.session.execute(db.text('SELECT COUNT(*) as total FROM qr_codes')).scalar()
        if qr_total:
            print(f'   QR Codes: {qr_used}/{qr_total} used ({int(100*qr_used/qr_total)}%)')
        else:
            print('   No QR codes found')
    except Exception as e:
        print(f'   Error fetching QR stats: {e}')
    
    print('\n✅ DATABASE VERIFICATION COMPLETE')
