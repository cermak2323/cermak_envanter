import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    print("❌ DATABASE_URL not found!")
    exit(1)

try:
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    # Check JCB3 package
    cursor.execute('''
        SELECT part_code, part_name, is_package, package_items 
        FROM part_codes 
        WHERE part_code LIKE 'JCB%'
        ORDER BY part_code
    ''')
    
    print("\n📦 Paketler:")
    print("=" * 80)
    for row in cursor.fetchall():
        part_code, part_name, is_package, package_items = row
        print(f"\nParça Kodu: {part_code}")
        print(f"Parça Adı: {part_name}")
        print(f"is_package: {is_package}")
        if package_items:
            print(f"package_items: {package_items[:100]}...")  # First 100 chars
        else:
            print(f"package_items: NULL")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
