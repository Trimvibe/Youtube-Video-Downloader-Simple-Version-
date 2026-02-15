from flask import Flask, render_template, request, jsonify
from download import download_youtube_video
import threading
import queue

app = Flask(__name__)
progress_queue = queue.Queue()

def progress_hook(percent, speed):
    speed = speed or 0
    progress_queue.put({
        "percent": percent,
        "speed": round(speed / 1e6, 2)
    })


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fetch", methods=["POST"])
def fetch():
    data = request.json

    def task():
        download_youtube_video(
            url=data["url"],
            selected_res=data.get("resolution", "Best"),
            file_type=data.get("file_type", "mp4"),
            progress_callback=progress_hook
        )
        progress_queue.put({"done": True})

    threading.Thread(target=task, daemon=True).start()
    return jsonify({"status": "started"})

@app.route("/progress")
def progress():
    if not progress_queue.empty():
        return jsonify(progress_queue.get())
    return jsonify({})

if __name__ == "__main__":
    app.run(debug=True)