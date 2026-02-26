#!/usr/bin/env python3
"""
SillyLead Pro — System Pre-Flight Checker & Auto-Installer
Checks if the user's device is ready to run SillyLead, installs missing
dependencies, downloads the correct OS binary, and validates everything.
"""

import os
import sys
import platform
import shutil
import subprocess
import urllib.request
import stat
import json

REPO_URL = "https://github.com/mma-k/SillyLead-Downloads/releases/latest/download"
MIN_PYTHON = (3, 9)

# ──────────────────────────────────────────────────────────
#  UTILITIES
# ──────────────────────────────────────────────────────────

class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    END = "\033[0m"

def ok(msg):
    print(f"  {Colors.GREEN}✓{Colors.END} {msg}")

def warn(msg):
    print(f"  {Colors.YELLOW}⚠{Colors.END} {msg}")

def fail(msg):
    print(f"  {Colors.RED}✖{Colors.END} {msg}")

def header(msg):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{msg}{Colors.END}")

def progress_bar(count, block_size, total_size):
    if total_size <= 0:
        return
    percent = min(int(count * block_size * 100 / total_size), 100)
    bar_len = 40
    filled = int(bar_len * percent // 100)
    bar = '█' * filled + '░' * (bar_len - filled)
    sys.stdout.write(f'\r  Downloading: |{bar}| {percent}%')
    sys.stdout.flush()
    if percent >= 100:
        sys.stdout.write('\n')


# ──────────────────────────────────────────────────────────
#  PRE-FLIGHT CHECKS
# ──────────────────────────────────────────────────────────

def check_python_version():
    """Verify Python version is 3.9+."""
    v = sys.version_info
    if (v.major, v.minor) >= MIN_PYTHON:
        ok(f"Python {v.major}.{v.minor}.{v.micro} (requires 3.9+)")
        return True
    else:
        fail(f"Python {v.major}.{v.minor} is too old. SillyLead requires Python 3.9 or newer.")
        return False


def check_os():
    """Detect and display the OS."""
    system = platform.system().lower()
    machine = platform.machine()
    names = {"windows": "🪟 Windows", "darwin": "🍎 macOS", "linux": "🐧 Linux"}
    name = names.get(system, system)
    ok(f"Operating System: {name} ({machine})")
    return system


def check_chromium():
    """
    Check if a compatible Chromium/Chrome browser is installed.
    SillyLead's scraper engine uses Selenium with ChromeDriver.
    The webdriver-manager package auto-downloads the matching driver,
    but a Chrome/Chromium BROWSER must be installed on the system.
    """
    chrome_paths = {
        "linux": [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium",
        ],
        "darwin": [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ],
        "windows": [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        ],
    }

    system = platform.system().lower()
    paths = chrome_paths.get(system, [])

    # Also check PATH
    chrome_cmd = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("chrome")

    found_path = None
    for p in paths:
        if os.path.exists(p):
            found_path = p
            break

    if not found_path and chrome_cmd:
        found_path = chrome_cmd

    if found_path:
        # Try to get Chrome version
        version = "unknown"
        try:
            result = subprocess.run([found_path, "--version"], capture_output=True, text=True, timeout=5)
            version = result.stdout.strip()
        except Exception:
            pass
        ok(f"Chrome/Chromium found: {version}")
        ok(f"  Path: {found_path}")
        return True
    else:
        fail("Chrome or Chromium browser NOT FOUND!")
        print()
        if system == "linux":
            warn("Install Chromium with:")
            print(f"    {Colors.DIM}sudo apt install chromium-browser{Colors.END}")
            print(f"    {Colors.DIM}  or{Colors.END}")
            print(f"    {Colors.DIM}sudo apt install google-chrome-stable{Colors.END}")
        elif system == "darwin":
            warn("Install Chrome from: https://www.google.com/chrome/")
            print(f"    {Colors.DIM}  or: brew install --cask google-chrome{Colors.END}")
        elif system == "windows":
            warn("Install Chrome from: https://www.google.com/chrome/")
        print()
        fail("SillyLead's scraper engine requires Chrome/Chromium to extract business data.")
        fail("The scraper will FAIL without it (you'll see a 'session not created' error).")
        return False


def check_disk_space():
    """Verify at least 500MB of free disk space."""
    try:
        usage = shutil.disk_usage(os.getcwd())
        free_gb = usage.free / (1024 ** 3)
        if free_gb >= 0.5:
            ok(f"Disk space: {free_gb:.1f} GB available")
            return True
        else:
            fail(f"Low disk space: only {free_gb:.2f} GB free. SillyLead needs at least 500 MB.")
            return False
    except Exception:
        warn("Could not check disk space.")
        return True


def check_network():
    """Test basic internet connectivity."""
    try:
        urllib.request.urlopen("https://api.github.com", timeout=5)
        ok("Internet connection: active")
        return True
    except Exception:
        fail("No internet connection detected. Required for downloading SillyLead and license activation.")
        return False


def check_port_available():
    """Check if port 8000 is available (or warn if busy)."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 8000))
        if result != 0:
            ok("Port 8000: available (SillyLead's default port)")
        else:
            warn("Port 8000 is currently in use. SillyLead will auto-select another port.")
    return True


# ──────────────────────────────────────────────────────────
#  DOWNLOAD
# ──────────────────────────────────────────────────────────

def download_binary(system):
    """Download the correct SillyLead binary for this OS."""
    file_map = {
        "windows": ("windows-sillylead.exe", "windows-sillylead.exe"),
        "darwin": ("macos-sillylead", "sillylead"),
        "linux": ("linux-sillylead", "sillylead"),
    }

    if system not in file_map:
        fail(f"Unsupported operating system: {system}")
        return False

    remote_name, local_name = file_map[system]
    url = f"{REPO_URL}/{remote_name}"
    dest = os.path.join(os.getcwd(), local_name)

    print(f"\n  Fetching {remote_name} from GitHub Releases...")
    try:
        urllib.request.urlretrieve(url, dest, reporthook=progress_bar)
        if system != "windows":
            os.chmod(dest, os.stat(dest).st_mode | stat.S_IEXEC)
        ok(f"Downloaded to: {dest}")
        return True
    except Exception as e:
        fail(f"Download failed: {e}")
        fail("Make sure the release is published at:")
        print(f"    {Colors.DIM}https://github.com/mma-k/SillyLead-Downloads/releases{Colors.END}")
        return False


# ──────────────────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────────────────

def main():
    print()
    print(f"{Colors.BOLD}{'='*50}")
    print(f"    SillyLead Pro — System Pre-Flight Checker")
    print(f"{'='*50}{Colors.END}")

    all_ok = True

    # ─── System Info ───
    header("1. System Information")
    system = check_os()
    if not check_python_version():
        all_ok = False

    # ─── Dependencies ───
    header("2. Required Dependencies")
    if not check_chromium():
        all_ok = False

    # ─── Resources ───
    header("3. System Resources")
    check_disk_space()
    if not check_network():
        all_ok = False
    check_port_available()

    # ─── Summary ───
    print()
    print(f"{Colors.BOLD}{'─'*50}{Colors.END}")

    if not all_ok:
        print()
        fail(f"{Colors.BOLD}Your system is NOT ready to run SillyLead.{Colors.END}")
        print("  Please fix the issues marked with ✖ above and re-run this script.")
        print()
        ans = input("  Continue with download anyway? (y/n): ").strip().lower()
        if ans != 'y':
            print("  Aborted. Fix the issues above, then run this script again.")
            sys.exit(1)
    else:
        print()
        ok(f"{Colors.BOLD}All checks passed! Your system is ready.{Colors.END}")

    # ─── Download ───
    header("4. Downloading SillyLead Pro")
    if download_binary(system):
        print()
        print(f"{Colors.BOLD}{Colors.GREEN}{'='*50}")
        print(f"    🎉  Installation Complete!")
        print(f"{'='*50}{Colors.END}")
        print()
        if system == "windows":
            print(f"  {Colors.BOLD}How to run:{Colors.END}")
            print(f"    Double-click {Colors.CYAN}windows-sillylead.exe{Colors.END}")
        else:
            print(f"  {Colors.BOLD}How to run:{Colors.END}")
            print(f"    {Colors.CYAN}./sillylead{Colors.END}")
        print()
        print(f"  {Colors.DIM}On first launch, you'll be asked for your License Key.")
        print(f"  Pro tip: Create a .env file with SILLYLEAD_LICENSE_KEY=your_key")
        print(f"  in the same folder to skip the prompt every time.{Colors.END}")
        print()
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
