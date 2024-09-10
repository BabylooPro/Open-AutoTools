import requests
import os
from pathlib import Path
from urllib.parse import urlsplit
from tqdm import tqdm
import yt_dlp
import platform
import subprocess


# FUNCTION TO GET DEFAULT DOWNLOAD DIRECTORY
def get_default_download_dir():
    return Path(os.getenv('USERPROFILE') if os.name == 'nt' else Path.home()) / 'Downloads'


# FUNCTION TO GET FILENAME FROM URL WITH DEFAULT AND EXTENSION HANDLING
def get_filename_from_url(url):
    filename = os.path.basename(urlsplit(url).path)
    if not filename:  # IF NO FILENAME IN URL
        return "downloaded_file"
    if not Path(filename).suffix:  # IF NO EXTENSION IN FILENAME
        return f"{filename}.bin"
    return filename


# FUNCTION TO OPEN DOWNLOAD DIRECTORY AFTER DOWNLOAD IS COMPLETE
def open_download_folder(path):
    try:
        if platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', '--', path], check=True)
        elif platform.system() == 'Windows':  # Windows
            subprocess.run(['explorer', str(path)], check=True)
        elif platform.system() == 'Linux':  # Linux
            subprocess.run(['xdg-open', str(path)], check=True)
    except Exception as e:
        print(f"Could not open the folder: {e}")


# FUNCTION TO VALIDATE YOUTUBE URL FORMAT
def validate_youtube_url(url):
    try:
        # USE YT-DLP TO CHECK IF THE URL IS VALID
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            ydl.extract_info(url, download=False)
        return True
    except yt_dlp.utils.DownloadError as e:
        print(f"Invalid YouTube URL: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during URL validation: {e}")
        return False


# FUNCTION TO DOWNLOAD FILES WITH REQUESTS, INCLUDING ERROR HANDLING AND PROGRESS BAR
def download_file(url):
    download_dir = get_default_download_dir()
    filename = get_filename_from_url(url)
    dest_file = download_dir / filename

    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1KB

            with tqdm(total=total_size if total_size else None, unit='iB', unit_scale=True, desc=f"Downloading {filename}", leave=True) as tqdm_bar:
                with open(dest_file, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            file.write(chunk)
                            tqdm_bar.update(len(chunk))

        # AUTOMATICALLY OPEN DOWNLOAD FOLDER AFTER FILE DOWNLOAD IS COMPLETE
        open_download_folder(download_dir)
    except requests.exceptions.RequestException as e:
        print(f"Error during file download: {e}")


# FUNCTION TO DOWNLOAD YOUTUBE VIDEOS WITH YT-DLP AND SPECIFIED FORMAT AND QUALITY
def download_youtube_video(url, file_format='mp4', quality='best'):
    # First, validate the YouTube URL
    if not validate_youtube_url(url):
        print(f"Aborting download: Invalid URL {url}")
        return

    download_dir = get_default_download_dir()

    video_formats = {
        '1440p': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
        '240p': 'bestvideo[height<=240]+bestaudio/best[height<=240]',
        'best': 'bestvideo+bestaudio/best'
    }

    selected_format = video_formats.get(quality, video_formats['best'])

    ydl_opts = {
        'format': selected_format if file_format == 'mp4' else 'bestaudio',
        'outtmpl': str(download_dir / '%(title)s.%(ext)s'),
        'progress_hooks': [tqdm_progress_hook],
        'quiet': True,  # SUPPRESS MOST OF YT-DLP OUTPUT EXCEPT PROGRESS
        'no_warnings': True,  # HIDE WARNINGS
        'merge_output_format': 'mp4'  # AUTOMATICALLY REMUX TO MP4 IF NEEDED
    }

    if file_format == 'mp3':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        # AUTOMATICALLY OPEN DOWNLOAD FOLDER AFTER YOUTUBE DOWNLOAD IS COMPLETE
        open_download_folder(download_dir)
    except yt_dlp.utils.DownloadError as e:
        print(f"Error during YouTube download: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# FUNCTION TO LIST AVAILABLE FORMATS FOR A YOUTUBE VIDEO
def list_available_formats(url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', None)
            if formats:
                for f in formats:
                    print(f"Format: {f['format_id']}, Resolution: {f.get('resolution')}, Extension: {f['ext']}")
    except yt_dlp.utils.DownloadError as e:
        print(f"Error fetching formats: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

pbar = None  # GLOBAL VARIABLE TO STORE PROGRESS BAR


# FUNCTION TO UPDATE PROGRESS BAR
def tqdm_progress_hook(d):
    global pbar

    if d['status'] == 'downloading':
        total = d.get('total_bytes', 0)
        downloaded = d.get('downloaded_bytes', 0)

        if pbar is None:
            pbar = tqdm(total=total, unit='B', unit_scale=True, desc="YouTube Download", leave=True)

        pbar.n = downloaded
        pbar.refresh()

    elif d['status'] == 'finished' and pbar:
        pbar.n = pbar.total
        pbar.close()
        print("Download completed")
        pbar = None


# FUNCTION TO DOWNLOAD FILE WITH SPECIFIC HANDLING AND FOLDER OPENING
def download_file_with_tqdm(url):
    download_dir = get_default_download_dir()
    filename = get_filename_from_url(url)
    dest_file = download_dir / filename

    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1KB

            with tqdm(total=total_size if total_size else None, unit='iB', unit_scale=True, desc=f"Downloading {filename}", leave=True) as tqdm_bar:
                with open(dest_file, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            file.write(chunk)
                            tqdm_bar.update(len(chunk))

        # AUTOMATICALLY OPEN DOWNLOAD FOLDER AFTER FILE DOWNLOAD IS COMPLETE
        open_download_folder(download_dir)
    except requests.exceptions.RequestException as e:
        print(f"Error during file download: {e}")
