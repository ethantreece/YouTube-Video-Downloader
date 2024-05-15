import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube

def download_video():
    url = url_entry.get()
    path = filedialog.askdirectory()
    if not path:
        return
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(path)
        messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("YouTube Video Downloader")

tk.Label(app, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=5)

download_btn = tk.Button(app, text="Download", command=download_video)
download_btn.pack(pady=20)

app.mainloop()
