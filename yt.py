import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading
import os
import time

class YTDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader (yt-dlp)")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.url_var = tk.StringVar()
        self.save_path_var = tk.StringVar()
        self.format_var = tk.StringVar(value="MP4 Video")
        self.quality_var = tk.StringVar(value="Best")
        self.status_var = tk.StringVar(value="Ready")
        self.progress_state = {"last_update": 0}

        default_path = os.getcwd()
        self.save_path_var.set(default_path)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Video URL:").pack(pady=(15, 5))
        tk.Entry(self.root, textvariable=self.url_var, width=50).pack(pady=5)

        dir_frame = tk.Frame(self.root)
        dir_frame.pack(pady=5)
        tk.Label(dir_frame, text="Save to: ").pack(side=tk.LEFT)
        tk.Entry(dir_frame, textvariable=self.save_path_var, width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(dir_frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)

        format_frame = tk.Frame(self.root)
        format_frame.pack(pady=10)

        tk.Label(format_frame, text="Format: ").pack(side=tk.LEFT)
        ttk.Combobox(
            format_frame,
            textvariable=self.format_var,
            values=["MP4 Video", "MP3 Audio"],
            state="readonly",
            width=15
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(format_frame, text="Quality: ").pack(side=tk.LEFT)
        ttk.Combobox(
            format_frame,
            textvariable=self.quality_var,
            values=["Best", "480P", "720P", "1080P"],
            state="readonly",
            width=15
        ).pack(side=tk.LEFT, padx=5)

        self.download_btn = tk.Button(
            self.root,
            text="Download",
            command=self.start_download_thread,
            bg="#4CAF50",
            fg="white",
            width=20
        )
        self.download_btn.pack(pady=10)

        self.progress_bar = ttk.Progressbar(
            self.root,
            orient=tk.HORIZONTAL,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(pady=5)

        tk.Label(self.root, textvariable=self.status_var, fg="gray").pack(pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path_var.set(folder)

    def start_download_thread(self):
        url = self.url_var.get()
        path = self.save_path_var.get()
        fmt = self.format_var.get()

        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        self.download_btn.config(state=tk.DISABLED, text="Downloading...")
        self.progress_bar['value'] = 0
        self.status_var.set("Starting download...")

        threading.Thread(
            target=self.download_video,
            args=(url, path, fmt),
            daemon=True
        ).start()

    def progress_hook(self, d):
        now = time.time()

        if now - self.progress_state["last_update"] < 0.3:
            return

        self.progress_state["last_update"] = now

        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate")

            if total:
                percent = downloaded / total
                percent_value = min(percent * 100, 100)
                percent_text = f"{percent * 100:.1f}%"
            else:
                percent_value = 0
                percent_text = "Calculating..."

            speed = d.get("speed") or 0
            eta = d.get("eta")

            status_line = (
                f"{percent_text} | "
                f"{downloaded / 1e6:.1f} MB | "
                f"{speed / 1e6:.1f} MB/s | "
                f"ETA: {eta if eta is not None else 'N/A'}"
            )

            self.root.after(
                0,
                self.update_progress_ui,
                percent_value,
                status_line
            )

        elif d["status"] == "finished":
            self.root.after(0, self.finish_progress_ui)


    def update_progress_ui(self, percent, status_text):
        self.progress_bar["value"] = percent
        self.status_var.set(status_text)


    def finish_progress_ui(self):
        self.progress_bar['value'] = 100
        self.status_var.set("Processing...")

    def download_video(self, url, path, fmt):
        try:
            ydl_opts = {
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
            }

            if fmt == "MP3 Audio":
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                format_map = {
                    'Best': 'bestvideo+bestaudio/best',
                    '480P': 'bestvideo[height<=480]+bestaudio/best',
                    '720P': 'bestvideo[height<=720]+bestaudio/best',
                    '1080P': 'bestvideo[height<=1080]+bestaudio/best'
                }

                ydl_opts.update({
                    'format': format_map[self.quality_var.get()],
                    'merge_output_format': 'mp4'
                })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.root.after(
                0,
                lambda: messagebox.showinfo("Success", f"{fmt} Downloaded Successfully!")
            )
            self.root.after(0, lambda: self.status_var.set("Ready"))

        except Exception as e:
            self.root.after(
                0,
                lambda: messagebox.showerror("Error", f"Failed to download:\n{e}")
            )
            self.root.after(0, lambda: self.status_var.set("Error"))

        finally:
            self.root.after(
                0,
                lambda: self.download_btn.config(state=tk.NORMAL, text="Download")
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = YTDownloaderApp(root)
    root.mainloop()
