

import json
from dataclasses import dataclass, asdict


@dataclass
class Segment: 
    start: float
    end: float
    text: str


@dataclass
class TranscriptionJsonResult: 
    file: str
    language: str
    duration: float
    segments: list[Segment]        

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)