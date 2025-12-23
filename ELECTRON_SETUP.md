# Cermak Envanter - Electron Setup Guide

## Quick Start

### Option 1: Run Electron + Flask Locally (Development)

```bash
cd electron
npm install
cd ..
python electron_launcher.py
```

This starts Flask backend automatically and opens Electron GUI.

### Option 2: Build Standalone Executable

```bash
python build_electron_app.py
```

This creates `CermakEnvanter.exe` that can be deployed to network shares.

## How It Works

### Electron Architecture

1. **Electron Main Process** (`electron/main.js`)
   - Manages Electron window lifecycle
   - Starts Flask backend automatically
   - Waits for Flask health check before opening window
   - Gracefully terminates Flask on app close

2. **Python Launcher** (`electron_launcher.py`)
   - Entry point for executable
   - Starts Flask subprocess
   - Launches Electron after Flask is ready
   - Handles cleanup and signals

3. **Flask Backend** (`app.py`)
   - Runs on port 5002
   - Serves all API endpoints
   - Serves static files from network

4. **Electron Window**
   - Displays Flask app at `http://localhost:5002`
   - No console window (--noconsole)
   - Frameless or minimal window decoration

## Installation Requirements

### For Development
```bash
# Install Node.js from https://nodejs.org
# Install Python 3.11+
# Install dependencies
cd electron
npm install
```

### For Building Executable
```bash
pip install PyInstaller
cd electron
npm install
npm install -g electron-builder  # Optional, for native builds
```

## Build Process

1. Install npm dependencies for Electron
2. Build Electron app (optional, can be skipped)
3. PyInstaller packages:
   - electron_launcher.py (entry point)
   - Flask backend (app.py + dependencies)
   - Electron app files
   - All data folders (templates, backend)
4. Result: Single .exe file (~400 MB)
5. Deployed to: `\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\CermakEnvanter.exe`

## File Structure

```
EnvanterQR/
├── app.py                    # Flask backend
├── electron_launcher.py      # Python launcher
├── build_electron_app.py     # Build script
├── electron/
│   ├── main.js              # Electron main process
│   ├── preload.js           # IPC bridge
│   ├── package.json         # npm config
│   └── node_modules/        # npm dependencies
├── templates/               # Flask templates
├── static/                  # Static files (on network)
└── backend/                 # Backend modules
```

## Debugging

### Run with Debug Logs
```bash
set ELECTRON_DEV=1
python build_electron_app.py
```

### Check Flask Health
```bash
curl http://localhost:5002/health
```

### View Electron Logs
Press Ctrl+Shift+I in Electron window to open DevTools

### Kill Stuck Processes
```bash
taskkill /F /IM python.exe /T
taskkill /F /IM CermakEnvanter.exe /T
```

## Troubleshooting

### "Flask backend failed to start"
- Check if port 5002 is available
- Verify Python and dependencies are installed
- Check app.py for syntax errors

### "npm: command not found"
- Install Node.js from https://nodejs.org
- Add Node.js to PATH environment variable

### "Electron window won't open"
- Flask may still be starting (wait 10-15 seconds)
- Check console output for error messages
- Verify FLASK_URL in main.js matches Flask port

### "Connection refused at http://localhost:5002"
- Flask process may have crashed
- Check app.py logs for errors
- Try running Flask manually: `python app.py`

## Performance Notes

- First launch takes 30-45 seconds (Flask startup + Electron)
- Subsequent launches cached by Electron
- Exe size ~400 MB (includes Python + all dependencies)
- Runs as single process on main thread

## Security

- All code runs on localhost (no network exposure of Flask)
- IPC communication between Electron and Flask via HTTP/localhost
- Session tokens stored in browser cookies
- Network file access via UNC paths

## Future Enhancements

- [ ] Auto-update mechanism using Electron Updater
- [ ] Tray icon with minimize/restore
- [ ] System tray integration
- [ ] Keyboard shortcuts customization
- [ ] Dark mode support
