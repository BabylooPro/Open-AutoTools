import requests
import os
from pathlib import Path
from urllib.parse import urlsplit
from tqdm import tqdm
import yt_dlp
import platform
import subprocess
import json


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
    """OPEN THE DOWNLOAD FOLDER IN THE DEFAULT FILE MANAGER"""
    # SKIP IN CI ENVIRONMENT
    if os.environ.get('CI'):
        return
        
    try:
        if platform.system() == 'Darwin':  # MACOS
            subprocess.run(['open', str(path)], check=True)
        elif platform.system() == 'Windows':  # WINDOWS
            os.startfile(str(path))
        else:  # LINUX
            subprocess.run(['xdg-open', str(path)], check=True)
    except Exception as e:
        print(f"Failed to open download folder: {e}")


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

# FUNCTION TO GET CONSENT FILE PATH
def get_consent_file_path():
    """GET PATH TO STORE CONSENT STATUS"""
    return Path.home() / '.autotools' / 'consent.json'

# FUNCTION TO LOAD CONSENT STATUS
def load_consent_status():
    """LOAD SAVED CONSENT STATUS"""
    consent_file = get_consent_file_path()
    
    # CHECK IF CONSENT FILE EXISTS
    if consent_file.exists():
        try:
            with open(consent_file) as f:
                return json.load(f).get('youtube_consent', False)
        except:
            return False
    return False

# FUNCTION TO SAVE CONSENT STATUS
def save_consent_status(status):
    """SAVE CONSENT STATUS"""
    consent_file = get_consent_file_path()
    consent_file.parent.mkdir(exist_ok=True)
    
    # SAVE CONSENT STATUS TO FILE
    with open(consent_file, 'w') as f:
        json.dump({'youtube_consent': status}, f)

# FUNCTION TO GET USER CONSENT WITH INTERACTIVE PROMPT
def get_user_consent():
    """GET USER CONSENT WITH INTERACTIVE PROMPT"""
    print("\n⚠️  Important Notice:")
    print("This tool will:")
    print("1. Access your Chrome browser cookies")
    print("2. Use them to authenticate with YouTube")
    print("3. Download video content to your local machine")
    
    # GET USER CONSENT WITH INTERACTIVE PROMPT
    while True:
        response = input("\nDo you consent to these actions? (yes/no): ").lower()
        if response in ['yes', 'y']:
            save_consent_status(True)
            return True
        elif response in ['no', 'n']:
            save_consent_status(False)
            return False
        print("Please answer 'yes' or 'no'")


# FUNCTION TO DOWNLOAD YOUTUBE VIDEOS WITH YT-DLP AND SPECIFIED FORMAT AND QUALITY
def download_youtube_video(url, format='mp4', quality='best'):
    """DOWNLOAD VIDEO WITH CONSENT CHECK"""
    # CHECK IF CONSENT IS REQUIRED
    if not load_consent_status():
        if not get_user_consent():
            print("\n❌ Download cancelled by user")
            return False
    
    print(f"\n🎥 Downloading video from: {url}")
    print(f"📋 Format: {format}, Quality: {quality}\n")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if format == 'mp4' else 'bestaudio[ext=mp3]/best',
        'quiet': False,
        'no_warnings': False,
        'cookiesfrombrowser': ('chrome',),
        'extractor_args': {'youtube': {'player_client': ['android']}},
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate'
        },
        'progress_hooks': [lambda d: print(f"⏳ {d['_percent_str']} of {d.get('_total_bytes_str', 'Unknown size')}") if d['status'] == 'downloading' else None]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Download completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False


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
