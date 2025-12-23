#!/usr/bin/env python3
"""
Restore missing ? and key Turkish characters where they break code
"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix critical SQL placeholders that are missing ?
fixes = [
    ("WHERE qc.qr_id = \n", "WHERE qc.qr_id = ?\n"),
    ("WHERE id = \n", "WHERE id = ?\n"),
    ("WHERE id = , (session_id,", "WHERE id = ?, (session_id,"),
    ("VALUES (, , , )", "VALUES (?, ?, ?, ?)"),
    ("WHERE session_id =  AND qr_id = ", "WHERE session_id = ? AND qr_id = ?"),
    ("WHERE id = , (prev_user_id,", "WHERE id = ?, (prev_user_id,"),
    ("qc.qr_id = ", "qc.qr_id = ?"),
    ("FROM count_sessions WHERE id = ,", "FROM count_sessions WHERE id = ?,"),
    # Fix broken SQL keywords
    ("SELECT COUNT(*) FROM count_sessions WHERE id = ,", "SELECT COUNT(*) FROM count_sessions WHERE id = ?,"),
]

for bad, good in fixes:
    if bad in content:
        content = content.replace(bad, good)
        print(f"✅ Fixed: {bad[:40]}")

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ SQL placeholders restored")

# Verify syntax
import subprocess
result = subprocess.run(['python', '-c', 'import ast; ast.parse(open("app.py").read())'],
                       capture_output=True, text=True, timeout=5)

if result.returncode == 0:
    print("✅ SYNTAX STILL VALID")
else:
    print(f"⚠️  Check syntax after fixes")
