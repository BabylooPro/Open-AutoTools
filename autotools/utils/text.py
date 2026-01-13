import sys
from typing import Any

# ENSURE TEXT IS SAFE TO WRITE TO THE CURRENT STDOUT ENCODING
# SOME WINDOWS TERMINALS USE LEGACY ENCODINGS THAT CANNOT ENCODE CERTAIN CHARACTERS
def safe_text(text: Any) -> Any:
    if not isinstance(text, str): return text

    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"

    try:
        text.encode(encoding)
        return text
    except Exception:
        try: return text.encode(encoding, errors="replace").decode(encoding)
        except Exception: return text.encode("ascii", errors="replace").decode("ascii")
