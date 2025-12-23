#!/usr/bin/env python3
"""
CermakEnvanter - Electron + Flask Launcher
Starts Flask backend and Electron GUI in a single executable
"""

import os
import sys
import time
import subprocess
import atexit
import signal
import requests
from pathlib import Path

FLASK_PORT = 5002
FLASK_URL = f"http://localhost:{FLASK_PORT}"
MAX_RETRIES = 30
RESOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

flask_process = None


def is_flask_ready():
    """Check if Flask is running and healthy"""
    try:
        response = requests.get(f"{FLASK_URL}/health", timeout=1)
        return response.status_code == 200
    except Exception:
        return False


def wait_for_flask(timeout_seconds=30):
    """Wait for Flask to start"""
    print("[LAUNCHER] Waiting for Flask backend to start...")
    start_time = time.time()
    
    while time.time() - start_time < timeout_seconds:
        if is_flask_ready():
            print("[LAUNCHER] ✓ Flask backend is ready!")
            return True
        time.sleep(1)
    
    print("[LAUNCHER] ✗ Flask backend failed to start")
    return False


def start_flask():
    """Start Flask backend process"""
    global flask_process
    
    print("[LAUNCHER] Starting Flask backend...")
    app_py = os.path.join(RESOURCE_PATH, "app.py")
    
    try:
        # Use shell=True for better subprocess handling on Windows
        flask_process = subprocess.Popen(
            [sys.executable, app_py],
            cwd=RESOURCE_PATH,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        )
        
        print(f"[LAUNCHER] Flask process started (PID: {flask_process.pid})")
        return True
    except Exception as e:
        print(f"[LAUNCHER] Failed to start Flask: {e}")
        return False


def start_electron():
    """Start Electron GUI"""
    electron_dir = os.path.join(RESOURCE_PATH, "electron")
    
    try:
        print("[LAUNCHER] Starting Electron GUI...")
        subprocess.run(
            ["npm", "start"],
            cwd=electron_dir,
            check=False,
        )
    except Exception as e:
        print(f"[LAUNCHER] Failed to start Electron: {e}")


def cleanup():
    """Cleanup: terminate Flask process"""
    global flask_process
    if flask_process:
        print("[LAUNCHER] Terminating Flask backend...")
        try:
            flask_process.terminate()
            flask_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            flask_process.kill()
        except Exception as e:
            print(f"[LAUNCHER] Error terminating Flask: {e}")


def signal_handler(sig, frame):
    """Handle shutdown signals"""
    print("[LAUNCHER] Received shutdown signal")
    cleanup()
    sys.exit(0)


def main():
    """Main launcher entry point"""
    print("=" * 70)
    print("CERMAK ENVANTER QR SİSTEMİ - Electron + Flask Launcher")
    print("=" * 70)
    print(f"[LAUNCHER] Resource path: {RESOURCE_PATH}")
    print(f"[LAUNCHER] Flask URL: {FLASK_URL}")
    
    # Register cleanup handlers
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start Flask (non-blocking)
    print("[LAUNCHER] Starting Flask backend...")
    start_flask()
    
    # Wait for Flask to be ready (with timeout)
    print("[LAUNCHER] Waiting for Flask to be ready...")
    flask_ready = wait_for_flask(timeout_seconds=30)
    
    if not flask_ready:
        print("[LAUNCHER] ⚠️  Flask not responding - continuing anyway")
        # Don't exit, try to open Electron anyway
    
    # Start Electron (blocking)
    print("[LAUNCHER] Starting Electron GUI...")
    try:
        start_electron()
    except KeyboardInterrupt:
        print("[LAUNCHER] Interrupted by user")
    except Exception as e:
        print(f"[LAUNCHER] Electron error: {e}")
    finally:
        cleanup()


if __name__ == "__main__":
    main()
