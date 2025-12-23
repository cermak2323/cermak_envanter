#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test TSPL Printer with updated Windows Print Spooler implementation
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Import TSPL
from tspl_printer import TSPLManager

def test_manager():
    """TSPLManager ile QR yazdırmayı test et"""
    logger.info("=" * 60)
    logger.info("Testing TSPLManager with Windows Print Spooler")
    logger.info("=" * 60)
    
    # Manager'ı oluştur
    manager = TSPLManager(printer_host="4BARCODE 4B-2054TF", printer_port=9100)
    
    # Test print with quantity=3 to test multiple PRINT commands
    success, message = manager.print_qr_code(
        qr_id="TEST_QR_001",
        part_code="TEST-001",
        part_name="Test Part",
        quantity=3  # Test multiple copies
    )
    
    logger.info(f"\nPrint Result:")
    logger.info(f"  Success: {success}")
    logger.info(f"  Message: {message}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Test Complete - Check printer for output")
    logger.info("=" * 60)

if __name__ == '__main__':
    test_manager()
