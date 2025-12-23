/**
 * 🎯 QR OVERLAY - Yeşil Tarama Alanı ve Mesajlar
 * Manuel overlay çünkü Nimiq'in built-in özellikleri her zaman çalışmıyor
 */

class QROverlay {
    constructor() {
        this.overlayContainer = null;
        this.scanRegion = null;
        this.messageContainer = null;
        this.cornerMarkers = [];
        
        console.log('🎯 QROverlay initialized');
    }

    /**
     * Overlay'i oluştur ve ekle
     */
    initialize() {
        try {
            console.log('🎨 QR Overlay oluşturuluyor...');
            
            // Ana overlay container
            this.overlayContainer = document.createElement('div');
            this.overlayContainer.id = 'qrOverlay';
            this.overlayContainer.style.cssText = `
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                z-index: 999999 !important;
                pointer-events: none !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            `;

            // Yeşil tarama alanı (merkez kutu)
            this.scanRegion = document.createElement('div');
            this.scanRegion.id = 'scanRegion';
            this.scanRegion.style.cssText = `
                position: relative !important;
                width: 300px !important;
                height: 300px !important;
                border: 5px solid #00ff00 !important;
                border-radius: 20px !important;
                box-shadow: 
                    0 0 0 9999px rgba(0, 0, 0, 0.7),
                    0 0 50px rgba(0, 255, 0, 0.8),
                    inset 0 0 50px rgba(0, 255, 0, 0.3) !important;
                background: rgba(0, 255, 0, 0.05) !important;
                animation: scanPulse 2s ease-in-out infinite !important;
            `;

            // Köşe işaretleri
            this.createCornerMarkers();

            // Mesaj container (overlay içinde)
            this.messageContainer = document.createElement('div');
            this.messageContainer.id = 'overlayMessages';
            this.messageContainer.style.cssText = `
                position: absolute !important;
                top: -100px !important;
                left: 50% !important;
                transform: translateX(-50%) !important;
                background: rgba(0, 255, 0, 0.95) !important;
                color: #000000 !important;
                padding: 20px 32px !important;
                border-radius: 16px !important;
                font-size: 18px !important;
                font-weight: 700 !important;
                text-align: center !important;
                min-width: 280px !important;
                box-shadow: 0 8px 20px rgba(0, 255, 0, 0.6) !important;
                backdrop-filter: blur(10px) !important;
                border: 3px solid #00ff00 !important;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.8) !important;
            `;
            this.messageContainer.innerHTML = '📱 QR KODU TARAMA ALANINA GETİRİN';

            // Overlay'i birleştir
            this.scanRegion.appendChild(this.messageContainer);
            this.overlayContainer.appendChild(this.scanRegion);

            // DOM'a ekle
            const readerDiv = document.getElementById('reader');
            if (readerDiv) {
                readerDiv.appendChild(this.overlayContainer);
            } else {
                document.body.appendChild(this.overlayContainer);
            }

            // CSS animasyon ekle
            this.addAnimations();

            console.log('✅ QR Overlay eklendi - Yeşil tarama alanı görünür');
            
        } catch (error) {
            console.error('❌ Overlay oluşturma hatası:', error);
        }
    }

    /**
     * Köşe işaretlerini oluştur
     */
    createCornerMarkers() {
        const corners = ['top-left', 'top-right', 'bottom-left', 'bottom-right'];
        const positions = {
            'top-left': 'top: -5px; left: -5px;',
            'top-right': 'top: -5px; right: -5px;',
            'bottom-left': 'bottom: -5px; left: -5px;',
            'bottom-right': 'bottom: -5px; right: -5px;'
        };

        corners.forEach(corner => {
            const marker = document.createElement('div');
            marker.className = `corner-marker ${corner}`;
            marker.style.cssText = `
                position: absolute !important;
                width: 50px !important;
                height: 50px !important;
                ${positions[corner]}
                z-index: 10 !important;
                filter: drop-shadow(0 0 10px rgba(0, 255, 0, 0.8)) !important;
            `;

            // Köşe çizgileri - daha kalın ve belirgin
            if (corner === 'top-left') {
                marker.style.borderTop = '8px solid #00ff00';
                marker.style.borderLeft = '8px solid #00ff00';
                marker.style.borderTopLeftRadius = '20px';
            } else if (corner === 'top-right') {
                marker.style.borderTop = '8px solid #00ff00';
                marker.style.borderRight = '8px solid #00ff00';
                marker.style.borderTopRightRadius = '20px';
            } else if (corner === 'bottom-left') {
                marker.style.borderBottom = '8px solid #00ff00';
                marker.style.borderLeft = '8px solid #00ff00';
                marker.style.borderBottomLeftRadius = '20px';
            } else if (corner === 'bottom-right') {
                marker.style.borderBottom = '8px solid #00ff00';
                marker.style.borderRight = '8px solid #00ff00';
                marker.style.borderBottomRightRadius = '20px';
            }

            this.scanRegion.appendChild(marker);
            this.cornerMarkers.push(marker);
        });
    }

    /**
     * Add CSS animations and ensure overlay is always visible
     */
    addAnimations() {
        if (document.getElementById('qrOverlayAnimations')) return;

        const style = document.createElement('style');
        style.id = 'qrOverlayAnimations';
        style.textContent = `
            /* ENSURE OVERLAY IS ALWAYS VISIBLE - HIGHEST Z-INDEX */
            #qrOverlay {
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                z-index: 999999 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                pointer-events: none !important;
                visibility: visible !important;
                opacity: 1 !important;
            }

            #scanRegion {
                position: relative !important;
                z-index: 999999 !important;
                pointer-events: none !important;
                visibility: visible !important;
                opacity: 1 !important;
            }

            #overlayMessages {
                position: absolute !important;
                z-index: 9999999 !important;
                pointer-events: none !important;
                visibility: visible !important;
                opacity: 1 !important;
                display: block !important;
            }

            @keyframes scanPulse {
                0%, 100% {
                    box-shadow: 
                        0 0 0 9999px rgba(0, 0, 0, 0.7),
                        0 0 50px rgba(0, 255, 0, 0.8),
                        inset 0 0 50px rgba(0, 255, 0, 0.3);
                    border-color: #00ff00;
                }
                50% {
                    box-shadow: 
                        0 0 0 9999px rgba(0, 0, 0, 0.7),
                        0 0 80px rgba(0, 255, 0, 1),
                        inset 0 0 70px rgba(0, 255, 0, 0.5);
                    border-color: #33ff33;
                }
            }

            @keyframes scanSuccess {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }

            /* ALL SCREEN SIZES */
            @media (max-width: 2000px) {
                #scanRegion { width: 300px !important; height: 300px !important; }
            }
            @media (max-width: 768px) {
                #scanRegion { width: 280px !important; height: 280px !important; }
                #overlayMessages { font-size: 16px !important; }
            }
            @media (max-width: 400px) {
                #scanRegion { width: 260px !important; height: 260px !important; }
                #overlayMessages { 
                    font-size: 14px !important;
                    padding: 16px 24px !important;
                    min-width: 240px !important;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Mesaj göster
     */
    showMessage(text, type = 'info') {
        if (!this.messageContainer) return;

        const colors = {
            'info': '#ffffff',
            'success': '#00ff00',
            'error': '#ff0000',
            'warning': '#ffaa00'
        };

        const icons = {
            'info': '📱',
            'success': '✅',
            'error': '❌',
            'warning': '⚠️'
        };

        this.messageContainer.style.color = colors[type] || colors.info;
        this.messageContainer.innerHTML = `${icons[type] || icons.info} ${text}`;
        
        console.log(`📢 Overlay mesaj: ${text} (${type})`);
    }

    /**
     * QR kod başarıyla okundu animasyonu
     */
    showSuccess() {
        if (!this.scanRegion) return;

        // Yeşil parlama animasyonu
        this.scanRegion.style.animation = 'none';
        setTimeout(() => {
            this.scanRegion.style.animation = 'scanSuccess 0.5s ease-out';
        }, 10);

        // Border'ı yeşile çevir
        this.scanRegion.style.borderColor = '#00ff00';
        this.scanRegion.style.boxShadow = `
            0 0 0 9999px rgba(0, 0, 0, 0.5),
            0 0 60px rgba(0, 255, 0, 1),
            inset 0 0 50px rgba(0, 255, 0, 0.4)
        `;

        // 1 saniye sonra normale dön
        setTimeout(() => {
            this.scanRegion.style.animation = 'scanPulse 2s ease-in-out infinite';
            this.scanRegion.style.borderColor = '#00ff00';
        }, 1000);
    }

    /**
     * Hata animasyonu
     */
    showError() {
        if (!this.scanRegion) return;

        // Kırmızı yanıp sönme
        this.scanRegion.style.borderColor = '#ff0000';
        this.scanRegion.style.boxShadow = `
            0 0 0 9999px rgba(0, 0, 0, 0.5),
            0 0 40px rgba(255, 0, 0, 0.8),
            inset 0 0 30px rgba(255, 0, 0, 0.3)
        `;

        setTimeout(() => {
            this.scanRegion.style.borderColor = '#00ff00';
            this.scanRegion.style.boxShadow = `
                0 0 0 9999px rgba(0, 0, 0, 0.5),
                0 0 30px rgba(0, 255, 0, 0.6),
                inset 0 0 30px rgba(0, 255, 0, 0.2)
            `;
        }, 500);
    }

    /**
     * Overlay'i göster/gizle
     */
    show() {
        if (this.overlayContainer) {
            this.overlayContainer.style.display = 'flex';
        }
    }

    hide() {
        if (this.overlayContainer) {
            this.overlayContainer.style.display = 'none';
        }
    }

    /**
     * Temizlik
     */
    destroy() {
        if (this.overlayContainer && this.overlayContainer.parentNode) {
            this.overlayContainer.parentNode.removeChild(this.overlayContainer);
        }
        
        const animStyle = document.getElementById('qrOverlayAnimations');
        if (animStyle && animStyle.parentNode) {
            animStyle.parentNode.removeChild(animStyle);
        }

        this.overlayContainer = null;
        this.scanRegion = null;
        this.messageContainer = null;
        this.cornerMarkers = [];
        
        console.log('🗑️ QROverlay temizlendi');
    }
}

// Global export
window.QROverlay = QROverlay;
console.log('✅ QROverlay yüklendi - Manuel yeşil tarama alanı');
