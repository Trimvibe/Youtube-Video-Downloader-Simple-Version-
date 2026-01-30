# 📺 Python YouTube Downloader (GUI)

A clean, lightweight, and fast YouTube video downloader built with Python. It features a modern GUI using **Tkinter** and uses the powerful **yt-dlp** engine for reliable downloads.

##  Prerequisites
Before running the app, ensure you have the following installed:

1.  **Python 3.x** ([Download Here](https://www.python.org/downloads/))
2.  **FFmpeg** (Required for MP3 conversion and 1080p video merging)
    * *Windows:* [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your system PATH or place `ffmpeg.exe` in this project folder.

##  Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/youtube-Video-Downloader-Simple-version.git](https://github.com/YOUR_USERNAME/youtube-downloader-gui.git)
    cd youtube-downloader-gui
    ```

2.  **Install Dependencies**
    This project relies on `yt-dlp`. Install it via pip:
    ```bash
    pip install yt-dlp
    ```

## Usage

1.  Run the script using Python:
    ```bash
    python downloader.py
    ```
2.  Paste a YouTube link into the URL field.
3.  Select your desired format (MP4 or MP3).
4.  Choose a download folder (default is `Downloads`).
5.  Click **Download**.


## Note - 
##  Troubleshooting

Error: "ffprobe/ffmpeg not found"
    * This means you are trying to download MP3 or high-quality video without FFmpeg installed.
    * **Fix:** Download `ffmpeg.exe` and put it in the same folder as `downloader.py`.

* **Error: "The downloaded file is empty"**
    * This happens if the stream is interrupted or incompatible.
    * **Fix:** Update the library by running `pip install --upgrade yt-dlp`.

##  License
This project is open-source and available under the [MIT License](LICENSE).

##  Disclaimer
This tool is for educational purposes only. Please respect YouTube's Terms of Service and copyright laws. Do not download copyrighted content without permission.
