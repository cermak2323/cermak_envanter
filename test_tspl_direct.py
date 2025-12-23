#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Direct TSPL Printer Test
USB yazıcı ile doğrudan bağlantı testi
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Import TSPL
from tspl_printer import TSPLPrinter

def test_connection():
    """Yazıcı bağlantısını test et"""
    logger.info("=" * 60)
    logger.info("TSPL Printer Direct Connection Test")
    logger.info("=" * 60)
    
    # USB yazıcıya bağlan
    printer = TSPLPrinter(host='usb://4BARCODE', port=9100)
    
    logger.info(f"\nConnection Type: {printer.connection_type}")
    logger.info(f"Host: {printer.host}")
    logger.info(f"Port: {printer.port}")
    
    # Bağlantıyı dene
    logger.info("\n[TEST 1] Testing connection...")
    if printer.connect():
        logger.info("[✓] Connection successful!")
        
        # Basit komut gönder
        logger.info("\n[TEST 2] Sending SIZE command...")
        if printer.send_command("SIZE 100 MM, 150 MM"):
            logger.info("[✓] SIZE command sent successfully")
        else:
            logger.error("[✗] SIZE command failed")
        
        # GAP komut gönder
        logger.info("\n[TEST 3] Sending GAP command...")
        if printer.send_command("GAP 3 MM, 0 MM"):
            logger.info("[✓] GAP command sent successfully")
        else:
            logger.error("[✗] GAP command failed")
        
        # CLS komut gönder
        logger.info("\n[TEST 4] Sending CLS command...")
        if printer.send_command("CLS"):
            logger.info("[✓] CLS command sent successfully")
        else:
            logger.error("[✗] CLS command failed")
        
        # TEXT komut gönder
        logger.info("\n[TEST 5] Sending TEXT command...")
        if printer.send_command("TEXT 10,10,\"1\",0,1,1,\"TEST\""):
            logger.info("[✓] TEXT command sent successfully")
        else:
            logger.error("[✗] TEXT command failed")
        
        # PRINT komut gönder
        logger.info("\n[TEST 6] Sending PRINT command...")
        if printer.send_command("PRINT 1"):
            logger.info("[✓] PRINT command sent successfully")
            logger.info("[!] Check if printer produced output")
        else:
            logger.error("[✗] PRINT command failed")
        
        # Bağlantıyı kapat
        printer.disconnect()
        logger.info("\n[✓] Connection closed")
    else:
        logger.error("[✗] Connection failed!")
        return False
    
    logger.info("\n" + "=" * 60)
    logger.info("Test Complete")
    logger.info("=" * 60)
    return True

if __name__ == '__main__':
    test_connection()
