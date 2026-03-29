import yt_dlp
import os


def get_title(url):
    opts = {"quiet": True, "noplaylist": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        data = ydl.extract_info(url, download=False)
        return data.get("title") or "Unknown Title"


def download_media(url, media_type, v_quality, a_quality, save_path):
    if media_type == "mp3":
        opts = {
            "format": "bestaudio[ext=m4a]/bestaudio",
            "outtmpl": os.path.join(save_path, "%(title)s.mp3"),
            "noplaylist": True,
        }
    else:
        res = "".join(c for c in str(v_quality) if c.isdigit()) if v_quality else "720"

        opts = {
            "format": f"bestvideo[height<={res}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={res}]+bestaudio/best[height<={res}]",
            "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
            "noplaylist": True,
        }

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])