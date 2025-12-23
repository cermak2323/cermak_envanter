import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "instance" / "envanter_local.db"
DB_PATH.parent.mkdir(exist_ok=True)

# Şirket içi MySQL bağlantısı (Hardcoded)
HARDCODED_MYSQL_HOST = "192.168.0.57"
HARDCODED_MYSQL_USER = "flaskuser"
HARDCODED_MYSQL_PASSWORD = "FlaskSifre123!"
HARDCODED_MYSQL_DATABASE = "flaskdb"
HARDCODED_MYSQL_PORT = 3306

# MySQL bağlantı string'i
HARDCODED_DATABASE_URL = f"mysql+pymysql://{HARDCODED_MYSQL_USER}:{HARDCODED_MYSQL_PASSWORD}@{HARDCODED_MYSQL_HOST}:{HARDCODED_MYSQL_PORT}/{HARDCODED_MYSQL_DATABASE}"

# Şirket içi MySQL kullan
USE_MYSQL = True  # Her zaman MySQL kullan

if USE_MYSQL:
    # MySQL Bağlantısı
    MYSQL_URI = os.environ.get("DATABASE_URL", HARDCODED_DATABASE_URL)
    SQLALCHEMY_DATABASE_URI = MYSQL_URI
    print(f"[DB] Şirket içi MySQL kullanılacak ({HARDCODED_MYSQL_HOST})")

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # MySQL ve SQLite için optimize ayarlar
    if USE_MYSQL:
        # MySQL bağlantı pool ayarları
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": 10,                    # Şirket içi sunucu - daha fazla bağlantı
            "max_overflow": 20,
            "pool_pre_ping": True,              # Bağlantı sağlığı kontrolü
            "pool_recycle": 3600,               # Her saatte yenile
            "connect_args": {
                "connect_timeout": 10
            }
        }
    else:
        # SQLite bağlantı ayarları
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": 20,
            "max_overflow": 30,
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "pool_timeout": 30,
            "connect_args": {
                "timeout": 20,
                "check_same_thread": False,
                "cached_statements": 100
            }
        }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = 86400

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = 86400
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

ENVIRONMENT = os.environ.get("FLASK_ENV", "development")
config = ProductionConfig() if ENVIRONMENT == "production" else DevelopmentConfig()

print(f"[DB] Lokal SQLite: {DB_PATH}")
print(f"[CONFIG] Ortam: {ENVIRONMENT}")
