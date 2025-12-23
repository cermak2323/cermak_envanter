#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
COM Port Baud Rate Test
Farklı baud rate'lerde yazıcı bağlantı testi
"""

import os
import sys
import logging
import serial
from serial.tools import list_ports

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_baud_rates():
    """Farklı baud rate'lerde test et"""
    logger.info("=" * 60)
    logger.info("Testing Baud Rates for TSPL Printer")
    logger.info("=" * 60)
    
    # COM portlarını listele
    logger.info("\n[1] Available COM Ports:")
    ports = list_ports.comports()
    for p in ports:
        logger.info(f"  - {p.device}: {p.description}")
    
    # Test et
    baud_rates = [9600, 19200, 38400, 57600, 115200]
    test_port = 'COM1'
    test_command = "SIZE 100 MM, 150 MM\n"
    
    logger.info(f"\n[2] Testing Baud Rates on {test_port}:")
    
    for baudrate in baud_rates:
        logger.info(f"\n  Baud Rate: {baudrate}")
        try:
            port = serial.Serial(
                port=test_port,
                baudrate=baudrate,
                timeout=1,
                stopbits=1,
                bytesize=8
            )
            logger.info(f"    [✓] Port opened successfully")
            
            # Test command gönder
            port.write(test_command.encode('utf-8'))
            logger.info(f"    [✓] Command sent: {test_command.strip()}")
            
            # Response okuma
            port.flush()
            response = port.read(100)
            if response:
                logger.info(f"    [!] Response received: {response}")
            else:
                logger.info(f"    [?] No response received")
            
            port.close()
            logger.info(f"    [✓] Port closed")
            
        except Exception as e:
            logger.error(f"    [✗] Error: {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Test Complete")
    logger.info("=" * 60)

if __name__ == '__main__':
    test_baud_rates()
