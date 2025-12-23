import psycopg2

conn = psycopg2.connect('postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require')
cur = conn.cursor()

# QR codes tablosu kolonları
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'qr_codes' ORDER BY ordinal_position")
print("qr_codes kolonları:", [r[0] for r in cur.fetchall()])

# Part codes tablosu kolonları
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'part_codes' ORDER BY ordinal_position")
print("part_codes kolonları:", [r[0] for r in cur.fetchall()])

conn.close()
