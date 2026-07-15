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
    LLMProcessingError,
    analyze_transcript
)

def main() -> int:
    parser = argparse.ArgumentParser("Audio transcription in Segments")
    parser.add_argument("sample", help="Audio file")
    parser.add_argument("--out", help="Output file")
    parser.add_argument("--analyze", action="store_true", help="Also run LLM analysis (needs OPENAI_API_KEY)")

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
    
    output = results.to_dict()
    if args.analyze:
        try:
            output["analysis"] = analyze_transcript(results)
        except LLMProcessingError as e:
            print(f"LLM analysis error: {e}", file=sys.stderr)
            return 4

    json_text = json.dumps(output, indent=2, ensure_ascii=False)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(json_text)
        print(f"Wrote {args.out}", file=sys.stderr)

    return 0




if __name__ == "__main__":
    sys.exit(main()) 
