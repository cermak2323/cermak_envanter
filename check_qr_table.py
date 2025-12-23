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

# Toplam kayıt
cursor.execute('SELECT COUNT(*) FROM qr_codes')
total_qr = cursor.fetchone()[0]

# Farklı part_code sayısı
cursor.execute('SELECT COUNT(DISTINCT part_code_id) FROM qr_codes')
unique_parts = cursor.fetchone()[0]

# İlk 10 QR_ID
cursor.execute('SELECT qr_id FROM qr_codes ORDER BY qr_id LIMIT 10')
sample_qrs = cursor.fetchall()

print("\n" + "="*70)
print("QR_CODES TABLOSU ANALİZİ")
print("="*70)
print(f"Toplam QR kaydı: {total_qr}")
print(f"Farklı parça sayısı: {unique_parts}")
print(f"Ortalama QR/parça: {total_qr / unique_parts:.1f}")
print("="*70)
print("\nÖrnek QR_ID'ler (ilk 10):")
for qr in sample_qrs:
    print(f"  {qr[0]}")

cursor.close()
conn.close()
