#!/usr/bin/env python3
"""
Check if part_codes table has any data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from models import PartCode

print("\n" + "="*70)
print("DATABASE CONTENT CHECK")
print("="*70 + "\n")

with app.app_context():
    try:
        # Count total part codes
        count = db.session.query(PartCode).count()
        print(f"Total part codes in database: {count}")
        
        if count > 0:
            # Get first 10 part codes
            print(f"\nFirst 10 part codes:")
            parts = db.session.query(PartCode).limit(10).all()
            for i, part in enumerate(parts, 1):
                print(f"  {i}. Code: {part.part_code}, Name: {part.part_name}")
        else:
            print("\n⚠️  Database is empty! No part codes found.")
            print("You need to import or add part codes before searching.")
    
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "="*70 + "\n")
