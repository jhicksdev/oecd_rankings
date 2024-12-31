from __future__ import annotations
from typing import List, Optional, TypedDict


class Result(TypedDict):
    code: str
    rank: int
    score: float


class Country:
    __instances: List[Country] = []

    def __init__(self, code: str):
        self.__code = code
        self.__scores: List[float] = []

    @staticmethod
    def create(code: str) -> Country:
        country = Country(code)
        Country.__instances.append(country)
        return country

    @staticmethod
    def get(code: str) -> Optional[Country]:
        for country in Country.__instances:
            if country.code == code:
                return country
        return None

    @staticmethod
    def get_all() -> List[Country]:
        return Country.__instances

    @staticmethod
    def get_results() -> List[Result]:
        return [country.to_json() for country in Country.get_all()]

    @property
    def code(self) -> str:
        return self.__code

    @property
    def scores(self) -> List[float]:
        return self.__scores

    def add_score(self, score: float):
        self.__scores.append(score)

    def get_average_score(self) -> float:
        return sum(self.__scores) / len(self.__scores) if self.__scores else 0.0

    def to_json(self) -> Result:
        return {
            "code": self.__code,
            "rank": 0,
            "score": self.get_average_score(),
        }
