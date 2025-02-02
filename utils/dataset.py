from typing import List, Optional

from utils.record import Record


class Dataset:
    def __init__(self, title: str, year: int):
        self._title = title
        self._year = year
        self._records: List[Record] = []

    def __len__(self):
        return len(self._records)

    def __iter__(self):
        return iter(self._records)

    def __str__(self):
        return f"<Dataset @ {hex(id(self))}> (title='{self._title}', year={self._year}, records={len(self)})"

    @property
    def title(self) -> str:
        return self._title

    @property
    def year(self) -> int:
        return self._year

    def add_record(self, record: Record):
        self._records.append(record)

    def get_record(self, country: str) -> Optional[Record]:
        return next(
            (record for record in self._records if record.code == country), None
        )

    def get_country_codes(self) -> List[str]:
        return [record.code for record in self._records]

    def remove_records_not_in(self, country_codes: set[str]):
        self._records = [
            record for record in self._records if record.code in country_codes
        ]

    def normalize(self):
        if not self._records:
            return  # Avoid division by zero if there are no records

        scores = [record.score for record in self._records]
        min_score, max_score = min(scores), max(scores)
        if min_score == max_score:
            return  # Avoid division by zero if all scores are the same

        for record in self._records:
            record.score = (record.score - min_score) / (max_score - min_score)
