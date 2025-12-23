#!/usr/bin/env python3
"""
Convert all get_db()/execute_query()/close_db() calls to SQLAlchemy directly
This is a reference for what needs to be done - DO NOT RUN DIRECTLY
"""

# PATTERN 1: Simple queries
# OLD: conn = get_db(); cursor = conn.cursor(); execute_query(cursor, 'SELECT ...')
# NEW: db.session.execute(text('SELECT ...'))

# PATTERN 2: With params
# OLD: execute_query(cursor, 'SELECT ... WHERE id = ?', (id,))
# NEW: db.session.execute(text('SELECT ... WHERE id = :id'), {'id': id})

# PATTERN 3: Fetch results  
# OLD: cursor.fetchone() / cursor.fetchall()
# NEW: result.fetchone() / result.fetchall() (same)

# PATTERN 4: Insert/Update/Delete
# OLD: cursor.execute('INSERT INTO ...'); conn.commit()
# NEW: db.session.execute(text('INSERT INTO ...')); db.session.commit()

# EXAMPLES:

# Example 1: Count query
# OLD: execute_query(cursor, 'SELECT COUNT(*) FROM users'); count = cursor.fetchone()[0]
# NEW: count = db.session.execute(text('SELECT COUNT(*) FROM users')).scalar()

# Example 2: Filter query
# OLD: execute_query(cursor, 'SELECT * FROM users WHERE id = ?', (1,)); user = cursor.fetchone()
# NEW: user = db.session.execute(text('SELECT * FROM users WHERE id = :id'), {'id': 1}).fetchone()

# Example 3: Insert
# OLD: cursor.execute('INSERT INTO users (name) VALUES (?)', (name,)); conn.commit()
# NEW: db.session.execute(text('INSERT INTO users (name) VALUES (:name)'), {'name': name}); db.session.commit()

print("Replace patterns documented - see this file for SQL conversion rules")
