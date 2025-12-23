const { app, BrowserWindow } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 764,
    center: true,
    resizable: true,
    frame: true,
    titleBarStyle: 'default',
    autoHideMenuBar: true,
    show: false,
    title: "Cermak Envanter QR Sistemi v2.0",
    icon: path.join(__dirname, 'cermaktakeuchi_logo.ico'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false
    }
  });

  // Splash screen
  mainWindow.loadFile(path.join(__dirname, 'splash.html'));

  // 2 saniye splash sonrası ana uygulamaya geç
  setTimeout(() => {
    // Ubuntu server'ın gerçek adresi
    mainWindow.loadURL('http://192.168.0.57:5002').catch(() => {
      mainWindow.loadFile(path.join(__dirname, 'error.html'));
    });

    mainWindow.once('ready-to-show', () => {
      mainWindow.show();
    });

    // Bağlantı hatasında error sayfası
    mainWindow.webContents.on('did-fail-load', () => {
      mainWindow.loadFile(path.join(__dirname, 'error.html'));
    });
  }, 2000);

  // Sağ tık menüsünü kapat
  mainWindow.webContents.on('context-menu', (e) => {
    e.preventDefault();
  });
}

// Tek örnek çalıştırma
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});