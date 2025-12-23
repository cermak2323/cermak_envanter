#!/usr/bin/env python3
"""
Nuclear: Strip ALL non-ASCII except Turkish, then compile and write
"""

with open('app_backup_20251120_124118.py', 'rb') as f:
    raw = f.read()

# Decode as latin-1 (never fails)
content = raw.decode('latin-1', errors='ignore')

# Keep ONLY: ASCII letters/numbers/symbols + Turkish vowels + whitespace  
KEEP = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \t\n\r!@#$%^&*()-_=+[]{}|;:,.<>?/~`\'"\\')
KEEP.update('çğıöşüÇĞİÖŞÜ')  # Turkish

cleaned_lines = []
for line in content.split('\n'):
    # Keep line if it has code characters
    cleaned_line = ''.join(c if c in KEEP else '?' for c in line)
    # Replace ? with nothing if not needed
    cleaned_line = cleaned_line.replace('?', '')
    cleaned_lines.append(cleaned_line)

cleaned_content = '\n'.join(cleaned_lines)

# Fix common patterns that might have been destroyed
cleaned_content = cleaned_content.replace('?', '')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(cleaned_content)

print(f"✅ Cleaned: {len(cleaned_content)} chars")

# Verify
import subprocess
result = subprocess.run(['python', '-c', 'import ast; ast.parse(open("app.py").read())'],
                       capture_output=True, text=True, timeout=5)

if result.returncode == 0:
    print("✅ SYNTAX VALID!")
    exit(0)
else:
    error_line = result.stderr.split('line ')[1].split('\n')[0] if 'line' in result.stderr else '?'
    print(f"❌ Syntax error at line {error_line}")
    # Show the problematic line
    with open('app.py', 'r') as f:
        lines = f.readlines()
        try:
            line_num = int(error_line)
            if line_num <= len(lines):
                print(f"   {lines[line_num-1][:80]}")
        except:
            pass
    exit(1)
