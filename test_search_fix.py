#!/usr/bin/env python3
"""
Test script to verify the SQL fix for search queries.
Tests that the execute_query function works correctly with %s placeholders.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, PartCode
from sqlalchemy import text

def test_search_placeholders():
    """Test that SQL queries with placeholders work correctly"""
    print("Testing SQL placeholder fixes...")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Test 1: Direct text query with %s placeholder
            print("\n[TEST 1] Testing execute_query with %s placeholders")
            from app import execute_query, get_db
            
            conn = get_db()
            cursor = conn.cursor()
            
            # Test a simple query with placeholder
            test_query = '''
                SELECT COUNT(*) FROM part_codes
                WHERE part_code = %s
                LIMIT 1
            '''
            
            execute_query(cursor, test_query, ('TEST_CODE',))
            result = cursor.fetchone()
            
            if result is not None:
                print(f"  -> Query executed successfully")
                print(f"  -> Result: {result}")
            else:
                print(f"  -> Query executed but returned None (expected for non-existent code)")
            
            # Test 2: LIKE query with multiple placeholders
            print("\n[TEST 2] Testing LIKE query with multiple %s placeholders")
            
            like_query = '''
                SELECT COUNT(*) FROM part_codes
                WHERE part_code LIKE %s 
                   OR part_name LIKE %s
                LIMIT 20
            '''
            
            search_pattern = '%Y%'
            execute_query(cursor, like_query, (search_pattern, search_pattern))
            result = cursor.fetchone()
            
            if result is not None:
                print(f"  -> LIKE query executed successfully")
                print(f"  -> Result count: {result[0]}")
            else:
                print(f"  -> Query executed but returned None")
            
            # Test 3: Multiple parameter query
            print("\n[TEST 3] Testing multiple parameter query")
            
            multi_query = '''
                SELECT COUNT(*) FROM scanned_qr 
                WHERE qr_id = %s AND session_id = %s
                LIMIT 1
            '''
            
            execute_query(cursor, multi_query, ('TEST_QR', 'TEST_SESSION'))
            result = cursor.fetchone()
            
            if result is not None:
                print(f"  -> Multi-parameter query executed successfully")
                print(f"  -> Result: {result}")
            else:
                print(f"  -> Query executed but returned None (expected)")
            
            print("\n" + "=" * 60)
            print("[SUCCESS] All SQL placeholder tests PASSED!")
            print("\nThe following errors should NO LONGER appear:")
            print("  - syntax error at or near \"LIMIT\"")
            print("  - syntax error at or near \"OR\"")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"\n[FAILED] Test FAILED with error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = test_search_placeholders()
    sys.exit(0 if success else 1)
