#!/usr/bin/env python
# Check if databases exist and what privileges flaskuser has

import pymysql

try:
    # Connect to MySQL server without specifying database
    conn = pymysql.connect(
        host='192.168.0.57',
        port=3306,
        user='flaskuser',
        password='FlaskSifre123!',
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    
    print("✅ Connected to MySQL as flaskuser\n")
    
    # List databases
    cursor.execute("SHOW DATABASES")
    databases = [row[0] for row in cursor.fetchall()]
    
    print("Available databases for flaskuser:")
    for db in databases:
        print(f"  - {db}")
    
    print()
    
    # Check if order_system_db exists
    if 'order_system_db' in databases:
        print("✅ order_system_db EXISTS")
        print("   Trying to access it...")
        
        try:
            conn2 = pymysql.connect(
                host='192.168.0.57',
                port=3306,
                user='flaskuser',
                password='FlaskSifre123!',
                database='order_system_db',
                charset='utf8mb4'
            )
            cursor2 = conn2.cursor()
            cursor2.execute("SHOW TABLES")
            tables = [row[0] for row in cursor2.fetchall()]
            print(f"   Tables: {tables}")
            cursor2.close()
            conn2.close()
        except Exception as e:
            print(f"   ❌ Cannot access: {e}")
    else:
        print("❌ order_system_db DOES NOT EXIST")
        print("   Need to create it with root privileges")
        print("\n   SQL command to run as root:")
        print("   CREATE DATABASE order_system_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print("   GRANT ALL ON order_system_db.* TO 'flaskuser'@'%' IDENTIFIED BY 'FlaskSifre123!';")
        print("   FLUSH PRIVILEGES;")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Connection error: {e}")
