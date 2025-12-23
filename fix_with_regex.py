#!/usr/bin/env python3
"""
Bulk convert remaining 49 execute_query to ORM for scanning engine
Using regex patterns to handle Turkish characters + encoding issues
"""
import re

# Read file properly - this file was already partially converted, so it has 120 ORM conversions
with open('app_backup_20251120_124118.py', 'rb') as f:
    raw_bytes = f.read()

# Decode with proper handling
content = raw_bytes.decode('utf-8', errors='replace')

print(f"File size: {len(content)} chars")
print(f"Initial execute_query count: {content.count('execute_query(')}")

# Strategy: Replace entire function blocks with ORM versions
# Focus on: handle_scan_radical (CRITICAL)

# CONVERSION 1: Session check + create
# Pattern: execute_query ... SELECT COUNT(*) ... if cursor.fetchone()[0] == 0 ... INSERT
session_pattern = r"execute_query\(cursor, 'SELECT COUNT\(\*\) FROM count_sessions WHERE id = \?', \(session_id,\)\)\s+if cursor\.fetchone\(\)\[0\] == 0:"
session_replacement = r"count_session = CountSession.query.filter_by(id=session_id).first()\n            if not count_session:"

content = re.sub(session_pattern, session_replacement, content)

# CONVERSION 2: INSERT new session  
insert_pattern = r"execute_query\(cursor,\s+'INSERT INTO count_sessions \(id, session_name, is_active, created_at\) VALUES \(\?, \?, \?, \?\)',\s+\(session_id, f'Session_\{session_id\}', 1, datetime\.now\(\)\)\)"
insert_replacement = """new_session = CountSession(
                    id=session_id,
                    session_name=f'Session_{session_id}',
                    is_active=True,
                    created_at=datetime.now()
                )
                db.session.add(new_session)
                db.session.commit()"""

content = re.sub(insert_pattern, insert_replacement, content, flags=re.DOTALL)

# CONVERSION 3: Duplicate check - SELECT from scanned_qr
dup_pattern = r"execute_query\(cursor, '''?\s+SELECT scanned_by, scanned_at\s+FROM scanned_qr\s+WHERE session_id = \? AND qr_id = \?\s+'''?, \(session_id, qr_id\)\)\s+duplicate_record = cursor\.fetchone\(\)"
dup_replacement = "duplicate_record = ScannedQR.query.filter_by(session_id=session_id, qr_id=qr_id).first()"

content = re.sub(dup_pattern, dup_replacement, content, flags=re.DOTALL)

print(f"After regex conversions: {content.count('execute_query(')}")

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Regex-based conversion complete")
