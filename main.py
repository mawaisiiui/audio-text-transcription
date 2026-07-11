"""
Step 1: Accept Audio file and validate, tramscribe

Run it with:
    python main.py audio_files/sample.wav --out output/sample.json
"""

import argparse
import json
import sys

from tools import (
    accept_audio_file,
    transcribe_segments,
    AudioValidationError,
    TranscriptionError,
)

def main():
    parser = argparse.ArgumentParser("Audio transcription in Segments")
    parser.add_argument("sample", help="Audio file")
    parser.add_argument("--out", help="Output file")

    args = parser.parse_args()

    try:
        audio_file = accept_audio_file(args.sample)
        results = transcribe_segments(audio_file)
    except AudioValidationError as e:
        print(f"Input Error {args.sample}: {e}", file=sys.stderr)
        return 2
    except TranscriptionError as e:
        print(f"Transcription error: {e}")
        return 3

    json_text = results.to_json()

    if args.out:
        out_file = args.out

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(json_text)
        print(f"Wrote {out_file}", file=sys.stderr)

    else:
        print(results)


if __name__ == "__main__":
    main()
    sys.exit(0)
