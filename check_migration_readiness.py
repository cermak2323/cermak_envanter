#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-Migration Checklist
PostgreSQL'e geçişten ÖNCE tüm kontrolleri yap
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

print("""
╔══════════════════════════════════════════════════════════════╗
║         PostgreSQL Geçiş - Pre-Migration Checklist           ║
║              Hazırlık Denetim Listesi                        ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_sqlite_database():
    """SQLite veritabanı kontrolü"""
    print("\n1️⃣  SQLite Veritabanı Kontrolü:")
    print("-" * 60)
    
    db_path = Path("instance/envanter_local.db")
    
    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f"   ✅ SQLite DB bulunamaya: {db_path}")
        print(f"      Dosya Boyutu: {size_mb:.2f} MB")
        return True
    else:
        print(f"   ❌ SQLite DB bulunamadı: {db_path}")
        return False

def check_backup():
    """Yedek kontrolü"""
    print("\n2️⃣  Yedek Kontrolü:")
    print("-" * 60)
    
    backup_dir = Path("FULL_BACKUP_20251123_141034")
    
    if backup_dir.exists():
        backup_db = backup_dir / "instance" / "envanter_local.db"
        if backup_db.exists():
            size_mb = backup_db.stat().st_size / (1024 * 1024)
            print(f"   ✅ Yedek dizini bulundu: {backup_dir}")
            print(f"      Yedek DB Boyutu: {size_mb:.2f} MB")
            return True
        else:
            print(f"   ⚠️  Yedek dizini var ama DB bulunamadı")
            return False
    else:
        print(f"   ❌ Yedek dizini bulunamadı: {backup_dir}")
        print(f"      Oluşturulması şu komutla mümkün:")
        print(f"      Copy-Item -Recurse . 'FULL_BACKUP_20251123_141034'")
        return False

def check_env_file():
    """ENV dosyası kontrolü"""
    print("\n3️⃣  .env Dosyası Kontrolü:")
    print("-" * 60)
    
    env_path = Path(".env")
    
    if env_path.exists():
        print(f"   ✅ .env dosyası bulundu")
        
        load_dotenv()
        
        # PostgreSQL URI kontrolü
        db_uri = os.environ.get("DATABASE_URL")
        if db_uri and "postgresql" in db_uri:
            print(f"   ✅ DATABASE_URL yapılandırılmış")
            print(f"      URI: {db_uri[:50]}...***")
        else:
            print(f"   ⚠️  DATABASE_URL PostgreSQL değil veya boş")
            return False
        
        # USE_POSTGRESQL kontrolü
        use_pg = os.environ.get("USE_POSTGRESQL", "False").lower()
        if use_pg == "true":
            print(f"   ⚠️  USE_POSTGRESQL=True (HENÜZ etkinleştirilmemelidir!)")
            print(f"      İpucu: Veri geçişinden SONRA ayarla")
        else:
            print(f"   ✅ USE_POSTGRESQL=False (Doğru, henüz SQLite'de)")
        
        return True
    else:
        print(f"   ❌ .env dosyası bulunamadı")
        return False

def check_migration_scripts():
    """Geçiş betiği kontrolü"""
    print("\n4️⃣  Geçiş Betikleri Kontrolü:")
    print("-" * 60)
    
    scripts = [
        ("migrate_to_postgresql.py", "Veri Geçişi"),
        ("verify_postgresql_data.py", "Veri Doğrulama"),
    ]
    
    all_exist = True
    for script, purpose in scripts:
        script_path = Path(script)
        if script_path.exists():
            print(f"   ✅ {script:30s} ({purpose})")
        else:
            print(f"   ❌ {script:30s} BULUNAMADI")
            all_exist = False
    
    return all_exist

def check_app_files():
    """Ana uygulama dosyaları kontrolü"""
    print("\n5️⃣  Uygulama Dosyaları Kontrolü:")
    print("-" * 60)
    
    files = [
        ("app.py", "Ana Uygulama"),
        ("models.py", "ORM Modelleri"),
        ("db_config.py", "Veritabanı Konfigürasyonu"),
    ]
    
    all_exist = True
    for file, purpose in files:
        file_path = Path(file)
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            print(f"   ✅ {file:20s} ({purpose:20s}) {size_kb:6.1f} KB")
        else:
            print(f"   ❌ {file:20s} BULUNAMADI")
            all_exist = False
    
    return all_exist

def check_python_packages():
    """Gerekli Python paketleri kontrolü"""
    print("\n6️⃣  Python Paketleri Kontrolü:")
    print("-" * 60)
    
    packages = {
        "flask": "Flask Web Framework",
        "flask_sqlalchemy": "SQLAlchemy ORM",
        "psycopg2": "PostgreSQL Driver",
        "python-dotenv": "Environment Variables",
    }
    
    all_installed = True
    for package, purpose in packages.items():
        try:
            __import__(package.replace("-", "_"))
            print(f"   ✅ {package:20s} ({purpose})")
        except ImportError:
            print(f"   ❌ {package:20s} YÜKLENMEMIŞ!")
            print(f"      Yükle: pip install {package}")
            all_installed = False
    
    return all_installed

def check_neon_connection():
    """Neon bağlantısı kontrolü"""
    print("\n7️⃣  Neon PostgreSQL Bağlantısı Kontrolü:")
    print("-" * 60)
    
    try:
        import psycopg2
        
        load_dotenv()
        db_uri = os.environ.get("DATABASE_URL")
        
        if not db_uri:
            # Use unpooled endpoint
            db_uri = "postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require"
        
        try:
            conn = psycopg2.connect(db_uri)
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            
            print(f"   ✅ Neon PostgreSQL bağlantısı başarılı")
            print(f"      {version.split(',')[0]}")
            
            # Tabloları kontrol et
            cursor.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            tables = cursor.fetchall()
            
            if tables:
                print(f"   ⚠️  {len(tables)} tablo zaten var (yeniden oluşturulacak)")
            else:
                print(f"   ✅ Veritabanı boş (temiz geçiş)")
            
            conn.close()
            return True
        except Exception as e:
            print(f"   ❌ Bağlantı hatası: {e}")
            print(f"      Neon credentials kontrol et")
            return False
    
    except ImportError:
        print(f"   ⚠️  psycopg2 yüklü değil (daha sonra kullanılacak)")
        return True

def check_disk_space():
    """Disk alanı kontrolü"""
    print("\n8️⃣  Disk Alanı Kontrolü:")
    print("-" * 60)
    
    try:
        import shutil
        
        total, used, free = shutil.disk_usage("/")
        free_gb = free / (1024**3)
        
        if free_gb > 1:
            print(f"   ✅ Yeterli disk alanı: {free_gb:.2f} GB")
            return True
        else:
            print(f"   ⚠️  Düşük disk alanı: {free_gb:.2f} GB")
            return False
    except Exception as e:
        print(f"   ⚠️  Disk alanı kontrol edilemedi: {e}")
        return True

def main():
    """Ana kontrol fonksiyonu"""
    
    checks = [
        ("SQLite Veritabanı", check_sqlite_database),
        ("Sistem Yedeklemesi", check_backup),
        (".env Yapılandırması", check_env_file),
        ("Geçiş Betikleri", check_migration_scripts),
        ("Uygulama Dosyaları", check_app_files),
        ("Python Paketleri", check_python_packages),
        ("Neon Bağlantısı", check_neon_connection),
        ("Disk Alanı", check_disk_space),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} kontrolü başarısız: {e}")
            results.append((name, False))
    
    # Özet
    print("\n" + "="*60)
    print("📋 KONTROL ÖZETI:")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print("="*60)
    
    if passed == total:
        print(f"\n✅ TÜM KONTROLLER BAŞARILI ({passed}/{total})")
        print(f"   Geçişe HAZIRSIZ!")
        print(f"\n📝 Sonraki Adım: python migrate_to_postgresql.py")
        return 0
    elif passed >= total - 2:
        print(f"\n⚠️  {total - passed} KONTROL BAŞARIŞIZ ({passed}/{total})")
        print(f"   Bazı uyarılar var ama geçişe devam edebilirsiniz")
        print(f"\n📝 Eğer eminseniz: python migrate_to_postgresql.py")
        return 1
    else:
        print(f"\n❌ KRİTİK HATALAR ({total - passed}/{total})")
        print(f"   Lütfen yukarıdaki sorunları düzeltin")
        return 2

if __name__ == "__main__":
    sys.exit(main())
