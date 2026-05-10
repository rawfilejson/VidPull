import os
import yt_dlp


def get_info(url):
    opts = {"quiet": True, "noplaylist": False, "skip_download": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)


def get_title(url):
    info = get_info(url)
    if "entries" in info:
        n = len(info["entries"])
        return f"[playlist] {info.get('title', 'untitled')} — {n} videos"
    return info.get("title") or "Unknown Title"


def get_thumbnail(url):
    try:
        info = get_info(url)
        if "entries" in info and info["entries"]:
            info = info["entries"][0]
        return info.get("thumbnail")
    except Exception:
        return None


def download_media(url, media_type, v_quality, a_quality, save_path,
                   progress_hook=None, playlist=False):
    common = {
        "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
        "noplaylist": not playlist,
        "ignoreerrors": True,
        "quiet": True,
        "no_warnings": True,
    }
    if progress_hook:
        common["progress_hooks"] = [progress_hook]

    if media_type == "mp3":
        abr = "".join(c for c in str(a_quality) if c.isdigit()) or "160"
        opts = {
            **common,
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": abr,
            }],
        }
    else:
        res = "".join(c for c in str(v_quality) if c.isdigit()) or "720"
        opts = {
            **common,
            "format": (
                f"bestvideo[height<={res}][ext=mp4]+bestaudio[ext=m4a]/"
                f"bestvideo[height<={res}]+bestaudio/best[height<={res}]"
            ),
            "merge_output_format": "mp4",
        }

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
