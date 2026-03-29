from tkinter import *
from tkinter import filedialog
import yt_backend
import os
import sys


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# remembers where you saved last time so you dont have to click browse every time
def load_last_path():
    if not os.path.exists("last_path.txt"):
        return ""
    with open("last_path.txt", "r") as f:
        return f.read().strip()


def save_last_path(path):
    with open("last_path.txt", "w") as f:
        f.write(path)


window = Tk()
window.geometry("500x500")
window.title("Youtube Video Downloader")
window.config(background="black")

icon = PhotoImage(file=resource_path("assets/logo.png"))
window.iconphoto(True, icon)

# watermark
Label(window, text="by rawfilejson", font="Arial", fg="white", bg="black").pack()

fmt = StringVar(value="mp4")
vq_var = StringVar(value="1080p")
aq_var = StringVar(value="160kbps")
dest = StringVar(value=load_last_path())


def browse_folder():
    picked = filedialog.askdirectory()
    if picked:
        dest.set(picked)
        save_last_path(picked)


def submit():
    url = entry.get().strip()
    path = dest.get()

    if not url:
        status.config(text="Please Enter URL", fg="red")
        title_label.config(text="")
        return
    if not path:
        status.config(text="Please Select Save Location", fg="red")
        title_label.config(text="")
        return

    status.config(text="Fetching video info...", fg="yellow")
    window.update() # force redraw otherwise it stays blank until download finishes

    try:
        title = yt_backend.get_title(url)
        title_label.config(text=title)
        status.config(text="Downloading...", fg="yellow")
        window.update()

        yt_backend.download_media(url, fmt.get(), vq_var.get(), aq_var.get(), path)
        status.config(text="Download Complete!", fg="green")
    except Exception as e:
        # truncate because some yt_dlp errors are an essay
        status.config(text=f"Error: {str(e)[:30]}...", fg="red")
        title_label.config(text="")
        print("full error:", e)


frame = Frame(window, bg="black")
frame.pack(pady=10)

entry = Entry(frame, font=("Arial", 20), bd=0, relief="flat")
entry.pack(side=LEFT, fill=Y)

_img = PhotoImage(file=resource_path("assets/search.png"))
_img_small = _img.subsample(20, 20) # keep ref so it doesn't get garbage collected

Button(
    frame,
    command=submit,
    fg="black",
    bg="white",
    image=_img_small,
    compound="top",
    relief="flat",
    bd=0,
).pack(side=LEFT, fill=Y)

title_label = Label(
    window, text="", font=("Arial", 14, "bold"), fg="white", bg="black", wraplength=600
)
title_label.pack(pady=10)

optsframe = Frame(window, bg="black")
optsframe.pack(pady=10)

# reuse this dict so i dont have to copy paste the radiobutton styling 4 times
rb = dict(
    bg="black",
    fg="white",
    selectcolor="black",
    activebackground="black",
    activeforeground="white",
    bd=0,
    highlightthickness=0,
)

Radiobutton(optsframe, text="MP4", variable=fmt, value="mp4", **rb).grid(
    row=0, column=0, padx=10, pady=5
)
Radiobutton(optsframe, text="MP3", variable=fmt, value="mp3", **rb).grid(
    row=0, column=1, padx=10, pady=5
)

Label(optsframe, text="Video Quality:", bg="black", fg="white").grid(
    row=1, column=0, pady=5, sticky=E
)
vq_menu = OptionMenu(optsframe, vq_var, "1080p", "720p", "480p", "360p")
vq_menu.config(
    bg="black",
    fg="white",
    bd=0,
    highlightthickness=0,
    activebackground="grey",
    activeforeground="white",
    relief="flat",
)
vq_menu["menu"].config(bg="black", fg="white", bd=0, activebackground="grey")
vq_menu.grid(row=1, column=1, pady=5, sticky=W)

Label(optsframe, text="Audio Quality:", bg="black", fg="white").grid(
    row=2, column=0, pady=5, sticky=E
)
aq_menu = OptionMenu(optsframe, aq_var, "160kbps", "128kbps", "70kbps")
aq_menu.config(
    bg="black",
    fg="white",
    bd=0,
    highlightthickness=0,
    activebackground="grey",
    activeforeground="white",
    relief="flat",
)
aq_menu["menu"].config(bg="black", fg="white", bd=0, activebackground="grey")
aq_menu.grid(row=2, column=1, pady=5, sticky=W)

Button(
    optsframe,
    text="Browse Destination",
    command=browse_folder,
    bg="black",
    fg="white",
    bd=1,
    highlightthickness=0,
    activebackground="grey",
    activeforeground="white",
    relief="flat",
).grid(row=3, column=0, pady=15)

Label(optsframe, textvariable=dest, bg="black", fg="gray").grid(
    row=3, column=1, pady=15, sticky=W
)

status = Label(window, text="", font=("Arial", 12), fg="red", bg="black")
status.pack()

window.mainloop()