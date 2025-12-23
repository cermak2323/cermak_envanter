#!/usr/bin/env python3
"""
qr_codes tablosuna used_at kolonu ekle
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def add_used_at_column():
    """qr_codes tablosuna used_at kolonu ekle"""
    
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL bulunamadı!")
        return
    
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        print("🔧 qr_codes tablosuna used_at kolonu ekleniyor...\n")
        
        # 1. Kolon ekle
        try:
            cursor.execute("""
                ALTER TABLE qr_codes 
                ADD COLUMN IF NOT EXISTS used_at TIMESTAMP
            """)
            conn.commit()
            print("✅ used_at kolonu eklendi")
        except Exception as e:
            print(f"⚠️  used_at kolonu: {e}")
            conn.rollback()
        
        # 2. Index ekle
        try:
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_qr_codes_used_at 
                ON qr_codes(used_at)
            """)
            conn.commit()
            print("✅ used_at index oluşturuldu")
        except Exception as e:
            print(f"⚠️  Index: {e}")
            conn.rollback()
        
        # 3. Mevcut is_used=true kayıtları güncelle
        try:
            cursor.execute("""
                UPDATE qr_codes 
                SET used_at = created_at 
                WHERE is_used = TRUE AND used_at IS NULL
            """)
            updated = cursor.rowcount
            conn.commit()
            print(f"✅ {updated} kayıt güncellendi (used_at = created_at)")
        except Exception as e:
            print(f"⚠️  Güncelleme: {e}")
            conn.rollback()
        
        cursor.close()
        conn.close()
        
        print("\n✅ used_at kolonu başarıyla eklendi!")
        print("Artık app.py'de used_at kullanabilirsiniz.")
        
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")

if __name__ == '__main__':
    add_used_at_column()
