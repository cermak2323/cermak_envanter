/**
 * 📝 LOGGER SERVICE - Merkezi log yönetimi
 * Sorumluluk: Console log, hata ayıklama, log seviyeleri
 */

class Logger {
    constructor() {
        this.isDebugMode = localStorage.getItem('debug_mode') === 'true';
        this.logs = [];
        this.maxLogs = 100;
    }

    /**
     * Debug mode aç/kapa
     */
    enableDebug() {
        this.isDebugMode = true;
        localStorage.setItem('debug_mode', 'true');
        console.log('🐛 Debug mode AÇIK');
    }

    disableDebug() {
        this.isDebugMode = false;
        localStorage.removeItem('debug_mode');
        console.log('🐛 Debug mode KAPALI');
    }

    /**
     * Log ekle
     */
    addLog(level, message, data = null) {
        const timestamp = new Date().toISOString();
        const logEntry = { timestamp, level, message, data };
        
        this.logs.push(logEntry);
        
        // Max log sınırı
        if (this.logs.length > this.maxLogs) {
            this.logs.shift();
        }

        return logEntry;
    }

    /**
     * Info log
     */
    info(message, data = null) {
        this.addLog('INFO', message, data);
        console.log(`ℹ️ ${message}`, data || '');
    }

    /**
     * Success log
     */
    success(message, data = null) {
        this.addLog('SUCCESS', message, data);
        console.log(`✅ ${message}`, data || '');
    }

    /**
     * Warning log
     */
    warn(message, data = null) {
        this.addLog('WARN', message, data);
        console.warn(`⚠️ ${message}`, data || '');
    }

    /**
     * Error log
     */
    error(message, error = null) {
        this.addLog('ERROR', message, error);
        console.error(`❌ ${message}`, error || '');
    }

    /**
     * Debug log (sadece debug mode açıksa)
     */
    debug(message, data = null) {
        if (this.isDebugMode) {
            this.addLog('DEBUG', message, data);
            console.debug(`🐛 ${message}`, data || '');
        }
    }

    /**
     * Tüm logları al
     */
    getLogs(level = null) {
        if (level) {
            return this.logs.filter(log => log.level === level);
        }
        return this.logs;
    }

    /**
     * Logları temizle
     */
    clearLogs() {
        this.logs = [];
        console.log('🗑️ Loglar temizlendi');
    }

    /**
     * Logları export et
     */
    exportLogs() {
        const logsText = this.logs.map(log => 
            `[${log.timestamp}] ${log.level}: ${log.message} ${log.data ? JSON.stringify(log.data) : ''}`
        ).join('\n');

        const blob = new Blob([logsText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `count-logs-${Date.now()}.txt`;
        a.click();
        URL.revokeObjectURL(url);
        
        console.log('💾 Loglar indirildi');
    }
}

// Global export
window.Logger = Logger;

// Global logger instance
window.logger = new Logger();

// Kolay erişim için global fonksiyonlar
window.enableDebug = () => window.logger.enableDebug();
window.disableDebug = () => window.logger.disableDebug();
window.exportLogs = () => window.logger.exportLogs();
