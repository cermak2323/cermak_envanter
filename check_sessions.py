import psycopg2

conn = psycopg2.connect('postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require')
cur = conn.cursor()

cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'count_sessions' ORDER BY ordinal_position")
print("count_sessions:", [r[0] for r in cur.fetchall()])

cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'scanned_qr' ORDER BY ordinal_position")
print("scanned_qr:", [r[0] for r in cur.fetchall()])

conn.close()
