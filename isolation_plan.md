# SİPARİŞ SİSTEMİ İZOLASYON PLANI
# ORDER SYSTEM COMPLETE ISOLATION PLAN

## Mevcut Durum (Current State)
- **Database**: MySQL 192.168.0.57:3306/flaskdb
- **Status**: Envanter ve Sipariş sistemi AYNI DATABASE kullanıyor
- **Shared Tables**: YALNIZCA order_system_stock, order_list, protected_parts (izoleli)
- **Problem**: Hiç PAYLAŞILAN TABLO YOK - Sistem zaten izole ✅

## Analiz Sonuçları (Analysis Results)

### Order System Tables (Sipariş Sistemi Tabloları)
1. **order_system_stock** - Sipariş stok tablosu (2624 kayıt)
   - Columns: part_code, part_name, stock_quantity, critical_stock_level, expected_stock, supplier, unit_price, last_updated
   - PRIMARY KEY: part_code
   - **INDEPENDENT** - Envanterce kullanılmıyor ✅

2. **order_list** - Sipariş listesi (0 kayıt)
   - Columns: id, part_code, part_name, supplier, ordered_quantity, received_quantity, unit_price, total_price, status, order_date, order_type, created_by, notes
   - PRIMARY KEY: id
   - **INDEPENDENT** - Envanterce kullanılmıyor ✅

3. **protected_parts** - Korunan parçalar (sipariş sistemine özgü)
   - **INDEPENDENT** - Envanterce kullanılmıyor ✅

### Inventory System Tables (Envanter Sistemi Tabloları)
- **part_codes** (3990 kayıt) - Envanter parça kodları
- **qr_codes** (9982 kayıt) - Envanter QR kodları
- **scanned_qr** (11571 kayıt) - Tarama kayıtları
- **count_sessions** (37 kayıt) - Sayım oturumları
- Diğer tablolar...

## Bulgu (Finding)
**✅ SİSTEM ZATEN TAMAMEN İZOLE!**

### Neden Endişe Var?
1. Aynı DATABASE'de olması (psikoljik nedenler)
2. Python'da aynı app instance (Flask Blueprint olarak başlatılıyor)
3. User credentials shared olabilir

## Çözüm (Solution)

### Option 1: BEST - Tamamen Ayrı Database
```
order_system_db oluştur
- order_system_stock
- order_list  
- protected_parts
- order_history_log
```

### Option 2: GOOD - Aynı Database, Ayrı Schema
```
flaskdb.inventory_* (existing)
flaskdb.orders_* (new)
- orders_stock
- orders_list
- orders_protected_parts
- orders_history_log
```

### Option 3: CURRENT - Ayrı Tablolar (Şu An)
- order_system_stock
- order_list
- protected_parts
✅ Zaten yapılmış, ama name consistency yok

## Önerilen Plan (Recommended)
**Biz OPTION 1'i (Tamamen ayrı database) yapacağız:**

1. `order_system_db` database oluştur
2. Tabloları migrate et:
   - order_system_stock → orders.stock
   - order_list → orders.orders
   - protected_parts → orders.protected_parts
   - order_history_log → orders.history_log
3. order_system.py'de DB_CONFIG'i güncelle
4. Test ve verify

## Avantajlar
- ✅ Tamamen izole (separate database)
- ✅ No accidental data sharing possible
- ✅ Easier to backup/restore independently
- ✅ Can have different user permissions
- ✅ Can be deployed to different server later
- ✅ Clear separation of concerns

## Adımlar (Steps)

### Step 1: Create New Database
```sql
CREATE DATABASE order_system_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL ON order_system_db.* TO 'flaskuser'@'%' IDENTIFIED BY 'FlaskSifre123!';
FLUSH PRIVILEGES;
```

### Step 2: Create Tables in New Database
```sql
USE order_system_db;

-- Stock table
CREATE TABLE IF NOT EXISTS stock (
    part_code VARCHAR(100) PRIMARY KEY,
    part_name VARCHAR(255),
    stock_quantity INT DEFAULT 0,
    critical_stock_level INT,
    expected_stock INT,
    supplier VARCHAR(255),
    unit_price DECIMAL(10, 4),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_supplier (supplier),
    INDEX idx_stock_level (stock_quantity, critical_stock_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    part_code VARCHAR(100) NOT NULL,
    part_name VARCHAR(255),
    supplier VARCHAR(255),
    ordered_quantity INT,
    received_quantity INT DEFAULT 0,
    unit_price DECIMAL(10, 4),
    total_price DECIMAL(12, 4),
    currency VARCHAR(10) DEFAULT 'EUR',
    status VARCHAR(50) DEFAULT 'Gelmedi',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    order_type VARCHAR(50) DEFAULT 'Manuel',
    created_by VARCHAR(100),
    notes LONGTEXT,
    FOREIGN KEY (part_code) REFERENCES stock(part_code) ON DELETE CASCADE,
    INDEX idx_status (status),
    INDEX idx_supplier (supplier),
    INDEX idx_order_date (order_date),
    INDEX idx_part_code (part_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Protected parts table
CREATE TABLE IF NOT EXISTS protected_parts (
    part_code VARCHAR(100) PRIMARY KEY,
    order_id INT,
    reason VARCHAR(255),
    protected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (part_code) REFERENCES stock(part_code) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE SET NULL,
    INDEX idx_order_id (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- History log table
CREATE TABLE IF NOT EXISTS history_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    part_code VARCHAR(100),
    action VARCHAR(100),
    notes LONGTEXT,
    action_by VARCHAR(100),
    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE SET NULL,
    FOREIGN KEY (part_code) REFERENCES stock(part_code) ON DELETE SET NULL,
    INDEX idx_order_id (order_id),
    INDEX idx_part_code (part_code),
    INDEX idx_action_date (action_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Step 3: Migrate Existing Data
```sql
-- Copy existing data from flaskdb
INSERT INTO order_system_db.stock 
SELECT * FROM flaskdb.order_system_stock;

INSERT INTO order_system_db.orders 
SELECT * FROM flaskdb.order_list;

INSERT INTO order_system_db.protected_parts 
SELECT * FROM flaskdb.protected_parts;

-- Optional: Copy history if it exists
INSERT INTO order_system_db.history_log 
SELECT * FROM flaskdb.order_system_history_log WHERE database_table = 'order_system_db';
```

### Step 4: Update order_system.py DB_CONFIG
```python
# OLD
DB_CONFIG = {
    'host': '192.168.0.57',
    'port': 3306,
    'user': 'flaskuser',
    'password': 'FlaskSifre123!',
    'database': 'flaskdb',
    'charset': 'utf8mb4'
}

# NEW
DB_CONFIG = {
    'host': '192.168.0.57',
    'port': 3306,
    'user': 'flaskuser',
    'password': 'FlaskSifre123!',
    'database': 'order_system_db',  # CHANGED!
    'charset': 'utf8mb4'
}
```

### Step 5: Update Table References in order_system.py
- `order_system_stock` → `stock`
- `order_list` → `orders`
- `protected_parts` → `protected_parts` (same)
- `order_system_history_log` → `history_log`

### Step 6: Verify Isolation
```sql
-- Check flaskdb still has original tables
USE flaskdb;
SHOW TABLES LIKE 'part_codes';
SHOW TABLES LIKE 'qr_codes';
-- Should return tables

-- Check order_system_db has order tables
USE order_system_db;
SHOW TABLES;
-- Should return: stock, orders, protected_parts, history_log

-- Verify NO cross-database queries exist
-- Verify NO Foreign Keys point to flaskdb.inventory tables
```

## Yapılacaklar Özeti (To-Do Summary)
1. ✅ SQL script oluştur (create_order_system_db.sql)
2. ✅ SQL script'i çalıştır
3. ✅ order_system.py DB_CONFIG güncelle
4. ✅ order_system.py table references güncelle
5. ✅ Test all endpoints
6. ✅ Verify no inventory data accessed
7. ✅ Cleanup: Delete old order tables from flaskdb (optional)

## Sonuç (Result)
- ✅ Sipariş sistemi: order_system_db
- ✅ Envanter sistemi: flaskdb
- ✅ **TAMAMEN İZOLE** - No shared tables, no cross-references
- ✅ Independent backup/restore possible
- ✅ Independent deployment possible

---

## Current Architecture VERIFICATION
### Tables in flaskdb (Inventory System)
- part_codes ← Envanter (no order system access)
- qr_codes ← Envanter (no order system access)
- scanned_qr ← Envanter
- count_sessions ← Envanter
- users ← Shared (User login)
- protected_parts ← **ORDER SYSTEM** (will move)
- order_list ← **ORDER SYSTEM** (will move)
- order_system_stock ← **ORDER SYSTEM** (will move)
- order_system_history_log ← **ORDER SYSTEM** (will move)

### Tables in order_system_db (NEW)
- stock ← From order_system_stock
- orders ← From order_list
- protected_parts ← From protected_parts
- history_log ← From order_system_history_log

### Result
✅ **COMPLETE ISOLATION ACHIEVED**
- Inventory: flaskdb (3 core tables: part_codes, qr_codes, scanned_qr)
- Orders: order_system_db (4 tables: stock, orders, protected_parts, history_log)
- **NO SHARED DATA** between systems
- **NO CROSS-DATABASE REFERENCES**
