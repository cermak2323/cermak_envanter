#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parça Sipariş Sistemi - Veritabanı Kurulum Script'i
Mevcut envanter sistemine dokunmadan yeni tabloları oluşturur
"""

import pymysql
import sys

# Veritabanı bağlantı bilgileri
DB_CONFIG = {
    'host': '192.168.0.57',
    'port': 3306,
    'user': 'flaskuser',
    'password': 'FlaskSifre123!',
    'database': 'flaskdb',
    'charset': 'utf8mb4'
}

def create_order_system_tables():
    """Sipariş sistemi tablolarını oluşturur"""
    try:
        print("🔌 Veritabanına bağlanılıyor...")
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("✅ Bağlantı başarılı!")
        print("\n📦 Parça Sipariş Sistemi tabloları oluşturuluyor...\n")
        
        # 1. Sipariş Sistemi Stok Tablosu
        print("1️⃣ order_system_stock tablosu oluşturuluyor...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_system_stock (
                id INT AUTO_INCREMENT PRIMARY KEY,
                part_code VARCHAR(100) NOT NULL UNIQUE,
                part_name VARCHAR(255),
                stock_quantity INT DEFAULT 0,
                critical_stock_level INT DEFAULT 0,
                supplier VARCHAR(255),
                unit_price DECIMAL(10, 2) DEFAULT 0.00,
                currency VARCHAR(10) DEFAULT '€',
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_part_code (part_code),
                INDEX idx_critical_check (stock_quantity, critical_stock_level)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   ✅ order_system_stock oluşturuldu")
        
        # 2. Sipariş Listesi Tablosu
        print("2️⃣ order_list tablosu oluşturuluyor...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_list (
                id INT AUTO_INCREMENT PRIMARY KEY,
                part_code VARCHAR(100) NOT NULL,
                part_name VARCHAR(255),
                supplier VARCHAR(255),
                ordered_quantity INT NOT NULL,
                unit_price DECIMAL(10, 2) DEFAULT 0.00,
                total_price DECIMAL(10, 2) DEFAULT 0.00,
                currency VARCHAR(10) DEFAULT '€',
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status ENUM('Gelmedi', 'Geldi') DEFAULT 'Gelmedi',
                status_updated_date TIMESTAMP NULL,
                order_type ENUM('Otomatik', 'Manuel') DEFAULT 'Otomatik',
                created_by VARCHAR(100),
                notes TEXT,
                INDEX idx_part_code (part_code),
                INDEX idx_status (status),
                INDEX idx_order_date (order_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   ✅ order_list oluşturuldu")
        
        # 3. Korumalı Parçalar Tablosu
        print("3️⃣ protected_parts tablosu oluşturuluyor...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS protected_parts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                part_code VARCHAR(100) NOT NULL UNIQUE,
                order_id INT NOT NULL,
                protected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reason VARCHAR(255) DEFAULT 'Aktif siparişte - Gelmedi durumunda',
                INDEX idx_part_code (part_code)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   ✅ protected_parts oluşturuldu")
        
        # 4. Sipariş Geçmişi Log Tablosu
        print("4️⃣ order_history_log tablosu oluşturuluyor...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_history_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT,
                part_code VARCHAR(100),
                action VARCHAR(50),
                old_status VARCHAR(20),
                new_status VARCHAR(20),
                stock_before INT,
                stock_after INT,
                action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                action_by VARCHAR(100),
                notes TEXT,
                INDEX idx_order_id (order_id),
                INDEX idx_action_date (action_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   ✅ order_history_log oluşturuldu")
        
        conn.commit()
        print("\n🎉 Tüm tablolar başarıyla oluşturuldu!")
        
        # Tabloları kontrol et
        print("\n📊 Oluşturulan tablolar:")
        cursor.execute("SHOW TABLES")
        all_tables = cursor.fetchall()
        for table in all_tables:
            table_name = table[0]
            if table_name.startswith('order_') or table_name.startswith('protected_'):
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   📦 {table_name} - {count} kayıt")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Kurulum tamamlandı!")
        print("🚀 Artık app.py'de Parça Sipariş Sistemi modülünü ekleyebilirsiniz.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ HATA: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = create_order_system_tables()
    sys.exit(0 if success else 1)
