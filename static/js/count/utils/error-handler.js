/**
 * 🚨 ERROR HANDLER - Global JavaScript Error Boundary
 * Tüm frontend hatalarını yakalar, loglar ve backend'e gönderir
 */

class ErrorHandler {
    constructor() {
        this.errors = [];
        this.maxErrors = 50;
        this.setupGlobalErrorHandler();
        
        if (window.logger) {
            window.logger.info('ErrorHandler başlatıldı');
        }
    }
    
    /**
     * Global error handler'ları kur
     */
    setupGlobalErrorHandler() {
        // JavaScript runtime hataları
        window.addEventListener('error', (event) => {
            this.handleError({
                type: 'JavaScript Error',
                message: event.message,
                file: event.filename,
                line: event.lineno,
                column: event.colno,
                stack: event.error?.stack || 'No stack trace',
                error: event.error
            });
            
            // Varsayılan davranışı engelle (console'a yazmayı)
            return true;
        });
        
        // Promise rejection hataları
        window.addEventListener('unhandledrejection', (event) => {
            this.handleError({
                type: 'Unhandled Promise Rejection',
                message: event.reason?.message || String(event.reason),
                stack: event.reason?.stack || 'No stack trace',
                promise: event.promise
            });
            
            // Varsayılan davranışı engelle
            event.preventDefault();
        });
        
        console.log('✅ Global Error Handler kuruldu');
    }
    
    /**
     * Hatayı işle
     */
    handleError(errorInfo) {
        console.error('❌ Global Error Caught:', errorInfo);
        
        // Logger varsa kaydet
        if (window.logger) {
            window.logger.error('Global error', errorInfo);
        }
        
        // Errors listesine ekle
        const errorRecord = {
            ...errorInfo,
            timestamp: new Date().toISOString(),
            url: window.location.href,
            userAgent: navigator.userAgent.substring(0, 100)
        };
        
        this.errors.push(errorRecord);
        
        // Max limit kontrolü
        if (this.errors.length > this.maxErrors) {
            this.errors.shift();
        }
        
        // Event yayınla
        if (window.eventBus) {
            window.eventBus.emit(window.EVENTS?.ERROR_CAUGHT || 'error:caught', errorRecord);
        }
        
        // Backend'e gönder
        this.reportToBackend(errorRecord);
        
        // Kullanıcıya göster (kritik hatalarda)
        if (this.isCriticalError(errorInfo)) {
            this.showErrorToUser(errorInfo);
        }
    }
    
    /**
     * Kritik hata mı kontrol et
     */
    isCriticalError(errorInfo) {
        const criticalKeywords = [
            'Cannot read',
            'undefined is not',
            'is not a function',
            'null',
            'ReferenceError',
            'TypeError'
        ];
        
        const message = errorInfo.message || '';
        return criticalKeywords.some(keyword => 
            message.toLowerCase().includes(keyword.toLowerCase())
        );
    }
    
    /**
     * Kullanıcıya hata göster
     */
    showErrorToUser(errorInfo) {
        // UI Manager varsa kullan
        if (window.uiManager) {
            window.uiManager.showMessage(
                '❌ Bir hata oluştu. Sayfa yenilenecek.',
                false
            );
        } else {
            // Fallback: basit alert
            console.warn('Kritik hata tespit edildi. Sayfa yenilenecek.');
        }
        
        // 3 saniye sonra sayfayı yenile
        setTimeout(() => {
            location.reload();
        }, 3000);
    }
    
    /**
     * Backend'e hata raporu gönder
     */
    async reportToBackend(errorInfo) {
        try {
            await fetch('/log_frontend_error', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    error: {
                        type: errorInfo.type,
                        message: errorInfo.message,
                        file: errorInfo.file,
                        line: errorInfo.line,
                        column: errorInfo.column,
                        stack: errorInfo.stack?.substring(0, 500) // İlk 500 karakter
                    },
                    context: {
                        url: window.location.href,
                        userAgent: navigator.userAgent,
                        timestamp: errorInfo.timestamp,
                        screenSize: `${window.innerWidth}x${window.innerHeight}`,
                        online: navigator.onLine
                    }
                })
            });
            
            if (window.logger) {
                window.logger.debug('Hata backend\'e gönderildi');
            }
        } catch (e) {
            console.warn('Backend\'e hata gönderilemedi:', e);
        }
    }
    
    /**
     * Tüm hataları getir
     */
    getErrors() {
        return this.errors;
    }
    
    /**
     * Son N hatayı getir
     */
    getRecentErrors(count = 10) {
        return this.errors.slice(-count);
    }
    
    /**
     * Hataları temizle
     */
    clearErrors() {
        this.errors = [];
        if (window.logger) {
            window.logger.info('Hatalar temizlendi');
        }
    }
    
    /**
     * Hata sayısını getir
     */
    getErrorCount() {
        return this.errors.length;
    }
    
    /**
     * Hataları dışa aktar
     */
    exportErrors() {
        const blob = new Blob(
            [JSON.stringify(this.errors, null, 2)], 
            { type: 'application/json' }
        );
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `frontend_errors_${new Date().toISOString()}.json`;
        a.click();
        URL.revokeObjectURL(url);
        
        if (window.logger) {
            window.logger.info('Hatalar dışa aktarıldı');
        }
    }
}

// Global instance oluştur
window.errorHandler = new ErrorHandler();

// Global helper fonksiyonlar
window.getErrors = () => window.errorHandler.getErrors();
window.clearErrors = () => window.errorHandler.clearErrors();
window.exportErrors = () => window.errorHandler.exportErrors();

console.log('✅ Error Handler modülü yüklendi');
