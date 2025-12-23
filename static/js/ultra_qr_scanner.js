/*
🚀 ULTRA MODERN QR SCANNER SYSTEM
En iyi kütüphaneler ve modern teknolojilerle
*/

// 🔧 Global Set - Bir sayımda okunan tüm QR'ları takip eder
if (typeof window.scannedQRsInSession === 'undefined') {
    window.scannedQRsInSession = new Set();
}

class UltraQRScanner {
    constructor() {
        this.isScanning = false;
        this.isProcessing = false; // 🔧 Processing lock for feedback
        this.lastScan = '';
        this.lastScanTime = 0;
        this.scanCount = 0;
        this.qrScanner = null;
        this.fallbackScanner = null;
        this.videoElement = null;
        this.currentSessionId = this.getSessionId();
        
        console.log('🚀 Ultra QR Scanner initializing...');
        this.init();
    }
    
    async init() {
        await this.loadLibraries();
        this.setupEventListeners();
        this.setupSocketIO();
        this.createUI();
        console.log('✅ Ultra QR Scanner ready!');
    }
    
    async loadLibraries() {
        console.log('📚 Loading modern QR libraries...');
        
        // Load QR Scanner library (UMD version to avoid ES6 export issues)
        if (!window.QrScanner) {
            const script1 = document.createElement('script');
            script1.src = 'https://cdn.jsdelivr.net/npm/qr-scanner@1.4.2/qr-scanner.umd.min.js';
            document.head.appendChild(script1);
            
            await new Promise(resolve => {
                script1.onload = () => {
                    console.log('✅ QR Scanner UMD library loaded');
                    resolve();
                };
                script1.onerror = () => {
                    console.warn('⚠️ QR Scanner library failed to load');
                    resolve();
                };
            });
        }
        
        // Load ZXing library as fallback
        if (!window.ZXing) {
            const script2 = document.createElement('script');
            script2.src = 'https://cdn.jsdelivr.net/npm/@zxing/library@0.20.0/umd/index.min.js';
            document.head.appendChild(script2);
            
            await new Promise(resolve => {
                script2.onload = () => {
                    console.log('✅ ZXing library loaded');
                    resolve();
                };
                script2.onerror = () => {
                    console.warn('⚠️ ZXing library failed to load');
                    resolve();
                };
            });
        }
        
        // Load jsQR as ultimate fallback
        if (!window.jsQR) {
            const script3 = document.createElement('script');
            script3.src = 'https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js';
            document.head.appendChild(script3);
            
            await new Promise(resolve => {
                script3.onload = () => {
                    console.log('✅ jsQR library loaded');
                    resolve();
                };
                script3.onerror = () => {
                    console.warn('⚠️ jsQR library failed to load');
                    resolve();
                };
            });
        }
        
        console.log('✅ Libraries loaded');
    }
    
    createUI() {
        // Create ultra modern scanner UI
        const scannerHTML = `
            <div id="ultraQRContainer" class="ultra-qr-container">
                <div id="ultraQROverlay" class="ultra-qr-overlay">
                    <div class="ultra-qr-frame">
                        <div class="corner corner-tl"></div>
                        <div class="corner corner-tr"></div>
                        <div class="corner corner-bl"></div>
                        <div class="corner corner-br"></div>
                        <div class="scan-line"></div>
                    </div>
                    <div class="ultra-qr-hint">QR kodu çerçeve içine hizalayın</div>
                </div>
                <video id="ultraQRVideo" class="ultra-qr-video" playsinline></video>
                <canvas id="ultraQRCanvas" class="ultra-qr-canvas" style="display: none;"></canvas>
                <div id="ultraQRMessages" class="ultra-qr-messages"></div>
            </div>
        `;
        
        // Add to page
        let container = document.getElementById('reader');
        if (!container) {
            container = document.createElement('div');
            container.id = 'reader';
            document.body.appendChild(container);
        }
        
        container.innerHTML = scannerHTML;
        this.videoElement = document.getElementById('ultraQRVideo');
        
        this.addUltraStyles();
    }
    
    addUltraStyles() {
        const styles = `
            <style id="ultraQRStyles">
                .ultra-qr-container {
                    position: relative;
                    width: 100%;
                    height: 100%;
                    background: #000;
                    overflow: hidden;
                }
                
                .ultra-qr-video {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }
                
                .ultra-qr-overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-direction: column;
                    z-index: 10;
                    pointer-events: none;
                }
                
                .ultra-qr-frame {
                    position: relative;
                    width: 280px;
                    height: 280px;
                    max-width: 80vw;
                    max-height: 80vw;
                    border: 2px solid rgba(0, 255, 0, 0.8);
                    border-radius: 20px;
                    box-shadow: 
                        0 0 20px rgba(0, 255, 0, 0.5),
                        inset 0 0 20px rgba(0, 255, 0, 0.1);
                    animation: pulseFrame 2s ease-in-out infinite;
                }
                
                .corner {
                    position: absolute;
                    width: 30px;
                    height: 30px;
                    border: 4px solid #00ff00;
                    border-radius: 5px;
                }
                
                .corner-tl {
                    top: -2px;
                    left: -2px;
                    border-right: none;
                    border-bottom: none;
                }
                
                .corner-tr {
                    top: -2px;
                    right: -2px;
                    border-left: none;
                    border-bottom: none;
                }
                
                .corner-bl {
                    bottom: -2px;
                    left: -2px;
                    border-right: none;
                    border-top: none;
                }
                
                .corner-br {
                    bottom: -2px;
                    right: -2px;
                    border-left: none;
                    border-top: none;
                }
                
                .scan-line {
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 3px;
                    background: linear-gradient(90deg, transparent, #00ff00, transparent);
                    border-radius: 2px;
                    animation: scanLine 2s ease-in-out infinite;
                }
                
                .ultra-qr-hint {
                    margin-top: 30px;
                    color: white;
                    font-size: 16px;
                    font-weight: 500;
                    text-align: center;
                    background: rgba(0, 0, 0, 0.7);
                    padding: 10px 20px;
                    border-radius: 25px;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }
                
                .ultra-qr-messages {
                    position: fixed;
                    top: 60px;
                    left: 50%;
                    transform: translateX(-50%);
                    z-index: 1000000;
                    pointer-events: none;
                }
                
                .ultra-message {
                    background: linear-gradient(135deg, #00ff88, #00cc77);
                    color: white;
                    padding: 20px 30px;
                    border-radius: 15px;
                    font-size: 18px;
                    font-weight: bold;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0, 255, 136, 0.4);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    animation: ultraBounce 0.6s ease;
                    margin-bottom: 10px;
                }
                
                .ultra-message.error {
                    background: linear-gradient(135deg, #ff4757, #ff3742);
                    box-shadow: 0 10px 30px rgba(255, 71, 87, 0.4);
                }
                
                @keyframes pulseFrame {
                    0%, 100% { 
                        border-color: rgba(0, 255, 0, 0.8);
                        box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
                    }
                    50% { 
                        border-color: rgba(0, 255, 0, 1);
                        box-shadow: 0 0 30px rgba(0, 255, 0, 0.8);
                    }
                }
                
                @keyframes scanLine {
                    0% { top: 0; opacity: 1; }
                    50% { opacity: 1; }
                    100% { top: calc(100% - 3px); opacity: 0; }
                }
                
                @keyframes pulse {
                    0% { 
                        transform: scale(0.8);
                        opacity: 0;
                    }
                    50% { 
                        transform: scale(1.1);
                        opacity: 1;
                    }
                    100% { 
                        transform: scale(1);
                        opacity: 1;
                    }
                }
                
                @keyframes ultraBounce {
                    0% { 
                        transform: translateX(-50%) scale(0.3) translateY(-100px);
                        opacity: 0;
                    }
                    50% { 
                        transform: translateX(-50%) scale(1.1) translateY(0);
                        opacity: 1;
                    }
                    100% { 
                        transform: translateX(-50%) scale(1) translateY(0);
                        opacity: 1;
                    }
                }
                
                /* Mobile optimizations */
                @media (max-width: 768px) {
                    .ultra-qr-container {
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100vw;
                        height: 100vh;
                        z-index: 999999;
                    }
                    
                    .ultra-qr-frame {
                        width: 250px;
                        height: 250px;
                    }
                    
                    .ultra-qr-hint {
                        font-size: 14px;
                        margin-top: 20px;
                    }
                }
            </style>
        `;
        
        if (!document.getElementById('ultraQRStyles')) {
            document.head.insertAdjacentHTML('beforeend', styles);
        }
    }
    
    async startScanning() {
        console.log('🚀 Starting ultra QR scanning...');
        
        try {
            // Method 1: Modern QR Scanner library
            if (window.QrScanner && QrScanner.hasCamera()) {
                await this.startQrScannerLibrary();
                return;
            }
            
            // Method 2: ZXing library
            if (window.ZXing) {
                await this.startZXingScanner();
                return;
            }
            
            // Method 3: Manual implementation with getUserMedia
            await this.startManualScanner();
            
        } catch (error) {
            console.error('❌ Ultra scanner failed:', error);
            this.showMessage('❌ Kamera başlatılamadı: ' + error.message, false);
        }
    }
    
    async startQrScannerLibrary() {
        console.log('📱 Using QR Scanner library');
        showFullScreenMessage('📷 Kamera açılıyor...', true);

        try {
            if (this.qrScanner) {
                this.qrScanner.destroy();
            }

            // 🔥 RADIKAL FIX: Video elementi ZORLA görünür - Mobilde tam ekran
            const isMobile = window.innerWidth <= 768;
            if (isMobile) {
                this.videoElement.style.cssText = `
                    position: fixed !important;
                    top: 0 !important;
                    left: 0 !important;
                    width: 100vw !important;
                    height: 100vh !important;
                    object-fit: cover !important;
                    z-index: 10000 !important;
                    display: block !important;
                    visibility: visible !important;
                    opacity: 1 !important;
                    background: #000 !important;
                `;
            } else {
                this.videoElement.style.display = 'block';
                this.videoElement.style.width = '100%';
                this.videoElement.style.height = '100%';
                this.videoElement.style.objectFit = 'cover';
            }
            this.videoElement.setAttribute('playsinline', 'true');
            this.videoElement.setAttribute('autoplay', 'true');

            this.qrScanner = new QrScanner(
                this.videoElement,
                (result) => this.handleQRDetected(result.data),
                {
                    highlightScanRegion: false,
                    highlightCodeOutline: false,
                    maxScansPerSecond: 10,
                    preferredCamera: 'environment'
                }
            );

            await this.qrScanner.start();
            this.isScanning = true;

            // Video'nun kesinlikle görünür olduğundan emin ol - RADIKAL FIX
            setTimeout(() => {
                const isMobile = window.innerWidth <= 768;
                if (isMobile) {
                    this.videoElement.style.cssText = `
                        position: fixed !important;
                        top: 0 !important;
                        left: 0 !important;
                        width: 100vw !important;
                        height: 100vh !important;
                        object-fit: cover !important;
                        z-index: 10000 !important;
                        display: block !important;
                        visibility: visible !important;
                        opacity: 1 !important;
                        background: #000 !important;
                    `;
                    console.log('✅ ULTRA SCANNER: Video visibility FORCED (mobile)');
                } else {
                    this.videoElement.style.display = 'block';
                    console.log('✅ ULTRA SCANNER: Video visibility enforced (desktop)');
                }
            }, 500);

            // 🔥 SÜREKLI VİDEO KONTROLÜ - Ultra Scanner için
            this.videoVisibilityInterval = setInterval(() => {
                if (!this.isScanning || !this.videoElement) {
                    clearInterval(this.videoVisibilityInterval);
                    return;
                }
                
                const isMobile = window.innerWidth <= 768;
                if (isMobile) {
                    const currentDisplay = window.getComputedStyle(this.videoElement).display;
                    const currentVisibility = window.getComputedStyle(this.videoElement).visibility;
                    const currentOpacity = parseFloat(window.getComputedStyle(this.videoElement).opacity);
                    
                    if (currentDisplay === 'none' || currentVisibility === 'hidden' || currentOpacity < 0.5) {
                        console.warn('⚠️ ULTRA SCANNER: Video gizlenmiş, tekrar görünür yapılıyor...');
                        this.videoElement.style.cssText = `
                            position: fixed !important;
                            top: 0 !important;
                            left: 0 !important;
                            width: 100vw !important;
                            height: 100vh !important;
                            object-fit: cover !important;
                            z-index: 10000 !important;
                            display: block !important;
                            visibility: visible !important;
                            opacity: 1 !important;
                            background: #000 !important;
                        `;
                    }
                }
            }, 1000); // Her saniye kontrol

            showFullScreenMessage('✅ Kamera hazır - QR okutabilirsiniz!', true);
            this.showMessage('📱 QR kodları taramaya hazır', true);

        } catch (error) {
            console.error('QR Scanner library failed:', error);
            showFullScreenMessage('⚠️ Kamera hatası - alternatif yöntem deneniyor...', false);
            await this.startZXingScanner();
        }
    }
    
    async startZXingScanner() {
        console.log('📱 Using ZXing library');
        
        try {
            // 🔧 Enhanced camera permission check
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                throw new Error('Camera API not supported');
            }
            
            // Check HTTPS requirement
            if (location.protocol !== 'https:' && location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {
                console.warn('⚠️ HTTPS required for camera access in production');
            }
            
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { 
                    facingMode: 'environment',
                    width: { ideal: 1920 },
                    height: { ideal: 1080 }
                }
            });
            
            this.videoElement.srcObject = stream;
            // Guard video.play() to prevent SecurityError
            try {
                await this.videoElement.play();
            } catch (e) {
                console.warn('📹 Video autoplay blocked (expected on first scan):', e.message);
            }
            
            const codeReader = new ZXing.BrowserQRCodeReader();
            
            codeReader.decodeFromVideoDevice(null, this.videoElement, (result, err) => {
                if (result) {
                    this.handleQRDetected(result.getText());
                }
            });
            
            this.isScanning = true;
            this.showMessage('📱 ZXing scanner başlatıldı', true);
            
        } catch (error) {
            console.error('ZXing failed:', error);
            await this.startManualScanner();
        }
    }
    
    async startManualScanner() {
        console.log('📱 Using manual scanner with jsQR');
        
        // 🔧 Enhanced camera constraints with multiple fallbacks
        const constraints = [
            { video: { facingMode: 'environment', width: { ideal: 1920 }, height: { ideal: 1080 } } },
            { video: { facingMode: 'environment' } },
            { video: { width: { ideal: 1280 }, height: { ideal: 720 } } },
            { video: true }
        ];
        
        let stream = null;
        for (const constraint of constraints) {
            try {
                console.log('🎥 Trying camera constraint:', constraint);
                stream = await navigator.mediaDevices.getUserMedia(constraint);
                console.log('✅ Camera access successful!');
                break;
            } catch (error) {
                console.warn('⚠️ Camera constraint failed:', error.message);
                continue;
            }
        }
        
        if (!stream) {
            throw new Error('Kamera erişimi reddedildi veya desteklenmiyor');
        }
        
        // Load jsQR as last resort
        if (!window.jsQR) {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js';
            document.head.appendChild(script);
            
            await new Promise(resolve => {
                script.onload = resolve;
                script.onerror = resolve;
            });
        }
        
        // Use the stream we already got from constraints loop
        this.videoElement.srcObject = stream;
        
        // 🔧 Enhanced video setup
        this.videoElement.setAttribute('playsinline', true);
        this.videoElement.setAttribute('muted', true);
        this.videoElement.style.display = 'block';
        
        // Wait for video to be ready
        await new Promise((resolve, reject) => {
            this.videoElement.onloadedmetadata = () => {
                console.log('📹 Video metadata loaded');
                this.videoElement.play()
                    .then(() => {
                        console.log('✅ Video playing successfully');
                        resolve();
                    })
                    .catch((e) => {
                        console.warn('📹 Video autoplay blocked:', e.message);
                        resolve(); // Don't reject, just continue
                    });
            };
            
            this.videoElement.onerror = (e) => {
                console.error('❌ Video error:', e);
                reject(new Error('Video failed to load'));
            };
            
            // Timeout fallback
            setTimeout(() => {
                console.warn('⚠️ Video load timeout, trying to play anyway');
                this.videoElement.play()
                    .then(resolve)
                    .catch((e) => {
                        console.warn('📹 Video autoplay blocked (timeout):', e.message);
                        resolve(); // Don't reject, just continue
                    });
            }, 3000);
        });
        
        const canvas = document.getElementById('ultraQRCanvas');
        const ctx = canvas.getContext('2d');
        
        const scanFrame = () => {
            if (!this.isScanning) return;
            
            if (this.videoElement.readyState === this.videoElement.HAVE_ENOUGH_DATA) {
                canvas.width = this.videoElement.videoWidth;
                canvas.height = this.videoElement.videoHeight;
                ctx.drawImage(this.videoElement, 0, 0, canvas.width, canvas.height);
                
                if (window.jsQR) {
                    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                    const code = jsQR(imageData.data, imageData.width, imageData.height);
                    
                    if (code) {
                        this.handleQRDetected(code.data);
                    }
                }
            }
            
            requestAnimationFrame(scanFrame);
        };
        
        this.isScanning = true;
        scanFrame();
        this.showMessage('📱 Manual scanner başlatıldı', true);
    }
    
    handleQRDetected(qrData) {
        const now = Date.now();
        
        // 🔧 KALICI DUPLICATE KONTROLÜ - Bir sayımda bir QR sadece 1 kez okunabilir
        if (window.scannedQRsInSession.has(qrData)) {
            console.log('⚠️ Bu QR zaten okundu, tekrar okuma engellendi');
            
            // Kullanıcıya bildir
            const overlay = document.createElement('div');
            overlay.style.cssText = `
                position: fixed;
                top: 0; left: 0;
                width: 100vw; height: 100vh;
                background: rgba(255, 0, 0, 0.95);
                z-index: 999999;
                display: flex;
                justify-content: center;
                align-items: center;
            `;
            overlay.innerHTML = `
                <div style="
                    font-size: 60px;
                    color: white;
                    font-weight: bold;
                    text-align: center;
                ">
                    ⚠️<br>
                    ZATEN OKUNDU
                </div>
            `;
            document.body.appendChild(overlay);
            setTimeout(() => overlay.remove(), 1500);
            
            return; // Sunucuya gönderme, direkt çık
        }
        
        // 🔧 İşlem kilidi kontrolü
        if (this.isProcessing) {
            console.log('⚠️ QR işleniyor, lütfen bekle');
            return;
        }
        
        this.isProcessing = true;
        this.lastScan = qrData;
        this.lastScanTime = now;
        this.scanCount++;
        
        console.log('🎯 QR Algılandı:', qrData);
        
        // 🔧 TAM EKRAN YEŞİL MESAJ + SES
        this.showSimpleGreenFeedback(qrData);
        
        // ✅ Set'e ekle (kalıcı)
        window.scannedQRsInSession.add(qrData);
        console.log('📝 QR Sete eklendi. Toplam:', window.scannedQRsInSession.size);
        
        // Sunucuya gönder
        this.sendQRToServer(qrData);
        
        // 500ms sonra işlemi bitir (yeni QR okumaya hazır ol)
        setTimeout(() => {
            this.isProcessing = false;
        }, 500);
    }
    
    showSimpleGreenFeedback(qrData) {
        // 🔧 BASİT TAM EKRAN YEŞİL MESAJ
        const overlay = document.createElement('div');
        overlay.id = 'simple-qr-feedback';
        overlay.style.cssText = `
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background: #000000;
            z-index: 999999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        `;
        
        overlay.innerHTML = `
            <div style="
                font-size: 80px;
                color: #00ff00;
                font-weight: bold;
                text-align: center;
                animation: pulse 0.5s ease;
            ">
                ✅<br>
                QR OKUNDU
            </div>
        `;
        
        // Eski overlay varsa kaldır
        const oldOverlay = document.getElementById('simple-qr-feedback');
        if (oldOverlay) oldOverlay.remove();
        
        document.body.appendChild(overlay);
        
        // 🔧 Ses çal
        this.playSuccessSound();
        
        // 1.5 saniye sonra kaldır
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.remove();
            }
        }, 1500);
    }
    
    showFullScreenFeedback(qrData) {
        // 🔧 Create full screen overlay
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background: rgba(0, 0, 0, 0.95);
            z-index: 999999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            animation: feedbackShow 0.3s ease;
        `;
        
        overlay.innerHTML = `
            <div style="font-size: 48px; margin-bottom: 20px;">✅</div>
            <div>QR KOD OKUNDU!</div>
            <div style="font-size: 16px; margin-top: 10px; opacity: 0.8;">${qrData.substring(0, 20)}...</div>
        `;
        
        document.body.appendChild(overlay);
        
        // 🔧 Play success sound (if available)
        this.playSuccessSound();
        
        // 🔧 Vibration
        this.safeVibrate([200, 100, 200]);
        
        // 🔧 Remove overlay after 1.5 seconds
        setTimeout(() => {
            overlay.style.animation = 'feedbackHide 0.3s ease';
            setTimeout(() => {
                overlay.remove();
                this.isProcessing = false; // Re-enable scanning
                console.log(' Scanning re-enabled');
            }, 300);
        }, 1500);
        
        // Add CSS animations if not exists
        if (!document.querySelector('#feedbackAnimations')) {
            const style = document.createElement('style');
            style.id = 'feedbackAnimations';
            style.textContent = `
                @keyframes feedbackShow {
                    from { opacity: 0; transform: scale(0.8); }
                    to { opacity: 1; transform: scale(1); }
                }
                @keyframes feedbackHide {
                    from { opacity: 1; transform: scale(1); }
                    to { opacity: 0; transform: scale(0.8); }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    playSuccessSound() {
        try {
            // Use a shared AudioContext to avoid creating one per-scan and to respect browser policies
            const audioContext = window.sharedAudioContext || (window.sharedAudioContext = new (window.AudioContext || window.webkitAudioContext)());

            if (audioContext.state === 'suspended' && window.userHasInteracted) {
                audioContext.resume().catch(e => console.warn('AudioContext resume failed:', e));
            }

            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.setValueAtTime(1000, audioContext.currentTime + 0.1);

            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.3);

            console.log('🔊 Success sound played');
        } catch (error) {
            console.warn('🔇 Could not play sound:', error.message);
        }
    }
    
    sendQRToServer(qrData) {
        // 🔥 SESSION ID - MULTI-SOURCE FETCH
        let sessionId = this.currentSessionId;
        
        if (!sessionId || sessionId === '1') {
            sessionId = document.body.dataset.sessionId || 
                       window.currentSessionId || 
                       sessionStorage.getItem('currentSessionId');
        }
        
        // Son çare: API'den al
        if (!sessionId || sessionId === '1') {
            console.warn('⚠️ Session ID eksik, API\'den alınıyor...');
            showFullScreenMessage('🔄 Session ID alınıyor...', true);
            
            fetch('/get_count_status')
                .then(r => r.json())
                .then(data => {
                    if (data.active && data.session_id) {
                        sessionId = data.session_id;
                        this.currentSessionId = sessionId;
                        window.currentSessionId = sessionId;
                        sessionStorage.setItem('currentSessionId', sessionId);
                        
                        // Session ID alındıktan sonra tekrar dene
                        this.sendQRToServerWithSession(qrData, sessionId);
                    } else {
                        showFullScreenMessage('❌ Aktif sayım bulunamadı!', false);
                    }
                })
                .catch(e => {
                    console.error('Session ID fetch failed:', e);
                    showFullScreenMessage('❌ Bağlantı hatası!', false);
                });
            return;
        }
        
        this.sendQRToServerWithSession(qrData, sessionId);
    }
    
    sendQRToServerWithSession(qrData, sessionId) {
        const scanData = {
            qr_id: qrData,
            session_id: sessionId,
            timestamp: Date.now(),
            count_access: true
        };

        console.log('📤 Sending to server:', scanData);
        console.log('   Session ID:', sessionId);
        console.log('   Socket connected:', window.socket && window.socket.connected);

        // Primary: Socket.IO
        if (window.socket && window.socket.connected) {
            console.log('✅ Sending via Socket.IO');
            window.socket.emit('scan_qr', scanData);
            window.socket.emit('scan_qr_radical', scanData);
        } else {
            console.warn('⚠️ Socket not connected, using AJAX fallback');
            this.sendViaAJAX(scanData);
        }
    }
    
    async sendViaAJAX(scanData) {
        try {
            const response = await fetch('/api/scan_qr', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(scanData)
            });
            
            const result = await response.json();
            this.handleScanResult(result);
            
        } catch (error) {
            console.error('❌ AJAX failed:', error);
            this.showMessage('❌ Bağlantı hatası!', false);
        }
    }
    
    handleScanResult(data) {
        console.log('📨 Scan result:', data);
        
        if (data.success) {
            this.showMessage(data.message || '✅ QR kod başarıyla okundu!', true);
            this.updateStats();
        } else {
            this.showMessage(data.message || '❌ QR kod okunamadı!', false);
            // Reset processing on error (success is handled by full screen feedback)
            this.isProcessing = false;
        }
    }
    
    flashSuccess() {
        // Green flash effect
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background: rgba(0, 255, 136, 0.3);
            z-index: 999998;
            pointer-events: none;
            animation: flashEffect 0.8s ease;
        `;
        
        document.body.appendChild(flash);
        
        setTimeout(() => flash.remove(), 800);
        
        // 🔧 SAFE VIBRATION: Only after user interaction
        this.safeVibrate([100, 50, 100]);
        
        // Add flash animation if not exists
        if (!document.querySelector('#flashAnimation')) {
            const style = document.createElement('style');
            style.id = 'flashAnimation';
            style.textContent = `
                @keyframes flashEffect {
                    0% { opacity: 0; }
                    50% { opacity: 1; }
                    100% { opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    safeVibrate(pattern) {
        // Titreşim kaldırıldı - sadece ses kullanılıyor
        console.log('📳 Vibration disabled - using sound only');
    }
    
    showMessage(text, isSuccess = true) {
        console.log('💬 Message:', text);
        
        const messagesContainer = document.getElementById('ultraQRMessages');
        if (!messagesContainer) return;
        
        // Clear existing messages
        messagesContainer.innerHTML = '';
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `ultra-message ${isSuccess ? '' : 'error'}`;
        messageDiv.textContent = text;
        
        messagesContainer.appendChild(messageDiv);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (messageDiv.parentElement) {
                messageDiv.remove();
            }
        }, 3000);
    }
    
    updateStats() {
        // Update scan counter
        const counter = document.getElementById('scanCount');
        if (counter) {
            counter.textContent = this.scanCount;
            counter.style.animation = 'bounce 0.5s ease';
        }
        
        // Update activity timeline
        this.updateActivityTimeline();
    }
    
    updateActivityTimeline() {
        const timeline = document.getElementById('activityTimeline');
        if (!timeline) return;
        
        // Add new activity item
        const timeStr = new Date().toLocaleTimeString('tr-TR', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const activityHTML = `
            <div class="activity-item ultra-activity" style="animation: slideInRight 0.5s ease;">
                <div class="activity-icon" style="background: linear-gradient(135deg, #00ff88, #00cc77);">
                    <i class="bi bi-qr-code" style="color: white;"></i>
                </div>
                <div class="activity-content">
                    <div class="activity-title">QR Kod Okundu</div>
                    <div class="activity-meta">
                        <span class="activity-time">${timeStr}</span>
                    </div>
                </div>
            </div>
        `;
        
        timeline.insertAdjacentHTML('afterbegin', activityHTML);
        
        // Keep only last 10 items
        while (timeline.children.length > 10) {
            timeline.removeChild(timeline.lastChild);
        }
    }
    
    setupEventListeners() {
        // Socket.IO events
        if (window.socket) {
            window.socket.on('scan_result', (data) => this.handleScanResult(data));
            window.socket.on('qr_scanned', (data) => this.handleScanResult(data));
            window.socket.on('activity_update', (data) => this.handleScanResult(data));
        }
        
        // Visibility change
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pauseScanning();
            } else {
                this.resumeScanning();
            }
        });
        
        // Orientation change
        window.addEventListener('orientationchange', () => {
            setTimeout(() => this.adjustLayout(), 500);
        });
    }
    
    setupSocketIO() {
        if (!window.socket) return;
        
        window.socket.on('connect', () => {
            console.log('✅ Socket connected');
            this.showMessage('🔗 Bağlantı kuruldu', true);
        });
        
        window.socket.on('disconnect', () => {
            console.log('❌ Socket disconnected');
            this.showMessage('⚠️ Bağlantı kesildi', false);
        });
    }
    
    pauseScanning() {
        this.isScanning = false;
        if (this.qrScanner) {
            this.qrScanner.pause();
        }
    }
    
    resumeScanning() {
        this.isScanning = true;
        if (this.qrScanner) {
            this.qrScanner.start();
        }
    }
    
    stopScanning() {
        this.isScanning = false;
        
        // 🔥 Video kontrol interval'ini temizle
        if (this.videoVisibilityInterval) {
            clearInterval(this.videoVisibilityInterval);
            this.videoVisibilityInterval = null;
            console.log('✅ Video visibility interval cleared');
        }
        
        if (this.qrScanner) {
            this.qrScanner.destroy();
            this.qrScanner = null;
        }
        
        if (this.videoElement && this.videoElement.srcObject) {
            const tracks = this.videoElement.srcObject.getTracks();
            tracks.forEach(track => track.stop());
            this.videoElement.srcObject = null;
        }
        
        console.log('🛑 Ultra QR Scanner stopped');
    }
    
    adjustLayout() {
        // Auto-adjust for different screen sizes
        const container = document.getElementById('ultraQRContainer');
        if (!container) return;
        
        const isPortrait = window.innerHeight > window.innerWidth;
        const isMobile = window.innerWidth <= 768;
        
        if (isMobile) {
            container.style.position = 'fixed';
            container.style.top = '0';
            container.style.left = '0';
            container.style.width = '100vw';
            container.style.height = '100vh';
            container.style.zIndex = '999999';
        }
    }
    
    getSessionId() {
        return window.currentSessionId || 
               localStorage.getItem('currentSessionId') ||
               sessionStorage.getItem('currentSessionId') ||
               document.body.dataset.sessionId ||
               '1';
    }

    // 🔥 YENİ: Sayım sıfırlandığında Set'i temizle
    resetSession(newSessionId) {
        console.log('🔄 Ultra Scanner - Session reset:', newSessionId);
        
        // Global Set'i temizle
        if (window.scannedQRsInSession) {
            window.scannedQRsInSession.clear();
            console.log('🗑️ scannedQRsInSession.clear() - Ultra Scanner');
        }
        
        // Session ID'yi güncelle
        if (newSessionId) {
            this.currentSessionId = newSessionId;
            window.currentSessionId = newSessionId;
            sessionStorage.setItem('currentSessionId', newSessionId);
            console.log('✅ Yeni Session ID: ', newSessionId);
        }
        
        // Scanner state'i sıfırla
        this.lastScan = '';
        this.lastScanTime = 0;
        this.scanCount = 0;
        
        console.log('✅ Ultra Scanner reset tamamlandı');
    }
}

// 🚀 AUTO-INITIALIZE
let ultraScanner = null;

function initUltraQRScanner() {
    if (ultraScanner) {
        ultraScanner.stopScanning();
    }
    
    ultraScanner = new UltraQRScanner();
    
    // Global access
    window.ultraScanner = ultraScanner;
    
    return ultraScanner;
}

function startUltraScanning() {
    if (!ultraScanner) {
        ultraScanner = initUltraQRScanner();
    }
    
    return ultraScanner.startScanning();
}

function stopUltraScanning() {
    if (ultraScanner) {
        ultraScanner.stopScanning();
    }
}

// Replace existing camera functions
if (typeof window.startCamera === 'function') {
    const originalStartCamera = window.startCamera;
    window.startCamera = async function() {
        console.log('🚀 Hijacked startCamera - using Ultra Scanner');
        await startUltraScanning();
    };
}

if (typeof window.stopCamera === 'function') {
    const originalStopCamera = window.stopCamera;
    window.stopCamera = function() {
        console.log('🛑 Hijacked stopCamera - using Ultra Scanner');
        stopUltraScanning();
    };
}

// Auto-start on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Ultra QR Scanner DOM ready');
    
    // Auto-start if on count page
    if (window.location.pathname.includes('/count') || 
        document.getElementById('reader') ||
        document.querySelector('.scanner-section')) {
        
        setTimeout(() => {
            console.log('🚀 Auto-starting Ultra QR Scanner');
            initUltraQRScanner();
        }, 1000);
    }
});

console.log('🚀 Ultra QR Scanner Module Loaded!');