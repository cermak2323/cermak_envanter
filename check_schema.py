import sqlite3

conn = sqlite3.connect('instance/envanter_local.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(envanter_users)")
cols = cursor.fetchall()
print('Columns:')
for c in cols:
    print(f'  {c[1]} ({c[2]})')
conn.close()
