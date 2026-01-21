import os
from pathlib import Path
from typing import Optional

# CONVERTS AUDIO BETWEEN FORMATS
def convert_audio(input_path: str, output_path: str, output_format: Optional[str] = None) -> bool:
    try:
        from pydub import AudioSegment

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"INPUT FILE NOT FOUND: {input_path}")
        if output_format is None: output_format = Path(output_path).suffix[1:].lower()

        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=output_format)

        return True

    except ImportError:
        raise ImportError("PYDUB is required for audio conversion. Install with: pip install pydub. Also install FFMPEG.")
    except (OSError, ValueError, IOError) as e:
        raise RuntimeError(f"AUDIO CONVERSION FAILED: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"AUDIO CONVERSION FAILED: {str(e)}")
