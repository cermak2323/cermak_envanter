#!/usr/bin/env python3
"""
SURGICAL approach: Find exact SQL patterns and replace with ORM
One pattern at a time, verify syntax after each batch
"""
import re
import subprocess

def check_syntax():
    result = subprocess.run(['python', '-c', 'import ast; ast.parse(open("app.py").read())'],
                           capture_output=True, text=True, timeout=5)
    return result.returncode == 0

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

initial = content.count('execute_query(')
print(f"Starting: {initial} execute_query() calls")

# STRATEGY: Replace only EXACT patterns with full context to avoid syntax errors

# 1. Handle simple COUNT(*) queries - but be very careful
# Pattern: execute_query(cursor, 'SELECT COUNT(*) FROM table')
# This should match the whole statement AND assignment

simple_counts = [
    (r"execute_query\(cursor, 'SELECT COUNT\(\*\) FROM scanned_qr WHERE session_id = \?', \(session_id,\)\)\s+scanned_count = cursor\.fetchone\(\)\[0\]",
     "scanned_count = db.session.query(ScannedQR).filter_by(session_id=session_id).count()"),
    
    (r"execute_query\(cursor, 'SELECT COUNT\(\*\) FROM qr_codes WHERE is_used = 0'\)\s+available = cursor\.fetchone\(\)\[0\]",
     "available = db.session.query(QRCode).filter_by(is_used=False).count()"),
    
    (r"execute_query\(cursor, 'SELECT COUNT\(\*\) FROM qr_codes WHERE is_used = 1'\)\s+used = cursor\.fetchone\(\)\[0\]",
     "used = db.session.query(QRCode).filter_by(is_used=True).count()"),
]

for pattern, replacement in simple_counts:
    if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
        before = content.count('execute_query(')
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)
        after = content.count('execute_query(')
        if after < before:
            print(f"✅ {before - after} COUNT queries converted")

# 2. User full name lookups
user_patterns = [
    (r"execute_query\(cursor, 'SELECT full_name FROM envanter_users WHERE id = \?', \(.*?\)\)\s+user_result = cursor\.fetchone\(\)\s+user_name = user_result\[0\] if user_result else '.*?'",
     "user = User.query.filter_by(id=user_id).first()\n            user_name = user.full_name if user else 'Kullanici'"),
]

for pattern, replacement in user_patterns:
    if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
        before = content.count('execute_query(')
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)
        after = content.count('execute_query(')
        if after < before:
            print(f"✅ {before - after} user lookups converted")

# 3. Check syntax after these conversions
if check_syntax():
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    final = content.count('execute_query(')
    print(f"\n✅ Syntax valid. Converted: {initial - final} more calls")
    print(f"Remaining: {final}")
else:
    print("\n❌ Syntax error - reverting")
    exit(1)
