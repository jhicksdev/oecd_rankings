from dataclasses import dataclass


@dataclass
class Record:
    name: str
    score: float
    normalized_score: float = 0.0
