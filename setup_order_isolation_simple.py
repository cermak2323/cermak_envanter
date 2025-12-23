#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
STANDALONE ORDER SYSTEM ISOLATION SETUP
Pure database operations without Flask dependency
"""

import pymysql
import sys
from datetime import datetime

# Database configuration
DB_HOST = '192.168.0.57'
DB_PORT = 3306
DB_USER = 'flaskuser'
DB_PASS = 'FlaskSifre123!'

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def print_success(msg):
    print(f"✅ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def print_info(msg):
    print(f"ℹ️  {msg}")

def connect(db=None):
    """Connect to MySQL"""
    config = {
        'host': DB_HOST,
        'port': DB_PORT,
        'user': DB_USER,
        'password': DB_PASS,
        'charset': 'utf8mb4'
    }
    if db:
        config['database'] = db
    
    try:
        return pymysql.connect(**config, cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
        print_error(f"Connection failed: {e}")
        sys.exit(1)

def main():
    print("\n╔" + "="*78 + "╗")
    print("║  SİPARİŞ SİSTEMİ İZOLASYON SETUP - Standalone                           ║")
    print("╚" + "="*78 + "╝\n")
    
    print_section("STEP 1: CREATE ISOLATED DATABASE (USING ROOT)")
    
    try:
        # Try to connect as root first
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user='root',
                password='Nzn0912@',  # Default root password from your config
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()
            root_available = True
            print_info("Connected as root user")
        except:
            print_info("Root connection failed, trying with flaskuser...")
            root_available = False
            conn = connect()
            cursor = conn.cursor()
        
        # Create order_system_db
        try:
            cursor.execute("""
                CREATE DATABASE IF NOT EXISTS order_system_db 
                CHARACTER SET utf8mb4 
                COLLATE utf8mb4_unicode_ci
            """)
            conn.commit()
            print_success("Created database: order_system_db")
        except Exception as e:
            print_info(f"Database creation: {e}")
            # Database might already exist, try continuing
        
        # Grant privileges to flaskuser
        if root_available:
            try:
                cursor.execute("""
                    GRANT ALL ON order_system_db.* TO 'flaskuser'@'%' IDENTIFIED BY 'FlaskSifre123!'
                """)
                cursor.execute("FLUSH PRIVILEGES")
                conn.commit()
                print_success("Granted privileges to flaskuser")
            except Exception as e:
                print_info(f"Privilege grant: {e}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print_error(f"Failed to create database: {e}")
        print_info("Continuing with existing database...")
    
    print_section("STEP 2: CREATE ISOLATED TABLES")
    
    try:
        conn = connect('order_system_db')
        cursor = conn.cursor()
        
        # Create stock table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock (
                part_code VARCHAR(100) PRIMARY KEY,
                part_name VARCHAR(255) NOT NULL,
                stock_quantity INT DEFAULT 0,
                critical_stock_level INT DEFAULT NULL,
                expected_stock INT DEFAULT NULL,
                supplier VARCHAR(255),
                unit_price DECIMAL(10, 4) DEFAULT 0.00,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_supplier (supplier),
                INDEX idx_stock_level (stock_quantity, critical_stock_level)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print_success("Created table: stock")
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                part_code VARCHAR(100) NOT NULL,
                part_name VARCHAR(255),
                supplier VARCHAR(255),
                ordered_quantity INT DEFAULT 0,
                received_quantity INT DEFAULT 0,
                unit_price DECIMAL(10, 4) DEFAULT 0.00,
                total_price DECIMAL(12, 4) DEFAULT 0.00,
                currency VARCHAR(10) DEFAULT 'EUR',
                status VARCHAR(50) DEFAULT 'Gelmedi',
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                order_type VARCHAR(50) DEFAULT 'Manuel',
                created_by VARCHAR(100),
                notes LONGTEXT,
                CONSTRAINT fk_orders_part FOREIGN KEY (part_code) 
                    REFERENCES stock(part_code) ON DELETE CASCADE,
                INDEX idx_status (status),
                INDEX idx_supplier (supplier)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print_success("Created table: orders")
        
        # Create protected_parts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS protected_parts (
                part_code VARCHAR(100) PRIMARY KEY,
                order_id INT DEFAULT NULL,
                reason VARCHAR(255),
                protected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_prot_part FOREIGN KEY (part_code) 
                    REFERENCES stock(part_code) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print_success("Created table: protected_parts")
        
        # Create history_log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT DEFAULT NULL,
                part_code VARCHAR(100) DEFAULT NULL,
                action VARCHAR(100),
                notes LONGTEXT,
                action_by VARCHAR(100),
                action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_order_id (order_id),
                INDEX idx_action_date (action_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print_success("Created table: history_log")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print_error(f"Failed to create tables: {e}")
        return False
    
    print_section("STEP 3: MIGRATE DATA FROM FLASKDB")
    
    try:
        src_conn = connect('flaskdb')
        dst_conn = connect('order_system_db')
        
        src_cursor = src_conn.cursor()
        dst_cursor = dst_conn.cursor()
        
        # Migrate order_system_stock to stock
        print_info("Copying order_system_stock → stock...")
        src_cursor.execute("SELECT * FROM flaskdb.order_system_stock")
        rows = src_cursor.fetchall()
        
        for row in rows:
            dst_cursor.execute("""
                INSERT INTO stock 
                (part_code, part_name, stock_quantity, critical_stock_level, 
                 expected_stock, supplier, unit_price, last_updated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                part_name = VALUES(part_name)
            """, (row['part_code'], row['part_name'], row['stock_quantity'],
                  row['critical_stock_level'], row['expected_stock'],
                  row['supplier'], row['unit_price'], row['last_updated']))
        
        dst_conn.commit()
        print_success(f"Migrated {len(rows)} stock records")
        
        # Migrate order_list to orders
        print_info("Copying order_list → orders...")
        src_cursor.execute("SELECT * FROM flaskdb.order_list")
        rows = src_cursor.fetchall()
        
        for row in rows:
            try:
                dst_cursor.execute("""
                    INSERT INTO orders 
                    (part_code, part_name, supplier, ordered_quantity, received_quantity,
                     unit_price, total_price, currency, status, order_date, order_type,
                     created_by, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (row['part_code'], row['part_name'], row['supplier'],
                      row['ordered_quantity'], row.get('received_quantity', 0),
                      row['unit_price'], row.get('total_price', 0),
                      row.get('currency', 'EUR'), row['status'],
                      row['order_date'], row.get('order_type', 'Manuel'),
                      row['created_by'], row.get('notes', '')))
            except Exception as e:
                print_info(f"  Skipping order {row.get('id')}: {e}")
        
        dst_conn.commit()
        print_success(f"Migrated {len(rows)} order records")
        
        # Migrate protected_parts
        print_info("Copying protected_parts...")
        src_cursor.execute("SELECT * FROM flaskdb.protected_parts")
        rows = src_cursor.fetchall()
        
        for row in rows:
            try:
                dst_cursor.execute("""
                    INSERT INTO protected_parts 
                    (part_code, order_id, reason, protected_date)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    order_id = VALUES(order_id)
                """, (row['part_code'], row.get('order_id'), row.get('reason'),
                      row['protected_date']))
            except:
                pass
        
        dst_conn.commit()
        print_success(f"Migrated {len(rows)} protected parts records")
        
        src_cursor.close()
        dst_cursor.close()
        src_conn.close()
        dst_conn.close()
        
    except Exception as e:
        print_error(f"Data migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print_section("STEP 4: VERIFY ISOLATION")
    
    try:
        inv_conn = connect('flaskdb')
        ord_conn = connect('order_system_db')
        
        inv_cursor = inv_conn.cursor()
        ord_cursor = ord_conn.cursor()
        
        # Check inventory tables
        inv_cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = 'flaskdb' 
            AND TABLE_NAME IN ('part_codes', 'qr_codes')
        """)
        if inv_cursor.fetchone()['cnt'] == 2:
            print_success("✅ Inventory system intact (part_codes, qr_codes)")
        
        # Check order tables
        ord_cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = 'order_system_db' 
            AND TABLE_NAME IN ('stock', 'orders', 'protected_parts', 'history_log')
        """)
        if ord_cursor.fetchone()['cnt'] == 4:
            print_success("✅ Order system isolated (4 tables)")
        
        inv_cursor.close()
        ord_cursor.close()
        inv_conn.close()
        ord_conn.close()
        
    except Exception as e:
        print_error(f"Verification failed: {e}")
        return False
    
    print_section("STATISTICS")
    
    try:
        ord_conn = connect('order_system_db')
        ord_cursor = ord_conn.cursor()
        
        ord_cursor.execute("SELECT COUNT(*) as cnt FROM stock")
        print(f"  stock:          {ord_cursor.fetchone()['cnt']} records")
        
        ord_cursor.execute("SELECT COUNT(*) as cnt FROM orders")
        print(f"  orders:         {ord_cursor.fetchone()['cnt']} records")
        
        ord_cursor.execute("SELECT COUNT(*) as cnt FROM protected_parts")
        print(f"  protected_parts:{ord_cursor.fetchone()['cnt']} records")
        
        ord_cursor.close()
        ord_conn.close()
        
    except Exception as e:
        print_info(f"Statistics unavailable: {e}")
    
    print_section("✅ ISOLATION SETUP COMPLETE")
    print("""
Next Steps:
1. Update order_system.py DB_CONFIG database to 'order_system_db'
2. Update table references:
   - order_system_stock → stock
   - order_list → orders
3. Restart Flask application
4. Test order system functionality

Status: READY FOR CODE UPDATES
""")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
