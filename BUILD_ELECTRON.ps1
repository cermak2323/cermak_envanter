#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Cermak Envanter - Build Electron + Flask Application
.DESCRIPTION
    Builds standalone executable with embedded Electron GUI and Flask backend
#>

$ErrorActionPreference = "Stop"

Write-Host "╔════════════════════════════════════════════════════════════════╗"
Write-Host "║   CERMAK ENVANTER - Electron + Flask Build (PowerShell)        ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝"
Write-Host ""

# Colors
$Green = 'Green'
$Yellow = 'Yellow'
$Red = 'Red'

function Check-Command {
    param([string]$Command, [string]$InstallUrl)
    
    try {
        $result = & $Command --version 2>&1
        Write-Host "✓ $Command found" -ForegroundColor $Green
        return $true
    } catch {
        Write-Host "✗ $Command not found!" -ForegroundColor $Red
        if ($InstallUrl) {
            Write-Host "  Install from: $InstallUrl" -ForegroundColor $Yellow
        }
        return $false
    }
}

# Check prerequisites
Write-Host ""
Write-Host "Checking prerequisites..."
Write-Host ""

if (-not (Check-Command "python" "https://python.org")) {
    exit 1
}

if (-not (Check-Command "node" "https://nodejs.org")) {
    Write-Host "⚠ Node.js not found, attempting build anyway..." -ForegroundColor $Yellow
}

# Check PyInstaller
Write-Host ""
Write-Host "Checking PyInstaller..."
try {
    python -m PyInstaller --version | Out-Null
    Write-Host "✓ PyInstaller ready" -ForegroundColor $Green
} catch {
    Write-Host "Installing PyInstaller..."
    python -m pip install PyInstaller | Out-Null
    Write-Host "✓ PyInstaller installed" -ForegroundColor $Green
}

# Menu
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════"
Write-Host "Build Options:"
Write-Host "════════════════════════════════════════════════════════════════"
Write-Host "1) Run locally (development mode)"
Write-Host "2) Build executable (production build)"
Write-Host "3) Clean and rebuild"
Write-Host "4) Exit"
Write-Host ""

$choice = Read-Host "Enter choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Starting development mode..."
        Write-Host ""
        python electron_launcher.py
    }
    "2" {
        Write-Host ""
        Write-Host "Building executable..."
        Write-Host ""
        python build_electron_app.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✓ Build complete!" -ForegroundColor $Green
            Write-Host ""
            $exePath = ".\dist\CermakEnvanter.exe"
            if (Test-Path $exePath) {
                $size = [math]::Round((Get-Item $exePath).Length / 1MB, 1)
                Write-Host "Executable: CermakEnvanter.exe ($size MB)"
                Write-Host "Location: .\dist\"
                Write-Host ""
                Write-Host "Ready for deployment to:"
                Write-Host "  \\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\"
            }
        } else {
            Write-Host ""
            Write-Host "✗ Build failed!" -ForegroundColor $Red
            exit 1
        }
    }
    "3" {
        Write-Host ""
        Write-Host "Cleaning build artifacts..."
        Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
        Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "✓ Cleaned" -ForegroundColor $Green
        Write-Host ""
        Write-Host "Building..."
        python build_electron_app.py
    }
    "4" {
        Write-Host "Exiting..."
        exit 0
    }
    default {
        Write-Host "Invalid choice" -ForegroundColor $Red
        exit 1
    }
}

Read-Host "Press Enter to continue"
