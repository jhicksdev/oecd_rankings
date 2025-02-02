from json import dump
from pathlib import Path
from typing import List, Optional

from utils.country import Country
from utils.dataset_manager import DatasetManager


class CountryManager:
    _instance: Optional["CountryManager"] = None

    def __init__(self):
        self._countries: List[Country] = []

    def __len__(self):
        return len(self._countries)

    def __iter__(self):
        return iter(self._countries)

    def __str__(self):
        return f"<CountryManager @ {hex(id(self))}> (countries={len(self)})"

    @staticmethod
    def get_instance() -> "CountryManager":
        if CountryManager._instance is None:
            CountryManager._instance = CountryManager()
        return CountryManager._instance

    def add_country(self, country: Country):
        self._countries.append(country)

    def get_country(self, code: str) -> Optional[Country]:
        for country in self._countries:
            if country.code == code:
                return country
        return None

    def load(self):
        dataset_manager = DatasetManager.get_instance()
        for dataset in dataset_manager:
            for record in dataset:
                country = self.get_country(record.code)
                if country is None:
                    country = Country(record.code)
                    self.add_country(country)
                country.add_score(record.normalized_score)

        self._countries = [
            country for country in self._countries if len(country.get_scores()) > 0
        ]

    def save(self, file_path: Path):
        with file_path.open("w") as file:
            # Sort countries by score
            results = [  # type: ignore
                {
                    "code": country.code,
                    "rank": 0,  # Placeholder rank
                    "score": round(country.get_average_score() or 0.0, 3),
                }
                for country in self._countries
            ]
            results.sort(key=lambda x: x["score"], reverse=True)  # type: ignore

            # Assign ranks
            previous_score = None
            for index, result in enumerate(results):  # type: ignore
                if result["score"] != previous_score:
                    result["rank"] = index + 1
                else:
                    result["rank"] = results[index - 1]["rank"]
                previous_score = result["score"]  # type: ignore

            dump(results, file, separators=(",", ":"))
