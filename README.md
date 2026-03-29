# VidPull

**VidPull** is a high-speed, ad-free YouTube video downloader for Windows. It provides a secure, private alternative to web-based downloaders that are often filled with intrusive ads, trackers, and malicious redirects.

---

## 📥 Quick Start (Portable)

You do not need to install Python or set up an environment. Just download and run.

1.  **Download** `VidPull.exe` from this repository.
2.  **Run** the executable.
3.  **Paste** your YouTube URL and choose your save location.

> **Note:** If Windows Defender flags the file, it is a common false positive for standalone Python-to-EXE files.

---

## 🚀 Features

* **100% Ad-Free:** No pop-ups, banners, or redirects.
* **High Quality:** Automatically fetches the best available resolution.
* **Privacy-Focused:** Does not route traffic through third-party servers.
* **Standalone:** A single portable file with no installation required.

---

## 📂 Project Structure

* `VidPull.exe` — The main standalone Windows application.
* `GUI.py` — The core application entry point.
* `yt_backend.py` — Logic for video fetching and processing.
* `assets` — Images and icons used for the user interface.

---

## 🛠️ Running from Source

If you prefer to run the project via Python instead of the executable:

```bash
# Clone the repository
git clone https://github.com/rawfilejson/VidPull.git

# Enter the directory
cd VidPull/Source Code

# Install required dependencies
pip install -r requirements.txt

# Run the app
python GUI.py
