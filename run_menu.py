#!/usr/bin/env python3
"""
Cermak Envanter - Build & Run Menu
Provides easy access to all build and run options
"""

import os
import sys
import subprocess
from pathlib import Path
from enum import Enum

class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class Option(Enum):
    RUN_LOCAL = 1
    BUILD_EXE = 2
    TEST_ELECTRON = 3
    CHECK_DEPS = 4
    CLEAN_BUILD = 5
    VIEW_LOGS = 6
    EXIT = 0

APP_DIR = Path(__file__).parent

def print_header():
    print("\n" + "=" * 80)
    print(f"{Color.BOLD}{Color.CYAN}CERMAK ENVANTER - Build & Run Menu{Color.END}")
    print("=" * 80)
    print(f"{Color.GREEN}✓{Color.END} Electron Integration Complete")
    print(f"{Color.GREEN}✓{Color.END} Flask Backend Ready")
    print(f"{Color.GREEN}✓{Color.END} Network Deployment Configured")
    print("=" * 80)
    print()

def print_menu():
    print(f"{Color.BOLD}Options:{Color.END}\n")
    print(f"  {Color.CYAN}1){Color.END} {Color.WHITE}Run Locally (Development Mode){Color.END}")
    print(f"     - Start Flask backend + Electron GUI")
    print(f"     - Best for testing and development")
    print()
    print(f"  {Color.CYAN}2){Color.END} {Color.WHITE}Build Standalone Executable{Color.END}")
    print(f"     - Create CermakEnvanter.exe")
    print(f"     - Deploy to network shared folder")
    print()
    print(f"  {Color.CYAN}3){Color.END} {Color.WHITE}Test Electron Only{Color.END}")
    print(f"     - Run Electron app directly")
    print(f"     - Requires Flask running separately")
    print()
    print(f"  {Color.CYAN}4){Color.END} {Color.WHITE}Check Dependencies{Color.END}")
    print(f"     - Verify Python, Node.js, PyInstaller")
    print(f"     - Install missing packages")
    print()
    print(f"  {Color.CYAN}5){Color.END} {Color.WHITE}Clean and Rebuild{Color.END}")
    print(f"     - Remove build artifacts")
    print(f"     - Rebuild from scratch")
    print()
    print(f"  {Color.CYAN}6){Color.END} {Color.WHITE}View Recent Logs{Color.END}")
    print(f"     - Check Flask and build logs")
    print()
    print(f"  {Color.CYAN}0){Color.END} {Color.WHITE}Exit{Color.END}")
    print()

def run_local():
    print(f"\n{Color.BOLD}Starting Local Development Mode...{Color.END}\n")
    print("This will:")
    print("  1. Start Flask backend on port 5002")
    print("  2. Wait for Flask to become ready")
    print("  3. Open Electron GUI window")
    print()
    
    try:
        subprocess.run(
            [sys.executable, "electron_launcher.py"],
            cwd=APP_DIR,
            check=False,
        )
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}⚠ Stopped by user{Color.END}")
    except Exception as e:
        print(f"{Color.RED}✗ Error: {e}{Color.END}")

def build_exe():
    print(f"\n{Color.BOLD}Building Standalone Executable...{Color.END}\n")
    print("This will:")
    print("  1. Install npm dependencies")
    print("  2. Build Electron app")
    print("  3. Package with PyInstaller")
    print("  4. Deploy to network path")
    print()
    print(f"{Color.YELLOW}⏳ This may take 10-20 minutes on first build{Color.END}")
    print()
    
    try:
        result = subprocess.run(
            [sys.executable, "build_electron_app.py"],
            cwd=APP_DIR,
            check=False,
        )
        
        if result.returncode == 0:
            exe_path = APP_DIR / "dist" / "CermakEnvanter.exe"
            if exe_path.exists():
                size = exe_path.stat().st_size / (1024 * 1024)
                print(f"\n{Color.GREEN}✓ Build successful!{Color.END}")
                print(f"  Executable: CermakEnvanter.exe ({size:.1f} MB)")
                print(f"  Location: {exe_path.parent}")
                print(f"  Status: Ready for deployment")
            else:
                print(f"{Color.YELLOW}⚠ Build completed but exe not found{Color.END}")
        else:
            print(f"{Color.RED}✗ Build failed{Color.END}")
            
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}⚠ Build cancelled{Color.END}")
    except Exception as e:
        print(f"{Color.RED}✗ Error: {e}{Color.END}")

def test_electron():
    print(f"\n{Color.BOLD}Testing Electron...{Color.END}\n")
    print("Requirements:")
    print("  - Flask must be running (python app.py in another terminal)")
    print("  - Node.js must be installed")
    print()
    
    electron_dir = APP_DIR / "electron"
    
    print(f"{Color.YELLOW}Installing npm dependencies...{Color.END}")
    result = subprocess.run(
        ["npm", "install"],
        cwd=electron_dir,
        capture_output=True,
        check=False,
    )
    
    if result.returncode != 0:
        print(f"{Color.RED}✗ npm install failed{Color.END}")
        print(result.stderr.decode('utf-8', errors='ignore'))
        return
    
    print(f"{Color.GREEN}✓ Dependencies installed{Color.END}")
    print(f"\n{Color.BOLD}Starting Electron...{Color.END}\n")
    
    try:
        subprocess.run(
            ["npm", "start"],
            cwd=electron_dir,
            check=False,
        )
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}⚠ Stopped by user{Color.END}")
    except Exception as e:
        print(f"{Color.RED}✗ Error: {e}{Color.END}")

def check_dependencies():
    print(f"\n{Color.BOLD}Checking Dependencies...{Color.END}\n")
    
    deps_ok = True
    
    # Check Python
    try:
        result = subprocess.run(
            [sys.executable, "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"{Color.GREEN}✓{Color.END} Python: {result.stdout.strip()}")
    except Exception:
        print(f"{Color.RED}✗{Color.END} Python: Not found")
        deps_ok = False
    
    # Check Node.js
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"{Color.GREEN}✓{Color.END} Node.js: {result.stdout.strip()}")
    except Exception:
        print(f"{Color.RED}✗{Color.END} Node.js: Not found (install from https://nodejs.org)")
        deps_ok = False
    
    # Check PyInstaller
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"{Color.GREEN}✓{Color.END} PyInstaller: {result.stdout.strip()}")
    except Exception:
        print(f"{Color.YELLOW}⚠{Color.END} PyInstaller: Not found")
        print(f"   Installing...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "PyInstaller"],
                capture_output=True,
                check=True,
            )
            print(f"{Color.GREEN}✓{Color.END} PyInstaller: Installed")
        except Exception:
            print(f"{Color.RED}✗{Color.END} PyInstaller: Installation failed")
            deps_ok = False
    
    # Check Flask
    try:
        __import__('flask')
        print(f"{Color.GREEN}✓{Color.END} Flask: Installed")
    except ImportError:
        print(f"{Color.YELLOW}⚠{Color.END} Flask: Missing (install with: pip install -r requirements.txt)")
        deps_ok = False
    
    print()
    if deps_ok:
        print(f"{Color.GREEN}All dependencies OK!{Color.END}")
    else:
        print(f"{Color.YELLOW}Some dependencies missing - try: pip install -r requirements.txt{Color.END}")

def clean_build():
    print(f"\n{Color.BOLD}Cleaning Build Artifacts...{Color.END}\n")
    
    dirs_to_clean = [
        APP_DIR / "build",
        APP_DIR / "dist",
        APP_DIR / ".pytest_cache",
        APP_DIR / "__pycache__",
    ]
    
    for dir_path in dirs_to_clean:
        if dir_path.exists():
            import shutil
            try:
                shutil.rmtree(dir_path)
                print(f"{Color.GREEN}✓{Color.END} Removed {dir_path.name}")
            except Exception as e:
                print(f"{Color.YELLOW}⚠{Color.END} Failed to remove {dir_path.name}: {e}")
    
    print(f"\n{Color.BOLD}Rebuilding...{Color.END}\n")
    build_exe()

def view_logs():
    print(f"\n{Color.BOLD}Recent Logs...{Color.END}\n")
    
    log_files = [
        APP_DIR / "app.log",
        APP_DIR / "app_latest.log",
        APP_DIR / "app_error.log",
    ]
    
    for log_file in log_files:
        if log_file.exists():
            print(f"{Color.CYAN}{log_file.name}:{Color.END}")
            print("-" * 80)
            
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                # Show last 20 lines
                for line in lines[-20:]:
                    print(line.rstrip())
            
            print()
            print("(showing last 20 lines)")
            print("=" * 80)
            print()

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_header()
        print_menu()
        
        try:
            choice_str = input(f"{Color.CYAN}Enter your choice: {Color.END}").strip()
            
            if not choice_str:
                continue
            
            choice_num = int(choice_str)
            
            if choice_num == 1:
                run_local()
            elif choice_num == 2:
                build_exe()
            elif choice_num == 3:
                test_electron()
            elif choice_num == 4:
                check_dependencies()
            elif choice_num == 5:
                clean_build()
            elif choice_num == 6:
                view_logs()
            elif choice_num == 0:
                print(f"\n{Color.GREEN}Goodbye!{Color.END}\n")
                break
            else:
                print(f"{Color.RED}Invalid choice{Color.END}")
        
        except ValueError:
            print(f"{Color.RED}Please enter a valid number{Color.END}")
        except KeyboardInterrupt:
            print(f"\n{Color.YELLOW}Interrupted{Color.END}")
        except Exception as e:
            print(f"{Color.RED}Error: {e}{Color.END}")
        
        input(f"\n{Color.YELLOW}Press Enter to continue...{Color.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}Interrupted by user{Color.END}\n")
        sys.exit(1)
