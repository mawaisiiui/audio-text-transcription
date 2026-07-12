# Audio Transcribe & LLM integration to summarize the text 

A modular transciption pipeline that validates the audio file, transcribe speech to text, also converts the speech into segments with duration and timestamps and output structured JSON 


## Quick start

```bash
pip install faster-whisper
python main.py audio_files/english.mp3       
python main.py audio_files/english.mp3 --out result.json
python main.py audio_files/english.mp3 --analyze --out output/english.json
```


