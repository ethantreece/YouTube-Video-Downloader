import tkinter as tk
from tkinter import filedialog, messagebox
import os
from moviepy.editor import VideoFileClip, AudioFileClip
from downloader import get_video_info, download_video
from video_preview import display_video_thumbnail

class YouTubeDownloaderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Video Downloader")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="YouTube URL:").pack(pady=5)
        
        url_frame = tk.Frame(self.root)
        url_frame.pack(pady=5)
        
        self.url_entry = tk.Entry(url_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=5)
        self.url_entry.bind("<Return>", self.fetch_video_info)
        
        search_btn = tk.Button(url_frame, text="Search", command=self.fetch_video_info)
        search_btn.pack(side=tk.LEFT)

        self.video_frame = tk.Frame(self.root)
        self.video_frame.pack(pady=20)

        self.quality_var = tk.StringVar(self.root)
        self.quality_menu = None
        self.download_btn = None

    def fetch_video_info(self, event=None):
        url = self.url_entry.get()
        try:
            title, thumbnail_url, video_streams, audio_streams = get_video_info(url)
            self.show_video_info(title, thumbnail_url, video_streams, audio_streams)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_video_info(self, title, thumbnail_url, video_streams, audio_streams):
        for widget in self.video_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.video_frame, text=title, wraplength=400).pack()
        display_video_thumbnail(self.video_frame, thumbnail_url)
        
        resolutions = sorted(set(stream.resolution for stream in video_streams))
        self.quality_var.set(resolutions[0])
        self.quality_menu = tk.OptionMenu(self.video_frame, self.quality_var, *resolutions)
        self.quality_menu.pack(pady=5)
        
        self.download_btn = tk.Button(self.video_frame, text="Download", command=self.download)
        self.download_btn.pack(pady=20)

    def download(self):
        url = self.url_entry.get()
        path = filedialog.askdirectory()
        if not path:
            return
        try:
            quality = self.quality_var.get()
            video_file, audio_file = download_video(url, path, quality)
            output_file = os.path.join(path, "output.mp4")
            self.combine_video_audio(video_file, audio_file, output_file)
            os.remove(video_file)
            os.remove(audio_file)
            messagebox.showinfo("Success", "Video downloaded and combined successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def combine_video_audio(self, video_file, audio_file, output_file):
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')

    def run(self):
        self.root.mainloop()
