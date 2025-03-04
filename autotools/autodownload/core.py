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
from yt_dlp.cookies import extract_cookies_from_browser


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

# FUNCTION TO SAFELY PRINT WITH EMOJI FALLBACK
def safe_print(text):
    """PRINT TEXT WITH EMOJI FALLBACK FOR WINDOWS"""
    try:
        print(text)
    except UnicodeEncodeError:
        # REPLACE EMOJIS WITH ASCII ALTERNATIVES
        text = (text.replace('⚠️', '!')
                   .replace('🔍', '*')
                   .replace('🎥', '>')
                   .replace('📋', '+')
                   .replace('❌', 'X')
                   .replace('✅', 'V')
                   .replace('↓', 'v'))
        print(text)

# FUNCTION TO GET USER CONSENT WITH INTERACTIVE PROMPT
def get_user_consent():
    """GET USER CONSENT WITH INTERACTIVE PROMPT"""
    safe_print("\n!  Important Notice:")
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
        safe_print("\nX Invalid YouTube URL")
        return False

    # CHECK FOR SAVED CONSENT FIRST AND GET NEW CONSENT IF NEEDED
    if not load_consent_status() and not get_user_consent():
        safe_print("\nX Download cancelled by user")
        return False
    
    # UPDATE YT-DLP FIRST
    try:
        yt_dlp.utils.std_headers.clear()
        yt_dlp.update.__version__ = yt_dlp.version.__version__
        yt_dlp.update.update()
    except Exception:
        pass  # IGNORE UPDATE ERRORS

    # SETUP CUSTOM HEADERS AND COOKIES
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://www.youtube.com',
        'Referer': 'https://www.youtube.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Cookie': '',
        'TE': 'trailers'
    }
    
    # FIRST CHECK VIDEO INFO AND EXISTENCE
    try:
        ydl_opts = {
            'quiet': False,  # ENABLE OUTPUT
            'verbose': True,  # ENABLE VERBOSE MODE
            'no_warnings': False,  # SHOW WARNINGS
            'rm_cachedir': True,  # CLEAR CACHE
            'http_headers': custom_headers,
            'cookiesfrombrowser': get_browser_cookies(),  # TRY TO GET COOKIES FROM BROWSER
            'format_sort': ['res:2160', 'res:1440', 'res:1080', 'ext:mp4:m4a'],  # FORCE HIGH QUALITY
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios'],
                    'formats': 'all',
                    'format': '313+251/271+251/137+251'  # 4K+AUDIO / 1440p+AUDIO / 1080p+AUDIO
                }
            },
            'socket_timeout': 30,  # INCREASE TIMEOUT
            'nocheckcertificate': True,  # SKIP CERTIFICATE VALIDATION
            'ignoreerrors': True  # CONTINUE ON ERRORS
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            if not formats:
                safe_print("\nX No formats available for this video")
                return False
            
            # FIND BEST AVAILABLE QUALITY
            best_height = 0
            for f in formats:
                height = f.get('height')
                if height is not None and height > best_height:
                    best_height = height
            
            # IF NO VALID HEIGHT FOUND, DEFAULT TO 1080P
            if best_height == 0:
                best_height = 1080
            
            # IF QUALITY IS 'BEST', USE THE BEST AVAILABLE
            if quality == 'best':
                height = best_height
                # ASK FOR CONFIRMATION IF 4K OR HIGHER (ONLY FOR MP4)
                if format == 'mp4' and height >= 2160:
                    safe_print(f"\n! This video is available in {height}p quality!")
                    while True:
                        response = input(f"Do you want to download in {height}p quality? (yes/no): ").lower()
                        if response in ['no', 'n']:
                            height = 1080
                            print("\nDowngrading to 1080p quality.")
                            break
                        elif response in ['yes', 'y']:
                            break
                        print("Please answer 'yes' or 'no'")
            else:
                # EXTRACT HEIGHT FROM QUALITY STRING
                try:
                    height = int(quality.lower().replace('p', ''))
                except ValueError:
                    height = 1080  # DEFAULT TO 1080P IF INVALID FORMAT
            
            # CHECK IF FILE EXISTS AND GET REPLACEMENT CONSENT
            force_download = check_existing_video(info, format)
            if not force_download:
                safe_print("\nX Download cancelled - file already exists")
                return False
                
            # OPEN DOWNLOADS FOLDER IF STARTING NEW DOWNLOAD OR REPLACING
            download_dir = get_default_download_dir()
            open_download_folder(download_dir)

    except Exception as e:
        safe_print(f"\nX Error checking video: {str(e)}")
        return False
    
    loading = LoadingAnimation()
    
    # START LOADING FOR DOWNLOAD PROCESS
    with loading:
        loading._spinner.start()
        safe_print("\n* Starting download...")
    
    safe_print(f"\n> Downloading video from: {url}")
    if format == 'mp3':
        safe_print(f"+ Format: {format}\n")
    else:
        safe_print(f"+ Format: {format}, Quality: {height}p\n")

    # YT-DLP PERMISSION OPTIONS FOR DOWNLOADING YOUTUBE VIDEOS
    ydl_opts = {
        'format': 'bestvideo[height>=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height>=2160][ext=webm]+bestaudio[ext=webm]/bestvideo[height>=2160]+bestaudio/best',
        'format_sort': ['res:2160', 'res:1440', 'res:1080', 'ext:mp4:m4a'],
        'format_sort_force': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format == 'mp3' else [],
        'quiet': True,  # HIDE MOST OUTPUT
        'verbose': False,  # DISABLE VERBOSE MODE
        'no_warnings': True,  # HIDE WARNINGS
        'progress': True,
        'progress_hooks': [lambda d: update_progress(d)],
        'outtmpl': str(download_dir / '%(title)s.%(ext)s'),
        'overwrites': True,
        'retries': 10,
        'fragment_retries': 10,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://www.youtube.com',
            'Referer': 'https://www.youtube.com/',
            'Connection': 'keep-alive'
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['ios'],
                'formats': 'all',
                'format': '313+251/271+251/137+251'  # 4K+AUDIO / 1440p+AUDIO / 1080p+AUDIO
            }
        },
        'socket_timeout': 30,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'noresizebuffer': True,
        'nopart': True,
        'continuedl': False,
        'allow_unplayable_formats': False,
        'no_check_formats': False,
        'prefer_free_formats': False,
        'hls_prefer_native': True,
        'hls_use_mpegts': False,
        'concurrent_fragment_downloads': 1,
        'external_downloader': 'native',
        'no_color': True,  # DISABLE COLORED OUTPUT
        'logtostderr': False,  # DISABLE STDERR LOGGING
        'consoletitle': False,  # DISABLE CONSOLE TITLE
        'prefer_insecure': True,  # IGNORE SSL ERRORS
        'no_call_home': True  # DISABLE ANALYTICS
    }

    try:
        # THEN DOWNLOAD
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                safe_print("\nV Download completed successfully!")
                return True
            except Exception as e:
                if "HTTP Error 403" in str(e):
                    safe_print("\n! Access denied for requested quality. Trying lower quality...")
                    # TRY DOWNLOADING WITH LOWER QUALITY
                    if height > 720:
                        new_height = min(height - 360, 1080)  # STEP DOWN QUALITY
                        safe_print(f"v Falling back to {new_height}p")
                        ydl_opts['format'] = (
                            f'bestvideo[height<={new_height}][ext=mp4]+bestaudio[ext=m4a]/'
                            f'bestvideo[height<={new_height}][ext=webm]+bestaudio[ext=webm]/'
                            f'best[height<={new_height}]/'
                            'best'
                        )
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
                            ydl2.download([url])
                        safe_print("\nV Download completed successfully!")
                        return True
                    else:
                        safe_print("\nX Failed to download video at any quality")
                        return False
                else:
                    raise e
                
    # CATCH ANY EXCEPTIONS AND HANDLE THEM
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
def update_progress(d):
    global pbar
    if d['status'] == 'downloading':
        total = d.get('total_bytes', 0)
        downloaded = d.get('downloaded_bytes', 0)

        if pbar is None:
            pbar = tqdm(total=total, unit='B', unit_scale=True, desc="⏳ Downloading", leave=True, ncols=80, bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]')

        if total > 0:
            pbar.n = downloaded
            pbar.total = total
            pbar.refresh()

    elif d['status'] == 'finished' and pbar:
        pbar.close()
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


# FUNCTION TO GET BROWSER COOKIES
def get_browser_cookies():
    """GET BROWSER COOKIES WITH FALLBACK OPTIONS"""
    try:
        # TRY CHROME FIRST
        cookies = extract_cookies_from_browser('chrome')
        if cookies:
            return ('chrome',)
    except Exception:
        pass
        
    try:
        # TRY FIREFOX IF CHROME FAILS
        cookies = extract_cookies_from_browser('firefox')
        if cookies:
            return ('firefox',)
    except Exception:
        pass
        
    # IF ALL FAILS, RETURN NONE AND CONTINUE WITHOUT COOKIES
    return None
