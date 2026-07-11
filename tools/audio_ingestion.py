"""
Step 1: Accept Audio file and validate

Run it with:
    python audio_ingestion.py sample.wav
"""
import sys
from pathlib import Path

SUPPORTED_FORMATS = ["wav", "mp3", "m4a", "flac", "ogg"]
MAX_FILE_SIZE = 500 * 1024 * 1024 # 500 MB

class AudioValidationError(Exception):
    """Raised when the input file is unusable."""

def accept_audio_file(path_txt):
    path = Path(path_txt)

    file_format = path.suffix.lstrip(".").lower()

    if not path.is_file():
        raise AudioValidationError("File not exist: {path}")

    if file_format not in SUPPORTED_FORMATS:
        raise AudioValidationError("Format not supported")

    size = path.stat().st_size

    if size == 0:
        raise AudioValidationError("File is empty")
    if size > MAX_FILE_SIZE:
        raise AudioValidationError("File is too large")

    print(f"File: {path_txt} Accepted. format: {file_format} Size: {size} bytes")

    return path

