/* 🔥 RADICAL QR SCANNER FRONTEND FIX */

// 🔥 GLOBAL VARIABLES - ULTRA SIMPLE
let isQrScanning = false;
let lastScannedQr = '';
let lastScannedTime = 0;
let scanCount = 0;

// 🔥 RADICAL MESSAGE DISPLAY - ALWAYS VISIBLE
function showRadicalMessage(message, isSuccess = true) {
    console.log('🔥 RADICAL MESSAGE:', message);
    
    // Remove any existing messages
    const existing = document.querySelectorAll('.radical-message');
    existing.forEach(el => el.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = 'radical-message';
    messageDiv.innerHTML = message;
    
    // ULTRA VISIBLE STYLING
    messageDiv.style.cssText = `
        position: fixed !important;
        top: 80px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 2147483647 !important;
        padding: 20px 30px !important;
        border-radius: 15px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-align: center !important;
        width: 85% !important;
        max-width: 400px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.8) !important;
        pointer-events: auto !important;
        border: 3px solid rgba(255,255,255,0.7) !important;
        animation: radicalPulse 0.5s ease !important;
        ${isSuccess ? 
            'background: #28a745 !important; color: white !important;' : 
            'background: #dc3545 !important; color: white !important;'
        }
    `;
    
    document.body.appendChild(messageDiv);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (messageDiv.parentElement) {
            messageDiv.remove();
        }
    }, 3000);
    
    // SUCCESS EFFECTS
    if (isSuccess) {
        // Flash effect
        document.body.style.backgroundColor = 'rgba(40, 167, 69, 0.3)';
        setTimeout(() => {
            document.body.style.backgroundColor = '';
        }, 500);
        
        // Vibrate if available
        if (navigator.vibrate) {
            navigator.vibrate([100, 50, 100]);
        }
    }
}

// 🔥 RADICAL QR SCAN HANDLER
function handleRadicalQrScan(qrCode) {
    console.log('🔥 RADICAL QR SCAN:', qrCode);
    
    // Prevent spam scanning
    const now = Date.now();
    if (qrCode === lastScannedQr && (now - lastScannedTime) < 2000) {
        console.log('⚠️ SPAM DETECTED - ignoring');
        return;
    }
    
    lastScannedQr = qrCode;
    lastScannedTime = now;
    scanCount++;
    
    // Show scanning message
    showRadicalMessage('📡 QR kod işleniyor...', true);
    
    // Get session ID
    const sessionId = getCurrentSessionId();
    if (!sessionId) {
        showRadicalMessage('❌ Session ID bulunamadı!', false);
        return;
    }
    
    // Send to server with multiple fallbacks
    const scanData = {
        qr_id: qrCode,
        session_id: sessionId,
        timestamp: now,
        count_access: true
    };
    
    console.log('📤 Sending scan data:', scanData);
    
    // Primary method - Socket.IO
    if (window.socket && window.socket.connected) {
        window.socket.emit('scan_qr', scanData);
        console.log('✅ Sent via Socket.IO');
    } else {
        // Fallback - AJAX
        fetch('/api/scan_qr', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(scanData)
        })
        .then(response => response.json())
        .then(data => {
            handleScanResult(data);
        })
        .catch(error => {
            console.error('❌ AJAX fallback failed:', error);
            showRadicalMessage('❌ Bağlantı hatası!', false);
        });
        console.log('✅ Sent via AJAX fallback');
    }
}

// 🔥 RADICAL SCAN RESULT HANDLER
function handleScanResult(data) {
    console.log('🔥 RADICAL SCAN RESULT:', data);
    
    if (data.success) {
        showRadicalMessage(data.message || '✅ QR kod başarıyla okundu!', true);
        updateScanCounter();
        updateActivityList(data);
    } else {
        showRadicalMessage(data.message || '❌ QR kod okunamadı!', false);
    }
}

// 🔥 UPDATE SCAN COUNTER
function updateScanCounter() {
    const counterEl = document.getElementById('scanCount');
    if (counterEl) {
        counterEl.textContent = scanCount;
        counterEl.style.animation = 'bounce 0.5s ease';
    }
}

// 🔥 UPDATE ACTIVITY LIST
function updateActivityList(data) {
    const timeline = document.getElementById('activityTimeline');
    if (!timeline) return;
    
    // Remove placeholder if exists
    const placeholder = timeline.querySelector('.text-center');
    if (placeholder) placeholder.remove();
    
    // Create new activity item
    const activityDiv = document.createElement('div');
    activityDiv.className = 'activity-item radical-activity';
    activityDiv.style.animation = 'slideInRight 0.5s ease';
    
    const timeStr = new Date().toLocaleTimeString('tr-TR', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    activityDiv.innerHTML = `
        <div class="activity-icon" style="background: #28a745;">
            <i class="bi bi-qr-code" style="color: white;"></i>
        </div>
        <div class="activity-content">
            <div class="activity-title">${data.part_name || 'QR Kod'}</div>
            <div class="activity-meta">
                <span class="activity-code">${data.part_code || data.qr_code}</span>
                <span class="activity-time">${timeStr}</span>
            </div>
        </div>
    `;
    
    // Insert at top
    timeline.insertBefore(activityDiv, timeline.firstChild);
    
    // Keep only last 10 items
    while (timeline.children.length > 10) {
        timeline.removeChild(timeline.lastChild);
    }
}

// 🔥 GET CURRENT SESSION ID
function getCurrentSessionId() {
    // Try multiple sources
    const sessionId = 
        window.currentSessionId || 
        localStorage.getItem('currentSessionId') ||
        sessionStorage.getItem('currentSessionId') ||
        document.body.dataset.sessionId ||
        '1'; // Fallback
    
    console.log('📱 Current Session ID:', sessionId);
    return sessionId;
}

// 🔥 RADICAL SOCKET.IO SETUP
function setupRadicalSocket() {
    if (!window.socket) {
        console.log('⚠️ Socket.IO not available');
        return;
    }
    
    // Listen for scan results
    window.socket.on('scan_result', handleScanResult);
    window.socket.on('qr_scanned', handleScanResult);  // Alternative event
    window.socket.on('activity_update', handleScanResult);  // Activity event
    
    // Connection status
    window.socket.on('connect', () => {
        console.log('✅ Socket connected');
        showRadicalMessage('🔗 Bağlantı kuruldu', true);
    });
    
    window.socket.on('disconnect', () => {
        console.log('❌ Socket disconnected');
        showRadicalMessage('⚠️ Bağlantı kesildi', false);
    });
}

// 🔥 RADICAL QR FRAME - ALWAYS VISIBLE
function ensureQrFrameVisible() {
    const qrFrame = document.getElementById('qrScanFrame');
    if (!qrFrame) return;
    
    // FORCE VISIBLE
    qrFrame.style.cssText = `
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 280px !important;
        height: 280px !important;
        max-width: 80vw !important;
        max-height: 80vw !important;
        z-index: 999999 !important;
        pointer-events: none !important;
        border: 4px solid #007bff !important;
        border-radius: 20px !important;
        box-shadow: 0 0 20px rgba(0, 123, 255, 0.5) !important;
    `;
    
    console.log('🔥 QR Frame forced visible');
}

// 🔥 RADICAL CAMERA SETUP
function setupRadicalCamera() {
    console.log('🔥 RADICAL CAMERA SETUP');
    
    // Ensure QR frame is visible
    ensureQrFrameVisible();
    
    // Setup continuous monitoring
    setInterval(ensureQrFrameVisible, 1000);
    
    // Setup Socket.IO
    setupRadicalSocket();
    
    console.log('🔥 RADICAL SETUP COMPLETE');
}

// 🔥 RADICAL CSS ANIMATIONS
const radicalStyles = `
<style>
@keyframes radicalPulse {
    0% { transform: translateX(-50%) scale(0.8); opacity: 0; }
    50% { transform: translateX(-50%) scale(1.1); opacity: 1; }
    100% { transform: translateX(-50%) scale(1); opacity: 1; }
}

@keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes bounce {
    0%, 20%, 60%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    80% { transform: translateY(-5px); }
}

.radical-activity {
    border-left: 4px solid #28a745 !important;
    background: rgba(40, 167, 69, 0.1) !important;
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', radicalStyles);

// 🔥 AUTO SETUP ON LOAD
document.addEventListener('DOMContentLoaded', setupRadicalCamera);

console.log('🔥 RADICAL QR SCANNER LOADED');