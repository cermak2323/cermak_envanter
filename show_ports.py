#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
COM Port ve Device Info
USB device türünü ve bağlantı bilgisini kontrol
"""

import os
import sys
import logging
from serial.tools import list_ports

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def show_port_info():
    """COM port bilgisini göster"""
    logger.info("=" * 60)
    logger.info("COM Port and Device Information")
    logger.info("=" * 60)
    
    ports = list_ports.comports()
    
    if not ports:
        logger.warning("No COM ports found!")
        return
    
    logger.info(f"\nFound {len(ports)} COM port(s):\n")
    
    for p in ports:
        logger.info(f"Port: {p.device}")
        logger.info(f"  Description: {p.description}")
        logger.info(f"  Manufacturer: {p.manufacturer}")
        logger.info(f"  Serial Number: {p.serial_number}")
        logger.info(f"  Location: {p.location}")
        logger.info(f"  VID:PID: {p.vid}:{p.pid}")
        logger.info("")

if __name__ == '__main__':
    show_port_info()
