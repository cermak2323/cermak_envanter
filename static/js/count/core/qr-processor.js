/**
 * 🔍 QR PROCESSOR - ZXing Edition
 * QR kod işleme, doğrulama ve backend iletişimi
 * ZXing otomatik okuma yapıyor, sadece business logic burada
 */

class QRProcessor {
    constructor(apiService, uiManager) {
        this.apiService = apiService;
        this.uiManager = uiManager;
        this.scannedCodes = new Set();
        this.isProcessing = false;
        this.lastScanTime = 0;
        this.SCAN_COOLDOWN = 500; // 500ms (yarım saniye) - daha responsive
        
        console.log('🔍 QRProcessor initialized - Cooldown: 500ms');
    }

    /**
     * QR kod okunduğunda çağrılır
     * @param {string} decodedText - QR kod içeriği
     */
    async handleQRCode(decodedText) {
        try {
            console.log('🔍🔍🔍 QR PROCESSOR handleQRCode ÇAĞRILDI! 🔍🔍🔍');
            console.log('📝 Decoded Text:', decodedText);
            
            // Boş kod kontrolü
            if (!decodedText || decodedText.trim() === '') {
                console.warn('⚠️ Boş QR kod');
                return;
            }

            const now = Date.now();
            
            // Cooldown kontrolü (çok hızlı okuma önleme)
            if (now - this.lastScanTime < this.SCAN_COOLDOWN) {
                console.log('⏳ Cooldown aktif (500ms), QR işlenmedi');
                return;
            }

            // Duplicate kontrolü (aynı QR tekrar okunmasın)
            if (this.scannedCodes.has(decodedText)) {
                console.log('⚠️ Bu QR zaten okundu:', decodedText);
                this.uiManager.showDuplicateMessage(decodedText);
                this.lastScanTime = now;
                return;
            }

            // İşlem devam ediyorsa bekle
            if (this.isProcessing) {
                console.log('⏳ QR işleme devam ediyor, bekleyin...');
                return;
            }

            this.isProcessing = true;
            this.lastScanTime = now;

            console.log('✅ YENİ QR KOD OKUNDU:', decodedText);
            console.log('🚀 Backend\'e gönderiliyor...');
            
            // Backend'e gönder
            await this.processQRCode(decodedText);
            
            // Okunan kodlar listesine ekle
            this.scannedCodes.add(decodedText);
            
            console.log('✅ QR işleme tamamlandı!');
            
        } catch (error) {
            console.error('❌ QR işleme hatası:', error);
            this.uiManager.showErrorMessage(error.message || 'QR kod işlenemedi');
        } finally {
            this.isProcessing = false;
        }
    }

    /**
     * QR kodu backend'e gönder ve işle
     */
    async processQRCode(qrCode) {
        try {
            console.log('📤 Backend\'e QR gönderiliyor:', qrCode);
            
            // UI feedback (okuma başladı)
            this.uiManager.showScanningMessage();
            
            // Backend API çağrısı
            const response = await this.apiService.submitQRScan(qrCode);
            
            if (response.success) {
                console.log('✅ QR başarıyla işlendi:', response);
                
                // Başarı mesajı göster
                this.uiManager.showSuccessMessage(
                    response.part_name || 'Parça',
                    response.current_count || 0,
                    response.expected_count || 0
                );
                
                // WebSocket ile diğer kullanıcıları bilgilendir
                if (window.socketHandler) {
                    window.socketHandler.emitScan({
                        qr_code: qrCode,
                        part_name: response.part_name,
                        count: response.current_count
                    });
                }
                
            } else {
                console.error('❌ Backend hatası:', response.message);
                this.uiManager.showErrorMessage(response.message || 'QR kod işlenemedi');
                
                // Hatalı kod listeden çıkar (tekrar denenebilsin)
                this.scannedCodes.delete(qrCode);
            }
            
        } catch (error) {
            console.error('❌ Backend iletişim hatası:', error);
            this.uiManager.showErrorMessage('Sunucu bağlantısı kurulamadı');
            
            // Hatalı kod listeden çıkar
            this.scannedCodes.delete(qrCode);
            throw error;
        }
    }

    /**
     * İşleme hatası durumunda
     */
    handleError(error) {
        // Sadece ciddi hataları logla (NotFoundException normal)
        if (error && error.name !== 'NotFoundException') {
            console.error('❌ QR okuma hatası:', error);
        }
    }

    /**
     * Okunan kodları temizle
     */
    clearScannedCodes() {
        this.scannedCodes.clear();
        console.log('🗑️ Okunan kodlar temizlendi');
    }

    /**
     * Belirli bir kodu listeden çıkar
     */
    removeScannedCode(qrCode) {
        this.scannedCodes.delete(qrCode);
        console.log('🗑️ QR kod listeden çıkarıldı:', qrCode);
    }

    /**
     * Okunan kod sayısı
     */
    getScannedCount() {
        return this.scannedCodes.size;
    }

    /**
     * Temizlik
     */
    destroy() {
        this.clearScannedCodes();
        this.isProcessing = false;
        console.log('🗑️ QRProcessor temizlendi');
    }
}

// Global export
window.QRProcessor = QRProcessor;
console.log('✅ QRProcessor (ZXing) yüklendi');
