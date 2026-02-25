import os
import platform
import urllib.request
import stat

REPO_URL = "https://github.com/mma-k/SillyLead-Downloads/releases/latest/download"

def download_file(url, dest):
    print(f"Downloading SillyLead Pro from {url}...")
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"✅ Successfully downloaded to {dest}")
        return True
    except Exception as e:
        print(f"❌ Error downloading. Ensure GitHub releases are published: {e}")
        return False

def main():
    print("🚀 SillyLead Pro - Auto Installer")
    print("-" * 35)
    
    system = platform.system().lower()
    
    if system == "windows":
        print("💻 Detected Windows")
        filename = "sillylead.exe"
        url = f"{REPO_URL}/{filename}"
        dest = os.path.join(os.getcwd(), filename)
        if download_file(url, dest):
            print("\n🎉 Installation Complete!\nDouble-click 'sillylead.exe' in your folder to start scraping!")
            
    elif system == "darwin":
        print("🍎 Detected macOS")
        filename = "sillylead_macos"
        url = f"{REPO_URL}/{filename}"
        dest = os.path.join(os.getcwd(), "sillylead")
        if download_file(url, dest):
            os.chmod(dest, os.stat(dest).st_mode | stat.S_IEXEC)
            print("\n🎉 Installation Complete!\nRun it using this command in your terminal:\n\n./sillylead")
            
    elif system == "linux":
        print("🐧 Detected Linux")
        filename = "sillylead_linux"
        url = f"{REPO_URL}/{filename}"
        dest = os.path.join(os.getcwd(), "sillylead")
        if download_file(url, dest):
            os.chmod(dest, os.stat(dest).st_mode | stat.S_IEXEC)
            print("\n🎉 Installation Complete!\nRun it using this command in your terminal:\n\n./sillylead")
    else:
        print(f"Unsupported Operating System: {system}")

if __name__ == "__main__":
    main()
