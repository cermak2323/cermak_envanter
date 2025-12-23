#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR Kod Dönüşüm Test Script
Scanner'ın okuduğu karakterleri doğru dönüştürüyor mu kontrol eder
"""

def test_qr_transformation():
    """QR dönüşümlerini test et"""
    
    print("⚡ QR KOD DÖNÜŞÜM TESTİ")
    print("=" * 80)
    
    test_cases = [
        # (Scanner'ın okuduğu, Sayım var mı?, Olması gereken)
        ("ANTF03?6", True, "ANTF03_6"),           # Sayımda _6 korunur
        ("ANTF03?6", False, "ANTF03"),            # Sayım yoksa _6 kaldırılır
        ("Y129648*01780", True, "Y129648-01780"), # * -> - çevrilir
        ("Y129648*01780", False, "Y129648-01780"),
        ("Y129648*01780?1", True, "Y129648-01780_1"),  # Sayımda _1 korunur
        ("Y129648*01780?1", False, "Y129648-01780"),   # Sayım yoksa _1 kaldırılır
        ("TEST*QR?CODE", True, "TEST-QR_CODE"),
        ("TEST*QR?CODE", False, "TEST-QR_CODE"),
        ("PART?3", True, "PART_3"),               # Sayımda _3 önemli!
        ("PART?3", False, "PART"),                # Sayım yoksa kaldır
        ("NORMAL_CODE", True, "NORMAL_CODE"),
        ("NORMAL_CODE", False, "NORMAL_CODE"),
    ]
    
    print("Scanner Okur         Sayım?  → Dönüştürülmüş      → Durum")
    print("-" * 80)
    
    all_passed = True
    
    for scanner_input, has_session, expected_output in test_cases:
        # Dönüşüm yap (kod'daki gibi)
        transformed = scanner_input.replace('?', '_').replace('*', '-')
        
        # Sonundaki _X formatını SADECE sayım yokken kaldır
        if not has_session and '_' in transformed:
            parts = transformed.split('_')
            if len(parts) > 1 and parts[-1].isdigit() and len(parts[-1]) == 1:
                transformed = '_'.join(parts[:-1])
        
        # Kontrol
        status = "✅ PASS" if transformed == expected_output else "❌ FAIL"
        if transformed != expected_output:
            all_passed = False
        
        session_text = "VAR " if has_session else "YOK "
        print(f"{scanner_input:20} {session_text} → {transformed:20} → {status}")
        if transformed != expected_output:
            print(f"  Beklenen: {expected_output}")
    
    print("=" * 80)
    
    if all_passed:
        print("✅ TÜM TESTLER BAŞARILI!")
    else:
        print("❌ BAZI TESTLER BAŞARISIZ!")
    
    print("\n📝 AÇIKLAMA:")
    print("  Scanner ? okur  → Sistem _ yapar  (ANTF03?6 -> ANTF03_6)")
    print("  Scanner * okur  → Sistem - yapar  (Y129648*01780 -> Y129648-01780)")
    print("  Sonundaki _X:")
    print("    - Sayım VARKEN  → KORUNUR  (PART?3 -> PART_3) ✅ Önemli!")
    print("    - Sayım YOKKEN  → KALDIRILIR (PART?3 -> PART) ✅ Temiz görünüm")

if __name__ == "__main__":
    test_qr_transformation()
