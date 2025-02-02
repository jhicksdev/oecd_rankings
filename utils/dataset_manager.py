from csv import DictReader
from json import load
from typing import List, Optional, Set

from utils.dataset import Dataset
from utils.paths import CODES_JSON, DATA_CSV
from utils.record import Record


class DatasetManager:
    _instance: Optional["DatasetManager"] = None

    def __init__(self):
        self._datasets: List[Dataset] = []

    def __len__(self):
        return len(self._datasets)

    def __iter__(self):
        return iter(self._datasets)

    def __str__(self):
        return f"<DatasetManager @ {hex(id(self))}> (datasets={len(self)})"

    @staticmethod
    def get_instance() -> "DatasetManager":
        if DatasetManager._instance is None:
            DatasetManager._instance = DatasetManager()
        return DatasetManager._instance

    def add_dataset(self, dataset: Dataset):
        self._datasets.append(dataset)

    def get_dataset(self, title: str, year: int) -> Optional[Dataset]:
        for dataset in self._datasets:
            if dataset.title == title and dataset.year == year:
                return dataset
        return None

    def load(self):
        try:
            with CODES_JSON.open() as file:
                codes: List[str] = load(file)

            with DATA_CSV.open() as file:
                reader = DictReader(file)
                for row in reader:
                    dataset_title = row["dataset"]
                    dataset_year = int(row["year"])
                    country_code = row["country"]
                    score = float(row["normalized_score"])

                    if country_code not in codes:
                        continue

                    dataset = self.get_dataset(dataset_title, dataset_year)
                    if dataset is None:
                        dataset = Dataset(dataset_title, dataset_year)
                        self.add_dataset(dataset)

                    record = Record(country_code, score)
                    dataset.add_record(record)
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except KeyError as e:
            print(f"Error: Missing expected key in CSV file: {e}")
        except ValueError as e:
            print(f"Error: Invalid value in data: {e}")

    def synchronize(self):
        if not self._datasets:
            return

        # Find common countries across all datasets
        common_countries: Set[str] = set.intersection(  # type: ignore
            *[set(dataset.get_country_codes()) for dataset in self._datasets]
        )

        for dataset in self._datasets:
            dataset.remove_records_not_in(common_countries)

    def normalize(self):
        for dataset in self._datasets:
            dataset.normalize()
