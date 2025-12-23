import os
import mysql.connector
from mysql.connector import Error
import json
from pathlib import Path

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="192.168.0.57",
        user="root",
        password="root",
        database="flaskdb"
    )

def scan_all_wrong_qr_ids():
    """Tüm parçalarda yanlış part_code_id ile bağlı QR kodlarını bul"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Adım 1: Tüm part_codes'ı getir
        cursor.execute("SELECT id, part_code FROM part_codes ORDER BY id")
        all_parts = cursor.fetchall()
        print(f"✅ Toplam {len(all_parts)} parça bulundu")
        print()
        
        # Adım 2: Her parça için, doğru part_code_id ile QR var mı kontrol et
        wrong_qr_assignments = []
        parts_with_issues = {}
        
        for part in all_parts:
            part_id = part['id']
            part_code = part['part_code']
            
            # Bu part_code_id ile kaç QR kod var?
            cursor.execute(
                "SELECT COUNT(*) as count FROM qr_codes WHERE part_code_id = %s",
                (part_id,)
            )
            qr_count_correct = cursor.fetchone()['count']
            
            if qr_count_correct == 0:
                continue
                
            # Adım 3: Shared folder'da bu parça için QR dosyaları var mı?
            qr_folder = f"\\\\DCSRV\\tahsinortak\\CermakDepo\\CermakEnvanter\\static\\qr_codes\\{part_code}"
            
            if not os.path.exists(qr_folder):
                continue
            
            # Folder'daki QR dosyalarını say
            qr_files = [f for f in os.listdir(qr_folder) if f.endswith('.png')]
            
            if len(qr_files) == 0:
                continue
            
            # Adım 4: Bu parçanın QR pattern'ini kontrol et
            # Pattern: {part_code}_{number}.png
            # Örn: Y129A00-55730_1.png
            qr_pattern = f"{part_code}_"
            matching_qr_files = [f for f in qr_files if f.startswith(qr_pattern)]
            
            if len(matching_qr_files) == 0:
                continue
            
            # Adım 5: Bu parça pattern'i ile DB'de kaç QR var?
            cursor.execute(
                "SELECT COUNT(*) as count FROM qr_codes WHERE qr_id LIKE %s",
                (f"{part_code}_%",)
            )
            qr_count_with_pattern = cursor.fetchone()['count']
            
            # Adım 6: Bu QR'ların hangi part_code_id'ler ile bağlı olduğunu bul
            cursor.execute(
                "SELECT DISTINCT part_code_id FROM qr_codes WHERE qr_id LIKE %s",
                (f"{part_code}_%",)
            )
            wrong_ids = cursor.fetchall()
            
            if len(wrong_ids) > 0:
                for row in wrong_ids:
                    wrong_id = row['part_code_id']
                    if wrong_id != part_id:  # Yanlış ID'ye bağlı QR kodları bulduk
                        cursor.execute(
                            "SELECT COUNT(*) as count FROM qr_codes WHERE qr_id LIKE %s AND part_code_id = %s",
                            (f"{part_code}_%", wrong_id)
                        )
                        count = cursor.fetchone()['count']
                        
                        wrong_qr_assignments.append({
                            'part_code': part_code,
                            'correct_part_code_id': part_id,
                            'wrong_part_code_id': wrong_id,
                            'qr_count': count,
                            'file_count': len(matching_qr_files)
                        })
                        
                        if part_code not in parts_with_issues:
                            parts_with_issues[part_code] = []
                        parts_with_issues[part_code].append({
                            'wrong_id': wrong_id,
                            'count': count
                        })
        
        # Sonuçları göster
        if wrong_qr_assignments:
            print("🔴 YANLIŞ PART_CODE_ID İLE BAĞLI QR KODLARI BULUNDU:")
            print("=" * 80)
            for item in wrong_qr_assignments:
                print(f"📦 Parça: {item['part_code']}")
                print(f"   Doğru ID: {item['correct_part_code_id']}")
                print(f"   Yanlış ID: {item['wrong_part_code_id']}")
                print(f"   Yanlış bağlı QR: {item['qr_count']} (dosya: {item['file_count']})")
                print()
            
            print(f"⚠️  TOPLAM YANLIŞ PARÇA: {len(parts_with_issues)}")
            print(f"⚠️  TOPLAM YANLIŞ QR KOD: {sum(item['qr_count'] for item in wrong_qr_assignments)}")
        else:
            print("✅ Tüm QR kodlar doğru part_code_id'ler ile bağlı!")
        
        # JSON dosyasına kaydet
        with open('wrong_qr_assignments.json', 'w', encoding='utf-8') as f:
            json.dump(wrong_qr_assignments, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Detaylar 'wrong_qr_assignments.json' dosyasına kaydedildi")
        
    except Error as e:
        print(f"❌ Veritabanı hatası: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    scan_all_wrong_qr_ids()
