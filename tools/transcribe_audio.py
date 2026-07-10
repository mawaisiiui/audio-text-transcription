

"""
Step 2: Transcribe the audio file

source .venv/bin/activate
uv add -r requirements.txt

python3 transcribe_audio.py sample.wav

"""
import sys


class TranscriptionError(Exception):
    """Raised when the fails to transcribe."""


def transcribe_segments(audio_file):

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Please install faster_whisper uv pip install faster-whisper")

    model = WhisperModel('tiny', device="cpu", compute_type='int8')

    segments, info = model.transcribe(str(audio_file))

    chunks = []
    for seg in segments:
        chunks.append({
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip(),
        })

    results = {
        "file": str(audio_file),
        "segments": chunks,
        "info": info.language,
        "duration": info.duration,
    }

    return results


def transcribe_audio(audio_file):

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
