(function() {
    'use strict';

    console.log('COUNT MAIN LOADING...');

    let cameraManager = null;
    let qrProcessor = null;
    let uiManager = null;
    let apiService = null;
    let socketHandler = null;

    document.addEventListener('DOMContentLoaded', async function() {
        try {
            console.log('DOM LOADED');

            if (typeof Html5Qrcode === 'undefined') {
                console.error('Html5Qrcode NOT LOADED!');
                alert('QR Scanner yuklenemedi! Sayfayi yenileyin.');
                return;
            }

            console.log('Html5Qrcode READY');

            apiService = new window.APIService();
            console.log('API Service ready');

            uiManager = new window.UIManager();
            console.log('UI Manager ready');

            const authData = await apiService.checkAuth();
            if (!authData || !authData.username) {
                window.location.href = '/login';
                return;
            }

            document.getElementById('userName').textContent = authData.username;
            document.getElementById('sessionInfo').textContent = 'Session ID: ' + (authData.session_id || '-');
            console.log('User:', authData.username);

            qrProcessor = new window.QRProcessor(apiService, uiManager);
            console.log('QR Processor ready');

            cameraManager = new window.CameraManager();
            await cameraManager.initialize();
            console.log('Camera Manager ready');

            try {
                socketHandler = new window.SocketHandler(apiService, uiManager);
                socketHandler.connect();
                console.log('Socket connected');
            } catch (error) {
                console.warn('Socket error:', error);
            }

            await startScanning();

            console.log('SYSTEM READY!');

        } catch (error) {
            console.error('Init error:', error);
            alert('Sistem hatasi: ' + error.message);
        }
    });

    async function startScanning() {
        try {
            console.log('Starting scan...');

            await cameraManager.startCamera(
                (qrText) => handleQRSuccess(qrText),
                (error) => handleQRError(error)
            );

            console.log('CAMERA ACTIVE - GREEN BOX VISIBLE!');

        } catch (error) {
            console.error('Camera start error:', error);
            alert('Camera hatasi: ' + error.message);
        }
    }

    async function handleQRSuccess(qrText) {
        try {
            console.log('QR SCANNED:', qrText);
            await qrProcessor.handleQRCode(qrText);
        } catch (error) {
            console.error('QR process error:', error);
        }
    }

    function handleQRError(error) {
        console.error('QR scan error:', error);
    }

    async function stopScanning() {
        try {
            if (cameraManager) {
                await cameraManager.stopCamera();
            }
            console.log('Camera stopped');
        } catch (error) {
            console.error('Stop error:', error);
        }
    }

    window.goToMain = function() {
        stopScanning().then(() => {
            window.location.href = '/main';
        });
    };

    window.goToReports = function() {
        stopScanning().then(() => {
            window.location.href = '/reports';
        });
    };

    window.logout = async function() {
        try {
            await stopScanning();
            await apiService.logout();
            window.location.href = '/login';
        } catch (error) {
            console.error('Logout error:', error);
            window.location.href = '/login';
        }
    };

    window.finishCount = async function() {
        console.log('Finish count called');
        
        try {
            const authData = await apiService.checkAuth();
            if (authData.role !== 'admin') {
                uiManager.showMessage('Sadece adminler sayimi bitirebilir!', false);
                return;
            }
        } catch (error) {
            console.error('Auth check error', error);
            return;
        }
        
        const finishModal = new bootstrap.Modal(document.getElementById('finishCountModal'));
        finishModal.show();
    };

    window.confirmFinishCount = async function() {
        try {
            console.log('Confirming finish count...');
            
            const response = await apiService.finishCount();
            
            if (response.success) {
                await stopScanning();
                uiManager.showMessage('Sayim tamamlandi! Raporlar sayfasina yonlendiriliyorsunuz...', true);
                
                setTimeout(() => {
                    window.location.href = '/reports';
                }, 2000);
            } else {
                uiManager.showMessage('Sayim bitirilemedi: ' + (response.message || ''), false);
            }
        } catch (error) {
            console.error('Finish count error', error);
            uiManager.showMessage('Sayim bitirilemedi: ' + error.message, false);
        }
    };

    window.toggleDebugPanel = function() {
        const debugPanel = document.getElementById('debugPanel');
        if (debugPanel) {
            debugPanel.classList.toggle('active');
        }
    };

    window.toggleFlash = async function() {
        if (cameraManager) {
            await cameraManager.toggleFlash();
        }
    };

    window.switchCamera = async function() {
        if (cameraManager) {
            await cameraManager.switchCamera();
        }
    };

    window.addEventListener('beforeunload', function() {
        stopScanning();
    });

    console.log('COUNT MAIN LOADED!');

})();
