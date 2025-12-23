#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR Tarama Performans Test Script
Sistemin ne kadar hızlı çalıştığını ölçer
"""

import time
import requests
import statistics

# Test parametreleri
API_URL = "http://localhost:5002/api/scan_qr"
TEST_QR_CODES = [
    "TEST_QR_001",
    "TEST_QR_002", 
    "TEST_QR_003",
    "TEST_QR_004",
    "TEST_QR_005"
]
SESSION_ID = "999"  # Test session
ITERATIONS = 10  # Her QR'ı kaç kez test et

def test_scan_speed():
    """QR tarama hızını test et"""
    
    print("⚡ QR TARAMA PERFORMANS TESTİ")
    print("=" * 60)
    print(f"API: {API_URL}")
    print(f"Test QR Sayısı: {len(TEST_QR_CODES)}")
    print(f"Tekrar Sayısı: {ITERATIONS}")
    print("=" * 60)
    
    all_times = []
    
    for iteration in range(ITERATIONS):
        print(f"\n🔄 İterasyon {iteration + 1}/{ITERATIONS}")
        
        for qr_code in TEST_QR_CODES:
            start = time.time()
            
            try:
                response = requests.post(
                    API_URL,
                    json={
                        'qr_id': qr_code,
                        'session_id': SESSION_ID
                    },
                    timeout=5
                )
                
                elapsed_ms = (time.time() - start) * 1000
                all_times.append(elapsed_ms)
                
                status = "✅" if response.status_code == 200 else "❌"
                print(f"  {status} {qr_code}: {elapsed_ms:.1f}ms")
                
            except Exception as e:
                print(f"  ❌ {qr_code}: ERROR - {e}")
        
        time.sleep(0.5)  # İterasyonlar arası bekleme
    
    # Sonuçlar
    print("\n" + "=" * 60)
    print("📊 PERFORMANS SONUÇLARI")
    print("=" * 60)
    
    if all_times:
        print(f"Toplam Tarama: {len(all_times)}")
        print(f"Ortalama: {statistics.mean(all_times):.1f}ms")
        print(f"En Hızlı: {min(all_times):.1f}ms")
        print(f"En Yavaş: {max(all_times):.1f}ms")
        print(f"Medyan: {statistics.median(all_times):.1f}ms")
        
        if len(all_times) > 1:
            print(f"Std Sapma: {statistics.stdev(all_times):.1f}ms")
        
        # Hedef: <50ms
        fast_count = sum(1 for t in all_times if t < 50)
        print(f"\n⚡ <50ms olan taramalar: {fast_count}/{len(all_times)} ({fast_count/len(all_times)*100:.1f}%)")
        
        if statistics.mean(all_times) < 50:
            print("\n✅ HEDEF BAŞARILI: Ortalama <50ms!")
        else:
            print(f"\n⚠️ HEDEF AŞILDI: Ortalama {statistics.mean(all_times):.1f}ms (hedef: <50ms)")
    
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_scan_speed()
    except KeyboardInterrupt:
        print("\n\n❌ Test iptal edildi")
    except Exception as e:
        print(f"\n\n❌ Test hatası: {e}")
