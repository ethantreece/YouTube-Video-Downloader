from pytube import YouTube

def get_video_info(url):
    yt = YouTube(url)
    title = yt.title
    thumbnail_url = yt.thumbnail_url
    streams = yt.streams.filter(progressive=False).order_by('resolution').desc()
    
    video_streams = []
    resolutions = set()
    for stream in streams:
        if stream.resolution and stream.resolution not in resolutions:
            video_streams.append(stream)
            resolutions.add(stream.resolution)
    audio_streams = yt.streams.filter(only_audio=True)
    return title, thumbnail_url, video_streams, audio_streams

def download_video(url, path, resolution):
    yt = YouTube(url)
    video_stream = yt.streams.filter(res=resolution, only_video=True).first()
    audio_stream = yt.streams.filter(only_audio=True).first()

    if not video_stream:
        raise ValueError(f"Video stream with resolution {resolution} not available.")
    if not audio_stream:
        raise ValueError("Audio stream not available.")

    video_file = video_stream.download(output_path=path, filename_prefix="video_")
    audio_file = audio_stream.download(output_path=path, filename_prefix="audio_")
    
    return video_file, audio_file