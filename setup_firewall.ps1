# Flask EnvanterQR - Firewall Kuralı Kurulum Script'i
# Bu script'i YÖNETİCİ OLARAK çalıştırın!

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "🔥 WINDOWS FIREWALL KURULUMU - Flask EnvanterQR" -ForegroundColor Yellow
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host ""

# Admin kontrolü
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ HATA: Bu script YÖNETİCİ haklarıyla çalıştırılmalı!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Çözüm:" -ForegroundColor Yellow
    Write-Host "  1. PowerShell'i SAĞ TIK → 'Yönetici olarak çalıştır'" -ForegroundColor White
    Write-Host "  2. Bu script'i tekrar çalıştır" -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}

Write-Host "✅ Yönetici hakları doğrulandı" -ForegroundColor Green
Write-Host ""

# Mevcut kuralı kontrol et
$existingRule = Get-NetFirewallRule -DisplayName "Flask EnvanterQR*" -ErrorAction SilentlyContinue

if ($existingRule) {
    Write-Host "⚠️  Mevcut kural bulundu, siliniyor..." -ForegroundColor Yellow
    Remove-NetFirewallRule -DisplayName "Flask EnvanterQR*"
    Write-Host "✅ Eski kural silindi" -ForegroundColor Green
    Write-Host ""
}

# Yeni firewall kuralı oluştur
Write-Host "🔧 Yeni firewall kuralı oluşturuluyor..." -ForegroundColor Cyan
Write-Host ""

try {
    New-NetFirewallRule `
        -DisplayName "Flask EnvanterQR - Port 5002" `
        -Direction Inbound `
        -Protocol TCP `
        -LocalPort 5002 `
        -Action Allow `
        -Profile Private,Domain `
        -Description "Flask EnvanterQR uygulaması için gelen bağlantılara izin ver (Port 5002)"
    
    Write-Host "✅ Firewall kuralı başarıyla oluşturuldu!" -ForegroundColor Green
    Write-Host ""
    
    # Kuralı göster
    Write-Host "📋 Oluşturulan Kural Detayları:" -ForegroundColor Cyan
    Write-Host ""
    Get-NetFirewallRule -DisplayName "Flask EnvanterQR*" | Format-Table -Property DisplayName, Enabled, Direction, Action
    
    Write-Host ""
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host ("=" * 69) -ForegroundColor Green
    Write-Host "🎉 KURULUM TAMAMLANDI!" -ForegroundColor Green
    Write-Host ("=" * 70) -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 Artık aynı WiFi ağındaki telefonlar bağlanabilir!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Sonraki adımlar:" -ForegroundColor Cyan
    Write-Host "  1. python app.py          (Flask'ı başlat)" -ForegroundColor White
    Write-Host "  2. python get_network_ip.py  (IP adresini öğren)" -ForegroundColor White
    Write-Host "  3. Telefondan o IP:5002 adresine bağlan" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "❌ HATA: Firewall kuralı oluşturulamadı!" -ForegroundColor Red
    Write-Host "Hata mesajı: $_" -ForegroundColor Red
    Write-Host ""
    pause
    exit 1
}

pause
