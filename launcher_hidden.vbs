' CermakEnvanter Launcher - Hidden Console
' Bu script Flask backend'ini arka planda başlatıp Electron GUI'ı açar

Dim objShell
Dim strPath
Dim strFlaskExe
Dim strElectronApp

Set objShell = CreateObject("WScript.Shell")

' Network path
strPath = "\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\"
strFlaskExe = strPath & "CermakEnvanter.exe"
strElectronApp = strPath & "resources\app\main.js"

' Flask'ı arka planda (hidden) başlat
objShell.Run strFlaskExe, 0, False

' 2 saniye bekle (Flask başlatılsın)
WScript.Sleep 2000

' Electron GUI'ı aç
' (Electron zaten kurulu ve main.js Flask'ı başlatacak)
objShell.Run "npx electron " & strElectronApp, 1, False

' Goodbye
Set objShell = Nothing
