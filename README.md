# VidPull

A small, fast YouTube downloader for Windows. No ads, no shady redirects, no "click here to continue" pop-ups. Just a paste-box, a download button, and the file ends up where you told it to.

<img src="Source Code/assets/VidPull.png" width="500" alt="VidPull"/>

<a href="https://www.buymeacoffee.com/rawfilejson" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me a Coffee" style="height: 60px !important;width: 217px !important;" ></a>

## Why

Every web-based YT downloader I tried was 90% ads and 10% bait-and-switch. So I packaged `yt-dlp` behind a tiny Tk GUI and called it a day.

## Features

- **MP4** up to 1080p, or **MP3** up to 320kbps
- **Playlist mode** — toggle the box, paste a playlist URL, walk away
- **Real progress bar** with live speed + ETA (it actually moves)
- **Thumbnail preview** before you commit to a download
- **Recent downloads** list — double-click to open the folder
- **Clipboard paste** button next to the URL field
- Remembers your last save folder and quality choices between runs
- Single portable `.exe`, no Python install required

## Quick start

1. Grab `VidPull.exe` from this repo.
2. Run it. Paste a URL. Click download.

> Windows Defender sometimes flags PyInstaller exes as a false positive. If that bothers you, run from source — see below.

## Run from source

```bash
git clone https://github.com/rawfilejson/VidPull.git
cd "VidPull/Source Code"
pip install -r requirements.txt
python GUI.py
```

You'll also want **ffmpeg** on your PATH for MP4 merging and MP3 conversion. On Windows: `winget install Gyan.FFmpeg`.

## Project layout

```
Source Code/
├─ GUI.py            tkinter front-end
├─ yt_backend.py     yt-dlp wrapper (info, thumbnail, download)
├─ requirements.txt
└─ assets/           icons
VidPull.exe          the bundled portable build
```

## Roadmap-ish

Things I might add when I have an evening:

- subtitle download toggle
- batch URL queue
- dark/light theme toggle
- per-channel download presets

PRs welcome, file a bug if you hit one.

---

If VidPull saved you from yet another adware site:

<a href="https://www.buymeacoffee.com/rawfilejson" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me a Coffee" style="height: 60px !important;width: 217px !important;" ></a>
