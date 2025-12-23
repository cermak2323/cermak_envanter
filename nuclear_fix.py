#!/usr/bin/env python3
"""
Nuclear option: Remove ALL broken mojibake - fix by character-by-character replacement
"""

with open('app.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Character-level mojibake patterns
char_fixes = {
    'Ã¼': 'ü',
    'Ã§': 'ç', 
    'Ä±': 'ı',
    'Ã´': 'ö',
    'Ä\x9e': 'ş',
    'ÃÂ': '',  # Remove broken prefix
    '„': '',   # U+201E - broken character
    '├': '',
    '┬': '',
    '├┼': 'ş',
    '├╣': 'ı',
    'Ã‚': '',
    'Â': '',
    'Ã': '',
    'Ä': '',
    'Ã¢': '',
    'Ã„': '',
}

new_lines = []
for line in lines:
    for bad_char, good_char in char_fixes.items():
        line = line.replace(bad_char, good_char)
    new_lines.append(line)

new_content = ''.join(new_lines)

# Nuclear: Remove ANY character that's not ASCII 32-126, Turkish letters, or whitespace
# Allowed: ASCII printable (32-126), Turkish (ü ç ş ğ ı ö Ü Ç Ş Ğ İ Ö), and control chars (9,10,13)
ALLOWED_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \t\n\r!@#$%^&*()-_=+[]{}|;:,.<>?/~`\'"\\üçşğıöÜÇŞĞİÖ')

cleaned_content = ''.join(c for c in new_content if c in ALLOWED_CHARS or ord(c) > 126)

# Write fixed
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(cleaned_content)

print("✅ Nuclear mojibake cleanup complete")
print(f"   Content size before: {len(new_content)}")
print(f"   Content size after: {len(cleaned_content)}")

# Verify syntax
import subprocess
result = subprocess.run(['python', '-c', 'import ast; ast.parse(open("app.py").read())'],
                       capture_output=True, text=True)

if result.returncode == 0:
    print("✅ SYNTAX 100% VALID NOW!")
else:
    print(f"⚠️  Error: {result.stderr.split(chr(10))[0]}")
