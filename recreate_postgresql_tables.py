#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostgreSQL Tablo Kurtarma Betiği
Mevcut tabloları sil ve doğru schema ile yeniden oluştur
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

load_dotenv()

# PostgreSQL Connection (Unpooled)
POSTGRESQL_URI = os.environ.get("DATABASE_URL")
if not POSTGRESQL_URI:
    POSTGRESQL_URI = "postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require"

print("""
╔══════════════════════════════════════════════════════════════╗
║         PostgreSQL Tablo Kurtarma Betiği                     ║
║           Drop Old + Create Correct Tables                   ║
╚══════════════════════════════════════════════════════════════╝
""")

def recreate_tables():
    """Tabloları sil ve yeniden oluştur"""
    try:
        conn = psycopg2.connect(POSTGRESQL_URI)
        cursor = conn.cursor()
        
        print("🔴 Eski tabloları siliniyor...\n")
        
        # Drop old tables in reverse dependency order
        tables_to_drop = [
            'scanned_qr',
            'count_passwords',
            'count_sessions',
            'qr_codes',
            'part_codes',
            'envanter_users'
        ]
        
        for table in tables_to_drop:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                print(f"   ✅ {table} silindi")
            except Exception as e:
                print(f"   ⚠️  {table} silinirken hata: {e}")
        
        conn.commit()
        
        print("\n📊 Yeni tabloları oluşturuluyor...\n")
        
        # 1. part_codes tablosu - with all existing columns from SQLite
        cursor.execute("""
            CREATE TABLE part_codes (
                id SERIAL PRIMARY KEY,
                part_code VARCHAR(50) UNIQUE NOT NULL,
                part_name VARCHAR(255) NOT NULL,
                description TEXT,
                is_package BOOLEAN DEFAULT FALSE,
                package_items TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                photo_path TEXT,
                catalog_image TEXT,
                used_in_machines TEXT,
                specifications TEXT,
                stock_location TEXT,
                supplier TEXT,
                unit_price REAL,
                critical_stock_level INTEGER,
                notes TEXT,
                last_updated TIMESTAMP,
                updated_by INTEGER
            )
        """)
        print("   ✅ part_codes tablosu oluşturuldu")
        
        # 2. qr_codes tablosu - with all existing columns
        cursor.execute("""
            CREATE TABLE qr_codes (
                id SERIAL PRIMARY KEY,
                qr_id VARCHAR(100) UNIQUE NOT NULL,
                part_code_id INTEGER REFERENCES part_codes(id),
                blob_url VARCHAR(500),
                blob_file_id VARCHAR(100),
                is_used BOOLEAN DEFAULT FALSE,
                used_count INTEGER DEFAULT 0,
                first_used_at TIMESTAMP,
                last_used_at TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP
            )
        """)
        print("   ✅ qr_codes tablosu oluşturuldu")
        
        # 3. envanter_users tablosu - with ALL existing columns
        cursor.execute("""
            CREATE TABLE envanter_users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255),
                password_hash VARCHAR(255),
                full_name VARCHAR(255),
                role VARCHAR(50),
                created_at TIMESTAMP,
                real_name VARCHAR(255),
                email VARCHAR(255),
                job_title VARCHAR(120),
                title VARCHAR(120),
                work_position VARCHAR(120),
                user_group VARCHAR(120),
                user_role VARCHAR(120),
                signature_path VARCHAR(500),
                profile_image_path VARCHAR(500),
                is_active_user BOOLEAN,
                can_mark_used BOOLEAN,
                email_2fa_enabled BOOLEAN,
                email_2fa_code VARCHAR(6),
                email_2fa_expires TIMESTAMP,
                email_2fa_attempts INTEGER,
                email_2fa_locked_until TIMESTAMP,
                tc_number VARCHAR(20),
                last_password_change TIMESTAMP,
                force_password_change BOOLEAN,
                force_tutorial BOOLEAN,
                first_login_completed BOOLEAN,
                last_login TIMESTAMP,
                terms_accepted BOOLEAN,
                updated_at TIMESTAMP
            )
        """)
        print("   ✅ envanter_users tablosu oluşturuldu")
        
        # 4. count_sessions tablosu - with all columns
        cursor.execute("""
            CREATE TABLE count_sessions (
                id SERIAL PRIMARY KEY,
                session_name VARCHAR(255),
                session_password VARCHAR(255),
                created_by INTEGER,
                is_active BOOLEAN,
                created_at TIMESTAMP,
                started_at TIMESTAMP,
                ended_at TIMESTAMP,
                description TEXT,
                total_expected INTEGER,
                total_scanned INTEGER,
                report_file_path TEXT
            )
        """)
        print("   ✅ count_sessions tablosu oluşturuldu")
        
        # 5. scanned_qr tablosu - with all columns
        cursor.execute("""
            CREATE TABLE scanned_qr (
                id SERIAL PRIMARY KEY,
                session_id INTEGER,
                qr_id VARCHAR(255),
                part_code VARCHAR(255),
                scanned_by INTEGER,
                scanned_at TIMESTAMP
            )
        """)
        print("   ✅ scanned_qr tablosu oluşturuldu")
        
        # 6. count_passwords tablosu - with all columns
        cursor.execute("""
            CREATE TABLE count_passwords (
                id SERIAL PRIMARY KEY,
                session_id INTEGER,
                password VARCHAR(255),
                created_at TIMESTAMP,
                created_by INTEGER
            )
        """)
        print("   ✅ count_passwords tablosu oluşturuldu")
        
        # Indexler ekle
        print("\n📇 Indexleri Oluşturuluyor...")
        
        cursor.execute("CREATE INDEX idx_part_codes_part_code ON part_codes(part_code)")
        cursor.execute("CREATE INDEX idx_qr_codes_qr_id ON qr_codes(qr_id)")
        cursor.execute("CREATE INDEX idx_qr_codes_part_code_id ON qr_codes(part_code_id)")
        cursor.execute("CREATE INDEX idx_envanter_users_username ON envanter_users(username)")
        cursor.execute("CREATE INDEX idx_count_sessions_created_by ON count_sessions(created_by)")
        cursor.execute("CREATE INDEX idx_scanned_qr_session_id ON scanned_qr(session_id)")
        
        print("   ✅ Indexler oluşturuldu")
        
        conn.commit()
        
        print("\n" + "="*60)
        print("✅ PostgreSQL TABLOLARI YENİDEN OLUŞTURULDU!")
        print("="*60)
        print("\nSonraki Adım:")
        print("  python migrate_to_postgresql.py")
        print("\n" + "="*60)
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ PostgreSQL hatası: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔐 Neon PostgreSQL Veritabanına Bağlanıluyor...")
    try:
        conn = psycopg2.connect(POSTGRESQL_URI)
        conn.close()
        print("✅ Bağlantı başarılı\n")
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        sys.exit(1)
    
    success = recreate_tables()
    sys.exit(0 if success else 1)
