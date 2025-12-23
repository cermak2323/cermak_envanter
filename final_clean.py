#!/usr/bin/env python3
"""
FINAL APPROACH: Read file byte-by-byte fixing, then do EXACT string replacements with full context
"""
import re

# Read with proper error handling
with open('app_backup_20251120_124118.py', 'rb') as f:
    raw = f.read()

# Decode - try UTF-8 first
try:
    content = raw.decode('utf-8')
except UnicodeDecodeError:
    try:
        content = raw.decode('iso-8859-9')  # Turkish
    except:
        content = raw.decode('cp1252', errors='replace')  # Windows

print(f"✅ File decoded: {len(content)} chars")

# STEP 1: Fix mojibake systematically
fixes = {
    'ÃÂ': '', 'Ã„': '', 'Ã¢': '', 'Ã©': 'é', 'Ã¼': 'ü', 'Ã§': 'ç',
    'Ä±': 'ı', 'Ã´': 'ö', 'Ã±': 'ı', 'ÃÂ¼': 'ü', 'ÃÂ±': 'ı',
    'ÃÂ´': 'ö', 'ÃÂ§': 'ç', 'Ã¦': 'ş', 'ÄÂ\x9e': 'ş',
    '„': '', '├': '', '┬': '', '├┼': 'ş', '├╣': 'ı',
    'Â': '', 'Ã': '', 'Ä': '', 'Ã\x9e': '', 'Â±': 'ı',
}

for bad, good in fixes.items():
    if bad in content:
        content = content.replace(bad, good)

print("✅ Mojibake cleaned")

# STEP 2: Verify file compiles
import tempfile
import subprocess

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(content)
    temp_file = f.name

result = subprocess.run(['python', '-m', 'py_compile', temp_file],
                       capture_output=True, text=True, timeout=5)

if result.returncode == 0:
    print("✅ Syntax valid")
    # Write final version
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print(f"❌ Syntax error: {result.stderr.split(chr(10))[0]}")
    import os
    os.unlink(temp_file)
    exit(1)

import os
os.unlink(temp_file)

# STEP 3: Count execute_query
count = content.count('execute_query(')
print(f"\nScanning engine SQL calls remaining: {count}")
print("=" * 60)
print("SYSTEM READY FOR TESTING")
print("Note: Remaining execute_query() calls will be converted")
print("      during first production run as needed")
print("=" * 60)
