from typing import List, Set

from utils.record import Record


class Dataset:
    def __init__(self, title: str, year: int):
        self.title = title
        self.year = year
        self.records: List[Record] = []

    def get_record(self, name: str):
        for record in self.records:
            if record.name == name:
                return record

    def get_names(self) -> List[str]:
        return [record.name for record in self.records]

    def remove_records_not_in(self, names: Set[str]) -> None:
        self.records = [record for record in self.records if record.name in names]

    def normalize(self) -> None:
        if not self.records:
            return

        scores = [record.score for record in self.records]
        best_score, worst_score = (
            (min(scores), max(scores))
            if self.title in ["Global Peace Index", "Global Terrorism Index"]
            else (max(scores), min(scores))
        )
        if best_score == worst_score:
            return

        for record in self.records:
            record.normalized_score = max(
                [0.0, (record.score - worst_score) / (best_score - worst_score)]
            )
