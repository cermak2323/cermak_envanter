#!/usr/bin/env python3
"""
Yazıcı entegrasyonu - app.py ile birlikte kullanılır
Ubuntu sunucuda QR kod ve barkod yazdırma işlemleri
"""

from tspl_printer import TSPLPrinter
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class PrinterManager:
    """
    Yazıcı yönetimi ve etiket yazdırma işlemleri
    """
    
    _instance: Optional['PrinterManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.printer = TSPLPrinter()
        self._initialized = True
        self._configure_printer()
    
    def _configure_printer(self):
        """Yazıcıyı varsayılan ayarlarla yapılandırır"""
        if not self.printer.connected:
            logger.warning("Yazıcı bağlanmadı")
            return
        
        self.printer.set_label_size(100, 150)  # 100x150mm
        self.printer.set_gap(2.0)  # 2mm boşluk
        self.printer.set_darkness(10)  # Orta koyuluk
        self.printer.set_speed(4)  # Normal hız
    
    def print_qr_label(
        self,
        qr_data: str,
        label_text: str = "",
        quantity: int = 1,
        auto_print: bool = True
    ) -> bool:
        """
        QR kodlu etiket yazdırır
        
        Args:
            qr_data: QR kod içeriği
            label_text: Etiket üzerindeki metin
            quantity: Yazdırılacak kopya sayısı
            auto_print: Otomatik yazdırma
        """
        try:
            self.printer.clear_buffer()
            
            # QR kodu orta konuma yerleştir
            self.printer.print_qrcode(
                qr_data=qr_data,
                x=150,
                y=20,
                size=8,
                eccl="H"
            )
            
            # Metin ekle
            if label_text:
                self.printer.print_text(
                    text=label_text,
                    x=20,
                    y=100,
                    font="1",
                    size="2"
                )
            
            # Yazdır
            if auto_print:
                self.printer.print_label(label_count=quantity)
            
            logger.info(f"QR etiketi yazdırıldı: {qr_data[:20]}...")
            return True
        
        except Exception as e:
            logger.error(f"QR etiket yazdırma hatası: {e}")
            return False
    
    def print_barcode_label(
        self,
        barcode_data: str,
        barcode_type: str = "CODE128",
        label_text: str = "",
        quantity: int = 1,
        auto_print: bool = True
    ) -> bool:
        """
        Barkodlu etiket yazdırır
        
        Args:
            barcode_data: Barkod verileri
            barcode_type: Barkod türü
            label_text: Etiket metni
            quantity: Kopya sayısı
            auto_print: Otomatik yazdırma
        """
        try:
            self.printer.clear_buffer()
            
            # Barkodu yazdır
            self.printer.print_barcode(
                barcode_data=barcode_data,
                barcode_type=barcode_type,
                x=50,
                y=30,
                height=60,
                width=2
            )
            
            # Metin ekle
            if label_text:
                self.printer.print_text(
                    text=label_text,
                    x=20,
                    y=100,
                    font="1",
                    size="2"
                )
            
            if auto_print:
                self.printer.print_label(label_count=quantity)
            
            logger.info(f"Barkod etiketi yazdırıldı: {barcode_data}")
            return True
        
        except Exception as e:
            logger.error(f"Barkod etiket yazdırma hatası: {e}")
            return False
    
    def print_combined_label(
        self,
        qr_data: str,
        barcode_data: str = "",
        title: str = "",
        quantity: int = 1,
        auto_print: bool = True
    ) -> bool:
        """
        QR + Barkod kombinasyonu yazdırır
        
        Args:
            qr_data: QR kod içeriği
            barcode_data: Barkod (opsiyonel)
            title: Başlık
            quantity: Kopya sayısı
            auto_print: Otomatik yazdırma
        """
        try:
            self.printer.clear_buffer()
            
            # Başlık
            if title:
                self.printer.print_text(
                    text=title,
                    x=20,
                    y=10,
                    font="1",
                    size="1",
                    bold=True
                )
            
            # QR kod (sol taraf)
            self.printer.print_qrcode(
                qr_data=qr_data,
                x=20,
                y=40,
                size=6,
                eccl="H"
            )
            
            # Barkod (sağ taraf)
            if barcode_data:
                self.printer.print_barcode(
                    barcode_data=barcode_data,
                    barcode_type="CODE128",
                    x=250,
                    y=50,
                    height=50,
                    width=2
                )
            
            if auto_print:
                self.printer.print_label(label_count=quantity)
            
            logger.info("Kombinasyon etiketi yazdırıldı")
            return True
        
        except Exception as e:
            logger.error(f"Kombinasyon etiketi yazdırma hatası: {e}")
            return False
    
    def test_print(self) -> bool:
        """Test etiketi yazdırır"""
        return self.print_qr_label(
            qr_data="TEST_QR_CODE",
            label_text="Test Etiketi",
            quantity=1
        )
    
    def get_status(self) -> dict:
        """Yazıcı durumunu döndürür"""
        return {
            "connected": self.printer.connected,
            "status": self.printer.status(),
            "device": self.printer.device_path
        }


def get_printer_manager() -> PrinterManager:
    """PrinterManager singleton örneğini döndürür"""
    return PrinterManager()
