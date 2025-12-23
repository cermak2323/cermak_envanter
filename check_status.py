import mysql.connector

conn = mysql.connector.connect(
    host='192.168.0.57',
    user='flaskuser',
    password='FlaskSifre123!',
    database='flaskdb'
)
cursor = conn.cursor()
cursor.execute("DESCRIBE order_list")
for row in cursor.fetchall():
    if 'status' in str(row[0]).lower():
        print(f"Kolon: {row[0]}, Tip: {row[1]}")
        
print("\nTüm sütunlar:")
cursor.execute("DESCRIBE order_list")
for row in cursor.fetchall():
    print(f"{row[0]} -> {row[1]}")

conn.close()
