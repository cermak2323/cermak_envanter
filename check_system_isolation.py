#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistem Izolasyon Kontrol Araci
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, PartCode, QRCode
import pymysql

DB_CONFIG = {
    'host': '192.168.0.57',
    'port': 3306,
    'user': 'flaskuser',
    'password': 'FlaskSifre123!',
    'database': 'flaskdb'
}

def check_system_isolation():
    """Sistem izolasyonunu dogrula"""
    
    print("\n" + "="*70)
    print("[SYSTEM ISOLATION CONTROL]".center(70))
    print("="*70)
    
    with app.app_context():
        try:
            # 1. Envanter Sistemi
            print("\n[INVENTORY SYSTEM]")
            print("-" * 70)
            
            part_count = db.session.query(PartCode).count()
            qr_count = db.session.query(QRCode).count()
            
            print(f"  part_codes: {part_count} pieces")
            print(f"  qr_codes: {qr_count} QR codes")
            
            # 2. Siparis Sistemi
            print("\n[ORDER SYSTEM]")
            print("-" * 70)
            
            conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as cnt FROM order_system_stock")
            stock_count = cursor.fetchone()['cnt']
            print(f"  order_system_stock: {stock_count} pieces")
            
            cursor.execute("SELECT COUNT(*) as cnt FROM order_list")
            order_count = cursor.fetchone()['cnt']
            print(f"  order_list: {order_count} orders")
            
            # 3. QR Kod Kontrolü
            print("\n[QR CODE INTEGRITY]")
            print("-" * 70)
            
            cursor.execute("""
                SELECT COUNT(q.id) as wrong_count
                FROM qr_codes q
                LEFT JOIN part_codes p ON q.part_code_id = p.id
                WHERE p.id IS NULL
            """)
            wrong_qr_count = cursor.fetchone()['wrong_count']
            
            if wrong_qr_count == 0:
                print(f"  [OK] All QR codes linked correctly")
            else:
                print(f"  [WARNING] {wrong_qr_count} QR codes with errors!")
            
            # 4. Durum Ozeti
            print("\n" + "="*70)
            print("[STATUS SUMMARY]".center(70))
            print("="*70)
            
            print(f"\nInventory: {part_count} pieces, {qr_count} QR codes")
            print(f"Orders: {stock_count} stock pieces, {order_count} orders")
            print(f"Data Integrity: {qr_count - wrong_qr_count}/{qr_count} correct")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"\n[ERROR] {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    check_system_isolation()
