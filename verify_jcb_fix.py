import pymysql
conn = pymysql.connect(
    host='192.168.0.57', port=3306, user='flaskuser', password='FlaskSifre123!',
    database='flaskdb', charset='utf8mb4'
)
cursor = conn.cursor()

# Check QR linkage
cursor.execute("SELECT qr_code, part_code_id FROM qr_codes WHERE qr_code = 'JCB'")
qr = cursor.fetchone()
print(f'QR JCB points to part_code_id: {qr[1] if qr else "NOT FOUND"}')

# Check what record that points to
if qr:
    cursor.execute("SELECT part_code, is_package, CHAR_LENGTH(package_items) FROM part_codes WHERE id = %s", (qr[1],))
    pkg = cursor.fetchone()
    print(f'  part_code: {pkg[0]}, is_package: {pkg[1]}, items_len: {pkg[2]}')

conn.close()
