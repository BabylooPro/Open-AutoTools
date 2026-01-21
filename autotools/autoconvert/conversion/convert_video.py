import os
from pathlib import Path
from typing import Optional

# CONVERTS VIDEO BETWEEN FORMATS
def convert_video(input_path: str, output_path: str, output_format: Optional[str] = None) -> bool:
    try:
        from moviepy.editor import VideoFileClip
        
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"INPUT FILE NOT FOUND: {input_path}")
        if output_format is None: output_format = Path(output_path).suffix[1:].lower()

        with VideoFileClip(input_path) as video: video.write_videofile(output_path, codec='libx264', audio_codec='aac')

        return True

    except ImportError:
        raise ImportError("MOVIEPY IS REQUIRED FOR VIDEO CONVERSION. INSTALL WITH: pip install moviepy. ALSO INSTALL FFMPEG.")

    except (OSError, ValueError, IOError) as e:
        raise RuntimeError(f"VIDEO CONVERSION FAILED: {str(e)}")

    except Exception as e:
        raise RuntimeError(f"VIDEO CONVERSION FAILED: {str(e)}")
