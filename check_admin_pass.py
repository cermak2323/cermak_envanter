from werkzeug.security import check_password_hash
import psycopg2

conn = psycopg2.connect('postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require')
cur = conn.cursor()
cur.execute("SELECT username, password_hash FROM envanter_users WHERE username='admin'")
row = cur.fetchone()

if row:
    username, hash_val = row
    print(f'Username: {username}')
    print(f'Hash: {hash_val[:60]}...')
    
    test_password = '@R9t$L7e!xP2w'
    is_valid = check_password_hash(hash_val, test_password)
    print(f'Password "@R9t$L7e!xP2w" is valid: {is_valid}')
else:
    print('Admin user not found!')

conn.close()
