from csv import DictReader
from typing import List, Set

from utils.dataset import Dataset
from utils.paths import DATA_CSV
from utils.record import Record


class DatasetManager:
    def __init__(self):
        self.datasets: List[Dataset] = []

    def get_dataset(self, title: str, year: int):
        for dataset in self.datasets:
            if dataset.title == title and dataset.year == year:
                return dataset

    def load(self) -> None:
        try:
            with DATA_CSV.open() as file:
                reader = DictReader(file)
                for row in reader:
                    title = row["dataset"]
                    year = int(row["year"])
                    name = row["name"]
                    score = float(row["score"])

                    dataset = self.get_dataset(title, year)
                    if dataset is None:
                        dataset = Dataset(title, year)
                        self.datasets.append(dataset)

                    record = Record(name, score)
                    dataset.records.append(record)
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except KeyError as e:
            print(f"Error: Missing expected key in CSV file: {e}")
        except ValueError as e:
            print(f"Error: Invalid value in data: {e}")

    def synchronize(self) -> None:
        if not self.datasets:
            return

        common_countries: Set[str] = set.intersection(  # type: ignore
            *[set(dataset.get_names()) for dataset in self.datasets]
        )

        for dataset in self.datasets:
            dataset.remove_records_not_in(common_countries)

    def normalize(self) -> None:
        for dataset in self.datasets:
            dataset.normalize()
