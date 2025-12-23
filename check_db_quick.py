import sqlite3

conn = sqlite3.connect('instance/envanter_local.db')
c = conn.cursor()

# Check tables
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()

print("Tables:")
for table in tables:
    c.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = c.fetchone()[0]
    print(f"  {table[0]}: {count} rows")

# Check if JPN exists
c.execute("SELECT * FROM part_codes WHERE part_code = 'JPN'")
jpn = c.fetchone()
print(f"\nJPN package: {jpn}")

conn.close()
