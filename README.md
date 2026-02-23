<div align="center">

# SillyLead Pro

**The Ultimate Google Maps B2B Scraper & CRM Tracker**
<br>
*Plug & Play Executables for Windows, macOS, and Linux*

</div>

---

**IMPORTANT SETUP: You must create a `.env` file containing your license key before running the application. Please paste your license key along with this specific variable name:**
```env
SILLYLEAD_LICENSE_KEY=
```

Welcome to **SillyLead Pro**! This tool empowers you to extract high-quality B2B leads from Google Maps completely on autopilot. All data is saved into a local searchable CRM with one-click statuses (Contacted, Blacklisted, Archived).

This repository contains the standalone, pre-compiled executables. **No coding knowledge, Python installation, or complex setup is required.** Just download, open, and start scraping!

---

## 🚀 Getting Started

Follow the instructions below for your specific operating system to get started immediately.

### 🪟 Windows (Recommended)
1. Navigate to the `windows/` folder in this repository.
2. Download `sillylead.exe`.
3. Double-click the file to run it.
4. *Note: If Windows SmartScreen blocks it, click **"More info"** → **"Run anyway"**.*

### 🍎 macOS
1. Navigate to the `macos/` folder.
2. Download the `sillylead` binary.
3. Open Terminal, navigate to your downloads folder, and make the file executable:
   ```bash
   chmod +x sillylead
   ```
4. Run it:
   ```bash
   ./sillylead
   ```
5. *Note: If macOS blocks the app, go to **System Preferences → Security & Privacy → General** and click **"Open Anyway"**.*

### 🐧 Linux
1. Navigate to the `linux/` folder.
2. Download the `sillylead` binary.
3. Open your terminal, navigate to your downloads folder, and make the file executable:
   ```bash
   chmod +x sillylead
   ```
4. Run it:
   ```bash
   ./sillylead
   ```

---

## 🔑 Activation & License Key

On your very first launch, SillyLead Pro will ask for your **License Key**. 

- **Hardware Locked:** Your license key is permanently tied to the first computer you activate it on. It cannot be shared or reused on a different machine.
- **Offline Capable:** After successful activation, SillyLead securely caches your license locally so you can scrape and manage leads offline.
- **Lost Key?** Use the `Show hardware fingerprint` option in the CLI menu and contact support.

---

## ⚙️ How It Works

Once open, SillyLead runs entirely in your terminal and browser:
1. **The Engine:** A local server starts in the background (you will see "Engine running on port 8000").
2. **The Dashboard:** The beautiful Web UI automatically opens in your default browser at `http://localhost:8000`.
3. **The Scraper:** When you start a scraping job from the dashboard, SillyLead launches an undetectable stealth browser in the background to safely extract leads.

### Dashboard Features
- **Scrape Leads:** Enter a niche and location (e.g., "Plumbers in Austin, TX") and set the max results.
- **Manage CRM:** View your extracted leads, filter them by status, and click icons to mark them as `Contacted`, `Blacklisted`, or track them natively.
- **Map View:** Visualize all your scraped leads directly on an interactive map.

---

## ♻️ Built-In Auto-Updater

You never have to manually check this repository for updates again! 

SillyLead Pro features a **built-in auto-updater**. Every time you launch the tool, it checks this repository for the latest version. If an update is found:
1. You will be prompted in the terminal to update.
2. SillyLead will automatically download the correct new executable for your OS.
3. It will safely replace your old file and restart itself instantly.

---

## ❓ Troubleshooting

- **"No module named..." or "Browser crashed"**: Ensure your internet connection is stable. The stealth browser requires an active connection to navigate Maps.
- **Port 8000 is in use**: SillyLead dynamically hunts for open ports. It will automatically switch to 8001, 8002, etc., if needed.
- **Lost Data**: All your leads are securely saved in a portable `sillylead.db` file generated next to your executable. Do not delete this file! You can move it alongside new versions to keep your data intact.

<div align="center">
<i>Built with ❤️ for serious lead generation.</i>
</div>
