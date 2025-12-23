import pymysql

try:
    conn = pymysql.connect(
        host='192.168.0.57',
        user='flaskuser',
        password='FlaskSifre123!',
        database='flaskdb',
        port=3306,
        charset='utf8mb4'
    )
    print("✅ MySQL bağlantısı başarılı!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"MySQL Version: {version[0]}")
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"Tablolar: {[t[0] for t in tables]}")
    
    conn.close()
except Exception as e:
    print(f"❌ Hata: {e}")
