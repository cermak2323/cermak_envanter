class CameraManager {
    constructor() {
        this.html5QrCode = null;
        this.isScanning = false;
        this.onScanSuccess = null;
        this.onScanError = null;
        this.lastScanTime = 0;
        this.DEBOUNCE_TIME = 500;
        console.log("CameraManager initialized");
    }

    async initialize() {
        try {
            console.log("Camera initializing...");
            this.html5QrCode = new Html5Qrcode("reader");
            console.log("Html5Qrcode ready");
            return true;
        } catch (error) {
            console.error("Init error:", error);
            throw error;
        }
    }

    async startCamera(onScanSuccess, onScanError) {
        try {
            if (this.isScanning) {
                console.warn("Camera already active");
                return;
            }

            this.onScanSuccess = onScanSuccess;
            this.onScanError = onScanError;

            const config = { 
                fps: 10,
                qrbox: { width: 300, height: 300 },
                aspectRatio: 1.0,
                formatsToSupport: [ Html5QrcodeSupportedFormats.QR_CODE ]
            };

            await this.html5QrCode.start(
                { facingMode: "environment" },
                config,
                (text, result) => { 
                    this._handleScan(text, result); 
                },
                (err) => {
                    // Ignore scan errors
                }
            );

            this.isScanning = true;
            console.log("✅ CAMERA STARTED - GREEN BOX VISIBLE!");
            console.log("📸 Scanning at 10 fps, 300x300 green box");
            
        } catch (error) {
            console.error("Start error:", error);
            throw error;
        }
    }

    _handleScan(text, result) {
        try {
            const now = Date.now();
            if (now - this.lastScanTime < this.DEBOUNCE_TIME) return;
            this.lastScanTime = now;

            console.log("🎯 QR DETECTED:", text);
            
            // BEEP SOUND
            this._playBeep();
            
            // VIBRATE
            this._vibrate();
            
            if (this.onScanSuccess) {
                this.onScanSuccess(text, null);
            }
        } catch (error) {
            console.error("Scan error:", error);
        }
    }

    _playBeep() {
        try {
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            oscillator.frequency.value = 1200;
            oscillator.type = 'sine';
            gainNode.gain.value = 0.3;
            
            oscillator.start();
            oscillator.stop(audioCtx.currentTime + 0.2);
            
            console.log("🔊 BEEP!");
        } catch (e) {
            console.warn("Sound failed");
        }
    }

    _vibrate() {
        try {
            if (navigator.vibrate) {
                navigator.vibrate(200);
                console.log("📳 VIBRATE!");
            }
        } catch (e) {
            console.warn("Vibrate failed");
        }
    }

    async stopCamera() {
        try {
            if (this.html5QrCode && this.isScanning) {
                await this.html5QrCode.stop();
            }
            this.isScanning = false;
        } catch (error) {
            console.error("Stop error:", error);
        }
    }

    isActive() {
        return this.isScanning;
    }

    async destroy() {
        await this.stopCamera();
        this.html5QrCode = null;
    }
}

window.CameraManager = CameraManager;
console.log("CameraManager loaded");
