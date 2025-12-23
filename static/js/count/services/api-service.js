/**
 * 🌐 API SERVICE - Tüm backend çağrıları burada
 * Sorumluluk: HTTP istekleri, veri dönüşümü, hata yönetimi
 */

class APIService {
    constructor() {
        this.baseURL = window.location.origin;
    }

    /**
     * Generic fetch wrapper
     */
    async request(endpoint, options = {}) {
        try {
            const url = endpoint.startsWith('http') ? endpoint : `${this.baseURL}${endpoint}`;
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`❌ API Error [${endpoint}]:`, error);
            throw error;
        }
    }

    /**
     * Auth - Kullanıcı kimlik doğrulama
     */
    async checkAuth() {
        const config = window.APP_CONFIG?.API;
        return this.request(config?.CHECK_AUTH || '/check_auth');
    }

    async logout() {
        return this.request('/logout', { method: 'POST' });
    }

    /**
     * Session - Sayım oturumu
     */
    async getSessionStats() {
        const config = window.APP_CONFIG?.API;
        return this.request(config?.SESSION_STATS || '/get_session_stats');
    }

    async getCountStatus() {
        return this.request('/get_count_status');
    }

    /**
     * Finish Count - Sayımı bitir (Admin)
     */
    async finishCount() {
        return this.request('/finish_count', { method: 'POST' });
    }

    /**
     * Activities - QR okuma geçmişi
     */
    async getRecentActivities() {
        const config = window.APP_CONFIG?.API;
        return this.request(config?.ACTIVITIES || '/get_recent_activities');
    }

    /**
     * Live Count - Canlı sayım takibi
     */
    async getLiveCountStatus() {
        const config = window.APP_CONFIG?.API;
        return this.request(config?.LIVE_COUNT || '/get_live_count_status');
    }

    async exportLiveCount() {
        const config = window.APP_CONFIG?.API;
        window.location.href = config?.EXPORT_LIVE || '/export_live_count';
    }

    /**
     * QR Activities Export
     */
    async exportQRActivities() {
        window.location.href = '/export_qr_activities';
    }
}

// Global export
window.APIService = APIService;
