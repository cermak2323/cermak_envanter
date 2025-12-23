import requests
import json

# Başlat count session
session_res = requests.post('http://localhost:5002/api/start_count_session', json={
    'expected_item_count': 10
})

print(f"Start session response: {session_res.status_code}")
session_data = session_res.json()
session_id = session_data.get('session_id')
print(f"Session ID: {session_id}")

# JPN QR'ı tara
scan_res = requests.post('http://localhost:5002/api/scan_qr', json={
    'qr_id': 'JPN',
    'session_id': session_id
})

print(f"\nScan response: {scan_res.status_code}")
print(f"Response: {json.dumps(scan_res.json(), indent=2)}")

# Kontrol: scanned_qr tablosuna bak
import sqlite3
conn = sqlite3.connect('instance/envanter_local.db')
c = conn.cursor()

c.execute('''
    SELECT part_code, COUNT(*) FROM scanned_qr 
    WHERE session_id = ? 
    GROUP BY part_code 
    ORDER BY part_code
''', (session_id,))

print("\nScanned QR Records:")
rows = c.fetchall()
for row in rows:
    print(f"  {row[0]}: {row[1]} scans")

# Önemli: JPN bulundu mu?
c.execute("SELECT COUNT(*) FROM scanned_qr WHERE session_id = ? AND part_code = 'JPN'", (session_id,))
jpn_count = c.fetchone()[0]

if jpn_count > 0:
    print(f"\n❌ PROBLEM: JPN itself was counted ({jpn_count} times)!")
else:
    print(f"\n✅ SUCCESS: JPN was NOT counted (only its contents)")

conn.close()
