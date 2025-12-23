import mysql.connector

conn = mysql.connector.connect(
    host='192.168.0.57',
    user='flaskuser',
    password='FlaskSifre123!',
    database='flaskdb'
)
cursor = conn.cursor()

print("Status ENUM şeması güncelleniyor...")

try:
    # Status ENUM'unu güncelle - 'Kısmi' ekle
    cursor.execute("""
        ALTER TABLE order_list 
        MODIFY status ENUM('Gelmedi', 'Kısmi', 'Geldi')
    """)
    conn.commit()
    print("✅ Status ENUM başarıyla güncellendi: 'Gelmedi', 'Kısmi', 'Geldi'")
    
    # Doğrulama
    cursor.execute("DESCRIBE order_list")
    for row in cursor.fetchall():
        if row[0] == 'status':
            print(f"Doğrulama - Status sütunu: {row[1]}")
            
except Exception as e:
    print(f"❌ Hata: {e}")
finally:
    conn.close()
