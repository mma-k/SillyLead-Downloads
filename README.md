<div align="center">

# SillyLead Pro v1.02 🚀

**The Ultimate Google Maps B2B Scraper & CRM Tracker**
<br>
*Threaded Architecture · Deep-Link Email Hunting · Unlimited Storage · Real-Time Progress*

<img src="assets/dashboard.png" alt="SillyLead Dashboard" width="800"/>

</div>

---

## 📋 Table of Contents

- [What is SillyLead?](#-what-is-sillylead)
- [What's New in v1.02](#-whats-new-in-v102)
- [1-Click Installation](#-1-click-installation)
- [System Requirements](#-system-requirements)
- [Activation & License Key](#-activation--license-key)
- [How It Works](#-how-it-works)
- [Features in Detail](#-features-in-detail)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)

> 📖 **New to this?** Check out our **[Visual Setup Guide (SETUP_GUIDE.md)](SETUP_GUIDE.md)** — a step-by-step walkthrough with screenshots, designed for non-developers.

---

## 🧐 What is SillyLead?

SillyLead Pro is a professional-grade lead generation tool that extracts high-quality B2B business data from Google Maps and organizes it in a beautiful, local CRM dashboard. Everything runs on **your machine** — no cloud subscriptions, no monthly fees, no data shared with third parties.

**Key capabilities:**
- 🔍 Search any niche + location (e.g. *"Plumbers in Austin TX"*)
- 📊 Extract name, phone, address, website, rating, reviews, and more
- 📧 Automatically hunt emails from business websites
- 🗺️ View leads on an interactive map
- 📋 Manage leads with one-click CRM statuses (Contacted, Blacklisted, Archived)
- 💾 Unlimited local SQLite database — only limited by your disk space

---

## 🆕 What's New in v1.02

> **This is a major upgrade.** Your existing database is fully preserved when updating.

### Performance & Capacity
- **Unlimited database storage** — removed the 100-record cap. Now only limited by disk space.
- **Max results increased to 1,000** per scrape job
- **Threaded panel extraction** — 5 background workers process business side-panels simultaneously while the browser clicks the next result, making scraping 3-5× faster
- **Real-time progress tracking** — search page shows live progress bar with percentage and time estimates

### Email Hunting
- **Deep-link email scanner** — automatically crawls `/contact`, `/about`, `/team`, `/support` sub-pages on business websites
- **Smart email filtering** — prioritizes personal business emails over generic `info@` and `support@` addresses
- **Multiple extraction methods** — regex patterns, mailto links, and structured data parsing

### Leads Management
- **Grid + List view toggle** — switch between card grid layout and compact table view
- **Bulk actions** — select multiple leads (or select all) and bulk delete, archive, blacklist, or mark as contacted
- **Advanced filtering** — filter by has email, has website, has phone, rating range, and status

<img src="assets/leads_table.png" alt="SillyLead Leads Table with Bulk Actions" width="800"/>

### Settings Page
- **Persistent search filters** — save your preferred filters (e.g., "only businesses with email") so they apply automatically on every new scrape
- **Default max results** — set your preferred scrape size
- **Theme toggle** — dark/light mode

<img src="assets/settings_page.png" alt="SillyLead Settings Page" width="800"/>

### Search & Extraction

<img src="assets/search_progress.png" alt="Real-Time Scrape Progress" width="800"/>

- **Live result streaming** — businesses appear in the search page as they are found and saved
- **Progress bar** with percentage, elapsed time, and estimated completion
- **Auto-pause on network loss** — the scraper pauses if your internet drops and resumes when it reconnects

### Network & Reliability
- **Online/Offline indicator** — banner in the header shows real-time connectivity status
- **Auto-pause scraping** on weak or lost network connection
- **Zero-downtime database migrations** — upgrading from v1.0.x preserves all your data

### Map View

<img src="assets/map_view.png" alt="SillyLead Interactive Map View" width="800"/>

- Interactive Leaflet map with clustered markers
- Click any pin to see full business details

---

## 🚀 1-Click Installation

We built a smart cross-platform installer that **checks your system**, verifies you have Chrome/Chromium installed, validates your Python version, and then downloads the correct binary for your OS.

**Open your terminal and run:**
```bash
curl -sL https://raw.githubusercontent.com/mma-k/SillyLead-Downloads/main/install.py | python3
```

The installer will run through these checks automatically:

```
==================================================
    SillyLead Pro — System Pre-Flight Checker
==================================================

1. System Information
  ✓ Operating System: 🐧 Linux (x86_64)
  ✓ Python 3.11.2 (requires 3.9+)

2. Required Dependencies
  ✓ Chrome/Chromium found: Chromium 124.0.6367.155
    Path: /usr/bin/chromium

3. System Resources
  ✓ Disk space: 45.2 GB available
  ✓ Internet connection: active
  ✓ Port 8000: available

4. Downloading SillyLead Pro
  Downloading: |████████████████████████████████████████| 100%
  ✓ Downloaded to: ./sillylead

==================================================
    🎉  Installation Complete!
==================================================
```

### Manual Download

If you prefer to download directly:

| Operating System | Download |
|------------------|----------|
| **🪟 Windows** | [📥 windows-sillylead.exe](https://github.com/mma-k/SillyLead-Downloads/releases/latest/download/windows-sillylead.exe) |
| **🍎 macOS** | [📥 macos-sillylead](https://github.com/mma-k/SillyLead-Downloads/releases/latest/download/macos-sillylead) |
| **🐧 Linux** | [📥 linux-sillylead](https://github.com/mma-k/SillyLead-Downloads/releases/latest/download/linux-sillylead) |

For macOS/Linux, make the file executable after downloading:
```bash
chmod +x sillylead && ./sillylead
```

---

## ⚙️ System Requirements

| Requirement | Details |
|-------------|---------|
| **OS** | Windows 10+, macOS 12+, Linux (Ubuntu 20.04+, Debian 11+, Fedora 36+) |
| **Chrome/Chromium** | **Required.** Any recent version. The scraper engine needs a Chrome browser to extract data from Google Maps. |
| **Python** | Only needed if using the `install.py` auto-installer (v3.9+). Not needed if downloading the binary directly. |
| **Disk Space** | 500 MB minimum (binary + database growth) |
| **Internet** | Required for scraping and license activation. Offline mode supported after initial activation. |

> ⚠️ **Most common error:** If the scraper shows *"session not created: This version of ChromeDriver only supports Chrome version X"*, it means your Chrome browser is outdated or missing. Update Chrome to the latest version and try again. The install script (`install.py`) will detect this for you.

---

## 🔑 Activation & License Key

On your first launch, SillyLead will ask for your **License Key**.

- **Hardware Locked:** Your key is permanently bound to the first device you activate on. Copying the executable to another machine will require a new key.
- **Offline Mode:** After initial activation, SillyLead works fully offline using the cached license.
- **Auto-Key via `.env` file:** Create a file called `.env` in the same folder as the executable with this content:

```env
SILLYLEAD_LICENSE_KEY=SLL-XXXX-XXXX-XXXX
```

This skips the license prompt on every launch — perfect for headless or automated setups.

---

## 💻 How It Works

1. **Launch** the executable (double-click on Windows, `./sillylead` on Mac/Linux)
2. **Enter your license key** (first time only, or use `.env`)
3. SillyLead boots its embedded engine and opens the **Web Dashboard** in your browser at `http://localhost:8000`
4. **Search:** Enter a business category + location → the threaded scraper extracts leads in real-time
5. **Manage:** Use the CRM dashboard to filter, sort, contact, archive, or blacklist leads
6. **Export:** Your data is in a local SQLite database you can query anytime

---

## 📖 Features in Detail

### The Dashboard
<img src="assets/dashboard.png" alt="Dashboard Overview" width="800"/>

The home screen shows at-a-glance statistics: total leads, active prospects, contacted, blacklisted, and archived counts.

### Search & Extraction
<img src="assets/search.png" alt="Search Page" width="800"/>

Enter your search query and max results. The threaded engine runs in the background while you see results stream in live with a progress bar.

### Leads CRM
<img src="assets/leads_table.png" alt="Leads Management" width="800"/>

- Toggle between **Grid** (cards) and **List** (table) views
- **Bulk select** leads with checkboxes → apply actions to all selected
- **Filter** by: has email, has website, has phone, rating range, CRM status
- **One-click actions:** Contact, Blacklist, Archive, Delete

### Interactive Map
<img src="assets/map_view.png" alt="Map View" width="800"/>

Visualize all your leads geographically. Click markers for quick details.

### Settings
<img src="assets/settings_page.png" alt="Settings" width="800"/>

Save your preferred filters and default max results so they persist across sessions.

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| **"session not created: ChromeDriver version mismatch"** | Update Google Chrome to the latest version. SillyLead auto-downloads the matching ChromeDriver, but it needs a compatible Chrome browser installed. |
| **Backend warning: "may not have started correctly"** | A previous SillyLead instance may still be running. Close all terminals and try again, or restart your computer. |
| **Desktop GUI shows unstyled HTML** | The Qt WebEngine on some Linux distros has limited CSS support. Use the **Web Dashboard** option instead for the full experience. |
| **License rejected on new device** | Each license is hardware-locked. Contact the seller to unbind your old device and reactivate on the new one. |
| **Scraper is slow** | Ensure stable internet. SillyLead auto-pauses on weak connections. Close other bandwidth-heavy applications. |
| **Port 8000 in use** | SillyLead auto-detects this and picks the next available port (8001, 8002, etc.). |

---

## ❓ FAQ

**Q: Do I need to install Node.js or Python?**
A: No. The executable is fully self-contained. Just download and run.

**Q: Will updating to v1.02 delete my existing data?**
A: No. The database migration is automatic and non-destructive. All your leads are preserved.

**Q: Can I use SillyLead offline?**
A: Yes, after initial license activation. The scraper obviously needs internet, but the CRM dashboard works fully offline.

**Q: How many leads can I store?**
A: Unlimited. The only limit is your disk space.

---

<div align="center">
<i>Built with ❤️ for serious lead generation.</i>
<br><br>
<b>SillyLead Pro v1.02</b> · © 2026
</div>
