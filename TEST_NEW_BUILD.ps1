# ========================================
# YENİ BUILD TEST SCRİPTİ
# ========================================
# Bu script yeni installer'ı test etmek için kullanılır

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "    KRİTİK FIX TEST" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "KRİTİK DÜZELTİLER:" -ForegroundColor Red
Write-Host "✓ B2 sync KALDIRILDI startup'tan (1726 dosya indirmiyordu!)" -ForegroundColor Green
Write-Host "✓ Static klasörler AppData kullanıyor" -ForegroundColor Green
Write-Host "✓ Admin izni ile çalışıyor`n" -ForegroundColor Green

Write-Host "BEKLENTİLER:" -ForegroundColor Yellow
Write-Host "1. Uygulama 5-10 saniyede açılacak (30-40 dakika DEĞİL!)" -ForegroundColor White
Write-Host "2. Login ekranı hemen görünecek" -ForegroundColor White
Write-Host "3. QR kodlar eksik olabilir (normal - manuel sync gerekli)" -ForegroundColor White
Write-Host "4. Log'larda B2 sync GÖRÜNMEYECEk`n" -ForegroundColor White

Write-Host "TEST ADIMLARI:" -ForegroundColor Yellow
Write-Host "1. Eski Cermak-Envanter'ı kaldır (İsteğe bağlı)" -ForegroundColor White
Write-Host "2. Yeni installer'ı çalıştır" -ForegroundColor White
Write-Host "3. Uygulamayı aç ve bekle" -ForegroundColor White
Write-Host "4. Bu script'i tekrar çalıştır LOG KONTROLÜ için`n" -ForegroundColor White

$choice = Read-Host "Test etmek istiyor musun? (E/H)"

if ($choice -eq "E" -or $choice -eq "e") {
    Write-Host "`n[1] Installer açılıyor..." -ForegroundColor Cyan
    $installer = "frontend\electron\dist\Cermak-Envanter-Setup-0.1.0.exe"
    
    if (Test-Path $installer) {
        Start-Process $installer -Wait
        
        Write-Host "`n[2] Kurulum tamamlandı, şimdi log kontrolü yapılıyor..." -ForegroundColor Cyan
        Start-Sleep -Seconds 3
        
        $logDir = "$env:APPDATA\Cermak-Envanter\logs"
        
        Write-Host "`n=== LOG KONTROLÜ ===" -ForegroundColor Yellow
        Write-Host "Log dizini: $logDir`n" -ForegroundColor Cyan
        
        if (Test-Path $logDir) {
            Write-Host "✓ Log dizini bulundu!" -ForegroundColor Green
            
            $logFiles = Get-ChildItem $logDir -File | Sort-Object LastWriteTime -Descending
            
            if ($logFiles.Count -gt 0) {
                Write-Host "✓ Log dosyaları oluşturuldu:`n" -ForegroundColor Green
                
                foreach ($log in $logFiles) {
                    $size = $log.Length
                    $time = $log.LastWriteTime
                    Write-Host "  📄 $($log.Name)" -ForegroundColor White
                    Write-Host "     Boyut: $size bytes" -ForegroundColor Gray
                    Write-Host "     Tarih: $time`n" -ForegroundColor Gray
                }
                
                Write-Host "`n=== SON LOG İÇERİĞİ ===" -ForegroundColor Yellow
                $latestLog = $logFiles[0]
                Write-Host "Dosya: $($latestLog.Name)`n" -ForegroundColor Cyan
                
                Get-Content $latestLog.FullName -Tail 20
                
                Write-Host "`n✅ BAŞARILI! Backend logları çalışıyor!" -ForegroundColor Green
            } else {
                Write-Host "✗ Log dosyası yok - Backend hala başlamadı" -ForegroundColor Red
                Write-Host "`nŞunları kontrol et:" -ForegroundColor Yellow
                Write-Host "1. Uygulama açıldı mı?" -ForegroundColor White
                Write-Host "2. Backend başlatma ekranı göründü mü?" -ForegroundColor White
                Write-Host "3. Herhangi bir hata mesajı var mı?`n" -ForegroundColor White
            }
        } else {
            Write-Host "✗ Log dizini bulunamadı - Backend hiç çalışmadı!" -ForegroundColor Red
            Write-Host "`nOlası nedenler:" -ForegroundColor Yellow
            Write-Host "1. Uygulama hiç açılmadı" -ForegroundColor White
            Write-Host "2. Backend exe çalıştırılamadı" -ForegroundColor White
            Write-Host "3. AppData izinleri sorunu`n" -ForegroundColor White
        }
        
        # Static klasör kontrolü
        Write-Host "`n=== STATIC KLASÖR KONTROLÜ ===" -ForegroundColor Yellow
        $staticDir = "$env:APPDATA\Cermak-Envanter\static"
        
        if (Test-Path $staticDir) {
            Write-Host "✓ Static dizini bulundu!" -ForegroundColor Green
            Get-ChildItem $staticDir -Directory | ForEach-Object {
                Write-Host "  📁 $($_.Name)" -ForegroundColor Cyan
            }
        } else {
            Write-Host "✗ Static dizini yok" -ForegroundColor Red
        }
        
    } else {
        Write-Host "✗ Installer bulunamadı: $installer" -ForegroundColor Red
    }
    
} elseif ($choice -eq "L" -or $choice -eq "l") {
    # Sadece log kontrolü
    Write-Host "`n=== MEVCUT LOG KONTROLÜ ===" -ForegroundColor Yellow
    
    $logDir = "$env:APPDATA\Cermak-Envanter\logs"
    
    if (Test-Path $logDir) {
        $logFiles = Get-ChildItem $logDir -File -Recurse | Sort-Object LastWriteTime -Descending
        
        if ($logFiles.Count -gt 0) {
            Write-Host "✓ $($logFiles.Count) log dosyası bulundu:`n" -ForegroundColor Green
            
            foreach ($log in $logFiles) {
                Write-Host "📄 $($log.Name)" -ForegroundColor Cyan
                Write-Host "   $($log.FullName)" -ForegroundColor Gray
                Write-Host "   $([math]::Round($log.Length / 1KB, 2)) KB - $($log.LastWriteTime)`n" -ForegroundColor White
            }
            
            Write-Host "`n=== EN SON LOG (20 satır) ===" -ForegroundColor Yellow
            Get-Content $logFiles[0].FullName -Tail 20
        } else {
            Write-Host "✗ Log dosyası yok" -ForegroundColor Red
        }
    } else {
        Write-Host "✗ Log dizini yok: $logDir" -ForegroundColor Red
    }
} else {
    Write-Host "`nTest iptal edildi.`n" -ForegroundColor Yellow
}

Write-Host "`n========================================`n" -ForegroundColor Cyan
