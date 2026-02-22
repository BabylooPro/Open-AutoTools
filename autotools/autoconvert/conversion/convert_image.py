import os
from pathlib import Path
from typing import Optional

# CONVERTS IMAGE BETWEEN FORMATS
def convert_image(input_path: str, output_path: str, output_format: Optional[str] = None) -> bool:
    try:
        from PIL import Image
        input_ext = Path(input_path).suffix[1:].lower()
        if input_ext in ('heic', 'heif'):
            try:
                from pillow_heif import register_heif_opener
                register_heif_opener()
            except ImportError:
                pass

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"INPUT FILE NOT FOUND: {input_path}")
        if output_format is None: output_format = Path(output_path).suffix[1:].upper()

        format_aliases = {'JPG': 'JPEG', 'TIF': 'TIFF'}
        output_format = format_aliases.get(output_format.upper(), output_format.upper())

        with Image.open(input_path) as img:
            if output_format in ['JPG', 'JPEG'] and img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P': img = img.convert('RGBA')
                rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = rgb_img
            
            img.save(output_path, format=output_format)
        return True

    except ImportError:
        raise ImportError("PILLOW (PIL) is required for image conversion. Install with: pip install Pillow")
    except (OSError, ValueError, IOError) as e:
        raise RuntimeError(f"IMAGE CONVERSION FAILED: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"IMAGE CONVERSION FAILED: {str(e)}")
