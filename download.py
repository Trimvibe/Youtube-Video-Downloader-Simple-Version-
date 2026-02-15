import yt_dlp
import os
import time

def download_youtube_video(
    url,
    selected_res="Best",
    audio_quality="192k",
    file_type="mp4",
    output_path="downloads",
    progress_callback=None
):
    os.makedirs(output_path, exist_ok=True)

    format_maps = {
        "Best": "bestvideo+bestaudio/best",
        "480P": "bestvideo[height<=480]+bestaudio/best",
        "720P": "bestvideo[height<=720]+bestaudio/best",
        "1080P": "bestvideo[height<=1080]+bestaudio/best",
    }

    aud_maps = {
        "128k": "128",
        "192k": "192",
        "256k": "256",
        "320k": "320",
    }

    def hook(d):
        if progress_callback and d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
            percent = int(downloaded / total * 100)

            speed = d.get("speed")
            if speed is None:
                speed = 0

            progress_callback(percent, speed)


    ydl_opts = {
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        "noplaylist": True,
        "progress_hooks": [hook],
    }

    if file_type == "mp4":
        ydl_opts["format"] = format_maps[selected_res]
        ydl_opts["merge_output_format"] = "mp4"

    else:
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": aud_maps[audio_quality],
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    return file_path
