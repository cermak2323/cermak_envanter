#!/usr/bin/env python3
"""
Aggressive mojibake cleanup for Turkish characters
"""

with open('app.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Common mojibake patterns in Turkish
mojibake_patterns = {
    'yuzdÄÂµ': 'yüzde',
    'yuzsÃ¼': 'yüzü',
    'Ã¼': 'ü',
    'Ã§': 'ç',
    'Ä±': 'ı',
    'Ã´': 'ö',
    'Ã±': 'ı',
    'ÃÂ±': 'ı',
    'ÃÂ´': 'ö',
    'ÃÂ¼': 'ü',
    'ÃÂ§': 'ç',
    'Ã§': 'ç',
    'Ä\x9e': 'ş',
    'Ã\x9e': 'ş',
    'Ã¦': 'ş',
    # Common compound mojibake
    'AkÃÂ±llÃÂ±': 'Akıllı',
    'DÃ³Ã¼': 'Döndürü',
    'zaman': 'zaman',
    'Bilinmeyen': 'Bilinmeyen',
}

for bad, good in mojibake_patterns.items():
    if bad in content:
        content = content.replace(bad, good)
        print(f"✅ Fixed: {bad} -> {good}")

# Remove remaining invalid non-printable characters
content = ''.join(char if ord(char) >= 32 or char in '\n\r\t' else '' for char in content)

# Count execute_query
execute_count = content.count('execute_query(')
print(f"\nFinal execute_query count: {execute_count}")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Encoding cleanup complete")
