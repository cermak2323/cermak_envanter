/* ======================
   MOBIL PERFORMANS JAVASCRIPT
   - Hafif ve hızlı
   - Touch optimizasyonları
   ====================== */

document.addEventListener('DOMContentLoaded', function() {
    // Mobile detection
    const isMobile = /Android|iPhone|iPad|iPod|BlackBerry|Windows Phone/i.test(navigator.userAgent);
    
    if (isMobile) {
        document.body.classList.add('mobile-device');
        
        // Touch optimization
        document.body.style.touchAction = 'manipulation';
        
        // Prevent zoom on input focus (iOS)
        const viewport = document.querySelector('meta[name="viewport"]');
        if (viewport) {
            viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
        }
    }
    
    // Loading states for buttons
    function showButtonLoading(button) {
        button.classList.add('btn-loading');
        button.disabled = true;
    }
    
    function hideButtonLoading(button) {
        button.classList.remove('btn-loading');
        button.disabled = false;
    }
    
    // Add loading to form submissions
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                showButtonLoading(submitBtn);
                
                // Reset loading after 10 seconds (fallback)
                setTimeout(() => {
                    hideButtonLoading(submitBtn);
                }, 10000);
            }
        });
    });
    
    // Fast click for mobile
    if (isMobile) {
        let touchStartTime = 0;
        
        document.addEventListener('touchstart', function(e) {
            touchStartTime = Date.now();
        });
        
        document.addEventListener('touchend', function(e) {
            const touchTime = Date.now() - touchStartTime;
            if (touchTime < 150) { // Fast tap
                const target = e.target.closest('.btn, .action-card');
                if (target && !target.disabled) {
                    target.classList.add('active');
                    setTimeout(() => target.classList.remove('active'), 100);
                }
            }
        });
    }
    
    // Simple loading overlay
    window.showLoading = function() {
        let overlay = document.getElementById('loading-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'loading-overlay';
            overlay.className = 'loading-overlay';
            overlay.innerHTML = '<div class="loading-spinner loading-spinner-lg"></div>';
            document.body.appendChild(overlay);
        }
        overlay.style.display = 'flex';
    };
    
    window.hideLoading = function() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    };
    
    // Auto-hide loading on page load
    window.addEventListener('load', function() {
        hideLoading();
    });
});

// Performance: Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Performance: Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}