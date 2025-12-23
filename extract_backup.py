#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sqlite3
import os

# Check what backups we have
backup_path = "backups/envanter_backup_20251212_020000.db"

if os.path.exists(backup_path):
    print(f"✓ Backup DB found")
    
    # Read from SQLite backup
    try:
        conn = sqlite3.connect(backup_path)
        cursor = conn.cursor()
        
        # Get JCB package - try different variations
        cursor.execute("SELECT id, part_code, part_name, package_items FROM part_codes WHERE part_code='JCB' AND package_items IS NOT NULL LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            jcb_id, jcb_code, jcb_name, jcb_items = result
            print(f"✓ Found JCB in backup:")
            print(f"  ID: {jcb_id}, Code: {jcb_code}, Name: {jcb_name}")
            print(f"  Items size: {len(jcb_items) if jcb_items else 0} bytes")
            
            # Save to JSON
            backup_data = {
                "part_code": jcb_code,
                "part_name": jcb_name,
                "package_items": jcb_items.decode('utf-8') if isinstance(jcb_items, bytes) else jcb_items
            }
            
            with open("jcb_backup.json", "w", encoding="utf-8") as f:
                json.dump(backup_data, f, ensure_ascii=False)
            
            print(f"✓ Saved backup to jcb_backup.json")
        else:
            print("✗ No JCB found with package items")
        
        conn.close()
    except Exception as e:
        print(f"✗ Error reading backup: {e}")
else:
    print(f"✗ Backup not found at {backup_path}")

# Check if JSON backup now exists
if os.path.exists("jcb_backup.json"):
    print("\n✓ jcb_backup.json exists - ready to restore")
