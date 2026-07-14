# Audio Transcribe & LLM integration to summarize the text 

A modular transciption pipeline that validates the audio file, transcribe speech to text, also converts the speech into segments with duration and timestamps and output structured JSON 

Pipeline: validate audio -> transcribe (faster-whisper) -> JSON output -> optional LLM analysis

audio file (wav/mp3/m4a/flac/ogg) to text with timestamps per segment,


## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
uv add -r requirements.txt
```

For the `--analyze` step, set the API key for the LLM provider (Gemini is used by default):

```bash
export GEMINI_API_KEY="your-key-here"
```

OpenAI and Anthropic are also supported (see `tools/llm_processor.py`), using
`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`.

## Quick start

```bash
# transcription only, JSON to stdout
python main.py audio_files/english.mp3       

# write to a file
python main.py audio_files/sample.wav --out output/sample.json

# transcription + LLM analysis
python main.py audio_files/english.mp3 --analyze --out output/english.json
```


Exit codes: 2 = invalid input, 3 = transcription failed, 4 = LLM analysis failed.

## Project structure

```
main.py                    CLI entry point: argument parsing, exit codes, output
tools/
  audio_ingestion.py       input validation (exists, format allowlist, size limits)
  transcribe_audio.py      faster-whisper wrapper, builds timestamped segments
  schema.py                Segment / TranscriptionJsonResult dataclasses (output contract)
  llm_processor.py         LLM analysis step: prompt, JSON parsing, retry on bad output
```

- `audio_ingestion.py` rejects bad files before any compute is spent. Validation
  errors are never retried since a bad file stays bad.
- `transcribe_audio.py` runs Whisper (tiny model, CPU, int8) with `vad_filter=True`
  to skip silence. Whisper's objects are converted to our own Segment dataclass,
  so the rest of the code doesn't depend on the library's internal format.
- `schema.py` defines the JSON output shape. Everything downstream (files, the
  LLM step) depends on this schema, not on the STT engine.
- `llm_processor.py` asks the LLM for a fixed JSON shape at temperature 0,
  validates the reply, and on a parse failure retries once with the error and
  the previous reply fed back so the model can correct itself. The provider
  call is isolated in one function per provider, so switching providers is a
  one-line change.

## Sample output

```json
{
  "file": "english.mp3",
  "language": "en",
  "duration": 59.05,
  "segments": [
    {"start": 0.0, "end": 8.5, "text": "I believe in the power of words..."}
  ],
  "analysis": {
    "summary": "...",
    "action_items": [],
    "topics": ["..."],
    "language_quality": "clean"
  }
}
```

## Notes / possible improvements

- The Whisper model currently loads on each run. Behind a service (FastAPI) it
  would be loaded once per process and reused across requests.
- Long recordings: VAD filtering already skips silence; the next step would be
  chunking on silence boundaries and processing chunks in parallel.
- The extension check trusts the filename. For untrusted uploads I'd verify
  file signatures and normalize everything to 16kHz mono wav with ffmpeg first.
