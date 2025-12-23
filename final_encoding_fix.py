#!/usr/bin/env python3
"""
Last resort: Detect actual encoding and convert properly
"""
import chardet

# Detect encoding
with open('app_backup_20251120_124118.py', 'rb') as f:
    raw = f.read()

detection = chardet.detect(raw)
print(f"Detected encoding: {detection}")

# Try to decode with detected encoding
try:
    if detection['encoding']:
        content = raw.decode(detection['encoding'], errors='replace')
    else:
        # Fallback to latin-1 which never fails
        content = raw.decode('latin-1', errors='replace')
except:
    content = raw.decode('utf-8', errors='replace')

# Fix Turkish mojibake patterns more aggressively
fixes = [
    ('yuzdÄ\x9eÂ\xb5', 'yüzde'),
    ('yuzdÄ', 'yüz'),
    ('DÃ³Ã¼', 'Dö'),
]

for bad, good in fixes:
    content = content.replace(bad, good)

# Write with UTF-8
with open('app_fixed.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Test syntax
import tempfile
import os
result = os.system(f'python -m py_compile app_fixed.py 2>&1 | head -1')

if result == 0:
    print("✅ Fixed version compiles!")
    os.replace('app_fixed.py', 'app.py')
else:
    print("⚠️ Still syntax errors - need manual fix")
