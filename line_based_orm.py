#!/usr/bin/env python3
"""
LINE-BASED approach: Parse app.py line by line and convert SQL functions
to ORM equivalents while preserving structure
"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Building ORM conversion map...")

# Map of function names and their SQL patterns to ORM versions
conversions_needed = {}

# Read through and find all db_connection blocks
in_db_block = False
block_start = 0

for i, line in enumerate(lines):
    if 'with db_connection() as conn:' in line and 'cursor = conn.cursor()' in lines[i+1]:
        in_db_block = True
        block_start = i
    
    if in_db_block and 'cursor.close()' in line or (in_db_block and i > block_start + 100):
        in_db_block = False

# Count patterns
execute_count = sum(1 for line in lines if 'execute_query(' in line)
print(f"Found {execute_count} execute_query() calls across {len(lines)} lines")

# Simple approach: Replace entire db_connection blocks with ORM equivalents
# Focus on the top 20 most-used patterns

key_replacements = [
    # Session creation check
    ("execute_query(cursor, 'SELECT COUNT(*) FROM count_sessions WHERE id = ?', (session_id,))\n            if cursor.fetchone()[0] == 0:",
     "count_session = CountSession.query.filter_by(id=session_id).first()\n            if not count_session:"),
    
    # User lookups
    ("execute_query(cursor, 'SELECT * FROM envanter_users WHERE",
     "user = User.query.filter(User."),
    
    # QR code checks
    ("execute_query(cursor, 'SELECT COUNT(*) FROM qr_codes",
     "qr_count = db.session.query(QRCode).filter("),
]

# Do simple string replacements
content = ''.join(lines)
replaced = 0

for old, new in key_replacements:
    if old in content:
        content = content.replace(old, new)
        replaced += 1
        print(f"✅ Replaced pattern")

# Quick syntax check
import subprocess
import tempfile

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(content)
    temp_file = f.name

result = subprocess.run(['python', '-c', f'import ast; ast.parse(open("{temp_file}").read())'],
                       capture_output=True, text=True, timeout=5)

import os
os.unlink(temp_file)

if result.returncode == 0:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    final_count = content.count('execute_query(')
    print(f"\n✅ SYNTAX VALID")
    print(f"Converted: {execute_count - final_count} more patterns")
    print(f"Remaining: {final_count} execute_query() calls")
else:
    print(f"⚠️  Skipping due to syntax concerns")
    print(f"Using existing working version")
