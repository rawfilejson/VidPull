from tkinter import *
from tkinter import filedialog, ttk
import threading
import webbrowser
import json
import os
import sys
import io
from urllib.request import urlopen

import yt_backend

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


CFG_FILE = "vidpull_cfg.json"
HISTORY_FILE = "vidpull_history.json"
BMC_URL = "https://www.buymeacoffee.com/rawfilejson"


def resource_path(rel):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel)
    return os.path.join(os.path.abspath("."), rel)


def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError:
        pass


cfg = load_json(CFG_FILE, {"last_path": "", "format": "mp4", "vq": "1080p", "aq": "160kbps"})
history = load_json(HISTORY_FILE, [])

window = Tk()
window.geometry("560x680")
window.title("VidPull — YouTube Downloader")
window.config(background="#0d0d0d")
window.minsize(520, 620)

try:
    icon = PhotoImage(file=resource_path("assets/logo.png"))
    window.iconphoto(True, icon)
except Exception:
    pass

ACCENT = "#ff3b30"
FG = "#f5f5f5"
DIM = "#888"
BG = "#0d0d0d"
PANEL = "#1a1a1a"

Label(window, text="VidPull", font=("Arial", 22, "bold"), fg=ACCENT, bg=BG).pack(pady=(14, 0))
Label(window, text="by rawfilejson", font=("Arial", 9), fg=DIM, bg=BG).pack()

fmt = StringVar(value=cfg.get("format", "mp4"))
vq_var = StringVar(value=cfg.get("vq", "1080p"))
aq_var = StringVar(value=cfg.get("aq", "160kbps"))
dest = StringVar(value=cfg.get("last_path", ""))
playlist_var = BooleanVar(value=False)

frame = Frame(window, bg=BG)
frame.pack(pady=14, padx=16, fill=X)

entry = Entry(frame, font=("Arial", 13), bd=0, relief="flat",
              bg="#fff", fg="#000", insertbackground="#000")
entry.pack(side=LEFT, fill=X, expand=True, ipady=8, padx=(0, 6))


def paste_clipboard():
    try:
        clip = window.clipboard_get()
        if "youtu" in clip:
            entry.delete(0, END)
            entry.insert(0, clip.strip())
    except Exception:
        pass


Button(frame, text="📋", command=paste_clipboard, bg=PANEL, fg=FG, bd=0,
       activebackground=ACCENT, font=("Arial", 12), padx=10).pack(side=LEFT, fill=Y, padx=(0, 4))


def submit_clicked():
    threading.Thread(target=run_download, daemon=True).start()


Button(frame, text="↓  Download", command=submit_clicked, bg=ACCENT, fg="white",
       bd=0, font=("Arial", 11, "bold"), padx=14, pady=6,
       activebackground="#c0271f", activeforeground="white").pack(side=LEFT, fill=Y)

thumb_label = Label(window, bg=BG)
thumb_label.pack(pady=(2, 4))

title_label = Label(window, text="", font=("Arial", 12, "bold"),
                    fg=FG, bg=BG, wraplength=520)
title_label.pack(pady=2)

# options
optsframe = Frame(window, bg=BG)
optsframe.pack(pady=8)

rb = dict(bg=BG, fg=FG, selectcolor=BG, activebackground=BG,
          activeforeground=ACCENT, bd=0, highlightthickness=0)

Radiobutton(optsframe, text="MP4", variable=fmt, value="mp4", **rb).grid(row=0, column=0, padx=8)
Radiobutton(optsframe, text="MP3", variable=fmt, value="mp3", **rb).grid(row=0, column=1, padx=8)
Checkbutton(optsframe, text="Playlist", variable=playlist_var, **rb).grid(row=0, column=2, padx=8)

Label(optsframe, text="Video:", bg=BG, fg=DIM).grid(row=1, column=0, sticky=E, pady=4)
vq_menu = OptionMenu(optsframe, vq_var, "1080p", "720p", "480p", "360p")
vq_menu.config(bg=PANEL, fg=FG, bd=0, highlightthickness=0,
               activebackground=ACCENT, activeforeground="white", relief="flat", width=8)
vq_menu["menu"].config(bg=PANEL, fg=FG, bd=0, activebackground=ACCENT)
vq_menu.grid(row=1, column=1, sticky=W, pady=4)

Label(optsframe, text="Audio:", bg=BG, fg=DIM).grid(row=1, column=2, sticky=E, pady=4)
aq_menu = OptionMenu(optsframe, aq_var, "320kbps", "192kbps", "160kbps", "128kbps", "70kbps")
aq_menu.config(bg=PANEL, fg=FG, bd=0, highlightthickness=0,
               activebackground=ACCENT, activeforeground="white", relief="flat", width=10)
aq_menu["menu"].config(bg=PANEL, fg=FG, bd=0, activebackground=ACCENT)
aq_menu.grid(row=1, column=3, sticky=W, pady=4)


def browse_folder():
    picked = filedialog.askdirectory(initialdir=dest.get() or os.path.expanduser("~"))
    if picked:
        dest.set(picked)
        cfg["last_path"] = picked
        save_json(CFG_FILE, cfg)


destframe = Frame(window, bg=BG)
destframe.pack(fill=X, padx=16, pady=4)

Button(destframe, text="📁 Save to…", command=browse_folder, bg=PANEL, fg=FG,
       bd=0, activebackground=ACCENT, activeforeground="white",
       relief="flat", padx=10, pady=4).pack(side=LEFT)

Label(destframe, textvariable=dest, bg=BG, fg=DIM, anchor="w").pack(side=LEFT, padx=8, fill=X, expand=True)

# progress + status
style = ttk.Style()
try:
    style.theme_use("clam")
except Exception:
    pass
style.configure("vp.Horizontal.TProgressbar", troughcolor=PANEL,
                background=ACCENT, bordercolor=BG, lightcolor=ACCENT, darkcolor=ACCENT)

progress = ttk.Progressbar(window, style="vp.Horizontal.TProgressbar",
                           length=520, mode="determinate", maximum=100)
progress.pack(pady=(12, 4), padx=16, fill=X)

status = Label(window, text="ready.", font=("Arial", 10), fg=DIM, bg=BG)
status.pack()

# history
hist_frame = Frame(window, bg=BG)
hist_frame.pack(fill=BOTH, expand=True, padx=16, pady=(10, 4))

Label(hist_frame, text="recent downloads", fg=DIM, bg=BG, font=("Arial", 9)).pack(anchor=W)

hist_list = Listbox(hist_frame, bg=PANEL, fg=FG, bd=0, highlightthickness=0,
                    selectbackground=ACCENT, font=("Arial", 9), height=6,
                    activestyle="none")
hist_list.pack(fill=BOTH, expand=True)


def refresh_history():
    hist_list.delete(0, END)
    for row in reversed(history[-20:]):
        hist_list.insert(END, f"  {row['title'][:60]}")


def open_history_item(_evt):
    idx = hist_list.curselection()
    if not idx:
        return
    row = list(reversed(history[-20:]))[idx[0]]
    folder = row.get("folder")
    if folder and os.path.isdir(folder):
        try:
            os.startfile(folder)
        except Exception:
            pass


hist_list.bind("<Double-Button-1>", open_history_item)
refresh_history()

# footer
foot = Frame(window, bg=BG)
foot.pack(pady=(6, 12))

bmc = Label(foot, text="☕  buy me a coffee", fg="#FAC921", bg=BG,
            cursor="hand2", font=("Arial", 10, "underline"))
bmc.pack()
bmc.bind("<Button-1>", lambda _: webbrowser.open(BMC_URL))


# thumbnail loading
def load_thumb(url):
    if not HAS_PIL:
        return
    try:
        thumb_url = yt_backend.get_thumbnail(url)
        if not thumb_url:
            return
        raw = urlopen(thumb_url, timeout=8).read()
        img = Image.open(io.BytesIO(raw))
        img.thumbnail((280, 158))
        photo = ImageTk.PhotoImage(img)
        thumb_label.config(image=photo)
        thumb_label.image = photo
    except Exception:
        pass


# progress hook
def hook(d):
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        done = d.get("downloaded_bytes", 0)
        if total:
            pct = done / total * 100
            progress["value"] = pct
            speed = d.get("speed") or 0
            mbps = speed / 1024 / 1024 if speed else 0
            eta = d.get("eta") or 0
            window.after(0, lambda: status.config(
                text=f"{pct:5.1f}%   •   {mbps:.2f} MB/s   •   eta {eta}s",
                fg=FG,
            ))
    elif d["status"] == "finished":
        window.after(0, lambda: status.config(text="merging / postprocessing…", fg="#FAC921"))


# main download flow
def run_download():
    url = entry.get().strip()
    path = dest.get()

    if not url:
        status.config(text="paste a URL first.", fg=ACCENT)
        return
    if not path:
        status.config(text="pick a save folder.", fg=ACCENT)
        return

    status.config(text="fetching info…", fg="#FAC921")
    progress["value"] = 0
    title_label.config(text="")
    thumb_label.config(image="")

    try:
        title = yt_backend.get_title(url)
        title_label.config(text=title)
        load_thumb(url)
    except Exception as e:
        status.config(text=f"info error: {str(e)[:50]}", fg=ACCENT)
        return

    cfg["format"] = fmt.get()
    cfg["vq"] = vq_var.get()
    cfg["aq"] = aq_var.get()
    save_json(CFG_FILE, cfg)

    try:
        yt_backend.download_media(url, fmt.get(), vq_var.get(), aq_var.get(), path,
                                  progress_hook=hook, playlist=playlist_var.get())
        status.config(text="done. ✓", fg="#3ddc84")
        progress["value"] = 100

        history.append({"title": title, "folder": path, "format": fmt.get()})
        save_json(HISTORY_FILE, history)
        refresh_history()

    except Exception as e:
        status.config(text=f"error: {str(e)[:60]}", fg=ACCENT)
        print("full error:", e)


window.mainloop()
