from pathlib import Path
from typing import Optional, Tuple

from .conversion.convert_text import convert_text_file
from .conversion.convert_image import convert_image
from .conversion.convert_audio import convert_audio
from .conversion.convert_video import convert_video

# DETECTS FILE TYPE AND CONVERTS ACCORDINGLY
def detect_file_type(file_path: str) -> str:
    ext = Path(file_path).suffix[1:].lower()

    # TEXT FORMATS
    text_formats = ['txt', 'md', 'markdown', 'json', 'xml', 'html', 'htm', 'csv']
    if ext in text_formats: return 'text'

    # IMAGE FORMATS
    image_formats = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff', 'tif', 'ico', 'svg']
    if ext in image_formats: return 'image'

    # AUDIO FORMATS
    audio_formats = ['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a', 'wma', 'opus']
    if ext in audio_formats: return 'audio'

    # VIDEO FORMATS
    video_formats = ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'm4v']
    if ext in video_formats: return 'video'
    
    return 'unknown'

# CONVERTS FILE FROM ONE FORMAT TO ANOTHER
def convert_file(input_path: str, output_path: str, input_type: Optional[str] = None, output_type: Optional[str] = None) -> Tuple[bool, str]:
    try:
        if input_type is None: input_type = detect_file_type(input_path)
        if output_type is None: output_type = detect_file_type(output_path)
        if input_type == 'text' and output_type == 'text': return convert_text_file(input_path, output_path)
        
        # HANDLE CONVERSIONS WITHIN THE SAME MEDIA TYPE
        elif input_type == 'image' and output_type == 'image':
            convert_image(input_path, output_path)
            return True, "IMAGE CONVERTED SUCCESSFULLY"
        elif input_type == 'audio' and output_type == 'audio':
            convert_audio(input_path, output_path)
            return True, "AUDIO CONVERTED SUCCESSFULLY"
        elif input_type == 'video' and output_type == 'video':
            convert_video(input_path, output_path)
            return True, "VIDEO CONVERTED SUCCESSFULLY"
        else:
            return False, f"UNSUPPORTED CONVERSION: {input_type} TO {output_type}"
    
    except FileNotFoundError:
        raise
    except Exception as e:
        return False, f"CONVERSION FAILED: {str(e)}"
