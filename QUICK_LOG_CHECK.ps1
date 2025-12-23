# HIZLI LOG KONTROLÜ

Write-Host "`n=== LOG KONTROLÜ ===" -ForegroundColor Yellow

$logDir = "$env:APPDATA\Cermak-Envanter\logs"

if (Test-Path $logDir) {
    Write-Host "✓ Log dizini bulundu: $logDir`n" -ForegroundColor Green
    
    $logFiles = Get-ChildItem $logDir -File | Sort-Object LastWriteTime -Descending
    
    if ($logFiles.Count -gt 0) {
        Write-Host "LOG DOSYALARI:" -ForegroundColor Cyan
        foreach ($log in $logFiles) {
            Write-Host "  📄 $($log.Name) - $([math]::Round($log.Length / 1KB, 2)) KB" -ForegroundColor White
        }
        
        Write-Host "`n=== SON 30 SATIR (startup.log) ===" -ForegroundColor Yellow
        $startupLog = $logFiles | Where-Object { $_.Name -eq 'startup.log' } | Select-Object -First 1
        
        if ($startupLog) {
            Get-Content $startupLog.FullName -Tail 30
            
            # B2 sync kontrolü
            Write-Host "`n=== B2 SYNC KONTROLÜ ===" -ForegroundColor Yellow
            $content = Get-Content $startupLog.FullName -Raw
            
            if ($content -match '\[SYNC\] Backblaze B2') {
                Write-Host "❌ SORUN! B2 sync hala çalışıyor!" -ForegroundColor Red
                Write-Host "Startup'ta B2 sync OLMAMALI!" -ForegroundColor Red
            } else {
                Write-Host "✅ TAMAM! B2 sync yok startup'ta" -ForegroundColor Green
            }
            
            if ($content -match '\[DOWNLOAD\].*files missing') {
                Write-Host "❌ SORUN! Dosya indirme var startup'ta!" -ForegroundColor Red
            } else {
                Write-Host "✅ TAMAM! Dosya indirme yok" -ForegroundColor Green
            }
            
            if ($content -match '\[BACKEND\] Backend hazır') {
                Write-Host "✅ TAMAM! Backend başarıyla başladı" -ForegroundColor Green
            } else {
                Write-Host "⚠️  UYARI! Backend başlamadı veya log eksik" -ForegroundColor Yellow
            }
            
        } else {
            Write-Host "✗ startup.log bulunamadı" -ForegroundColor Red
        }
        
    } else {
        Write-Host "✗ Log dosyası yok" -ForegroundColor Red
    }
} else {
    Write-Host "✗ Log dizini yok: $logDir" -ForegroundColor Red
    Write-Host "`nUygulama hiç açılmadı mı?" -ForegroundColor Yellow
}

Write-Host "`n========================================`n" -ForegroundColor Cyan
