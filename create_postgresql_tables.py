#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostgreSQL Tablo Oluşturma Betiği
Neon'da tabloları SQLAlchemy ORM ile oluşturur
"""

import os
import sys
from pathlib import Path
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
║         PostgreSQL Tablo Oluşturma Betiği                    ║
║              Create Tables in Neon Database                  ║
╚══════════════════════════════════════════════════════════════╝
""")

def create_tables():
    """PostgreSQL'de tabloları oluştur"""
    try:
        conn = psycopg2.connect(POSTGRESQL_URI)
        cursor = conn.cursor()
        
        print("📊 PostgreSQL Tablolarını Oluşturuluyor...\n")
        
        # 1. part_codes tablosu - with all existing columns from SQLite
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS part_codes (
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
            CREATE TABLE IF NOT EXISTS qr_codes (
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
            CREATE TABLE IF NOT EXISTS envanter_users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255),
                password_hash VARCHAR(255),
                full_name VARCHAR(255),
                role VARCHAR(50),
                created_at DATETIME,
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
                email_2fa_expires DATETIME,
                email_2fa_attempts INTEGER,
                email_2fa_locked_until DATETIME,
                tc_number VARCHAR(20),
                last_password_change DATETIME,
                force_password_change BOOLEAN,
                force_tutorial BOOLEAN,
                first_login_completed BOOLEAN,
                last_login DATETIME,
                terms_accepted BOOLEAN,
                updated_at DATETIME
            )
        """)
        print("   ✅ envanter_users tablosu oluşturuldu")
        
        # 4. count_sessions tablosu - with all columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS count_sessions (
                id SERIAL PRIMARY KEY,
                session_name VARCHAR(255),
                session_password VARCHAR(255),
                created_by INTEGER,
                is_active BOOLEAN,
                created_at DATETIME,
                started_at DATETIME,
                ended_at DATETIME,
                description TEXT,
                total_expected INTEGER,
                total_scanned INTEGER,
                report_file_path TEXT
            )
        """)
        print("   ✅ count_sessions tablosu oluşturuldu")
        
        # 5. scanned_qr tablosu - with all columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scanned_qr (
                id SERIAL PRIMARY KEY,
                session_id INTEGER,
                qr_id VARCHAR(255),
                part_code VARCHAR(255),
                scanned_by INTEGER,
                scanned_at DATETIME
            )
        """)
        print("   ✅ scanned_qr tablosu oluşturuldu")
        
        # 6. count_passwords tablosu - with all columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS count_passwords (
                id SERIAL PRIMARY KEY,
                session_id INTEGER,
                password VARCHAR(255),
                created_at DATETIME,
                created_by INTEGER
            )
        """)
        print("   ✅ count_passwords tablosu oluşturuldu")
        
        # Indexler ekle
        print("\n📇 Indexleri Oluşturuluyor...")
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_part_codes_part_code ON part_codes(part_code)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_qr_codes_qr_id ON qr_codes(qr_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_qr_codes_part_code_id ON qr_codes(part_code_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_envanter_users_username ON envanter_users(username)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_count_sessions_session_code ON count_sessions(session_code)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_count_sessions_created_by ON count_sessions(created_by)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_scanned_qr_qr_code_id ON scanned_qr(qr_code_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_scanned_qr_count_session_id ON scanned_qr(count_session_id)")
        
        print("   ✅ Indexler oluşturuldu")
        
        conn.commit()
        
        print("\n" + "="*60)
        print("✅ PostgreSQL TABLOLARI BAŞARIYLA OLUŞTURULDU!")
        print("="*60)
        print("\nSonraki Adım:")
        print("  python migrate_to_postgresql.py")
        print("\n" + "="*60)
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ PostgreSQL hatası: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Hata: {e}")
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
    
    success = create_tables()
    sys.exit(0 if success else 1)
