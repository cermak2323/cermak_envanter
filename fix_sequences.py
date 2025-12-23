#!/usr/bin/env python3
"""
PostgreSQL Sequence Fixer
Bu script tüm sequence'ları düzeltir ve duplicate key hatalarını önler
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def fix_all_sequences():
    """Tüm PostgreSQL sequence'larını düzelt"""
    
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL bulunamadı!")
        return
    
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        tables = [
            ('scanned_qr', 'id'),
            ('count_sessions', 'id'),
            ('qr_codes', 'id'),
            ('part_codes', 'id'),
            ('envanter_users', 'id'),
            ('count_reports', 'id')
        ]
        
        print("🔧 PostgreSQL Sequence Düzeltme Başlatıldı...\n")
        
        for table_name, id_column in tables:
            try:
                sequence_name = f"{table_name}_{id_column}_seq"
                
                # En yüksek id'yi al
                cursor.execute(f"SELECT MAX({id_column}) FROM {table_name}")
                max_id = cursor.fetchone()[0]
                
                if max_id is not None:
                    # Sequence'ı max_id + 1'e set et
                    cursor.execute(f"SELECT setval('{sequence_name}', %s, true)", (max_id,))
                    conn.commit()
                    print(f"✅ {table_name}: Sequence {max_id} -> {max_id + 1}")
                else:
                    print(f"⚠️  {table_name}: Tablo boş, sequence atlandı")
                    
            except Exception as e:
                print(f"❌ {table_name}: {e}")
                conn.rollback()
        
        cursor.close()
        conn.close()
        
        print("\n✅ Tüm sequence'lar düzeltildi!")
        print("Artık QR okutabilirsiniz.")
        
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")

if __name__ == '__main__':
    fix_all_sequences()
