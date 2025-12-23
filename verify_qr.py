#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""QR dosyalarının içeriğini doğrula"""

from pyzbar.pyzbar import decode
from PIL import Image
import os

qr_dir = r"\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\static\qr_codes"
files = os.listdir(qr_dir)[:10]

print("QR Dosya Kontrolu:")
print("="*60)
for f in files:
    filepath = os.path.join(qr_dir, f)
    try:
        img = Image.open(filepath)
        decoded = decode(img)
        if decoded:
            content = decoded[0].data.decode('utf-8')
            expected = f.replace(".png", "")
            match = "✓ DOGRU" if content == expected else "✗ YANLIS"
            print(f"{f}")
            print(f"  QR Icerik: {content}")
            print(f"  Beklenen:  {expected}")
            print(f"  Sonuc:     {match}")
            print()
    except Exception as e:
        print(f"{f} - hata: {e}")
