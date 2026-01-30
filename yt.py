import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading
import os

class YTDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader (yt-dlp)")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.url_var = tk.StringVar()
        self.save_path_var = tk.StringVar()
        self.format_var = tk.StringVar(value="MP4 Video") # Default choice
        self.status_var = tk.StringVar(value="Ready")
        
        default_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.save_path_var.set(default_path)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Video URL:").pack(pady=(15, 5))
        self.url_entry = tk.Entry(self.root, textvariable=self.url_var, width=50)
        self.url_entry.pack(pady=5)

        dir_frame = tk.Frame(self.root)
        dir_frame.pack(pady=5)
        tk.Label(dir_frame, text="Save to: ").pack(side=tk.LEFT)
        tk.Entry(dir_frame, textvariable=self.save_path_var, width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(dir_frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)

        # Format Selection (New Feature)
        format_frame = tk.Frame(self.root)
        format_frame.pack(pady=10)
        tk.Label(format_frame, text="Format: ").pack(side=tk.LEFT)
        
        formats = ["MP4 Video", "MP3 Audio"]
        self.format_menu = ttk.Combobox(format_frame, textvariable=self.format_var, values=formats, state="readonly", width=15)
        self.format_menu.pack(side=tk.LEFT, padx=5)

        self.download_btn = tk.Button(self.root, text="Download", command=self.start_download_thread, bg="#4CAF50", fg="white", width=20)
        self.download_btn.pack(pady=10)

        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress_bar.pack(pady=5)

        self.status_label = tk.Label(self.root, textvariable=self.status_var, fg="gray")
        self.status_label.pack(pady=5)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.save_path_var.set(folder_selected)

    def start_download_thread(self):
        url = self.url_var.get()
        path = self.save_path_var.get()
        fmt = self.format_var.get() # Get the user's choice

        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        self.download_btn.config(state=tk.DISABLED, text="Downloading...")
        self.progress_bar['value'] = 0
        
        # Pass the format choice to the thread
        thread = threading.Thread(target=self.download_video, args=(url, path, fmt))
        thread.start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%','')
                self.progress_bar['value'] = float(p)
                self.status_var.set(f"Downloading: {d.get('_percent_str')}")
                self.root.update_idletasks()
            except ValueError:
                pass
        elif d['status'] == 'finished':
            self.status_var.set("Download complete! Processing...")
            self.progress_bar['value'] = 100

    def download_video(self, url, path, fmt):
        try:
            # Base options
            ydl_opts = {
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
            }

            # Logic to switch based on Dropdown selection
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
                # MP4 Video
                # 'best[ext=mp4]' is the safest option if you don't have FFmpeg
                ydl_opts.update({
                    'format': 'best[ext=mp4]', 
                })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.root.after(0, lambda: messagebox.showinfo("Success", f"{fmt} Downloaded Successfully!"))
            self.status_var.set("Ready")

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to download:\n{str(e)}"))
            self.status_var.set("Error")
            
        finally:
            self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL, text="Download"))

if __name__ == "__main__":
    root = tk.Tk()
    app = YTDownloaderApp(root)
    root.mainloop()