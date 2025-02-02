from typing import List, Optional


class Country:
    def __init__(self, code: str):
        self._code = code
        self._scores: List[float] = []

    def __str__(self):
        return f"<Country @ {hex(id(self))}> (code='{self._code}', scores={len(self._scores)})"

    @property
    def code(self) -> str:
        return self._code

    def add_score(self, score: float):
        if score < 0:
            raise ValueError("Score cannot be negative")
        self._scores.append(score)

    def get_scores(self) -> List[float]:
        return self._scores

    def get_average_score(self) -> Optional[float]:
        if not self._scores:
            return None
        return sum(self._scores) / len(self._scores)
