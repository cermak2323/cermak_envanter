#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tüm yanlış part_code_id'leri tarayıp düzelt
"""

import os
import sys
import re
from collections import defaultdict

# Flask app'ı import et
sys.path.insert(0, os.path.dirname(__file__))
from app import app, db, PartCode, QRCode

def get_correct_part_code_id(qr_id):
    """QR ID'den doğru part_code_id'yi çıkar"""
    # QR ID format: {part_code}_{number} 
    # Örn: Y129A00-55730_1, Y129A00-55730_200
    parts = qr_id.rsplit('_', 1)
    if len(parts) != 2:
        return None
    
    part_code = parts[0]
    
    # part_codes table'dan bul
    pc = db.session.query(PartCode).filter_by(part_code=part_code).first()
    if pc:
        return pc.id
    
    return None

def fix_all_qr_codes():
    """Tüm yanlış QR kodlarını düzelt"""
    
    with app.app_context():
        print("🔍 Tüm QR kodları taranıyor...")
        
        # Tüm QR kodlarını al
        all_qrs = db.session.query(QRCode).all()
        print(f"📊 Toplam QR: {len(all_qrs)}")
        
        wrong_qrs = []
        fixed_count = 0
        
        for qr in all_qrs:
            # QR ID'den doğru part_code_id'yi al
            correct_id = get_correct_part_code_id(qr.qr_id)
            
            if correct_id is None:
                print(f"⚠️  {qr.qr_id} - Parça bulunamadı")
                continue
            
            # Eğer yanlışsa kaydet
            if qr.part_code_id != correct_id:
                wrong_qrs.append({
                    'qr_id': qr.qr_id,
                    'wrong_id': qr.part_code_id,
                    'correct_id': correct_id
                })
        
        print(f"\n⚠️  Yanlış bağlı QR kod: {len(wrong_qrs)}")
        
        if wrong_qrs:
            # Yanlış olanları gruplama
            wrong_by_part = defaultdict(list)
            for item in wrong_qrs:
                part_code = item['qr_id'].rsplit('_', 1)[0]
                wrong_by_part[part_code].append(item)
            
            print("\n📋 Yanlış bağlı parçalar:")
            for part_code, items in sorted(wrong_by_part.items()):
                print(f"  {part_code}: {len(items)} QR kod")
            
            # Tümünü düzelt
            print(f"\n🔧 Düzeltiliyor...")
            for item in wrong_qrs:
                qr = db.session.query(QRCode).filter_by(qr_id=item['qr_id']).first()
                if qr:
                    old_id = qr.part_code_id
                    qr.part_code_id = item['correct_id']
                    fixed_count += 1
                    if fixed_count <= 5:  # İlk 5'i yazdır
                        print(f"  ✅ {item['qr_id']}: {old_id} → {item['correct_id']}")
            
            if fixed_count > 5:
                print(f"  ... ve {fixed_count - 5} daha")
            
            db.session.commit()
            print(f"\n✅ Toplam düzeltilen QR: {fixed_count}")
        else:
            print("✅ Tüm QR kodları doğru bağlı!")
        
        # Son durum raporu
        print(f"\n📊 Final Rapor:")
        print(f"  ✅ Tüm QR kodları düzeltildi")
        print(f"  📈 Başarılı: {fixed_count} QR")
        
        # Parça başı QR istatistikleri
        print(f"\n📈 QR Kod İstatistikleri (En çok olan 10):")
        part_qr_counts = db.session.query(
            PartCode.code, 
            db.func.count(QRCode.qr_id).label('qr_count')
        ).outerjoin(QRCode).group_by(PartCode.id).order_by(db.func.count(QRCode.qr_id).desc()).limit(10).all()
        
        for code, count in part_qr_counts:
            if count > 0:
                print(f"  {code}: {count} QR")

if __name__ == '__main__':
    fix_all_qr_codes()
