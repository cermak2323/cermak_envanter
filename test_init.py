#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TSPL Printer Initialization Test
Yazıcı başlatma komutları test
"""

import os
import sys
import logging
import serial
import time

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_initialization():
    """Yazıcı başlatma komutlarını test et"""
    logger.info("=" * 60)
    logger.info("Testing TSPL Printer Initialization")
    logger.info("=" * 60)
    
    test_port = 'COM1'
    baudrate = 9600
    
    try:
        logger.info(f"\nOpening {test_port} at {baudrate} baud")
        port = serial.Serial(
            port=test_port,
            baudrate=baudrate,
            timeout=1,
            stopbits=1,
            bytesize=8
        )
        
        # Test 1: STATUS
        logger.info("\n[1] Testing STATUS command...")
        port.write(b"STATUS\n")
        port.flush()
        time.sleep(0.5)
        response = port.read(100)
        logger.info(f"    Response: {response}")
        
        # Test 2: RESET
        logger.info("\n[2] Testing RESET command...")
        port.write(b"RESET\n")
        port.flush()
        time.sleep(0.5)
        response = port.read(100)
        logger.info(f"    Response: {response}")
        
        # Test 3: VERSION
        logger.info("\n[3] Testing VERSION command...")
        port.write(b"VERSION\n")
        port.flush()
        time.sleep(0.5)
        response = port.read(100)
        logger.info(f"    Response: {response}")
        
        # Test 4: SELFTEST (etiket çıktısı)
        logger.info("\n[4] Testing SELFTEST command...")
        port.write(b"SELFTEST\n")
        port.flush()
        time.sleep(2)  # Self test için daha uzun bekleme
        response = port.read(100)
        logger.info(f"    Response: {response}")
        logger.info("    [!] Check if printer produced test output")
        
        port.close()
        logger.info("\n[✓] Port closed")
        
    except Exception as e:
        logger.error(f"[✗] Error: {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Test Complete")
    logger.info("=" * 60)

if __name__ == '__main__':
    test_initialization()
