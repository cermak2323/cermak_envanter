#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DATABASE_URL')
parsed = urlparse(db_url)

conn = psycopg2.connect(
    host=parsed.hostname,
    port=parsed.port or 5432,
    database=parsed.path[1:],
    user=parsed.username,
    password=parsed.password,
    sslmode='require'
)

cursor = conn.cursor()

# ANT ile başlayan tüm parçalar
cursor.execute("""
    SELECT part_code, part_name 
    FROM part_codes 
    WHERE part_code LIKE 'ANT%'
    ORDER BY part_code
""")

results = cursor.fetchall()

print("\n" + "="*70)
print("ANT İLE BAŞLAYAN TÜM PARÇALAR")
print("="*70)
if results:
    for code, name in results:
        print(f"  {code:20} - {name}")
else:
    print("  Hiç sonuç bulunamadı!")
print("="*70)

cursor.close()
conn.close()
