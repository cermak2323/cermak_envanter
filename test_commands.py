#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
4BARCODE Printer - Komut Test
Farklı TSPL komutlarını test et
"""

import logging
from tspl_printer import TSPLManager

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(message)s'
)

def test_simple_commands():
    """Basit komutları test et"""
    manager = TSPLManager(printer_host="4BARCODE 4B-2054TF", printer_port=9100)
    printer = manager.get_printer()
    
    # Test 1: Sadece TEXT
    print("\n[TEST 1] Only TEXT command")
    printer.connect()
    win32print = __import__('win32print')
    job_id = win32print.StartDocPrinter(printer.handle, 1, ("TEST", None, "RAW"))
    
    commands = """SIZE 100 MM, 100 MM
GAP 2 MM, 0 MM
CLS
TEXT 50,50,"2",0,1,1,"TEST"
PRINT 1
"""
    for cmd in commands.strip().split('\n'):
        win32print.WritePrinter(printer.handle, (cmd + '\n').encode('utf-8'))
        print(f"  Sent: {cmd}")
    
    win32print.EndDocPrinter(printer.handle)
    printer.disconnect()
    print("  Check printer - should print 'TEST' text")
    
    input("\nPress Enter after checking Test 1...")
    
    # Test 2: BARCODE komutu
    print("\n[TEST 2] BARCODE command (different syntax)")
    printer.connect()
    job_id = win32print.StartDocPrinter(printer.handle, 1, ("TEST2", None, "RAW"))
    
    commands = """SIZE 100 MM, 100 MM
GAP 2 MM, 0 MM
CLS
BARCODE 10,10,"128","100","40","0","123456"
PRINT 1
"""
    for cmd in commands.strip().split('\n'):
        win32print.WritePrinter(printer.handle, (cmd + '\n').encode('utf-8'))
        print(f"  Sent: {cmd}")
    
    win32print.EndDocPrinter(printer.handle)
    printer.disconnect()
    print("  Check printer - should print barcode")
    
    input("\nPress Enter after checking Test 2...")
    
    # Test 3: QR with different syntax
    print("\n[TEST 3] QR Code (alternative syntax)")
    printer.connect()
    job_id = win32print.StartDocPrinter(printer.handle, 1, ("TEST3", None, "RAW"))
    
    commands = """SIZE 100 MM, 100 MM
GAP 2 MM, 0 MM
CLS
TEXT 10,10,"1",0,1,1,"QR Test"
BARCODE 10,30,"QR","5","A","0","TEST_QR_DATA"
PRINT 1
"""
    for cmd in commands.strip().split('\n'):
        win32print.WritePrinter(printer.handle, (cmd + '\n').encode('utf-8'))
        print(f"  Sent: {cmd}")
    
    win32print.EndDocPrinter(printer.handle)
    printer.disconnect()
    print("  Check printer - should print text + QR code")

if __name__ == '__main__':
    test_simple_commands()
