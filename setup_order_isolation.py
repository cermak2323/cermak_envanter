#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SİPARİŞ SİSTEMİ İZOLASYON SCRIPTI
ORDER SYSTEM ISOLATION SCRIPT

Amaç: Sipariş sistemini envanter sisteminden tamamen izole etme
Purpose: Complete isolation of order system from inventory system
"""

import pymysql
import sys
from datetime import datetime

# ============================================================================
# Database Configurations
# ============================================================================

INVENTORY_DB_CONFIG = {
    'host': '192.168.0.57',
    'port': 3306,
    'user': 'flaskuser',
    'password': 'FlaskSifre123!',
    'database': 'flaskdb',
    'charset': 'utf8mb4'
}

ORDER_DB_CONFIG = {
    'host': '192.168.0.57',
    'port': 3306,
    'user': 'flaskuser',
    'password': 'FlaskSifre123!',
    'database': 'order_system_db',
    'charset': 'utf8mb4'
}

# ============================================================================
# Utility Functions
# ============================================================================

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def get_connection(db_config):
    """Get database connection"""
    try:
        conn = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            charset=db_config['charset'],
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print_error(f"Database connection failed: {e}")
        sys.exit(1)

def execute_sql_file(db_config, sql_file):
    """Execute SQL file against database"""
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Connect to MySQL server (without specifying database first)
        conn = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            charset=db_config['charset']
        )
        cursor = conn.cursor()
        
        # Split SQL into individual statements
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        
        for statement in statements:
            # Skip comments
            if statement.startswith('--'):
                continue
            
            cursor.execute(statement)
            conn.commit()
        
        cursor.close()
        conn.close()
        
        print_success(f"SQL file executed: {sql_file}")
        return True
        
    except Exception as e:
        print_error(f"SQL file execution failed: {e}")
        return False

def check_databases_exist():
    """Check if both databases exist"""
    print_section("CHECKING DATABASES")
    
    try:
        conn = pymysql.connect(
            host='192.168.0.57',
            port=3306,
            user='flaskuser',
            password='FlaskSifre123!',
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        cursor.execute("SHOW DATABASES LIKE 'flaskdb'")
        if cursor.fetchone():
            print_success("flaskdb exists (Inventory System)")
        else:
            print_error("flaskdb NOT found")
            return False
        
        cursor.execute("SHOW DATABASES LIKE 'order_system_db'")
        if cursor.fetchone():
            print_success("order_system_db exists (Order System)")
        else:
            print_info("order_system_db not yet created (will be created)")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"Database check failed: {e}")
        return False

def create_isolated_database():
    """Create isolated order system database"""
    print_section("CREATING ISOLATED DATABASE")
    
    try:
        conn = pymysql.connect(
            host='192.168.0.57',
            port=3306,
            user='flaskuser',
            password='FlaskSifre123!',
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("""
            CREATE DATABASE IF NOT EXISTS order_system_db 
            CHARACTER SET utf8mb4 
            COLLATE utf8mb4_unicode_ci
        """)
        conn.commit()
        print_success("Database 'order_system_db' created")
        
        # Create tables
        cursor.execute("""
            USE order_system_db;
            
            -- Stock table
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
                INDEX idx_stock_level (stock_quantity, critical_stock_level),
                INDEX idx_expected (expected_stock),
                INDEX idx_updated (last_updated)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            
            -- Orders table
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
                CONSTRAINT fk_orders_part_code FOREIGN KEY (part_code) 
                    REFERENCES stock(part_code) 
                    ON DELETE CASCADE ON UPDATE CASCADE,
                INDEX idx_status (status),
                INDEX idx_supplier (supplier),
                INDEX idx_order_date (order_date),
                INDEX idx_part_code (part_code),
                INDEX idx_created_by (created_by)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            
            -- Protected parts table
            CREATE TABLE IF NOT EXISTS protected_parts (
                part_code VARCHAR(100) PRIMARY KEY,
                order_id INT DEFAULT NULL,
                reason VARCHAR(255),
                protected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_protected_part_code FOREIGN KEY (part_code) 
                    REFERENCES stock(part_code) 
                    ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT fk_protected_order_id FOREIGN KEY (order_id) 
                    REFERENCES orders(id) 
                    ON DELETE SET NULL ON UPDATE CASCADE,
                INDEX idx_order_id (order_id),
                INDEX idx_protected_date (protected_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            
            -- History log table
            CREATE TABLE IF NOT EXISTS history_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT DEFAULT NULL,
                part_code VARCHAR(100) DEFAULT NULL,
                action VARCHAR(100) NOT NULL,
                notes LONGTEXT,
                action_by VARCHAR(100),
                action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_history_order_id FOREIGN KEY (order_id) 
                    REFERENCES orders(id) 
                    ON DELETE SET NULL ON UPDATE CASCADE,
                CONSTRAINT fk_history_part_code FOREIGN KEY (part_code) 
                    REFERENCES stock(part_code) 
                    ON DELETE SET NULL ON UPDATE CASCADE,
                INDEX idx_order_id (order_id),
                INDEX idx_part_code (part_code),
                INDEX idx_action (action),
                INDEX idx_action_date (action_date),
                INDEX idx_action_by (action_by)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        conn.commit()
        print_success("All tables created in isolated database")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"Database creation failed: {e}")
        return False

def migrate_data():
    """Migrate data from flaskdb to order_system_db"""
    print_section("MIGRATING DATA")
    
    try:
        inventory_conn = get_connection(INVENTORY_DB_CONFIG)
        order_conn = get_connection(ORDER_DB_CONFIG)
        
        inventory_cursor = inventory_conn.cursor()
        order_cursor = order_conn.cursor()
        
        # Migrate order_system_stock → stock
        print_info("Copying order_system_stock → stock...")
        inventory_cursor.execute("SELECT * FROM order_system_stock")
        rows = inventory_cursor.fetchall()
        
        for row in rows:
            order_cursor.execute("""
                INSERT INTO stock 
                (part_code, part_name, stock_quantity, critical_stock_level, 
                 expected_stock, supplier, unit_price, last_updated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                part_name = VALUES(part_name),
                stock_quantity = VALUES(stock_quantity),
                critical_stock_level = VALUES(critical_stock_level),
                expected_stock = VALUES(expected_stock),
                supplier = VALUES(supplier),
                unit_price = VALUES(unit_price)
            """, (row['part_code'], row['part_name'], row['stock_quantity'],
                  row['critical_stock_level'], row['expected_stock'],
                  row['supplier'], row['unit_price'], row['last_updated']))
        
        order_conn.commit()
        print_success(f"Migrated {len(rows)} records: order_system_stock → stock")
        
        # Migrate order_list → orders
        print_info("Copying order_list → orders...")
        inventory_cursor.execute("SELECT * FROM order_list")
        rows = inventory_cursor.fetchall()
        
        for row in rows:
            order_cursor.execute("""
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
        
        order_conn.commit()
        print_success(f"Migrated {len(rows)} records: order_list → orders")
        
        # Migrate protected_parts
        print_info("Copying protected_parts...")
        inventory_cursor.execute("SELECT * FROM protected_parts")
        rows = inventory_cursor.fetchall()
        
        for row in rows:
            order_cursor.execute("""
                INSERT INTO protected_parts 
                (part_code, order_id, reason, protected_date)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                order_id = VALUES(order_id),
                reason = VALUES(reason)
            """, (row['part_code'], row.get('order_id'), row.get('reason'),
                  row['protected_date']))
        
        order_conn.commit()
        print_success(f"Migrated {len(rows)} records: protected_parts")
        
        # Try to migrate history log if it exists
        try:
            inventory_cursor.execute("""
                SELECT * FROM order_system_history_log 
                WHERE database_table = 'order_system_db'
            """)
            rows = inventory_cursor.fetchall()
            
            if rows:
                for row in rows:
                    order_cursor.execute("""
                        INSERT INTO history_log 
                        (order_id, part_code, action, notes, action_by, action_date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (row.get('order_id'), row.get('part_code'),
                          row.get('action'), row.get('notes'),
                          row.get('action_by'), row.get('action_date')))
                
                order_conn.commit()
                print_success(f"Migrated {len(rows)} records: order_system_history_log → history_log")
        except:
            print_info("No history_log to migrate (table may not exist)")
        
        inventory_cursor.close()
        order_cursor.close()
        inventory_conn.close()
        order_conn.close()
        
        return True
        
    except Exception as e:
        print_error(f"Data migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_isolation():
    """Verify complete isolation between systems"""
    print_section("VERIFYING ISOLATION")
    
    try:
        inventory_conn = get_connection(INVENTORY_DB_CONFIG)
        order_conn = get_connection(ORDER_DB_CONFIG)
        
        inventory_cursor = inventory_conn.cursor()
        order_cursor = order_conn.cursor()
        
        # Check inventory system has inventory tables
        inventory_cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = 'flaskdb' 
            AND TABLE_NAME IN ('part_codes', 'qr_codes', 'scanned_qr', 'count_sessions')
        """)
        inv_count = inventory_cursor.fetchone()['cnt']
        
        if inv_count == 4:
            print_success("✅ Inventory system has all core tables (part_codes, qr_codes, scanned_qr, count_sessions)")
        else:
            print_error(f"⚠️  Expected 4 inventory tables, found {inv_count}")
        
        # Check order system has order tables
        order_cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = 'order_system_db' 
            AND TABLE_NAME IN ('stock', 'orders', 'protected_parts', 'history_log')
        """)
        order_count = order_cursor.fetchone()['cnt']
        
        if order_count == 4:
            print_success("✅ Order system has all 4 tables (stock, orders, protected_parts, history_log)")
        else:
            print_error(f"⚠️  Expected 4 order tables, found {order_count}")
        
        # Check NO order system tables in inventory database
        inventory_cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = 'flaskdb' 
            AND TABLE_NAME IN ('order_system_stock', 'order_list', 'protected_parts', 
                              'order_system_history_log')
        """)
        old_count = inventory_cursor.fetchone()['cnt']
        
        if old_count == 0:
            print_success("✅ No old order tables in flaskdb (clean separation)")
        else:
            print_info(f"⚠️  Found {old_count} old order tables in flaskdb (will be deleted next)")
        
        # Check Foreign Key constraints
        order_cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.REFERENTIAL_CONSTRAINTS
            WHERE CONSTRAINT_SCHEMA = 'order_system_db'
        """)
        fk_count = order_cursor.fetchone()['cnt']
        print_success(f"✅ Order system has {fk_count} Foreign Key constraints (all internal)")
        
        # Check NO Foreign Keys pointing to flaskdb
        order_cursor.execute("""
            SELECT COUNT(*) as cnt FROM information_schema.REFERENTIAL_CONSTRAINTS
            WHERE CONSTRAINT_SCHEMA = 'order_system_db'
            AND UNIQUE_CONSTRAINT_SCHEMA = 'flaskdb'
        """)
        cross_db_fk = order_cursor.fetchone()['cnt']
        
        if cross_db_fk == 0:
            print_success("✅ NO cross-database Foreign Keys (complete isolation)")
        else:
            print_error(f"❌ Found {cross_db_fk} cross-database Foreign Keys")
        
        inventory_cursor.close()
        order_cursor.close()
        inventory_conn.close()
        order_conn.close()
        
        return True
        
    except Exception as e:
        print_error(f"Isolation verification failed: {e}")
        return False

def show_statistics():
    """Show statistics about both systems"""
    print_section("SYSTEM STATISTICS")
    
    try:
        inventory_conn = get_connection(INVENTORY_DB_CONFIG)
        order_conn = get_connection(ORDER_DB_CONFIG)
        
        inventory_cursor = inventory_conn.cursor()
        order_cursor = order_conn.cursor()
        
        print("📊 INVENTORY SYSTEM (flaskdb)")
        print("-" * 40)
        
        inventory_cursor.execute("SELECT COUNT(*) as cnt FROM part_codes")
        print(f"  part_codes:     {inventory_cursor.fetchone()['cnt']:,}")
        
        inventory_cursor.execute("SELECT COUNT(*) as cnt FROM qr_codes")
        print(f"  qr_codes:       {inventory_cursor.fetchone()['cnt']:,}")
        
        inventory_cursor.execute("SELECT COUNT(*) as cnt FROM scanned_qr")
        print(f"  scanned_qr:     {inventory_cursor.fetchone()['cnt']:,}")
        
        inventory_cursor.execute("SELECT COUNT(*) as cnt FROM count_sessions")
        print(f"  count_sessions: {inventory_cursor.fetchone()['cnt']:,}")
        
        print("\n📊 ORDER SYSTEM (order_system_db)")
        print("-" * 40)
        
        order_cursor.execute("SELECT COUNT(*) as cnt FROM stock")
        print(f"  stock:          {order_cursor.fetchone()['cnt']:,}")
        
        order_cursor.execute("SELECT COUNT(*) as cnt FROM orders")
        print(f"  orders:         {order_cursor.fetchone()['cnt']:,}")
        
        order_cursor.execute("SELECT COUNT(*) as cnt FROM protected_parts")
        print(f"  protected_parts:{order_cursor.fetchone()['cnt']:,}")
        
        order_cursor.execute("SELECT COUNT(*) as cnt FROM history_log")
        print(f"  history_log:    {order_cursor.fetchone()['cnt']:,}")
        
        inventory_cursor.close()
        order_cursor.close()
        inventory_conn.close()
        order_conn.close()
        
    except Exception as e:
        print_error(f"Statistics retrieval failed: {e}")

def main():
    """Main execution function"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "SİPARİŞ SİSTEMİ İZOLASYON" + " "*34 + "║")
    print("║" + " "*15 + "ORDER SYSTEM COMPLETE ISOLATION" + " "*32 + "║")
    print("╚" + "="*78 + "╝")
    
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Step 1: Check databases
    if not check_databases_exist():
        print_error("Database check failed")
        return False
    
    # Step 2: Create isolated database
    if not create_isolated_database():
        print_error("Database creation failed")
        return False
    
    # Step 3: Migrate data
    if not migrate_data():
        print_error("Data migration failed")
        return False
    
    # Step 4: Verify isolation
    if not verify_isolation():
        print_error("Isolation verification failed")
        return False
    
    # Step 5: Show statistics
    show_statistics()
    
    # Completion
    print_section("ISOLATION COMPLETE ✅")
    print("""
✅ Sipariş Sistemi tamamen izole edildi!
✅ Order System completely isolated!

Next Steps:
1. Update order_system.py DB_CONFIG to use 'order_system_db'
2. Update table references (order_system_stock → stock, etc.)
3. Restart Flask application
4. Test all order system functionality
5. Verify no inventory system interference

Status: READY FOR CODE UPDATES
""")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
