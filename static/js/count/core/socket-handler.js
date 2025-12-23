/**
 * 🔌 SOCKET HANDLER - WebSocket yönetimi (SADECE MESAJLAŞMA)
 * Sorumluluk: Socket bağlantısı, mesaj gönder/al
 */

class SocketHandler {
    constructor() {
        this.socket = null;
        this.onScanResult = null;
        this.onSessionReset = null;
        this.onCountFinished = null;
        
        // Config'den ayarları oku
        this.config = window.APP_CONFIG?.SOCKET || {};
        
        if (window.logger) {
            window.logger.info('SocketHandler başlatılıyor...');
        }
    }

    /**
     * Socket bağlantısını başlat
     */
    connect(callbacks = {}) {
        if (window.logger) window.logger.info('Socket bağlantısı başlatılıyor...');

        this.onScanResult = callbacks.onScanResult;
        this.onSessionReset = callbacks.onSessionReset;
        this.onCountFinished = callbacks.onCountFinished;

        this.socket = io({
            reconnection: this.config.RECONNECTION !== false,
            reconnectionDelay: this.config.RECONNECTION_DELAY || 1000,
            reconnectionDelayMax: this.config.RECONNECTION_DELAY_MAX || 5000,
            reconnectionAttempts: this.config.RECONNECTION_ATTEMPTS || 10,
            transports: ['websocket', 'polling']
        });

        // Bağlantı başarılı
        this.socket.on('connect', () => {
            if (window.logger) {
                window.logger.success('WebSocket bağlandı', { id: this.socket.id });
            }
            
            if (window.eventBus) {
                window.eventBus.emit(window.EVENTS.SOCKET_CONNECTED);
            }
            
            if (window.showFullScreenMessage) {
                window.showFullScreenMessage('✅ Bağlantı kuruldu', true);
            }
        });

        // Bağlantı kesildi
        this.socket.on('disconnect', () => {
            if (window.logger) window.logger.warn('WebSocket bağlantısı kesildi');
            
            if (window.eventBus) {
                window.eventBus.emit(window.EVENTS.SOCKET_DISCONNECTED);
            }
            
            if (window.showFullScreenMessage) {
                window.showFullScreenMessage('❌ Bağlantı kesildi', false);
            }
        });

        // QR okuma sonucu
        this.socket.on('scan_result', (data) => {
            if (window.logger) {
                window.logger.info('Scan result alındı', data);
            }
            if (this.onScanResult) {
                this.onScanResult(data);
            }
        });

        // Session sıfırlandı
        this.socket.on('session_reset', (data) => {
            if (window.logger) window.logger.info('Session reset', data);
            if (this.onSessionReset) {
                this.onSessionReset(data);
            }
        });

        // Sayım bitti
        this.socket.on('count_finished', (data) => {
            if (window.logger) window.logger.info('Count finished', data);
            if (this.onCountFinished) {
                this.onCountFinished(data);
            }
        });

        return this.socket;
    }

    /**
     * QR kodu gönder
     */
    sendQR(qrCode) {
        if (this.socket && this.socket.connected) {
            if (window.logger) {
                window.logger.debug('QR gönderiliyor', qrCode);
            }
            this.socket.emit('scan_qr', { qr_id: qrCode });
            return true;
        } else {
            console.error('❌ Socket bağlı değil!');
            return false;
        }
    }

    /**
     * Bağlantı durumu
     */
    isConnected() {
        return this.socket && this.socket.connected;
    }

    /**
     * Bağlantıyı kapat
     */
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            console.log('🔌 Socket bağlantısı kapatıldı');
        }
    }
}

// Global export
window.SocketHandler = SocketHandler;
