#!/usr/bin/env python3
"""
Yazıcı test scripti - Ubuntu'da çalıştır
python3 test_printer.py
"""

import sys
import logging
from pathlib import Path

# Loglama ayarla
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from tspl_printer import TSPLPrinter
    from printer_integration import get_printer_manager
except ImportError as e:
    logger.error(f"Import hatası: {e}")
    sys.exit(1)


def test_printer_device():
    """Yazıcı cihazını test et"""
    print("\n" + "="*50)
    print("TSPL Yazıcı Test - Ubuntu")
    print("="*50 + "\n")
    
    # Adım 1: Cihaz kontrolü
    print("1️⃣  Cihaz Kontrolü")
    print("-" * 40)
    
    device_path = "/dev/usb/lp0"
    
    if Path(device_path).exists():
        print(f"✓ Cihaz bulundu: {device_path}")
        
        # İzin kontrolü
        import os
        if os.access(device_path, os.W_OK):
            print(f"✓ Yazma izni var")
        else:
            print(f"⚠️  Yazma izni yok - sudo ile çalıştırın")
    else:
        print(f"✗ Cihaz bulunamadı: {device_path}")
        print("\nAlternatif cihazları kontrol et:")
        import os
        for path in ["/dev/lp0", "/dev/usb/lp0", "/dev/parport0"]:
            if Path(path).exists():
                print(f"  - {path} bulundu")
        return False
    
    # Adım 2: Yazıcı bağlantısı
    print("\n2️⃣  Yazıcı Bağlantısı")
    print("-" * 40)
    
    printer = TSPLPrinter(device_path=device_path)
    
    if printer.connected:
        print("✓ Yazıcı bağlandı")
        print(f"  Durum: {printer.status()}")
    else:
        print("✗ Yazıcı bağlanmadı")
        return False
    
    # Adım 3: Yazıcı yapılandırması
    print("\n3️⃣  Yazıcı Yapılandırması")
    print("-" * 40)
    
    try:
        printer.initialize()
        print("✓ Başlatıldı")
        
        printer.set_label_size(100, 150)
        print("✓ Etiket boyutu: 100x150mm")
        
        printer.set_darkness(10)
        print("✓ Koyuluk: 10")
        
        printer.set_speed(4)
        print("✓ Hız: 4")
        
        printer.set_gap(2.0)
        print("✓ Boşluk: 2.0mm")
    
    except Exception as e:
        print(f"✗ Yapılandırma hatası: {e}")
        return False
    
    # Adım 4: PrinterManager test
    print("\n4️⃣  PrinterManager Test")
    print("-" * 40)
    
    try:
        manager = get_printer_manager()
        status = manager.get_status()
        print(f"✓ Manager başlatıldı")
        print(f"  - Bağlı: {status['connected']}")
        print(f"  - Durum: {status['status']}")
        print(f"  - Cihaz: {status['device']}")
    except Exception as e:
        print(f"✗ Manager hatası: {e}")
        return False
    
    # Adım 5: Test yazdırma (opsiyonel)
    print("\n5️⃣  Test Yazdırma (İsteğe Bağlı)")
    print("-" * 40)
    
    try:
        response = input("Test etiketi yazdırmak ister misiniz? (E/H): ").strip().upper()
        
        if response == 'E':
            print("Test etiketi yazdırılıyor...")
            
            # Basit test
            printer.clear_buffer()
            
            printer.print_text(
                text="TEST ETIKET",
                x=20, y=20,
                font="1", size="2", bold=True
            )
            
            printer.print_qrcode(
                qr_data="TEST_QR_CODE_12345",
                x=100, y=80,
                size=8, eccl="H"
            )
            
            printer.print_label(label_count=1)
            
            print("✓ Test etiketi gönderildi")
            print("  (Yazıcı aynı anda yazdırmalı)")
        
    except Exception as e:
        print(f"✗ Yazdırma hatası: {e}")
        return False
    
    # Sonuç
    print("\n" + "="*50)
    print("✓ TÜM TESTLER BAŞARILI")
    print("="*50)
    print("\nYazıcı hazır! app.py ile kullanabilirsiniz.")
    print("\nKullanım örneği:")
    print("-" * 40)
    print("""
from printer_integration import get_printer_manager

manager = get_printer_manager()
manager.print_qr_label(
    qr_data="ENVANTER_123456",
    label_text="Ürün Adı",
    quantity=1
)
    """)
    
    return True


if __name__ == "__main__":
    try:
        success = test_printer_device()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test iptal edildi")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
        sys.exit(1)
