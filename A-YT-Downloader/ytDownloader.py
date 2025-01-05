"""
- You may face a problem with tkinter .. 
- Run { sudo apt-get install python3-tk } to solve It ..
- Run { pip3 install pytube }.
"""
from pytube import YouTube
from pytube.exceptions import PytubeError
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import re
import logging


logging.basicConfig(filename="youtube_downloader.log", level=logging.ERROR)

def is_valid_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return re.match(youtube_regex, url) is not None

def sanitize_filename(filename):
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)
    return sanitized[:255]

def has_write_permission(directory):
    try:
        test_file = os.path.join(directory, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        return True
    except Exception:
        return False

def download_media(url, save_path, download_type="video"):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        if download_type == "video":
            streams = yt.streams.filter(progressive=True, file_extension="mp4")
            if not streams:
                messagebox.showerror("Error", "No MP4 streams available for this video.")
                return
            stream = streams.get_highest_resolution()
            file_name = sanitize_filename(f"{yt.title}.mp4")
        elif download_type == "audio":
            stream = yt.streams.filter(only_audio=True).first()
            file_name = sanitize_filename(f"{yt.title}.mp3")
        else:
            messagebox.showerror("Error", "Invalid download type.")
            return

        output_file = stream.download(output_path=save_path, filename=file_name)
        print(f"Downloaded: {output_file}")

        save_metadata(yt, save_path, file_name)

        messagebox.showinfo("Success", f"{download_type.capitalize()} downloaded successfully!")
    except PytubeError as e:
        logging.error(f"PytubeError: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def save_metadata(yt, save_path, file_name):
    metadata_file = os.path.join(save_path, f"{os.path.splitext(file_name)[0]}_metadata.txt")
    if os.path.exists(metadata_file):
        overwrite = messagebox.askyesno("File Exists", "Metadata file already exists. Overwrite?")
        if not overwrite:
            return
    with open(metadata_file, "w", encoding="utf-8") as f:
        f.write(f"Title: {yt.title}\n")
        f.write(f"Author: {yt.author}\n")
        f.write(f"Length: {yt.length} seconds\n")
        f.write(f"Views: {yt.views}\n")
        f.write(f"Description: {yt.description}\n")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = (bytes_downloaded / total_size) * 100
    progress_bar["value"] = progress
    root.update_idletasks()

def on_download_click():
    urls = url_text.get("1.0", tk.END).strip().split("\n")
    save_path = filedialog.askdirectory()
    if not save_path:
        messagebox.showwarning("Warning", "Please select a save location.")
        return
    if not urls or urls == [""]:
        messagebox.showwarning("Warning", "Please enter at least one URL.")
        return

    if not has_write_permission(save_path):
        messagebox.showerror("Error", "No write permissions in the selected directory.")
        return

    download_type = download_var.get()
    for url in urls:
        if url.strip():
            if not is_valid_youtube_url(url.strip()):
                messagebox.showerror("Error", f"Invalid YouTube URL: {url}")
                continue
            download_media(url.strip(), save_path, download_type)

root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("500x400")

url_label = tk.Label(root, text="Enter YouTube URL(s):")
url_label.pack(pady=5)
url_text = scrolledtext.ScrolledText(root, height=5, width=50)
url_text.pack(pady=5)

download_var = tk.StringVar(value="video")
video_radio = tk.Radiobutton(root, text="Download Video (MP4)", variable=download_var, value="video")
video_radio.pack(pady=5)
audio_radio = tk.Radiobutton(root, text="Download Audio (MP3)", variable=download_var, value="audio")
audio_radio.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

download_button = tk.Button(root, text="Download", command=on_download_click)
download_button.pack(pady=10)

root.mainloop()