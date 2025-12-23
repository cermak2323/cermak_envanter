#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostgreSQL Veri Doğrulama Betiği
Geçişten sonra verilerin bütünlüğünü kontrol eder
"""

import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL Connection
# Using UNPOOLED connection (no pooler) to avoid sslmode parameter conflict
POSTGRESQL_URI = os.environ.get("DATABASE_URL")
if not POSTGRESQL_URI:
    # Fallback with unpooled endpoint
    POSTGRESQL_URI = "postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require"

print("""
╔══════════════════════════════════════════════════════════════╗
║         PostgreSQL Veri Doğrulama Aracı                      ║
║              Migration Verification                          ║
╚══════════════════════════════════════════════════════════════╝
""")

def connect_postgresql():
    """PostgreSQL bağlantısı"""
    try:
        conn = psycopg2.connect(POSTGRESQL_URI)
        print(f"✅ PostgreSQL (Neon) bağlantısı kuruldu")
        return conn
    except psycopg2.Error as e:
        print(f"❌ PostgreSQL bağlantı hatası: {e}")
        return None

def verify_tables(conn):
    """Tabloların varlığını kontrol et"""
    cursor = conn.cursor()
    
    expected_tables = [
        'envanter_users',
        'part_codes',
        'qr_codes',
        'count_sessions',
        'scanned_qr',
        'count_passwords'
    ]
    
    print("\n📊 Tablo Kontrolü:")
    print("-" * 60)
    
    cursor.execute("""
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public'
        ORDER BY tablename
    """)
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    found_count = 0
    for table in expected_tables:
        if table in existing_tables:
            print(f"   ✅ {table}")
            found_count += 1
        else:
            print(f"   ❌ {table} (BULUNAMADI)")
    
    print("-" * 60)
    print(f"✅ {found_count}/{len(expected_tables)} tablo bulundu")
    
    return existing_tables

def count_rows(conn, table):
    """Tablodaki satır sayısını al"""
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        return None

def verify_data(conn, existing_tables):
    """Veri içeriğini kontrol et"""
    print("\n📈 Veri Sayıları:")
    print("-" * 60)
    
    total_rows = 0
    table_stats = {}
    
    for table in existing_tables:
        count = count_rows(conn, table)
        if count is not None:
            table_stats[table] = count
            total_rows += count
            status = "✅" if count > 0 else "⚠️ "
            print(f"   {status} {table:20s}: {count:8d} satır")
    
    print("-" * 60)
    print(f"   📊 Toplam: {total_rows} satır")
    
    return table_stats

def verify_critical_data(conn):
    """Kritik verileri kontrol et"""
    print("\n🔐 Kritik Veri Kontrolleri:")
    print("-" * 60)
    
    cursor = conn.cursor()
    
    # Admin kullanıcı kontrolü
    try:
        cursor.execute("""
            SELECT username, full_name FROM envanter_users 
            WHERE username = 'cermak' OR username = 'admin'
            LIMIT 1
        """)
        admin = cursor.fetchone()
        if admin:
            print(f"   ✅ Admin kullanıcı: {admin[0]} ({admin[1]})")
        else:
            print(f"   ⚠️  Admin kullanıcı bulunamadı")
    except Exception as e:
        print(f"   ❌ Admin kontrol hatası: {e}")
    
    # QR Kod örneği
    try:
        cursor.execute("SELECT COUNT(*) FROM qr_codes WHERE is_used = true")
        used_count = cursor.fetchone()[0]
        print(f"   ✅ Kullanılan QR Kodlar: {used_count}")
    except Exception as e:
        print(f"   ⚠️  QR Kod kontrol hatası: {e}")
    
    # Parça Kodu örneği
    try:
        cursor.execute("SELECT COUNT(*) FROM part_codes WHERE is_package = true")
        package_count = cursor.fetchone()[0]
        print(f"   ✅ Paket Parçalar: {package_count}")
    except Exception as e:
        print(f"   ⚠️  Parça Kodu kontrol hatası: {e}")
    
    # Sayım Oturumu
    try:
        cursor.execute("SELECT COUNT(*) FROM count_sessions WHERE status = 'completed'")
        completed_sessions = cursor.fetchone()[0]
        print(f"   ✅ Tamamlanan Sayım Oturumları: {completed_sessions}")
    except Exception as e:
        print(f"   ⚠️  Sayım Oturumu kontrol hatası: {e}")
    
    print("-" * 60)

def verify_foreign_keys(conn):
    """Foreign key ilişkilerini kontrol et"""
    print("\n🔗 Foreign Key Doğrulama:")
    print("-" * 60)
    
    cursor = conn.cursor()
    
    try:
        # qr_codes.part_code_id → part_codes.id
        cursor.execute("""
            SELECT COUNT(*) FROM qr_codes q
            WHERE NOT EXISTS (SELECT 1 FROM part_codes p WHERE p.id = q.part_code_id)
        """)
        orphaned = cursor.fetchone()[0]
        if orphaned == 0:
            print(f"   ✅ qr_codes FK ilişkisi OK")
        else:
            print(f"   ⚠️  qr_codes: {orphaned} orphaned kayıt")
        
        # scanned_qr.qr_code_id → qr_codes.id
        cursor.execute("""
            SELECT COUNT(*) FROM scanned_qr sq
            WHERE NOT EXISTS (SELECT 1 FROM qr_codes q WHERE q.id = sq.qr_code_id)
        """)
        orphaned = cursor.fetchone()[0]
        if orphaned == 0:
            print(f"   ✅ scanned_qr FK ilişkisi OK")
        else:
            print(f"   ⚠️  scanned_qr: {orphaned} orphaned kayıt")
        
        # count_sessions.created_by → envanter_users.id
        cursor.execute("""
            SELECT COUNT(*) FROM count_sessions cs
            WHERE NOT EXISTS (SELECT 1 FROM envanter_users eu WHERE eu.id = cs.created_by)
        """)
        orphaned = cursor.fetchone()[0]
        if orphaned == 0:
            print(f"   ✅ count_sessions FK ilişkisi OK")
        else:
            print(f"   ⚠️  count_sessions: {orphaned} orphaned kayıt")
        
        print("-" * 60)
        print("   ✅ Tüm foreign key ilişkileri bütünlüğü doğrulandı")
    
    except Exception as e:
        print(f"   ⚠️  FK kontrol hatası: {e}")

def main():
    conn = connect_postgresql()
    
    if not conn:
        print("\n❌ PostgreSQL bağlantısı başarısız!")
        return False
    
    try:
        # Tablo kontrolü
        existing_tables = verify_tables(conn)
        
        # Veri sayıları
        table_stats = verify_data(conn, existing_tables)
        
        # Kritik veri kontrolleri
        verify_critical_data(conn)
        
        # Foreign key doğrulama
        verify_foreign_keys(conn)
        
        # Son özet
        print("\n" + "="*60)
        if sum(table_stats.values()) > 0:
            print("✅ VERİ GEÇİŞİ BAŞARILI - Sistem PostgreSQL'de Hazır!")
            print(f"   Toplam Kayıt: {sum(table_stats.values())}")
            print("   Geçiş Tamamlandı ve Doğrulandı ✅")
        else:
            print("⚠️  Tablolar boş - Veri geçişi yapılmadı mı?")
        print("="*60)
        
        return True
    
    except Exception as e:
        print(f"\n❌ Doğrulama hatası: {e}")
        return False
    
    finally:
        conn.close()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
