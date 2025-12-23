import os
import json
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
    
    # Get latest session
    cursor.execute('''
        SELECT id, session_name, description, total_expected 
        FROM count_sessions 
        ORDER BY id DESC 
        LIMIT 1
    ''')
    
    row = cursor.fetchone()
    if row:
        session_id, session_name, description, total_expected = row
        print(f"\n📊 Latest Session:")
        print(f"  ID: {session_id}")
        print(f"  Name: {session_name}")
        print(f"  Total Expected: {total_expected}")
        print(f"\n📄 Description (raw):")
        print(f"  {description}")
        
        if description:
            try:
                expected_list = json.loads(description)
                print(f"\n✅ Parsed JSON ({len(expected_list)} items):")
                for i, item in enumerate(expected_list[:3]):  # Show first 3
                    print(f"\n  Item {i+1}:")
                    for key, value in item.items():
                        print(f"    {key}: {value}")
            except Exception as e:
                print(f"\n❌ JSON Parse Error: {e}")
    else:
        print("❌ No sessions found!")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
