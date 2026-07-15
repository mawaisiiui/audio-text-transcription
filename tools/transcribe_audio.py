

"""
Step 2: Transcribe the audio file

source .venv/bin/activate
uv add -r requirements.txt

python3 transcribe_audio.py sample.wav

"""
import sys
from pathlib import Path

from .schema import Segment, TranscriptionJsonResult

class TranscriptionError(Exception):
    """Raised when the fails to transcribe."""


def transcribe_segments(audio_file: Path) -> TranscriptionJsonResult:

    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise TranscriptionError(
            "Please install faster_whisper. uv -r requirements.txt"
        ) from e

    model = WhisperModel('tiny', device="cpu", compute_type='int8')

    try: 
        segs, info = model.transcribe(str(audio_file), vad_filter=True)

        chunks = []
        for seg in segs:
            chunks.append(
                Segment(
                    start= round(seg.start, 2),
                    end= round(seg.end, 2),
                    text= seg.text.strip(),
                )
            )

    except Exception as e:
        raise TranscriptionError(f"Failed on {audio_file.name}: {e}") from e


    results = TranscriptionJsonResult(
        file=audio_file.name,
        language=info.language,
        duration=round(info.duration, 2),
        segments=chunks,
    )
    
    return results


def transcribe_audio(audio_file: Path) -> str:

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Please install faster_whisper. uv -r requirements.txt")

    model  = WhisperModel("tiny", device="cpu", compute_type="int8")

    segments, info = model.transcribe(str(audio_file))

    # print(info)

    pieces = []
    for seg in segments:
        pieces.append(seg.text.strip())

    return " ".join(pieces)
