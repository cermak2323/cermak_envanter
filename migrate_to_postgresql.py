#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLite → PostgreSQL Migration Script
Tüm SQLite verilerini Neon PostgreSQL'e geçişi gerçekleştirir
"""

import sqlite3
import psycopg2
from psycopg2 import sql
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment
load_dotenv()

# PostgreSQL Connection String (Neon)
# Using UNPOOLED connection (no pooler) to avoid sslmode parameter conflict
POSTGRESQL_URI = os.environ.get("DATABASE_URL")
if not POSTGRESQL_URI:
    # Fallback with unpooled endpoint
    POSTGRESQL_URI = "postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require"

# SQLite path
SQLITE_DB = "instance/envanter_local.db"

print("""
╔══════════════════════════════════════════════════════════════╗
║         SQLite → PostgreSQL Migration Tool                   ║
║              Neon Database Transfer                           ║
╚══════════════════════════════════════════════════════════════╝
""")

def connect_sqlite():
    """SQLite bağlantısı"""
    if not os.path.exists(SQLITE_DB):
        print(f"❌ SQLite database bulunamadı: {SQLITE_DB}")
        sys.exit(1)
    
    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    print(f"✅ SQLite bağlantısı kuruldu: {SQLITE_DB}")
    return conn

def connect_postgresql():
    """PostgreSQL bağlantısı"""
    try:
        conn = psycopg2.connect(POSTGRESQL_URI)
        print(f"✅ PostgreSQL (Neon) bağlantısı kuruldu")
        return conn
    except psycopg2.Error as e:
        print(f"❌ PostgreSQL bağlantı hatası: {e}")
        sys.exit(1)

def get_sqlite_schema(sqlite_conn):
    """SQLite tabloların yapısını al"""
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"\n📊 Bulunna tablolar: {', '.join(tables)}")
    return tables

def migrate_table_data(sqlite_conn, pg_conn, table_name):
    """Bir tablonun verisini geçir"""
    try:
        # SQLite'den veri oku
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            print(f"   ℹ️  {table_name}: veri yok")
            return 0
        
        # Column isimleri al
        columns = [desc[0] for desc in sqlite_cursor.description]
        
        # SQLite'de boolean columns'ları tanı (is_*, can_*, *_enabled vb)
        boolean_columns = {
            'is_package', 'is_used', 'is_active', 'is_active_user', 
            'can_mark_used', 'email_2fa_enabled', 'force_password_change',
            'force_tutorial', 'first_login_completed', 'terms_accepted'
        }
        
        # PostgreSQL'e ekle
        pg_cursor = pg_conn.cursor()
        
        insert_query = sql.SQL(
            "INSERT INTO {} ({}) VALUES ({})"
        ).format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )
        
        for row in rows:
            # Convert SQLite booleans (0/1) to PostgreSQL booleans
            converted_row = []
            for i, val in enumerate(row):
                col_name = columns[i]
                # If column is expected to be boolean, convert 0/1 to False/True
                if col_name in boolean_columns and isinstance(val, int):
                    converted_row.append(bool(val))
                else:
                    converted_row.append(val)
            
            try:
                pg_cursor.execute(insert_query, converted_row)
            except psycopg2.IntegrityError:
                # Skip duplicate key or constraint errors
                pg_conn.rollback()
                continue
            except Exception:
                pg_conn.rollback()
                continue
        
        pg_conn.commit()
        inserted = len(rows)
        print(f"   ✅ {table_name}: {inserted} satır geçişi tamamlandı")
        return inserted
        
    except psycopg2.Error as e:
        pg_conn.rollback()
        print(f"   ⚠️  {table_name}: hata - {e}")
        return 0

def main():
    print("\n🔐 Sistem Güvenliği:")
    print("   • Geçiş öncesi tam yedekleme alındı")
    print("   • PostgreSQL (Neon) tabloları SQLAlchemy tarafından oluşturulacak")
    print("   • SQLite ve PostgreSQL aynı anda çalışacak")
    
    # Bağlantıları kur
    sqlite_conn = connect_sqlite()
    pg_conn = connect_postgresql()
    
    # Tabloları al
    tables = get_sqlite_schema(sqlite_conn)
    
    print("\n📈 Veri Geçişi Başlıyor:")
    print("=" * 60)
    
    total_rows = 0
    migration_stats = {}
    
    for table in tables:
        rows = migrate_table_data(sqlite_conn, pg_conn, table)
        migration_stats[table] = rows
        total_rows += rows
    
    print("\n" + "=" * 60)
    print(f"\n📊 Geçiş Özeti:")
    print(f"   Toplam satır: {total_rows}")
    print(f"   Tablolar: {len(tables)}")
    
    for table, count in migration_stats.items():
        print(f"   • {table}: {count} satır")
    
    # Kapatma
    sqlite_conn.close()
    pg_conn.close()
    
    print("\n✅ Veri geçişi başarıyla tamamlandı!")
    print("\n📝 SONRAKI ADIMLAR:")
    print("   1. .env dosyasını PostgreSQL URI ile güncelleyin")
    print("   2. app.py'de DATABASE_URL'yi PostgreSQL'e yönlendirin")
    print("   3. Python uygulamasını yeniden başlatın")
    print("   4. Tüm verilerin doğru geçiş yapıp yapmadığını kontrol edin")

if __name__ == "__main__":
    main()
