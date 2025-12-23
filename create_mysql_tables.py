import pymysql

conn = pymysql.connect(
    host='192.168.0.57',
    user='flaskuser',
    password='FlaskSifre123!',
    database='flaskdb',
    port=3306,
    charset='utf8mb4'
)

cursor = conn.cursor()

# Tabloları oluştur
tables = [
    """
    CREATE TABLE IF NOT EXISTS envanter_users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        full_name VARCHAR(255),
        role VARCHAR(50) DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS qr_codes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        qr_code VARCHAR(255) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS part_codes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        qr_code_id INT,
        part_number VARCHAR(255) NOT NULL,
        quantity INT DEFAULT 1,
        photo_path VARCHAR(500),
        catalog_image VARCHAR(500),
        description TEXT,
        used_in_machines TEXT,
        specifications TEXT,
        stock_location VARCHAR(255),
        supplier VARCHAR(255),
        unit_price DECIMAL(10,2),
        critical_stock_level INT,
        notes TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        updated_by INT,
        FOREIGN KEY (qr_code_id) REFERENCES qr_codes(id) ON DELETE CASCADE,
        FOREIGN KEY (updated_by) REFERENCES envanter_users(id) ON DELETE SET NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS scanned_qr (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_id INT,
        qr_code VARCHAR(255) NOT NULL,
        scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        part_number VARCHAR(255),
        quantity INT DEFAULT 1
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS count_sessions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_name VARCHAR(255) NOT NULL,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        finished_at TIMESTAMP NULL,
        started_by INT,
        finished_by INT,
        total_expected INT DEFAULT 0,
        total_scanned INT DEFAULT 0,
        report_file_path VARCHAR(500),
        FOREIGN KEY (started_by) REFERENCES envanter_users(id) ON DELETE SET NULL,
        FOREIGN KEY (finished_by) REFERENCES envanter_users(id) ON DELETE SET NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS count_passwords (
        id INT AUTO_INCREMENT PRIMARY KEY,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
]

for i, table_sql in enumerate(tables, 1):
    try:
        cursor.execute(table_sql)
        print(f"✅ Tablo {i} oluşturuldu")
    except Exception as e:
        print(f"❌ Tablo {i} hatası: {e}")

# Admin kullanıcısı ekle
from werkzeug.security import generate_password_hash

admin_hash = generate_password_hash("@R9t$L7e!xP2w")
try:
    cursor.execute("""
        INSERT INTO envanter_users (username, password_hash, full_name, role)
        VALUES ('admin', %s, 'Admin', 'admin')
    """, (admin_hash,))
    print("✅ Admin kullanıcısı oluşturuldu")
except Exception as e:
    print(f"ℹ️ Admin kullanıcısı zaten var veya hata: {e}")

conn.commit()
conn.close()

print("\n✅ Veritabanı hazır!")
