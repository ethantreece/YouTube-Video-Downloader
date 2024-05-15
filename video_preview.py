import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

def display_video_thumbnail(frame, url):
    response = requests.get(url)
    img_data = BytesIO(response.content)
    img = Image.open(img_data)
    img = img.resize((320, 180))
    img_tk = ImageTk.PhotoImage(img)

    label = tk.Label(frame, image=img_tk)
    label.image = img_tk
    label.pack(pady=5)
