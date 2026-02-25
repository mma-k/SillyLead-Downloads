<div align="center">

# SillyLead Pro 🚀

**The Ultimate Google Maps B2B Scraper & CRM Tracker**
<br>
*Blazing Fast. Threaded Architecture. Deep-Link Email Hunting.*

<img src="assets/dashboard.png" alt="SillyLead Dashboard" width="800"/>

</div>

---

Welcome to **SillyLead Pro**! This tool empowers you to extract high-quality B2B leads from Google Maps completely on autopilot. All data is saved into a local searchable CRM with one-click statuses (Contacted, Blacklisted, Archived).

This repository is the **official distribution hub** for the standalone, pre-compiled executables. **No coding knowledge or complex setup is required.** 

---

## ✨ Why SillyLead v1.0.1?

1. **⚡ Threaded Panel Extraction:** Bypasses slow DOM parsing by throwing Google Maps side-panels into a background 5-worker thread pool, allowing the stealth browser to instantly click the next business.
2. **📧 Deep-Link Email Hunter:** Automatically discovers and spiders website sub-pages (`/contact`, `/about`) to extract emails, utilizing smart heuristics to filter out generic `support@` addresses in favor of high-value personal contacts.
3. **🛡️ Zero-Downtime Migrations:** SillyLead manages its own SQLite database gracefully, automatically upgrading schemas and backfilling data without losing your previous leads.
4. **📦 Local & Secure:** The beautiful Next.js UI and your database run entirely local to your machine. No cloud subscriptions.

---

## 🚀 1-Click Installation (Recommended)

We built a smart cross-platform installer that will automatically detect your Operating System (Windows, macOS, or Linux) and download the correct pre-compiled executable!

**Open your terminal (or Command Prompt) and run:**
```bash
curl -sL https://raw.githubusercontent.com/mma-k/SillyLead-Downloads/main/install.py | python3
```

*Don't have Python? You can also manually download your OS executable straight from our Releases Page:*

| Operating System | Direct Download Link |
|------------------|----------------------|
| **Windows** | [📥 Download `windows-sillylead.exe`](https://github.com/mma-k/SillyLead-Downloads/releases/latest/download/windows-sillylead.exe) |
| **macOS** | [📥 Download `macos-sillylead`](https://github.com/mma-k/SillyLead-Downloads/releases/latest/download/macos-sillylead) |
| **Linux** | [📥 Download `linux-sillylead`](https://github.com/mma-k/SillyLead-Downloads/releases/latest/download/linux-sillylead) |

*For macOS and Linux users, remember to make the file executable after downloading by running `chmod +x <filename>` in your terminal.*

---

## 🔑 Activation & License Key

On your very first launch, SillyLead Pro will ask for your **License Key**. 

- **Hardware Locked:** Your license key is permanently tied to the first computer you activate it on. 
- **Auto-Activation:** Advanced users can create a `.env` file containing `SILLYLEAD_LICENSE_KEY=your_key` in the same folder as the executable to completely bypass the terminal setup prompt.

---

## ⚙️ How It Works

Once launched, SillyLead automatically boots up its background stealth engine and opens the beautiful Web UI in your default browser at `http://localhost:8000`.

### The CRM Dashboard
<img src="assets/leads_table.png" alt="SillyLead Leads Data" width="800"/>

- **Scrape Leads:** Enter a niche and location (e.g., "Roofers in Dallas, TX") and set the max results.
- **Manage CRM:** View your extracted leads, filter them by status, and click icons to mark them as `Contacted`, `Blacklisted`, or track them natively.
- **Auto-Updater:** Next time you launch, SillyLead checks for updates and replaces itself seamlessly if a new version exists.

---

<div align="center">
<i>Built with ❤️ for serious lead generation.</i>
</div>
