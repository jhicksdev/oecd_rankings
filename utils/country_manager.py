from typing import List

from utils.country import Country
from utils.dataset_manager import DatasetManager


class CountryManager:
    def __init__(self):
        self.countries: List[Country] = []

    def get_country(self, name: str):
        for country in self.countries:
            if country.name == name:
                return country

    def load(self, dataset_manager: DatasetManager) -> None:
        for dataset in dataset_manager.datasets:
            for record in dataset.records:
                country = self.get_country(record.name)
                if country is None:
                    country = Country(record.name)
                    self.countries.append(country)
                country.scores.append(record.normalized_score)

        self.countries = [
            country for country in self.countries if len(country.scores) > 0
        ]
