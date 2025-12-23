#!/usr/bin/env python3
"""
Fix encoding + convert remaining 49 execute_query calls to ORM
"""

# Read file properly
with open('app_backup_20251120_124118.py', 'rb') as f:
    raw_bytes = f.read()

# Decode with proper handling
try:
    content = raw_bytes.decode('utf-8', errors='replace')
except:
    content = raw_bytes.decode('latin-1', errors='replace')

# Count initial execute_query calls
initial_count = content.count('execute_query(')
print(f"Initial execute_query count: {initial_count}")

# Key conversions for scanning engine (handle_scan_radical function)
# This is the CRITICAL hot path that must be ORM

# 1. Session handling - these must be converted early
conversions = [
    # Session creation check + INSERT
    ('''execute_query(cursor, 'SELECT COUNT(*) FROM count_sessions WHERE id = ?', (session_id,))
            if cursor.fetchone()[0] == 0:
                logging.info(f"Creating new session {session_id}")
                execute_query(cursor, 
                    'INSERT INTO count_sessions (id, session_name, is_active, created_at) VALUES (?, ?, ?, ?)',
                    (session_id, f'Session_{session_id}', 1, datetime.now()))
                conn.commit()''',
     '''count_session = CountSession.query.filter_by(id=session_id).first()
            if not count_session:
                logging.info(f"Creating new session {session_id}")
                new_session = CountSession(
                    id=session_id,
                    session_name=f'Session_{session_id}',
                    is_active=True,
                    created_at=datetime.now()
                )
                db.session.add(new_session)
                db.session.commit()'''),
]

for old, new in conversions:
    if old in content:
        content = content.replace(old, new)
        print(f"✅ Converted session handling")

# Final count
final_count = content.count('execute_query(')
print(f"Final execute_query count: {final_count}")
print(f"Converted: {initial_count - final_count} calls")

# Write back
with open('app.py', 'w', encoding='utf-8', errors='replace') as f:
    f.write(content)

print("✅ Conversion complete - app.py updated")
