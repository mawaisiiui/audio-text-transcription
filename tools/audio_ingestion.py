"""
Step 1: Accept Audio file and validate

Run it with:
    python audio_ingestion.py sample.wav
"""
import sys
from pathlib import Path

SUPPORTED_FORMATS = ["wav", "mp3"]

class AudioValidationError(Exception):
    """Raised when the input file is unusable."""

def accept_audio_file(path_txt):
    path = Path(path_txt)

    file_format = path.suffix.lstrip(".").lower()

    if file_format not in SUPPORTED_FORMATS:
        sys.exit("Format not supported")


    if not path.is_file():
        sys.exit("File not exist")

    size = path.stat().st_size

    if size == 0:
        sys.exit("File is empty")

    print(f"File: {path_txt} Accepted. format: {file_format} Size: {size} bytes")

    return path

