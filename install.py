#!/usr/bin/env python3
"""
SillyLead Pro installer bootstrap.

Runs lightweight pre-flight checks, fetches the latest download manifest,
and downloads the correct binary/installer for the current OS.
"""

import json
import os
import platform
import shutil
import stat
import subprocess
import sys
import urllib.request
from urllib.parse import urlparse

MIN_PYTHON = (3, 9)
DOWNLOADS_REPO = "mma-k/SillyLead-Downloads"
LICENSE_SITE = "https://sillylead.vercel.app"
MANIFEST_URLS = [
    f"https://raw.githubusercontent.com/{DOWNLOADS_REPO}/main/latest.json",
    f"https://raw.githubusercontent.com/{DOWNLOADS_REPO}/master/latest.json",
]


class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    END = "\033[0m"


def ok(msg: str):
    print(f"  {Colors.GREEN}OK{Colors.END} {msg}")


def warn(msg: str):
    print(f"  {Colors.YELLOW}WARN{Colors.END} {msg}")


def fail(msg: str):
    print(f"  {Colors.RED}FAIL{Colors.END} {msg}")


def header(msg: str):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{msg}{Colors.END}")


def progress_bar(count: int, block_size: int, total_size: int):
    if total_size <= 0:
        return
    percent = min(int(count * block_size * 100 / total_size), 100)
    bar_len = 36
    filled = int(bar_len * percent / 100)
    bar = "#" * filled + "-" * (bar_len - filled)
    sys.stdout.write(f"\r  Downloading: [{bar}] {percent}%")
    sys.stdout.flush()
    if percent >= 100:
        sys.stdout.write("\n")


def check_python_version() -> bool:
    version = sys.version_info
    if (version.major, version.minor) >= MIN_PYTHON:
        ok(f"Python {version.major}.{version.minor}.{version.micro} (requires 3.9+)")
        return True
    fail(f"Python {version.major}.{version.minor} is too old. SillyLead requires Python 3.9+.")
    return False


def check_os() -> str:
    system = platform.system().lower()
    machine = platform.machine()
    names = {"windows": "Windows", "darwin": "macOS", "linux": "Linux"}
    ok(f"Operating System: {names.get(system, system)} ({machine})")
    return system


def check_chromium() -> bool:
    """
    SillyLead requires Chrome/Chromium for Selenium scraping.
    """
    system = platform.system().lower()

    known_paths = {
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

    browser_path = None
    for candidate in known_paths.get(system, []):
        if os.path.exists(candidate):
            browser_path = candidate
            break

    if not browser_path:
        browser_path = (
            shutil.which("google-chrome")
            or shutil.which("chromium")
            or shutil.which("chromium-browser")
            or shutil.which("chrome")
        )

    if not browser_path:
        fail("Chrome/Chromium not found. Install it before scraping.")
        return False

    version = "unknown"
    try:
        proc = subprocess.run([browser_path, "--version"], capture_output=True, text=True, timeout=5)
        output = (proc.stdout or proc.stderr or "").strip()
        if output:
            version = output
    except Exception:
        pass

    ok(f"Chrome/Chromium found: {version}")
    ok(f"Path: {browser_path}")
    return True


def check_disk_space() -> bool:
    try:
        usage = shutil.disk_usage(os.getcwd())
        free_gb = usage.free / (1024 ** 3)
        if free_gb >= 0.5:
            ok(f"Disk space: {free_gb:.1f} GB available")
            return True
        fail(f"Low disk space: {free_gb:.2f} GB free (needs at least 0.5 GB)")
        return False
    except Exception:
        warn("Could not verify disk space")
        return True


def check_network() -> bool:
    try:
        urllib.request.urlopen("https://api.github.com", timeout=5)
        ok("Internet connection: active")
        return True
    except Exception:
        fail("No internet connection. This installer needs internet access.")
        return False


def check_port_available() -> bool:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex(("127.0.0.1", 8000))
        if result != 0:
            ok("Port 8000: available")
        else:
            warn("Port 8000 is busy. SillyLead will choose another port automatically.")
    return True


def fetch_manifest() -> dict:
    last_error = None
    for url in MANIFEST_URLS:
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("Manifest JSON is not an object")
            return payload
        except Exception as exc:
            last_error = exc
            continue
    raise RuntimeError(f"Could not fetch latest.json from {DOWNLOADS_REPO}: {last_error}")


def _platform_key(system: str) -> str:
    if system == "darwin":
        return "macos"
    return system


def resolve_download_target(system: str, manifest: dict):
    platform_key = _platform_key(system)
    assets = manifest.get("assets", {}) or {}
    asset = assets.get(platform_key)

    if not isinstance(asset, dict):
        raise RuntimeError(
            f"Manifest does not define assets.{platform_key}. "
            "Update latest.json before running this installer."
        )

    download_url = asset.get("download_url") or asset.get("url")
    if not download_url:
        raise RuntimeError(f"Manifest assets.{platform_key} is missing download_url")

    default_name = {
        "windows": "windows-sillylead.exe",
        "linux": "sillylead",
        "macos": "sillylead",
    }[platform_key]

    local_name = asset.get("local_name") or asset.get("asset_name") or os.path.basename(urlparse(download_url).path) or default_name
    if platform_key != "windows" and local_name.lower().endswith(".exe"):
        local_name = "sillylead"

    return download_url, local_name


def download_binary(download_url: str, local_name: str, system: str) -> bool:
    destination = os.path.join(os.getcwd(), local_name)
    print(f"\n  Fetching: {download_url}")

    try:
        urllib.request.urlretrieve(download_url, destination, reporthook=progress_bar)
        if system != "windows":
            os.chmod(destination, os.stat(destination).st_mode | stat.S_IEXEC)
        ok(f"Downloaded to: {destination}")
        return True
    except Exception as exc:
        fail(f"Download failed: {exc}")
        return False


def print_run_instructions(system: str, local_name: str):
    print()
    print(f"{Colors.BOLD}{Colors.GREEN}{'=' * 52}{Colors.END}")
    print("    Installation Complete")
    print(f"{Colors.BOLD}{Colors.GREEN}{'=' * 52}{Colors.END}")
    print()

    if system == "windows":
        print(f"  Run: double-click {Colors.CYAN}{local_name}{Colors.END}")
    else:
        print(f"  Run: {Colors.CYAN}chmod +x {local_name} && ./{local_name}{Colors.END}")

    print(f"  Buy/manage license keys: {Colors.CYAN}{LICENSE_SITE}{Colors.END}")
    print(
        f"  Tip: create a .env file with {Colors.CYAN}SILLYLEAD_LICENSE_KEY=YOUR_KEY{Colors.END} "
        "to skip license prompts."
    )
    print()


def main():
    print()
    print(f"{Colors.BOLD}{'=' * 52}")
    print("    SillyLead Pro Installer")
    print(f"{'=' * 52}{Colors.END}")

    all_ok = True

    header("1) System Information")
    system = check_os()
    if not check_python_version():
        all_ok = False

    header("2) Required Dependencies")
    if not check_chromium():
        all_ok = False

    header("3) System Resources")
    if not check_disk_space():
        all_ok = False
    if not check_network():
        all_ok = False
    check_port_available()

    print()
    print(f"{Colors.BOLD}{'-' * 52}{Colors.END}")
    if not all_ok:
        warn("Some checks failed. You can continue, but scraping may not work correctly.")
        answer = input("Continue anyway? (y/n): ").strip().lower()
        if answer != "y":
            print("Aborted.")
            raise SystemExit(1)
    else:
        ok("All checks passed.")

    header("4) Download Latest Build")
    try:
        manifest = fetch_manifest()
        download_url, local_name = resolve_download_target(system, manifest)
    except Exception as exc:
        fail(str(exc))
        fail(f"See release files: https://github.com/{DOWNLOADS_REPO}/releases")
        raise SystemExit(1)

    if not download_binary(download_url, local_name, system):
        raise SystemExit(1)

    print_run_instructions(system, local_name)


if __name__ == "__main__":
    main()
