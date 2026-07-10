

"""
Step 2: Transcribe the audio file

source .venv/bin/activate
uv add -r requirements.txt

python3 transcribe_audio.py sample.wav

"""
import sys
from audio_ingestion import accept_audio_file

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

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("Usage: python audio_ingestion.py sample.wav")

    audio_path = accept_audio_file(sys.argv[1])

    text = transcribe_audio(audio_path)

    print("Transcribing audio file...")
    print(text)