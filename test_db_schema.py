#!/usr/bin/env python3
"""
Test script: Database schema ve parts_info tablosunun yapısını kontrol et
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# .env yükle
load_dotenv()

try:
    # MySQL bağlantısı
    conn = mysql.connector.connect(
        host='192.168.0.57',
        user='flaskuser',
        password='FlaskSifre123!',
        database='flaskdb',
        port=3306
    )
    
    cursor = conn.cursor()
    
    print("=" * 80)
    print("[1] PARTS_INFO TABLO YAPISI")
    print("=" * 80)
    
    cursor.execute('DESCRIBE parts_info')
    columns = cursor.fetchall()
    
    print(f"\nToplam kolon sayısı: {len(columns)}\n")
    
    for i, col in enumerate(columns, 1):
        col_name = col[0]
        col_type = col[1]
        nullable = col[2]
        key = col[3]
        default = col[4]
        extra = col[5]
        
        marker = ""
        if col_name in ['replacement_code', 'build_out']:
            marker = " <-- ARANILAN KOLON"
        
        print(f"{i:2}. {col_name:25} | {col_type:20} | Null:{nullable} | Default:{str(default):15}{marker}")
    
    print("\n" + "=" * 80)
    print("[2] ÖNEMLİ KOLON DURUMU")
    print("=" * 80)
    
    required_cols = ['replacement_code', 'build_out']
    found_cols = [col[0] for col in columns]
    
    for col in required_cols:
        if col in found_cols:
            print(f"✓ {col} - BULUNDU")
        else:
            print(f"✗ {col} - EKSIK (Gerek: ALTER TABLE parts_info ADD COLUMN {col})")
    
    print("\n" + "=" * 80)
    print("[3] İLK SATIR VERİSİ")
    print("=" * 80)
    
    cursor.execute('SELECT * FROM parts_info LIMIT 1')
    row = cursor.fetchone()
    
    if row:
        print(f"\nİlk satırda {len(row)} veri sütunu:\n")
        for i, col in enumerate(columns):
            col_name = col[0]
            if i < len(row):
                value = row[i]
                if isinstance(value, str) and len(value) > 50:
                    value = value[:50] + "..."
                print(f"  [{i:2}] {col_name:25} = {value}")
            else:
                print(f"  [{i:2}] {col_name:25} = (VERI YOK)")
    else:
        print("Tabloda veri yok!")
    
    print("\n" + "=" * 80)
    print("[4] VERİ İSTATİSTİKLERİ")
    print("=" * 80)
    
    cursor.execute('SELECT COUNT(*) as total FROM parts_info')
    count_result = cursor.fetchone()
    print(f"Toplam parça: {count_result[0] if count_result else 0}")
    
    # replacement_code dolu olanlar
    cursor.execute("SELECT COUNT(*) as cnt FROM parts_info WHERE replacement_code IS NOT NULL AND replacement_code != ''")
    repl_result = cursor.fetchone()
    print(f"replacement_code dolu: {repl_result[0] if repl_result else 0}")
    
    # build_out = 1 olanlar
    cursor.execute("SELECT COUNT(*) as cnt FROM parts_info WHERE build_out = 1")
    build_result = cursor.fetchone()
    print(f"build_out = 1: {build_result[0] if build_result else 0}")
    
    print("\n" + "=" * 80)
    print("✓ TEST TAMAMLANDI")
    print("=" * 80)
    
    cursor.close()
    conn.close()
    
except Error as e:
    print(f"✗ Database Error: {e}")
except Exception as e:
    print(f"✗ Error: {e}")
