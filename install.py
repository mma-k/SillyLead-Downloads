import os
import platform
import urllib.request
import stat

import sys

REPO_URL = "https://github.com/mma-k/SillyLead-Downloads/releases/latest/download"

def progress_bar(count, block_size, total_size):
    if total_size == -1: return
    percent = int(count * block_size * 100 / total_size)
    if percent > 100: percent = 100
    
    bar_length = 40
    filled_length = int(bar_length * percent // 100)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    sys.stdout.write(f'\rDownloading: |{bar}| {percent}% Complete')
    sys.stdout.flush()
    if percent == 100:
        sys.stdout.write('\n')

def download_file(url, dest):
    print(f"Fetching SillyLead Pro from {url}...\n")
    try:
        urllib.request.urlretrieve(url, dest, reporthook=progress_bar)
        print(f"\n✅ Successfully downloaded to {dest}")
        return True
    except Exception as e:
        print(f"\n❌ Error downloading. Ensure GitHub releases are published: {e}")
        return False

def main():
    print("🚀 SillyLead Pro - Auto Installer")
    print("-" * 35)
    
    system = platform.system().lower()
    
    if system == "windows":
        print("💻 Detected Windows")
        filename = "windows-sillylead.exe"
        url = f"{REPO_URL}/{filename}"
        dest = os.path.join(os.getcwd(), filename)
        if download_file(url, dest):
            print("\n🎉 Installation Complete!\nDouble-click 'windows-sillylead.exe' in your folder to start scraping!")
            
    elif system == "darwin":
        print("🍎 Detected macOS")
        filename = "macos-sillylead"
        url = f"{REPO_URL}/{filename}"
        dest = os.path.join(os.getcwd(), "sillylead")
        if download_file(url, dest):
            os.chmod(dest, os.stat(dest).st_mode | stat.S_IEXEC)
            print("\n🎉 Installation Complete!\nRun it using this command in your terminal:\n\n./sillylead")
            
    elif system == "linux":
        print("🐧 Detected Linux")
        filename = "linux-sillylead"
        url = f"{REPO_URL}/{filename}"
        dest = os.path.join(os.getcwd(), "sillylead")
        if download_file(url, dest):
            os.chmod(dest, os.stat(dest).st_mode | stat.S_IEXEC)
            print("\n🎉 Installation Complete!\nRun it using this command in your terminal:\n\n./sillylead")
    else:
        print(f"Unsupported Operating System: {system}")

if __name__ == "__main__":
    main()
