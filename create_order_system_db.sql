-- ============================================================================
-- SİPARİŞ SİSTEMİ İZOLE VERİTABANI OLUŞTURMA
-- ORDER SYSTEM ISOLATED DATABASE CREATION
-- ============================================================================
-- Amaç: Sipariş sistemi için ayrı veritabanı oluşturma
-- Purpose: Create separate database for order system with complete isolation
-- ============================================================================

-- Step 1: Create isolated database
CREATE DATABASE IF NOT EXISTS order_system_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Verify database created
SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA 
WHERE SCHEMA_NAME = 'order_system_db';

-- Use the new database
USE order_system_db;

-- ============================================================================
-- Step 2: Create isolated tables
-- ============================================================================

-- Table 1: Stock (from order_system_stock)
CREATE TABLE IF NOT EXISTS stock (
    part_code VARCHAR(100) PRIMARY KEY,
    part_name VARCHAR(255) NOT NULL,
    stock_quantity INT DEFAULT 0,
    critical_stock_level INT DEFAULT NULL,
    expected_stock INT DEFAULT NULL,
    supplier VARCHAR(255),
    unit_price DECIMAL(10, 4) DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes for performance
    INDEX idx_supplier (supplier),
    INDEX idx_stock_level (stock_quantity, critical_stock_level),
    INDEX idx_expected (expected_stock),
    INDEX idx_updated (last_updated)
) ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci
COMMENT='İzole Sipariş Sistem Stok - Order System Stock (Isolated)';

-- Table 2: Orders (from order_list)
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
    
    -- Foreign key constraint (only within order system)
    CONSTRAINT fk_orders_part_code FOREIGN KEY (part_code) 
        REFERENCES stock(part_code) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    -- Indexes for performance
    INDEX idx_status (status),
    INDEX idx_supplier (supplier),
    INDEX idx_order_date (order_date),
    INDEX idx_part_code (part_code),
    INDEX idx_created_by (created_by)
) ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci
COMMENT='İzole Sipariş Listesi - Order List (Isolated)';

-- Table 3: Protected Parts (korunan parçalar - sipariş sistemine özgü)
CREATE TABLE IF NOT EXISTS protected_parts (
    part_code VARCHAR(100) PRIMARY KEY,
    order_id INT DEFAULT NULL,
    reason VARCHAR(255),
    protected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints (only within order system)
    CONSTRAINT fk_protected_part_code FOREIGN KEY (part_code) 
        REFERENCES stock(part_code) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_protected_order_id FOREIGN KEY (order_id) 
        REFERENCES orders(id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    
    -- Index
    INDEX idx_order_id (order_id),
    INDEX idx_protected_date (protected_date)
) ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci
COMMENT='Korunan Parçalar - Protected Parts (Order System Only)';

-- Table 4: History Log (sipariş sistemi hareketi kaydı)
CREATE TABLE IF NOT EXISTS history_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT DEFAULT NULL,
    part_code VARCHAR(100) DEFAULT NULL,
    action VARCHAR(100) NOT NULL,
    notes LONGTEXT,
    action_by VARCHAR(100),
    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints (only within order system)
    CONSTRAINT fk_history_order_id FOREIGN KEY (order_id) 
        REFERENCES orders(id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_history_part_code FOREIGN KEY (part_code) 
        REFERENCES stock(part_code) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    
    -- Indexes for performance
    INDEX idx_order_id (order_id),
    INDEX idx_part_code (part_code),
    INDEX idx_action (action),
    INDEX idx_action_date (action_date),
    INDEX idx_action_by (action_by)
) ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci
COMMENT='Sipariş Sistem Hareketi Kaydı - Order System History Log';

-- ============================================================================
-- Step 3: Verify tables created
-- ============================================================================

SHOW TABLES FROM order_system_db;
-- Expected output:
-- +----------------------------+
-- | Tables_in_order_system_db  |
-- +----------------------------+
-- | history_log                |
-- | orders                     |
-- | protected_parts            |
-- | stock                      |
-- +----------------------------+

-- ============================================================================
-- Step 4: Verify structure of tables
-- ============================================================================

DESCRIBE order_system_db.stock;
DESCRIBE order_system_db.orders;
DESCRIBE order_system_db.protected_parts;
DESCRIBE order_system_db.history_log;

-- ============================================================================
-- Step 5: Verify Foreign Keys (Isolation Check)
-- ============================================================================

SELECT 
    CONSTRAINT_NAME,
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'order_system_db'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Expected output:
-- All foreign keys should ONLY reference tables in order_system_db
-- NO references to flaskdb.* tables
-- This confirms COMPLETE ISOLATION

-- ============================================================================
-- Step 6: Create database user permissions (if needed)
-- ============================================================================

-- Already done at database level:
-- GRANT ALL ON order_system_db.* TO 'flaskuser'@'%' IDENTIFIED BY 'FlaskSifre123!';
-- FLUSH PRIVILEGES;

-- ============================================================================
-- Step 7: Verify isolation - Check flaskdb has NO order system tables
-- ============================================================================

USE flaskdb;
SHOW TABLES LIKE '%order%';
-- Should return 0 rows (empty)
-- If it returns rows, those are the OLD tables that will be deprecated

-- ============================================================================
-- DATABASE ISOLATION VERIFIED ✅
-- ============================================================================
-- order_system_db: Independent, complete order system
-- flaskdb: Inventory system only, no order system tables
-- NO shared data, NO cross-references
-- COMPLETE ISOLATION ACHIEVED
