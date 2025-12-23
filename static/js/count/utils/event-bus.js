/**
 * 📡 EVENT BUS - Modüller arası haberleşme
 * Sorumluluk: Event pub/sub, loosely coupled modüller
 */

class EventBus {
    constructor() {
        this.events = {};
    }

    /**
     * Event'e abone ol
     * @param {string} eventName - Event adı
     * @param {function} callback - Çağrılacak fonksiyon
     */
    on(eventName, callback) {
        if (!this.events[eventName]) {
            this.events[eventName] = [];
        }
        this.events[eventName].push(callback);
        
        if (window.logger) {
            window.logger.debug(`Event dinleniyor: ${eventName}`);
        }
    }

    /**
     * Event'den aboneliği kaldır
     */
    off(eventName, callback) {
        if (!this.events[eventName]) return;
        
        this.events[eventName] = this.events[eventName].filter(cb => cb !== callback);
        
        if (window.logger) {
            window.logger.debug(`Event dinleme kaldırıldı: ${eventName}`);
        }
    }

    /**
     * Event yayınla
     * @param {string} eventName - Event adı
     * @param {any} data - Event verisi
     */
    emit(eventName, data = null) {
        if (!this.events[eventName]) return;

        if (window.logger) {
            window.logger.debug(`Event yayınlandı: ${eventName}`, data);
        }

        this.events[eventName].forEach(callback => {
            try {
                callback(data);
            } catch (error) {
                console.error(`Event callback hatası [${eventName}]:`, error);
            }
        });
    }

    /**
     * Bir kez dinle (auto-remove)
     */
    once(eventName, callback) {
        const onceCallback = (data) => {
            callback(data);
            this.off(eventName, onceCallback);
        };
        this.on(eventName, onceCallback);
    }

    /**
     * Tüm event'leri listele
     */
    listEvents() {
        return Object.keys(this.events);
    }

    /**
     * Event'leri temizle
     */
    clear() {
        this.events = {};
        if (window.logger) {
            window.logger.debug('Tüm event\'ler temizlendi');
        }
    }
}

// Global export
window.EventBus = EventBus;

// Global event bus instance
window.eventBus = new EventBus();

// Event adları (sabit - typo önleme)
window.EVENTS = {
    // Kamera
    CAMERA_STARTED: 'camera:started',
    CAMERA_STOPPED: 'camera:stopped',
    CAMERA_ERROR: 'camera:error',
    
    // QR
    QR_DETECTED: 'qr:detected',
    QR_SCANNED: 'qr:scanned',
    QR_DUPLICATE: 'qr:duplicate',
    QR_ERROR: 'qr:error',
    
    // Socket
    SOCKET_CONNECTED: 'socket:connected',
    SOCKET_DISCONNECTED: 'socket:disconnected',
    SCAN_RESULT: 'socket:scan_result',
    SESSION_RESET: 'socket:session_reset',
    COUNT_FINISHED: 'socket:count_finished',
    
    // UI
    STATS_UPDATED: 'ui:stats_updated',
    ACTIVITIES_LOADED: 'ui:activities_loaded',
    LIVE_COUNT_UPDATED: 'ui:live_count_updated',
    MESSAGE_SHOWN: 'ui:message_shown',
    
    // System
    APP_READY: 'app:ready',
    DATA_REFRESH: 'app:data_refresh'
};
