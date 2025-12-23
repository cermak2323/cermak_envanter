; EnvanterQR NSIS Installer Script
; Çift tıkla - Otomatik kurulur, başlatılır

;--------------------------------------
; Includes
;--------------------------------------
!include "MUI2.nsh"
!include "LogicLib.nsh"

;--------------------------------------
; Attributes
;--------------------------------------
Name "EnvanterQR v1.0"
OutFile "EnvanterQR_Setup.exe"
InstallDir "$PROGRAMFILES\EnvanterQR"

;--------------------------------------
; Installer Attributes
;--------------------------------------
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "Turkish"

;--------------------------------------
; Installer Sections
;--------------------------------------
Section "EnvanterQR Kur"
    SetOutPath "$INSTDIR"
    
    ; Main executable
    File "dist\EnvanterQR.exe"
    
    ; Database ve files
    SetOutPath "$INSTDIR\instance"
    File /r "instance\*.*"
    
    SetOutPath "$INSTDIR\static"
    File /r "static\*.*"
    
    SetOutPath "$INSTDIR\templates"
    File /r "templates\*.*"
    
    SetOutPath "$INSTDIR"
    File "*.py"
    File "*.txt"
    File "*.md"
    
    ; Create shortcuts
    SetOutPath "$INSTDIR"
    CreateDirectory "$SMPROGRAMS\EnvanterQR"
    CreateShortCut "$SMPROGRAMS\EnvanterQR\EnvanterQR.lnk" "$INSTDIR\EnvanterQR.exe" "" "$INSTDIR\EnvanterQR.exe" 0
    CreateShortCut "$SMPROGRAMS\EnvanterQR\Sil.lnk" "$SYSDIR\control.exe" "appwiz.cpl" "" 0
    CreateShortCut "$DESKTOP\EnvanterQR.lnk" "$INSTDIR\EnvanterQR.exe" "" "$INSTDIR\EnvanterQR.exe" 0
    
SectionEnd

;--------------------------------------
; Uninstaller
;--------------------------------------
Section "Uninstall"
    Delete "$SMPROGRAMS\EnvanterQR\EnvanterQR.lnk"
    Delete "$SMPROGRAMS\EnvanterQR\Sil.lnk"
    Delete "$DESKTOP\EnvanterQR.lnk"
    RMDir "$SMPROGRAMS\EnvanterQR"
    RMDir /r "$INSTDIR"
SectionEnd

;--------------------------------------
; Post-install
;--------------------------------------
Function .onInstallSuccess
    MessageBox MB_YESNO "EnvanterQR başlatılsın mı?" IDNO end
        ExecShell "open" "$INSTDIR\EnvanterQR.exe"
    end:
FunctionEnd
