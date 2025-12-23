#!/usr/bin/env python3
"""
TSPL Printer Module for Ubuntu/Linux
USB üzerinden doğrudan TSPL komutları /dev/usb/lp0'a gönderir
"""

import os
import sys
import logging
from typing import Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class TSPLPrinter:
    """
    TSPL (Thermal Sensitive Printer Language) yazıcısı için Linux/Ubuntu sürücüsü
    USB bağlantısı üzerinden RAW komutlar gönderir
    """
    
    def __init__(self, device_path: str = "/dev/usb/lp0", timeout: int = 5):
        """
        Yazıcı bağlantısını başlatır
        
        Args:
            device_path: USB yazıcı cihazı (/dev/usb/lp0)
            timeout: Bağlantı zaman aşımı (saniye)
        """
        self.device_path = device_path
        self.timeout = timeout
        self.connected = False
        self._verify_device()
    
    def _verify_device(self) -> bool:
        """USB cihazın mevcut olduğunu kontrol eder"""
        if not os.path.exists(self.device_path):
            logger.warning(f"USB yazıcı bulunamadı: {self.device_path}")
            return False
        
        if not os.access(self.device_path, os.W_OK):
            logger.warning(f"USB yazıcıya yazma izni yok: {self.device_path}")
            logger.info("Sudo ile çalıştırın veya /etc/udev/rules.d/ kurallarını ayarlayın")
            return False
        
        self.connected = True
        logger.info(f"USB yazıcı hazır: {self.device_path}")
        return True
    
    def _send_command(self, command: bytes) -> bool:
        """
        TSPL komutunu yazıcıya gönderir
        
        Args:
            command: Gönderilecek byte komut
            
        Returns:
            Başarıyı gösteren bool
        """
        if not self.connected:
            logger.error("Yazıcı bağlı değil")
            return False
        
        try:
            with open(self.device_path, 'wb') as printer:
                printer.write(command)
                printer.flush()
            logger.debug(f"Komut gönderildi: {command[:50]}...")
            return True
        except IOError as e:
            logger.error(f"Yazıcı yazma hatası: {e}")
            return False
        except Exception as e:
            logger.error(f"Beklenmeyen hata: {e}")
            return False
    
    def initialize(self) -> bool:
        """Yazıcıyı başlatır"""
        return self._send_command(b"SIZE 100mm,150mm\r\n")
    
    def reset(self) -> bool:
        """Yazıcıyı sıfırlar"""
        return self._send_command(b"SIZE 100mm,150mm\r\n")
    
    def set_speed(self, speed: int = 4) -> bool:
        """
        Yazdırma hızını ayarlar (1-5)
        
        Args:
            speed: Hız seviyesi 1-5
        """
        speed = max(1, min(5, speed))
        return self._send_command(f"SPEED {speed}\r\n".encode())
    
    def set_darkness(self, darkness: int = 8) -> bool:
        """
        Koyuluk seviyesini ayarlar (0-15)
        
        Args:
            darkness: Koyuluk değeri 0-15
        """
        darkness = max(0, min(15, darkness))
        return self._send_command(f"DENSITY {darkness}\r\n".encode())
    
    def set_label_size(self, width_mm: float, height_mm: float) -> bool:
        """
        Etiket boyutunu ayarlar (mm cinsinden)
        
        Args:
            width_mm: Etiket genişliği
            height_mm: Etiket yüksekliği
        """
        return self._send_command(f"SIZE {width_mm}mm,{height_mm}mm\r\n".encode())
    
    def set_gap(self, gap_mm: float = 2.0) -> bool:
        """
        Etiketler arası boşluğu ayarlar
        
        Args:
            gap_mm: Boşluk miktarı (mm)
        """
        return self._send_command(f"GAP {gap_mm}mm\r\n".encode())
    
    def print_qrcode(
        self,
        qr_data: str,
        x: int = 10,
        y: int = 10,
        size: int = 8,
        eccl: str = "L"
    ) -> bool:
        """
        QR kodu yazdırır
        
        Args:
            qr_data: QR kodunun içeriği
            x: X konumu (nokta)
            y: Y konumu (nokta)
            size: QR kod boyutu (1-14)
            eccl: Hata düzeltme seviyesi (L,M,Q,H)
        """
        size = max(1, min(14, size))
        if eccl not in ["L", "M", "Q", "H"]:
            eccl = "L"
        
        command = f"BARCODE {x} {y} QR {size} {eccl} 0\n{qr_data}\nENDBAR\r\n"
        return self._send_command(command.encode())
    
    def print_barcode(
        self,
        barcode_data: str,
        barcode_type: str = "CODE128",
        x: int = 10,
        y: int = 10,
        height: int = 50,
        width: int = 2
    ) -> bool:
        """
        Barkodu yazdırır
        
        Args:
            barcode_data: Barkod verileri
            barcode_type: Barkod türü (CODE128, EAN13, vb.)
            x: X konumu
            y: Y konumu
            height: Yükseklik
            width: Çubuk genişliği
        """
        command = f"BARCODE {x} {y} \"{barcode_type}\" {height} {width}\n{barcode_data}\nENDBAR\r\n"
        return self._send_command(command.encode())
    
    def print_text(
        self,
        text: str,
        x: int = 10,
        y: int = 10,
        font: str = "1",
        size: str = "1",
        bold: bool = False
    ) -> bool:
        """
        Metin yazdırır
        
        Args:
            text: Yazdırılacak metin
            x: X konumu
            y: Y konumu
            font: Font numarası (0-7)
            size: Boyut (1-8)
            bold: Kalın yazı
        """
        bold_str = "1" if bold else "0"
        command = f"TEXT {x} {y} \"{font}\" {size} {bold_str}\n{text}\r\n"
        return self._send_command(command.encode())
    
    def print_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        thickness: int = 1
    ) -> bool:
        """
        Çizgi çizer
        
        Args:
            x1, y1: Başlangıç noktası
            x2, y2: Bitiş noktası
            thickness: Çizgi kalınlığı
        """
        command = f"LINE {x1} {y1} {x2} {y2} {thickness}\r\n"
        return self._send_command(command.encode())
    
    def print_label(self, label_count: int = 1, pause: bool = False) -> bool:
        """
        Etiket yazdırır
        
        Args:
            label_count: Yazdırılacak etiket sayısı
            pause: Yazdırmadan önce duraklat
        """
        if pause:
            return self._send_command(f"PRINT {label_count} 0\r\n".encode())
        return self._send_command(f"PRINT {label_count} 1\r\n".encode())
    
    def clear_buffer(self) -> bool:
        """Yazıcı tamponunu temizler"""
        return self._send_command(b"CLS\r\n")
    
    def status(self) -> str:
        """Yazıcı durumunu döndürür"""
        if not self.connected:
            return "Bağlı değil"
        return "Hazır"
    
    def close(self):
        """Yazıcı bağlantısını kapatır"""
        self.connected = False
        logger.info("Yazıcı bağlantısı kapatıldı")


# Basit kullanım örneği
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    printer = TSPLPrinter()
    
    if printer.connected:
        printer.initialize()
        printer.set_darkness(10)
        printer.set_speed(4)
        print("Yazıcı hazır")
    else:
        print("Yazıcı bağlanamadı")
