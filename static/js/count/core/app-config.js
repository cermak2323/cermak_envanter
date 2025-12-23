/**
 * ⚙️ Uygulama Konfigürasyonu
 * Tüm sabit değerler burada - değiştirmek için kod karıştırma yok!
 */

const APP_CONFIG = {
    // 📹 Kamera Ayarları
    CAMERA: {
        FPS: 10,                           // Kare/saniye (10 = hızlı + stabil)
        QR_BOX_SIZE: 0.7,                  // QR okuma kutusu boyutu (ekranın %70'i)
        FORCE_VISIBILITY_DELAY: 500,       // Video görünür yapma gecikmesi (ms)
        VISIBILITY_CHECK_INTERVAL: 1000,   // Video kontrol aralığı (ms)
        ASPECT_RATIO: 1.0                  // Kamera en-boy oranı
    },

    // 🔄 QR İşleme Ayarları
    QR: {
        DUPLICATE_TIMEOUT: 1000,           // Aynı QR için bekleme süresi (ms)
        PROCESSING_LOCK_TIMEOUT: 800,      // İşlem kilidi süresi (ms)
        MAX_RETRIES: 3                     // Maksimum yeniden deneme
    },

    // 🎨 UI Ayarları
    UI: {
        MESSAGE_DURATION: 2000,            // Tam ekran mesaj süresi (ms)
        REFRESH_INTERVAL: 10000,           // Auto-refresh aralığı (ms)
        FADE_DURATION: 300,                // Animasyon süresi (ms)
        ACTIVITY_LIMIT: 20                 // Maksimum aktivite sayısı
    },

    // 🔌 Socket Ayarları
    SOCKET: {
        RECONNECTION_DELAY: 1000,          // Yeniden bağlanma gecikmesi (ms)
        RECONNECTION_DELAY_MAX: 5000,      // Maksimum yeniden bağlanma gecikmesi (ms)
        RECONNECTION_ATTEMPTS: 10          // Maksimum deneme sayısı
    },

    // 🎵 Ses Ayarları
    SOUND: {
        SUCCESS_FREQUENCY: 800,            // Başarı sesi frekansı (Hz)
        SUCCESS_DURATION: 0.2,             // Başarı sesi süresi (s)
        ERROR_FREQUENCY: 300,              // Hata sesi frekansı (Hz)
        ERROR_DURATION: 0.4,               // Hata sesi süresi (s)
        VOLUME: 0.3                        // Ses seviyesi (0-1)
    },

    // 📱 Cihaz Ayarları
    DEVICE: {
        MOBILE_MAX_WIDTH: 768,             // Mobil cihaz max genişlik (px)
        PC_CAMERA_ENABLED: false           // PC'de kamera açık mı?
    },

    // 🎨 Z-Index Hierarchy
    Z_INDEX: {
        VIDEO: 10000,
        OVERLAY: 50000,
        QR_FRAME: 100000,
        MESSAGES: 9999999
    },

    // 🔗 API Endpoints (İsteğe bağlı - şimdilik kullanılmıyor)
    API: {
        CHECK_AUTH: '/check_auth',
        SESSION_STATS: '/get_session_stats',
        ACTIVITIES: '/get_recent_activities',
        LIVE_COUNT: '/get_live_count_status',
        SCAN_QR: 'scan_qr',
        EXPORT_LIVE: '/export_live_count'
    }
};

// Global export
window.APP_CONFIG = APP_CONFIG;

// Freeze config (değiştirilemez yap - güvenlik)
Object.freeze(APP_CONFIG.CAMERA);
Object.freeze(APP_CONFIG.QR);
Object.freeze(APP_CONFIG.UI);
Object.freeze(APP_CONFIG.SOCKET);
Object.freeze(APP_CONFIG.SOUND);
Object.freeze(APP_CONFIG.DEVICE);
Object.freeze(APP_CONFIG.Z_INDEX);
Object.freeze(APP_CONFIG.API);
Object.freeze(APP_CONFIG);

console.log('⚙️ App Config loaded:', APP_CONFIG);
