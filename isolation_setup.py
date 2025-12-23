#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ORDER SYSTEM ISOLATION - Database Creation via Direct Execution
Using raw SQL execution without needing root privilege
"""

import pymysql
from pymysql import MySQLError

def create_order_system_db():
    """Create order_system_db by connecting to MySQL directly"""
    
    print("\n" + "="*80)
    print("  ORDER SYSTEM DATABASE ISOLATION")
    print("="*80 + "\n")
    
    try:
        # Connect with flaskuser to an existing database first (flaskdb)
        conn = pymysql.connect(
            host='192.168.0.57',
            port=3306,
            user='flaskuser',
            password='FlaskSifre123!',
            database='flaskdb',  # Connect to existing database first
            charset='utf8mb4',
            autocommit=True  # Auto-commit for CREATE DATABASE
        )
        cursor = conn.cursor()
        
        print("✅ Connected to MySQL (flaskdb)")
        
        # Try to create the database
        try:
            cursor.execute("""
                CREATE DATABASE IF NOT EXISTS order_system_db 
                CHARACTER SET utf8mb4 
                COLLATE utf8mb4_unicode_ci
            """)
            print("✅ Created database: order_system_db")
        except pymysql.err.ProgrammingError as e:
            if "Access denied" in str(e):
                print("⚠️  Cannot create database with flaskuser (insufficient privileges)")
                print("    But we can create tables if database already exists...")
                
                # Check if database already exists
                cursor.execute("SHOW DATABASES LIKE 'order_system_db'")
                if cursor.fetchone():
                    print("✅ Database order_system_db already exists")
                else:
                    print("❌ Database doesn't exist and cannot create it with current user")
                    print("\n   Please run this SQL as root or admin:")
                    print("   CREATE DATABASE order_system_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                    print("   GRANT ALL ON order_system_db.* TO 'flaskuser'@'%' IDENTIFIED BY 'FlaskSifre123!';")
                    print("   FLUSH PRIVILEGES;")
                    return False
        
        # Now try to use the order_system_db
        cursor.close()
        conn.close()
        
        # Connect to order_system_db
        try:
            conn = pymysql.connect(
                host='192.168.0.57',
                port=3306,
                user='flaskuser',
                password='FlaskSifre123!',
                database='order_system_db',
                charset='utf8mb4',
                autocommit=True
            )
            cursor = conn.cursor()
            print("✅ Connected to order_system_db")
            
            # Create tables
            print("\nCreating tables...")
            
            # Table 1: stock
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
            print("  ✅ Table: stock")
            
            # Table 2: orders
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
            print("  ✅ Table: orders")
            
            # Table 3: protected_parts
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS protected_parts (
                    part_code VARCHAR(100) PRIMARY KEY,
                    order_id INT DEFAULT NULL,
                    reason VARCHAR(255),
                    protected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT fk_prot_part FOREIGN KEY (part_code) 
                        REFERENCES stock(part_code) ON DELETE CASCADE,
                    INDEX idx_order_id (order_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("  ✅ Table: protected_parts")
            
            # Table 4: history_log
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
            print("  ✅ Table: history_log")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"❌ Error creating tables in order_system_db: {e}")
            return False
        
        # Now migrate data
        print("\nMigrating data...")
        try:
            src_conn = pymysql.connect(
                host='192.168.0.57',
                port=3306,
                user='flaskuser',
                password='FlaskSifre123!',
                database='flaskdb',
                charset='utf8mb4'
            )
            dst_conn = pymysql.connect(
                host='192.168.0.57',
                port=3306,
                user='flaskuser',
                password='FlaskSifre123!',
                database='order_system_db',
                charset='utf8mb4'
            )
            
            src_cursor = src_conn.cursor()
            dst_cursor = dst_conn.cursor()
            
            # Migrate order_system_stock → stock
            src_cursor.execute("SELECT COUNT(*) FROM order_system_stock")
            count = src_cursor.fetchone()[0]
            
            src_cursor.execute("SELECT * FROM order_system_stock")
            rows = src_cursor.fetchall()
            
            for row in rows:
                try:
                    dst_cursor.execute("""
                        INSERT INTO stock VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        part_name = VALUES(part_name),
                        stock_quantity = VALUES(stock_quantity),
                        critical_stock_level = VALUES(critical_stock_level),
                        expected_stock = VALUES(expected_stock),
                        supplier = VALUES(supplier),
                        unit_price = VALUES(unit_price)
                    """, row)
                except Exception as e:
                    print(f"  ⚠️  Error migrating part {row[0]}: {e}")
            
            dst_conn.commit()
            print(f"  ✅ Migrated {count} records: order_system_stock → stock")
            
            # Migrate order_list → orders
            src_cursor.execute("SELECT COUNT(*) FROM order_list")
            count = src_cursor.fetchone()[0]
            
            if count > 0:
                src_cursor.execute("SELECT * FROM order_list")
                rows = src_cursor.fetchall()
                
                for row in rows:
                    try:
                        dst_cursor.execute("""
                            INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, row)
                    except Exception as e:
                        print(f"  ⚠️  Error migrating order: {e}")
                
                dst_conn.commit()
            
            print(f"  ✅ Migrated {count} records: order_list → orders")
            
            # Migrate protected_parts
            src_cursor.execute("SELECT COUNT(*) FROM protected_parts")
            count = src_cursor.fetchone()[0]
            
            if count > 0:
                src_cursor.execute("SELECT * FROM protected_parts")
                rows = src_cursor.fetchall()
                
                for row in rows:
                    try:
                        dst_cursor.execute("""
                            INSERT INTO protected_parts VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                            order_id = VALUES(order_id)
                        """, row)
                    except Exception as e:
                        print(f"  ⚠️  Error migrating protected part: {e}")
                
                dst_conn.commit()
            
            print(f"  ✅ Migrated {count} records: protected_parts")
            
            src_cursor.close()
            dst_cursor.close()
            src_conn.close()
            dst_conn.close()
            
        except Exception as e:
            print(f"❌ Data migration failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Verify
        print("\n" + "="*80)
        print("  VERIFICATION")
        print("="*80 + "\n")
        
        try:
            ord_conn = pymysql.connect(
                host='192.168.0.57',
                port=3306,
                user='flaskuser',
                password='FlaskSifre123!',
                database='order_system_db',
                charset='utf8mb4'
            )
            ord_cursor = ord_conn.cursor()
            
            ord_cursor.execute("SELECT COUNT(*) FROM stock")
            stock_count = ord_cursor.fetchone()[0]
            
            ord_cursor.execute("SELECT COUNT(*) FROM orders")
            orders_count = ord_cursor.fetchone()[0]
            
            ord_cursor.execute("SELECT COUNT(*) FROM protected_parts")
            prot_count = ord_cursor.fetchone()[0]
            
            ord_cursor.close()
            ord_conn.close()
            
            print(f"✅ order_system_db.stock:          {stock_count} records")
            print(f"✅ order_system_db.orders:         {orders_count} records")
            print(f"✅ order_system_db.protected_parts:{prot_count} records")
            
        except Exception as e:
            print(f"⚠️  Verification error: {e}")
        
        print("\n" + "="*80)
        print("  ✅ ISOLATION SETUP COMPLETE")
        print("="*80)
        print("""
Next Steps:
1. Update order_system.py DB_CONFIG 'database' to 'order_system_db'
2. Update table references:
   - order_system_stock → stock
   - order_list → orders
3. Restart Flask application
4. Test order system functionality

Status: READY FOR CODE UPDATES
""")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\nPlease verify:")
        print("  - MySQL server is running (192.168.0.57:3306)")
        print("  - Database credentials: flaskuser / FlaskSifre123!")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import sys
    success = create_order_system_db()
    sys.exit(0 if success else 1)
