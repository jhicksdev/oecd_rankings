from typing import List


class Country:
    def __init__(self, name: str):
        self.name = name
        self.scores: List[float] = []

    def get_average_score(self):
        if not self.scores:
            return None
        return sum(self.scores) / len(self.scores)
