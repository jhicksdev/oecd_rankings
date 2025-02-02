from dataclasses import dataclass


@dataclass
class Record:
    code: str
    score: float
    _normalized_score: float = 0.0

    def __str__(self):
        return f"<Record @ {hex(id(self))}> (country='{self.code}', score={self.score}, normalized_score={self._normalized_score})"

    @property
    def normalized_score(self) -> float:
        return self._normalized_score

    @normalized_score.setter
    def normalized_score(self, value: float):
        self._normalized_score = value
