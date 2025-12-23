/**
 * TSPL Barcode Printer QR Integration
 * QR kod generation sırasında TSPL yazıcıya gönderim
 */

class TSPLPrinterHelper {
    constructor() {
        this.enabled = false;
        this.host = 'localhost';
        this.port = 9100;
        this.connected = false;
        
        // Başlat
        this.checkStatus();
    }
    
    /**
     * TSPL yazıcı durumunu kontrol et
     */
    async checkStatus() {
        try {
            const response = await fetch('/api/tspl/status', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            this.enabled = data.enabled;
            this.connected = data.connected;
            this.host = data.printer_host;
            this.port = data.printer_port;
            
            console.log('[TSPL]', {
                enabled: this.enabled,
                connected: this.connected,
                host: this.host,
                port: this.port
            });
            
            return data;
        } catch (error) {
            console.error('[TSPL] Status check failed:', error);
            this.enabled = false;
            this.connected = false;
            return null;
        }
    }
    
    /**
     * Test yazdırması (tüm QR'lar oluşturulduktan sonra)
     */
    async testPrint() {
        try {
            if (!this.enabled || !this.connected) {
                console.warn('[TSPL] Printer not available for test');
                return false;
            }
            
            const response = await fetch('/api/tspl/test-print', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    qr_id: 'TEST_QR_001',
                    part_code: 'TEST',
                    part_name: 'Test Print'
                })
            });
            
            const data = await response.json();
            console.log('[TSPL] Test print result:', data);
            
            return data.success;
        } catch (error) {
            console.error('[TSPL] Test print error:', error);
            return false;
        }
    }
    
    /**
     * QR kodu TSPL yazıcıdan çıktı al
     */
    async printQR(qrId, quantity = 1) {
        try {
            if (!this.enabled || !this.connected) {
                console.warn('[TSPL] Printer not available');
                return false;
            }
            
            const response = await fetch(`/api/tspl/print-qr/${qrId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    quantity: quantity
                })
            });
            
            const data = await response.json();
            console.log(`[TSPL] Print QR ${qrId}:`, data);
            
            return data.success;
        } catch (error) {
            console.error(`[TSPL] Print error for ${qrId}:`, error);
            return false;
        }
    }
    
    /**
     * Batch QR yazdırması
     */
    async printBatch(qrIds) {
        try {
            if (!this.enabled || !this.connected) {
                console.warn('[TSPL] Printer not available');
                return null;
            }
            
            const response = await fetch('/api/tspl/print-batch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    qr_ids: qrIds
                })
            });
            
            const data = await response.json();
            console.log('[TSPL] Batch print result:', data);
            
            return data;
        } catch (error) {
            console.error('[TSPL] Batch print error:', error);
            return null;
        }
    }
    
    /**
     * Konfigürasyonu güncelle (admin only)
     */
    async updateConfig(host, port, enabled) {
        try {
            const response = await fetch('/api/tspl/config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    host: host,
                    port: port,
                    enabled: enabled
                })
            });
            
            const data = await response.json();
            console.log('[TSPL] Config updated:', data);
            
            return data;
        } catch (error) {
            console.error('[TSPL] Config update error:', error);
            return null;
        }
    }
}

// Global instance
const tsplPrinter = new TSPLPrinterHelper();

/**
 * Generate QR ve isteğe bağlı TSPL yazdırması
 */
async function generateQRWithTSPL(partCode, quantity = 1, printToTSPL = false) {
    try {
        const response = await fetch(`/generate_qr/${partCode}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                quantity: quantity,
                print_to_tspl: printToTSPL && tsplPrinter.enabled && tsplPrinter.connected
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log(`[QR] ${quantity} QR codes generated for ${partCode}`);
            
            // TSPL sonuçlarını kontrol et
            if (data.tspl_results) {
                console.log('[QR] TSPL Results:', data.tspl_results);
                
                // UI'ye sonuçları göster
                const successful = data.tspl_results.filter(r => r.success).length;
                const total = data.tspl_results.length;
                
                if (successful === total) {
                    showNotification(
                        `✓ ${total} QR codes generated and printed via TSPL`,
                        'success'
                    );
                } else {
                    showNotification(
                        `⚠ ${successful}/${total} QR codes printed via TSPL`,
                        'warning'
                    );
                }
            } else if (printToTSPL) {
                showNotification(
                    `✓ ${quantity} QR codes generated (TSPL not configured)`,
                    'info'
                );
            } else {
                showNotification(
                    `✓ ${quantity} QR codes generated`,
                    'success'
                );
            }
        } else {
            showNotification(
                `✗ Failed to generate QR codes: ${data.error || 'Unknown error'}`,
                'error'
            );
        }
        
        return data;
    } catch (error) {
        console.error('[QR] Generation error:', error);
        showNotification(`✗ Error: ${error.message}`, 'error');
        return null;
    }
}

/**
 * UI notification helper (Mevcut sistemle entegrasyon)
 */
function showNotification(message, type = 'info') {
    // Bootstrap toast veya diğer notification sistemine uyarla
    console.log(`[NOTIFICATION] ${type.toUpperCase()}: ${message}`);
    
    // Eğer bootstrap toast kullanılıyorsa:
    if (typeof bootstrap !== 'undefined') {
        const toastElement = document.createElement('div');
        toastElement.className = `alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'warning'} alert-dismissible fade show`;
        toastElement.setAttribute('role', 'alert');
        toastElement.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        const container = document.getElementById('notification-container') || document.body;
        container.insertBefore(toastElement, container.firstChild);
        
        // 5 saniye sonra otomatik kapat
        setTimeout(() => toastElement.remove(), 5000);
    }
}
