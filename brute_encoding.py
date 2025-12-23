#!/usr/bin/env python3
"""
Try all possible encoding combinations to fix the backup file
"""

attempts = [
    ('utf-8', 'ascii', 'replace'),
    ('latin-1', 'utf-8', 'replace'),
    ('iso-8859-9', 'utf-8', 'replace'),  # Turkish ISO
    ('cp1252', 'utf-8', 'replace'),  # Windows encoding
]

for src_enc, tgt_enc, errors in attempts:
    try:
        with open('app_backup_20251120_124118.py', 'rb') as f:
            raw = f.read()
        
        # Decode with source encoding, re-encode to target
        content = raw.decode(src_enc, errors=errors)
        test_bytes = content.encode(tgt_enc, errors=errors)
        
        # Write test
        with open('app_test.py', 'wb') as f:
            f.write(test_bytes)
        
        # Try compile
        import subprocess
        result = subprocess.run(['python', '-m', 'py_compile', 'app_test.py'], 
                              capture_output=True, timeout=5)
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {src_enc} -> {tgt_enc}")
            import os
            os.replace('app_test.py', 'app.py')
            with open('SUCCESS.txt', 'w') as f:
                f.write(f"Fixed with: {src_enc} -> {tgt_enc}")
            exit(0)
    except Exception as e:
        pass

print("❌ No encoding combination worked")
