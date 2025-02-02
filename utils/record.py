from dataclasses import dataclass


@dataclass
class Record:
    code: str
    _score: float  # Private attribute for internal storage

    def __str__(self):
        return f"<Record @ {hex(id(self))}> (country='{self.code}', score={self.score})"

    @property
    def score(self) -> float:
        return self._score

    @score.setter
    def score(self, value: float):
        self._score = value
