#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Türkçe Karakter Test - QR kod dönüşümü
"""

def test_turkish_qr():
    """Türkçe karakterli QR kodları test et"""
    
    print("⚡ TÜRKÇE KARAKTER + QR DÖNÜŞÜM TESTİ")
    print("=" * 80)
    
    test_cases = [
        # (Scanner'ın okuduğu, Olması gereken)
        ("ANTİF03?6", "ANTİF03_6"),      # İ karakteri korunmalı
        ("ANTF03?6", "ANTF03_6"),        # Normal
        ("GÜNEŞ?5", "GÜNEŞ_5"),          # Ü, Ş korunmalı  
        ("ÇALIŞMA*01", "ÇALIŞMA-01"),    # Ç, I, Ş korunmalı
        ("ÖLÇÜ?3", "ÖLÇÜ_3"),            # Ö, Ç, Ü korunmalı
        ("Y129648*01780?1", "Y129648-01780_1"),
    ]
    
    print("Scanner Okur              → Dönüştürülmüş         → Durum")
    print("-" * 80)
    
    all_passed = True
    
    for scanner_input, expected_output in test_cases:
        # QR dönüşümü (türkçe karakterler korunur!)
        transformed = scanner_input.replace('?', '_').replace('*', '-')
        
        # Kontrol
        status = "✅ PASS" if transformed == expected_output else "❌ FAIL"
        if transformed != expected_output:
            all_passed = False
        
        print(f"{scanner_input:25} → {transformed:25} → {status}")
        if transformed != expected_output:
            print(f"  Beklenen: {expected_output}")
            print(f"  Alınan: {transformed}")
    
    print("=" * 80)
    
    if all_passed:
        print("✅ TÜM TESTLER BAŞARILI!")
        print("\n🎯 Türkçe karakterler korunuyor:")
        print("  İ, Ü, Ş, Ç, Ğ, Ö → KORUNUR ✅")
        print("  ? → _ (alt tire)")
        print("  * → - (tire)")
    else:
        print("❌ BAZI TESTLER BAŞARISIZ!")
    
    # Encoding test
    print("\n📝 ENCODING TEST:")
    test_str = "ANTİF03_6"
    print(f"  String: {test_str}")
    print(f"  Bytes: {test_str.encode('utf-8')}")
    print(f"  Length: {len(test_str)} karakter")

if __name__ == "__main__":
    test_turkish_qr()
