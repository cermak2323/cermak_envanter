#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostgreSQL Database Optimization Script
Adds missing indexes for faster QR scanning
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def optimize_database():
    """Add critical indexes for fast QR scanning"""
    
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL bulunamadı!")
        return
    
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        print("🔧 PostgreSQL Optimizasyonu Başlatılıyor...")
        print("=" * 60)
        
        # Critical indexes for QR scanning performance
        indexes = [
            # scanned_qr table - duplicate check için
            ("idx_scanned_qr_session_qr", "scanned_qr", "(session_id, qr_id)"),
            ("idx_scanned_qr_session", "scanned_qr", "session_id"),
            
            # qr_codes table - QR lookup için
            ("idx_qr_codes_qr_id", "qr_codes", "qr_id"),
            ("idx_qr_codes_part_code_id", "qr_codes", "part_code_id"),
            
            # part_codes table - part_code lookup için
            ("idx_part_codes_part_code", "part_codes", "part_code"),
            
            # count_sessions table - session stats için
            ("idx_count_sessions_id", "count_sessions", "id"),
        ]
        
        created_count = 0
        existing_count = 0
        
        for index_name, table_name, columns in indexes:
            try:
                # Check if index exists
                cursor.execute("""
                    SELECT 1 FROM pg_indexes 
                    WHERE indexname = %s
                """, (index_name,))
                
                if cursor.fetchone():
                    print(f"✓ {index_name} - zaten mevcut")
                    existing_count += 1
                else:
                    # Create index
                    sql = f"CREATE INDEX {index_name} ON {table_name} {columns}"
                    cursor.execute(sql)
                    conn.commit()
                    print(f"✅ {index_name} - oluşturuldu")
                    created_count += 1
                    
            except Exception as e:
                print(f"⚠️ {index_name} - hata: {e}")
                conn.rollback()
        
        print("=" * 60)
        print(f"📊 Sonuç: {created_count} yeni index oluşturuldu, {existing_count} zaten mevcut")
        
        # Analyze tables for query planner
        print("\n🔍 Tablo istatistikleri güncelleniyor...")
        tables = ['scanned_qr', 'qr_codes', 'part_codes', 'count_sessions']
        for table in tables:
            try:
                cursor.execute(f"ANALYZE {table}")
                print(f"✓ {table} - analiz edildi")
            except Exception as e:
                print(f"⚠️ {table} - analiz hatası: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ Optimizasyon tamamlandı!")
        print("💡 QR tarama hızı artık çok daha hızlı olmalı.")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    optimize_database()
