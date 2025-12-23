#!/usr/bin/env python
"""
Veritabanı Tabloları Oluştur
Lokal SQLite veya Production PostgreSQL için
"""

import os
import sys
from pathlib import Path

# Proje dizinini path'e ekle
sys.path.insert(0, str(Path(__file__).parent))

# Flask uygulamasını yapılandır
os.environ.setdefault('FLASK_ENV', 'development')

from models import db, PartCode, QRCode, CountSession, ScannedQR, User, CountPassword
from db_config import DevelopmentConfig, ProductionConfig

# Flask uygulaması oluştur (app.py'yi import etmiyoruz, kendi oluşturuyoruz)
from flask import Flask

app = Flask(__name__)

# Development konfigürasyonu kullan
print("💻 Development (Lokal) konfigürasyonu kullanılıyor...")
app.config.from_object(DevelopmentConfig)

# SQLAlchemy'yi app'e bağla
db.init_app(app)

def create_tables():
    """Veritabanı tablolarını oluştur"""
    with app.app_context():
        print("🔨 Veritabanı tabloları oluşturuluyor...")
        print(f"📍 Environment: {os.environ.get('FLASK_ENV', 'development')}")
        print(f"💾 Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'unknown')[:50]}...")
        
        try:
            db.create_all()
            print("✅ Tüm tablolar başarıyla oluşturuldu!")
            
            # Tablolar hakkında bilgi ver
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n📋 Oluşturulan Tablolar ({len(tables)}):")
            for table in sorted(tables):
                columns = inspector.get_columns(table)
                print(f"  ├─ {table} ({len(columns)} kolon)")
                if len(columns) <= 5:
                    for col in columns:
                        print(f"  │  ├─ {col['name']}: {col['type']}")
                else:
                    for col in columns[:3]:
                        print(f"  │  ├─ {col['name']}: {col['type']}")
                    print(f"  │  ├─ ... (+{len(columns)-3} kolon)")
            
            print("\n✨ Başarılı!")
            return True
            
        except Exception as e:
            print(f"❌ Hata: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = create_tables()
    sys.exit(0 if success else 1)