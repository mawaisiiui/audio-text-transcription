"""LLM step: transcript -> structured insights (summary, action items, topics)."""

import json
import os
import re

class LLMProcessingError(Exception):
    """Raised when the LLM step fails after retries."""


PROMPT_TEMPLATE = """\
You are an assistant that analyzes audio transcripts.

Analyze the transcript below and respond with ONLY a JSON object,
no markdown fences, no explanations, in exactly this shape:

{{
  "summary": "2-3 sentence summary",
  "action_items": ["task 1", "task 2"],
  "topics": ["topic 1", "topic 2"],
  "language_quality": "clean" or "noisy"
}}

Rules:
- "action_items": concrete tasks; empty list if none.
- "topics": 1-5 short noun phrases.
- "language_quality": "noisy" if the transcript looks garbled.

Transcript:
\"\"\"
{transcript}
\"\"\"
"""

REQUIRED_KEYS = {"summary", "action_items", "topics", "language_quality"}

def _call_llm_anthropic(prompt: str) -> str:
    """The ONLY function that knows which LLM provider we use."""
    try:
        from anthropic import Anthropic
    except ImportError as e:
        raise LLMProcessingError("Run: uv add anthropic") from e

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise LLMProcessingError("ANTHROPIC_API_KEY is not set")

    client = Anthropic()          # reads ANTHROPIC_API_KEY from the environment
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",   # fast + cheap: right for extraction
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text

def _call_llm_gemini(prompt: str) -> str:
    """The ONLY function that knows which LLM provider we use."""
    try:
        from openai import OpenAI
    except ImportError as e:
        raise LLMProcessingError("Run: uv add openai") from e

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise LLMProcessingError("GEMINI_API_KEY is not set")

    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite",     # the fast/cheap tier - right for extraction
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=500,
    )
    return response.choices[0].message.content

def _call_llm(prompt: str) -> str:
    """The ONLY function that knows which LLM provider we use."""
    try:
        from openai import OpenAI
    except ImportError as e:
        raise LLMProcessingError("Run: uv add openai") from e

    if not os.environ.get("OPENAI_API_KEY"):
        raise LLMProcessingError("OPENAI_API_KEY is not set")

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=500,
    )
    return response.choices[0].message.content


def _parse_json_reply(raw: str) -> dict:
    """Parse and VALIDATE the model's reply. Raises ValueError if bad."""
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
    data = json.loads(text)
    missing = REQUIRED_KEYS - set(data)
    if missing:
        raise ValueError(f"missing keys: {sorted(missing)}")
    return data


def analyze_transcript(results, max_retries: int = 1) -> dict:
    """Takes your TranscriptionJsonResult, returns the analysis dict."""
    transcript = " ".join(s.text for s in results.segments)
    
    if not transcript.strip():
        return {"summary": "No speech detected.", "action_items": [],
                "topics": [], "language_quality": "clean"}

    prompt = PROMPT_TEMPLATE.format(transcript=transcript)
    last_error = None

    for attempt in range(1 + max_retries):
        raw = _call_llm_gemini(prompt)

        try:
            return _parse_json_reply(raw)
        except ValueError as e:
            last_error = e
            prompt = (f"Your previous reply could not be parsed.\n"
                      f"Error: {e}\nPrevious reply:\n{raw}\n\n"
                      f"Respond again with ONLY the corrected JSON object.")
    raise LLMProcessingError(f"Invalid JSON after retries: {last_error}")