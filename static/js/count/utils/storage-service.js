/**
 * 💾 STORAGE SERVICE - LocalStorage/SessionStorage yönetimi
 * Sorumluluk: Veri saklama, cache, offline destek
 */

class StorageService {
    constructor() {
        this.prefix = 'count_app_';
    }

    /**
     * LocalStorage'a kaydet
     */
    setLocal(key, value) {
        try {
            const prefixedKey = this.prefix + key;
            const serialized = JSON.stringify(value);
            localStorage.setItem(prefixedKey, serialized);
            
            if (window.logger) {
                window.logger.debug(`LocalStorage set: ${key}`);
            }
            return true;
        } catch (error) {
            console.error('LocalStorage set error:', error);
            return false;
        }
    }

    /**
     * LocalStorage'dan oku
     */
    getLocal(key, defaultValue = null) {
        try {
            const prefixedKey = this.prefix + key;
            const item = localStorage.getItem(prefixedKey);
            
            if (item === null) return defaultValue;
            
            return JSON.parse(item);
        } catch (error) {
            console.error('LocalStorage get error:', error);
            return defaultValue;
        }
    }

    /**
     * LocalStorage'dan sil
     */
    removeLocal(key) {
        const prefixedKey = this.prefix + key;
        localStorage.removeItem(prefixedKey);
        
        if (window.logger) {
            window.logger.debug(`LocalStorage removed: ${key}`);
        }
    }

    /**
     * SessionStorage'a kaydet
     */
    setSession(key, value) {
        try {
            const prefixedKey = this.prefix + key;
            const serialized = JSON.stringify(value);
            sessionStorage.setItem(prefixedKey, serialized);
            return true;
        } catch (error) {
            console.error('SessionStorage set error:', error);
            return false;
        }
    }

    /**
     * SessionStorage'dan oku
     */
    getSession(key, defaultValue = null) {
        try {
            const prefixedKey = this.prefix + key;
            const item = sessionStorage.getItem(prefixedKey);
            
            if (item === null) return defaultValue;
            
            return JSON.parse(item);
        } catch (error) {
            console.error('SessionStorage get error:', error);
            return defaultValue;
        }
    }

    /**
     * SessionStorage'dan sil
     */
    removeSession(key) {
        const prefixedKey = this.prefix + key;
        sessionStorage.removeItem(prefixedKey);
    }

    /**
     * Tüm uygulama verilerini temizle
     */
    clearAll() {
        // LocalStorage
        Object.keys(localStorage).forEach(key => {
            if (key.startsWith(this.prefix)) {
                localStorage.removeItem(key);
            }
        });

        // SessionStorage
        Object.keys(sessionStorage).forEach(key => {
            if (key.startsWith(this.prefix)) {
                sessionStorage.removeItem(key);
            }
        });

        if (window.logger) {
            window.logger.info('Tüm storage temizlendi');
        }
    }

    /**
     * Cache yönetimi (TTL ile)
     */
    setCached(key, value, ttlMinutes = 60) {
        const expiresAt = Date.now() + (ttlMinutes * 60 * 1000);
        const cached = { value, expiresAt };
        this.setLocal(key, cached);
    }

    getCached(key) {
        const cached = this.getLocal(key);
        
        if (!cached) return null;
        
        // TTL kontrolü
        if (Date.now() > cached.expiresAt) {
            this.removeLocal(key);
            return null;
        }
        
        return cached.value;
    }
}

// Global export
window.StorageService = StorageService;

// Global storage instance
window.storage = new StorageService();
