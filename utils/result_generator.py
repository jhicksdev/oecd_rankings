from csv import DictWriter
from datetime import datetime
from json import dump
from logging import error, info
from typing import Dict, List

from matplotlib import pyplot as plt

from utils.country_manager import CountryManager
from utils.paths import RESULTS_CSV, RESULTS_JSON, RESULTS_PNG


class ResultGenerator:
    def __init__(self, country_manager: CountryManager):
        self.country_manager = country_manager

    def generate(self) -> None:
        info("Starting result generation process.")

        results: List[Dict[str, float]] = [
            {
                "name": country.name,
                "score": round(country.get_average_score() or 0.0, 3),
            }
            for country in self.country_manager.countries
        ]  # type: ignore
        results.sort(key=lambda x: x["score"], reverse=True)

        try:
            with open(RESULTS_CSV, "w") as file:
                writer = DictWriter(file, fieldnames=["name", "score"])
                writer.writeheader()
                writer.writerows(results)
            info(f"Successfully written results to file: {RESULTS_CSV}")

            with open(RESULTS_JSON, "w") as file:
                dump(results, file, indent=2)
            info(f"Successfully written results to file: {RESULTS_JSON}")

            names = [result["name"] for result in results]
            names.reverse()

            scores = [result["score"] for result in results]
            scores.reverse()

            _, ax = plt.subplots(
                figsize=(8, 16),
            )

            ax.barh(names, scores, 0.8)

            ax.set_xlabel("Score")
            ax.set_ylabel("Country")
            ax.set_title(f"Date: {datetime.now().strftime('%Y-%m-%d')}")

            plt.savefig(RESULTS_PNG, dpi=72, bbox_inches="tight")
            info(f"Successfully written results to file: {RESULTS_PNG}")
        except Exception as e:
            error(f"Failed to write results to file: {e}")

        info("Result generation process completed.")
