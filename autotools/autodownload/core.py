import requests
import os
from pathlib import Path
from urllib.parse import urlsplit
from tqdm import tqdm
import yt_dlp
import platform
import subprocess
import json
from rich.progress import Progress
from ..utils.loading import LoadingAnimation


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
    """BASIC URL VALIDATION WITH PROPER FORMAT CHECK"""
    # CHECK IF URL CONTAINS YOUTUBE DOMAIN
    is_youtube = any(domain in url for domain in ["youtube.com", "youtu.be", "music.youtube.com"])
    
    # CHECK IF URL HAS PROPER VIDEO ID FORMAT
    has_video_id = False
    if "youtube.com/watch" in url and "v=" in url:
        has_video_id = True
    elif "youtu.be/" in url and len(url.split("youtu.be/")[1]) > 0:
        has_video_id = True
    elif any(pattern in url for pattern in ["/watch/", "/shorts/", "/live/"]):
        path_parts = url.split("/")
        has_video_id = len(path_parts[-1]) > 0
    elif "attribution_link" in url and "watch?v=" in url:
        has_video_id = True
        
    return is_youtube and has_video_id


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
    # INFO: delete consent file with "rm -f ~/.autotools/consent.json" if you want to force new consent in local development
    return Path.home() / '.autotools' / 'consent.json'

# FUNCTION TO LOAD CONSENT STATUS
def load_consent_status():
    """LOAD SAVED CONSENT STATUS"""
    try:
        consent_file = get_consent_file_path()
        
        # FORCE NEW CONSENT IF FILE DOESN'T EXIST OR IS EMPTY
        if not consent_file.exists():
            return False
            
        # READ CONSENT STATUS
        with open(consent_file) as f:
            data = json.load(f)
            return data.get('youtube_consent', False)
    except Exception:
        # IF ANY ERROR OCCURS, FORCE NEW CONSENT
        return False

# FUNCTION TO SAVE CONSENT STATUS
def save_consent_status(status):
    """SAVE CONSENT STATUS"""
    try:
        consent_file = get_consent_file_path()
        consent_file.parent.mkdir(exist_ok=True)
        
        # SAVE CONSENT STATUS TO FILE
        with open(consent_file, 'w') as f:
            json.dump({'youtube_consent': status}, f)
        return True
    except Exception:
        # IF SAVING FAILS, RETURN FALSE TO FORCE NEW CONSENT NEXT TIME
        return False

# FUNCTION TO GET USER CONSENT WITH INTERACTIVE PROMPT
def get_user_consent():
    """GET USER CONSENT WITH INTERACTIVE PROMPT"""
    print("\n⚠️  Important Notice:")
    print("This tool will:")
    print("1. Download video content from YouTube")
    print("2. Save files to your local machine")
    print("3. Use mobile API for better compatibility")
    
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


# FUNCTION TO CHECK IF VIDEO EXISTS AND GET USER CONSENT FOR REPLACEMENT
def check_existing_video(info, format='mp4'):
    """CHECK IF VIDEO EXISTS AND ASK FOR REPLACEMENT"""
    download_dir = get_default_download_dir()
    title = info.get('title', '').replace('/', '_')  # SANITIZE TITLE
    filename = f"{title}.{format}"
    filepath = download_dir / filename

    # CHECK IF FILE EXISTS AND ASK FOR REPLACEMENT
    if filepath.exists():
        print(f"\n⚠️  File already exists: {filename}")
        while True:
            response = input("Do you want to replace it? (yes/no): ").lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                # OPEN DOWNLOADS FOLDER TO SHOW EXISTING FILE
                open_download_folder(download_dir)
                return False
            print("Please answer 'yes' or 'no'")
    return True


# FUNCTION TO DOWNLOAD YOUTUBE VIDEOS WITH YT-DLP AND SPECIFIED FORMAT AND QUALITY
def download_youtube_video(url, format='mp4', quality='best'):
    """DOWNLOAD VIDEO WITH CONSENT CHECK"""
    # VALIDATE URL FIRST
    if not validate_youtube_url(url):
        print("\n❌ Invalid YouTube URL")
        return False

    # CHECK FOR SAVED CONSENT FIRST AND GET NEW CONSENT IF NEEDED
    if not load_consent_status() and not get_user_consent():
        print("\n❌ Download cancelled by user")
        return False
    
    # FIRST CHECK VIDEO INFO AND EXISTENCE
    try:
        with yt_dlp.YoutubeDL({
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {'youtube': {
                'player_client': ['android'],
                'formats': ['missing_pot']  # ALLOW FORMATS WITHOUT PO TOKEN
            }}
        }) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            if not formats:
                print("\n❌ No formats available for this video")
                return False
            
            # CHECK IF FILE EXISTS AND GET REPLACEMENT CONSENT
            force_download = check_existing_video(info, format)
            if not force_download:
                print("\n❌ Download cancelled - file already exists")
                return False
                
            # OPEN DOWNLOADS FOLDER IF STARTING NEW DOWNLOAD OR REPLACING
            download_dir = get_default_download_dir()
            open_download_folder(download_dir)

    except Exception as e:
        print(f"\n❌ Error checking video: {str(e)}")
        return False
    
    loading = LoadingAnimation()
    
    # START LOADING FOR DOWNLOAD PROCESS
    with loading:
        loading._spinner.start()
        print("\n🔍 Starting download...")
    
    print(f"\n🎥 Downloading video from: {url}")
    print(f"📋 Format: {format}, Quality: {quality}\n")

    # YT-DLP PERMISSION OPTIONS FOR DOWNLOADING YOUTUBE VIDEOS
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if format == 'mp4' else 'bestaudio[ext=mp3]/best',
        'quiet': True,
        'no_warnings': True,
        'progress': True,
        'progress_hooks': [lambda d: print(f"⏳ {d['_percent_str']} of {d.get('_total_bytes_str', 'Unknown size')}") if d['status'] == 'downloading' else None],
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
                'formats': ['missing_pot']  # ALLOW FORMATS WITHOUT PO TOKEN
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36'
        },
        'outtmpl': str(download_dir / '%(title)s.%(ext)s'),  # SET OUTPUT TEMPLATE
        'overwrites': True  # FORCE OVERWRITE IF USER CONSENTED
    }

    try:
        # THEN DOWNLOAD
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Download completed successfully!")
        return True
    except Exception as e:
        error_msg = str(e)
        if "Requested format is not available" in error_msg:
            print("\n❌ Format not available. Available formats are:")
            for f in formats:
                print(f"- {f.get('format_id', 'N/A')}: {f.get('ext', 'N/A')} ({f.get('format_note', 'N/A')})")
        else:
            print(f"\n❌ ERROR: {error_msg}")
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
