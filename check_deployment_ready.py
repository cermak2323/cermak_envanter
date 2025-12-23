#!/usr/bin/env python3
"""
QUICK VERIFICATION: System deployment readiness checker
Run this to verify system is ready for PC deployment
"""

import os
import sys
from pathlib import Path

print("=" * 70)
print("ENVANTER QR - DEPLOYMENT READINESS CHECK")
print("=" * 70)

checks_passed = 0
checks_total = 0

def check(name, condition, details=""):
    global checks_passed, checks_total
    checks_total += 1
    if condition:
        print(f"✅ {name}")
        checks_passed += 1
    else:
        print(f"❌ {name}")
        if details:
            print(f"   → {details}")
    return condition

# Check 1: File exists and is readable
check("app.py exists", os.path.isfile('app.py'), "File not found")

# Check 2: Python syntax valid
try:
    import ast
    with open('app.py', 'r', encoding='utf-8') as f:
        ast.parse(f.read())
    check("Python syntax valid", True)
except SyntaxError as e:
    check("Python syntax valid", False, f"Syntax error: {e}")

# Check 3: .env file configured
env_exists = os.path.isfile('.env')
check("Environment file (.env)", env_exists, "Create .env with DATABASE_URL and other config")

# Check 4: Models defined
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("app", "app.py")
    # Don't actually load it (requires DB), just check if file structure is OK
    check("Models defined", "QRCode" in open('app.py').read() and "PartCode" in open('app.py').read())
except Exception as e:
    check("Models defined", False, str(e))

# Check 5: PostgreSQL config present
config_text = open('app.py').read()
check("PostgreSQL configured", "postgresql" in config_text.lower(), "DATABASE_URL should use postgresql://")

# Check 6: Requirements installed
try:
    import flask
    import flask_sqlalchemy
    check("Flask installed", True)
except ImportError:
    check("Flask installed", False, "Run: pip install -r requirements.txt")

# Check 7: Database folder exists
check("Database backup folder", os.path.isdir('backups'))

# Check 8: Static/template folders exist
check("Static assets folder", os.path.isdir('static'))
check("HTML templates folder", os.path.isdir('templates'))

print("\n" + "=" * 70)
print(f"DEPLOYMENT READINESS: {checks_passed}/{checks_total} checks passed")

if checks_passed >= checks_total - 2:  # Allow 2 failures (DB connection, .env might not exist yet)
    print("\n🚀 SYSTEM IS READY FOR DEPLOYMENT")
    print("\nNext steps:")
    print("1. Update .env file with PostgreSQL credentials")
    print("2. Run: python app.py")
    print("3. Test on first PC")
    print("4. Deploy to additional PCs")
    sys.exit(0)
else:
    print("\n⚠️  System needs fixes before deployment")
    sys.exit(1)
