/**
 * 🎨 UI MANAGER - Arayüz yönetimi (SADECE GÖSTERIM)
 * Sorumluluk: İstatistik, mesaj, aktivite gösterimi
 */

class UIManager {
    constructor(apiService = null) {
        this.apiService = apiService;
        this.stats = {
            scanned: 0,
            expected: 0,
            startTime: null
        };
        
        if (window.logger) window.logger.info('UIManager başlatılıyor...');
    }

    /**
     * İstatistikleri güncelle
     */
    updateStats(stats) {
        this.stats = { ...this.stats, ...stats };
        
        // Sayfa elementlerini güncelle
        const scannedEl = document.getElementById('scannedCount');
        const expectedEl = document.getElementById('expectedCount');
        const accuracyEl = document.getElementById('accuracyRate');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');

        if (scannedEl) scannedEl.textContent = this.stats.scanned;
        if (expectedEl) expectedEl.textContent = this.stats.expected;

        // Progress hesapla
        const progress = this.stats.expected > 0 
            ? (this.stats.scanned / this.stats.expected * 100) 
            : 0;

        if (accuracyEl) accuracyEl.textContent = Math.round(progress) + '%';
        if (progressBar) progressBar.style.width = Math.min(progress, 100) + '%';
        if (progressText) progressText.textContent = Math.round(progress) + '%';

        if (window.logger) {
            window.logger.debug('Stats güncellendi', this.stats);
        }
        
        if (window.eventBus) {
            window.eventBus.emit(window.EVENTS.STATS_UPDATED, this.stats);
        }
    }

    /**
     * Tam ekran mesaj göster
     */
    showMessage(message, isSuccess) {
        if (window.logger) {
            window.logger.info('Mesaj gösteriliyor', { message, isSuccess });
        }

        // Overlay oluştur
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background: ${isSuccess ? 'rgba(40, 167, 69, 0.95)' : 'rgba(220, 53, 69, 0.95)'} !important;
            z-index: 2147483647 !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            color: white !important;
            font-size: 28px !important;
            font-weight: bold !important;
            text-align: center !important;
            padding: 40px !important;
        `;

        overlay.innerHTML = `
            <div style="font-size: 80px; margin-bottom: 30px;">${isSuccess ? '✅' : '❌'}</div>
            <div style="font-size: 24px; line-height: 1.5;">${message}</div>
        `;

        document.body.appendChild(overlay);

        // Ses çal
        if (isSuccess && window.playSuccessSound) {
            window.playSuccessSound();
        } else if (!isSuccess && window.playDuplicateSound) {
            window.playDuplicateSound();
        }

        // 2 saniye sonra kaldır
        setTimeout(() => {
            overlay.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => overlay.remove(), 300);
        }, 2000);
    }

    /**
     * Aktivite ekle
     */
    async loadActivities() {
        try {
            const activities = this.apiService 
                ? await this.apiService.getRecentActivities()
                : await (await fetch('/get_recent_activities')).json();

            const timeline = document.getElementById('activityTimeline');
            const activityCount = document.getElementById('activityCount');

            if (!timeline) return;

            // Placeholder temizle
            if (timeline.querySelector('.text-center')) {
                timeline.innerHTML = '';
            }

            // Aktiviteleri ekle
            if (Array.isArray(activities) && activities.length > 0) {
                timeline.innerHTML = '';
                
                activities.forEach(activity => {
                    const activityDiv = document.createElement('div');
                    activityDiv.className = 'activity-item';

                    const timeStr = activity.scanned_at 
                        ? new Date(activity.scanned_at).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
                        : '--:--';

                    activityDiv.innerHTML = `
                        <div class="activity-icon"><i class="bi bi-qr-code"></i></div>
                        <div class="activity-content">
                            <div class="activity-title">${activity.qr_code || 'N/A'}</div>
                            <div class="activity-meta">
                                <span><i class="bi bi-person-fill"></i> ${activity.scanned_by || 'Bilinmeyen'}</span>
                                <span><i class="bi bi-clock"></i> ${timeStr}</span>
                                ${activity.part_name ? `<span><i class="bi bi-tag"></i> ${activity.part_name}</span>` : ''}
                            </div>
                        </div>
                    `;

                    timeline.appendChild(activityDiv);
                });

                if (activityCount) {
                    activityCount.textContent = activities.length;
                }

                console.log(`✅ ${activities.length} aktivite yüklendi`);
            }
        } catch (error) {
            console.error('❌ Aktivite yükleme hatası:', error);
        }
    }

    /**
     * Canlı sayım tablosunu güncelle
     */
    async loadLiveCount() {
        try {
            const data = this.apiService
                ? await this.apiService.getLiveCountStatus()
                : await (await fetch('/get_live_count_status')).json();

            const tbody = document.getElementById('liveCountBody');
            const badge = document.getElementById('liveCountBadge');

            if (!tbody) return;

            if (!data.active || !data.parts || data.parts.length === 0) {
                tbody.innerHTML = `
                    <tr><td colspan="3" class="text-center text-muted" style="padding: 1.5rem;">
                        Henüz parça bilgisi yok
                    </td></tr>
                `;
                return;
            }

            tbody.innerHTML = '';
            data.parts.forEach(part => {
                const statusColor = part.kalan_adet === 0 ? 'success' : 
                                   part.sayilan_adet === 0 ? 'secondary' : 'warning';
                const statusIcon = part.kalan_adet === 0 ? '✅' : '⏳';

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td style="padding: 0.5rem; font-size: 0.75rem;">
                        <strong>${part.part_code}</strong>
                        <small class="text-muted d-block">${part.part_name.substring(0, 20)}...</small>
                    </td>
                    <td style="padding: 0.5rem; text-align: center;">
                        <div style="font-size: 0.875rem; font-weight: 600; color: var(--bs-${statusColor});">
                            ${part.sayilan_adet}/${part.beklenen_adet}
                        </div>
                        <div class="progress" style="height: 4px; margin-top: 3px;">
                            <div class="progress-bar bg-${statusColor}" style="width: ${part.tamamlanma_yuzdesi}%"></div>
                        </div>
                    </td>
                    <td style="padding: 0.5rem; text-align: center; font-size: 0.875rem; font-weight: 600;">
                        ${statusIcon} ${part.kalan_adet}
                    </td>
                `;
                tbody.appendChild(row);
            });

            if (badge) {
                badge.textContent = `${data.completed_parts}/${data.total_parts}`;
            }

            console.log('✅ Canlı sayım güncellendi');
        } catch (error) {
            console.error('❌ Canlı sayım hatası:', error);
        }
    }
}

// Global export
window.UIManager = UIManager;
