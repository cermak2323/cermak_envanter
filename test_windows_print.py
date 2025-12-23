#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TSPL to Windows Print via Print Spooler
4BARCODE yazıcıya Windows Print Spooler'ı kullanarak erişim
"""

import os
import sys
import logging
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import ctypes
import struct

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Windows print API bindings
try:
    import win32print
    import win32api
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False
    logger.warning("win32print not installed, using alternative method")

def print_to_windows_printer(printer_name: str, command: bytes):
    """
    Windows Print Spooler'ı kullanarak yazıcıya gönder
    
    Args:
        printer_name: Yazıcı adı (Device Manager'da gösterilen)
        command: Gönderilecek veri (bytes)
    """
    if HAS_WIN32:
        try:
            logger.info(f"Opening printer: {printer_name}")
            handle = win32print.OpenPrinter(printer_name)
            
            logger.info(f"Starting document")
            job_id = win32print.StartDocPrinter(
                handle, 1, 
                ("TSPL Label", None, "RAW")
            )
            
            logger.info(f"Writing {len(command)} bytes to printer")
            win32print.WritePrinter(handle, command)
            
            logger.info(f"Ending document")
            win32print.EndDocPrinter(handle)
            
            logger.info(f"Closing printer")
            win32print.ClosePrinter(handle)
            
            logger.info("[✓] Print job sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"[✗] Print failed: {e}")
            return False
    else:
        logger.error("win32print module not available")
        return False

def test_print():
    """Test yazıcıya TSPL komutu gönder"""
    logger.info("=" * 60)
    logger.info("Testing TSPL via Windows Print Spooler")
    logger.info("=" * 60)
    
    printer_name = "4BARCODE 4B-2054TF"
    
    # TSPL komutları oluştur
    tspl_commands = b"""SIZE 100 MM, 150 MM
GAP 3 MM, 0 MM
CLS
TEXT 10,10,"1",0,1,1,"TEST LABEL"
BARCODE 10,40,QR,6,A,0,"TEST_QR_DATA"
PRINT 1
"""
    
    logger.info(f"Printer: {printer_name}")
    logger.info(f"Command length: {len(tspl_commands)} bytes")
    logger.info(f"Commands:\n{tspl_commands.decode('utf-8', errors='ignore')}")
    
    return print_to_windows_printer(printer_name, tspl_commands)

if __name__ == '__main__':
    try:
        success = test_print()
        if success:
            logger.info("\n[✓] Test completed - check printer for output")
        else:
            logger.error("\n[✗] Test failed - see error messages above")
            
            # Alternative: Check if printer is available
            if HAS_WIN32:
                logger.info("\nAvailable printers:")
                for printer_name in win32print.EnumPrinters(4, None, 1):
                    logger.info(f"  - {printer_name}")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
