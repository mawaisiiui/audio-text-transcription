import argparse
import json
import sys

from audio_ingestion import accept_audio_file


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

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Audio transcription in Segments")
    parser.add_argument("sample", help="Audio file")
    parser.add_argument("--out", help="Output file")

    args = parser.parse_args()

    audio_file = accept_audio_file(args.sample)
    results = transcribe_segments(audio_file)

    json_text = json.dumps(results, indent=2, ensure_ascii=False)

    if args.out:
        out_file = args.out

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(json_text)
        print(f"Wrote {out_file}", file=sys.stderr)

    else:
        print(results)




