#!/usr/bin/env python3
"""
Convert app.py from SQLite raw SQL to SQLAlchemy ORM
This script will:
1. Replace all get_db() + execute_query() with SQLAlchemy ORM calls
2. Replace cursor.fetchone() with ORM query results
3. Standardize database access patterns
"""

import re

def convert_app_py():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Store original
    with open('app_sqlalch_backup.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("=" * 70)
    print(" CONVERTING TO SQLALCHEMY ORM")
    print("=" * 70)
    
    # Fix 1: Remove all get_db() calls and use db.session directly
    print("\n[1/3] Removing get_db() calls...")
    content = re.sub(
        r'conn\s*=\s*get_db\(\)\s*\n\s*cursor\s*=\s*conn\.cursor\(\)',
        '# Using SQLAlchemy ORM - removed get_db()',
        content,
        flags=re.MULTILINE
    )
    
    # Fix 2: Remove close_db() calls
    print("[2/3] Removing close_db() calls...")
    content = re.sub(r'\s*close_db\(conn\)', '', content)
    
    # Fix 3: Replace execute_query with db.session.execute
    print("[3/3] Converting raw SQL to SQLAlchemy...")
    
    # Pattern for simple execute_query calls
    content = re.sub(
        r'execute_query\(cursor,\s*([\'"].*?[\'"])\)',
        r'db.session.execute(text(\1))',
        content,
        flags=re.DOTALL
    )
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ Basic conversion done!")
    print("⚠️  Manual review required for specific query patterns")
    print(f"📋 Backup saved: app_sqlalch_backup.py")

if __name__ == '__main__':
    convert_app_py()
