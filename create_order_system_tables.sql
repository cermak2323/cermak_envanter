-- PARÇA SİPARİŞ SİSTEMİ - VERİTABANI TABLOLARI
-- Mevcut envanter sistemine dokunulmaz, tamamen ayrı tablolar

-- 1. Sipariş Sistemi Stok Tablosu
CREATE TABLE IF NOT EXISTS order_system_stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    part_code VARCHAR(100) NOT NULL UNIQUE,
    part_name VARCHAR(255),
    stock_quantity INT DEFAULT 0,
    critical_stock_level INT DEFAULT 0,
    expected_stock INT DEFAULT 0,
    supplier VARCHAR(255),
    unit_price DECIMAL(10, 2) DEFAULT 0.00,
    currency VARCHAR(10) DEFAULT '€',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_part_code (part_code),
    INDEX idx_critical_check (stock_quantity, critical_stock_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Sipariş Listesi Tablosu
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
    INDEX idx_order_date (order_date),
    FOREIGN KEY (part_code) REFERENCES order_system_stock(part_code) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Korumalı Parçalar (Sipariş Bekleyen - Tekrar Sipariş Edilmeyecek)
CREATE TABLE IF NOT EXISTS protected_parts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    part_code VARCHAR(100) NOT NULL UNIQUE,
    order_id INT NOT NULL,
    protected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason VARCHAR(255) DEFAULT 'Aktif siparişte - Gelmedi durumunda',
    INDEX idx_part_code (part_code),
    FOREIGN KEY (part_code) REFERENCES order_system_stock(part_code) ON UPDATE CASCADE,
    FOREIGN KEY (order_id) REFERENCES order_list(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Sipariş Geçmişi Log Tablosu (İzlenebilirlik için)
CREATE TABLE IF NOT EXISTS order_history_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- İlk test verisi (opsiyonel)
-- Bu verileri mevcut part_codes tablosundan çekebilirsiniz
