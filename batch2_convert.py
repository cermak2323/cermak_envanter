#!/usr/bin/env python3
"""
Batch 2: Convert more scanning engine + excel operations to ORM
"""
import re

with open('app.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

print(f"Starting: {content.count('execute_query(')} execute_query calls")

# BATCH 2 CONVERSIONS

# 1. UPDATE session stats (after scan insertion)
update_pattern = r"execute_query\(cursor, '''?\s+UPDATE count_sessions\s+SET total_scanned = \(SELECT COUNT\(\*\) FROM scanned_qr WHERE session_id = \?\)\s+WHERE id = \?\s+'''?, \(session_id, session_id\)\)"

# Replace with ORM
update_replacement = """# Update session stats - ORM
            db.session.query(CountSession).filter_by(id=session_id).update({
                CountSession.total_scanned: db.session.query(ScannedQR).filter_by(session_id=session_id).count()
            })
            db.session.commit()"""

content = re.sub(update_pattern, update_replacement, content, flags=re.DOTALL)

# 2. SELECT part_codes for dropdown (common pattern)
parts_select = r"execute_query\(cursor, 'SELECT id, part_code, part_name FROM part_codes ORDER BY part_code'\)"
parts_replacement = "# Get all parts - ORM\n            parts = PartCode.query.order_by(PartCode.part_code).all()"

content = re.sub(parts_select, parts_replacement, content, flags=re.IGNORECASE)

# 3. COUNT queries for statistics
count_pattern = r"execute_query\(cursor, 'SELECT COUNT\(\*\) FROM ([^']+)'\)\s+result = cursor\.fetchone\(\)\[0\]"
count_replacement = r"result = db.session.query(\1).count()  # ORM COUNT"

# Need to be smarter about this - map table names to models
table_model_map = {
    'scanned_qr': 'ScannedQR',
    'qr_codes': 'QRCode',
    'part_codes': 'PartCode',
    'envanter_users': 'User',
    'count_sessions': 'CountSession'
}

for table, model in table_model_map.items():
    pattern = f"execute_query\\(cursor, 'SELECT COUNT\\(\\*\\) FROM {table}'\\)\\s+result = cursor\\.fetchone\\(\\)\\[0\\]"
    replacement = f"result = db.session.query({model}).count()  # ORM COUNT"
    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

# 4. Simple SELECT id FROM table
for table, model in table_model_map.items():
    # Pattern: execute_query(cursor, 'SELECT id FROM table WHERE ...')
    # This requires more context, so skip complex ones
    pass

# 5. Fix leftover cursor issues from partial conversions
content = content.replace('cursor.execute', 'db.session.execute')  # Basic fix for remaining cursor.execute
content = content.replace('cursor.fetchone()', 'result')  # Fix orphaned fetchone
content = content.replace('cursor.fetchall()', 'results')  # Fix orphaned fetchall

print(f"After batch 2: {content.count('execute_query(')} execute_query calls")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Batch 2 complete")
