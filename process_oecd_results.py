#!/usr/bin/env python3

import argparse
import logging
from csv import DictReader
from json import dump
from os import listdir
from os.path import abspath, dirname
from pathlib import Path
from typing import TypedDict

from country import Country, Result

ROOT_PATH = Path(dirname(abspath(__file__)))
DATA_PATH = ROOT_PATH / "data"
OECD_ANALYSIS_PATH = ROOT_PATH / "oecd_analysis.json"

# List of OECD member country codes
OECD_COUNTRIES = {
    "AT",
    "AU",
    "BE",
    "CA",
    "CH",
    "CL",
    "CO",
    "CR",
    "CZ",
    "DE",
    "DK",
    "EE",
    "ES",
    "FI",
    "FR",
    "GB",
    "GR",
    "HU",
    "IE",
    "IL",
    "IS",
    "IT",
    "JP",
    "KR",
    "LT",
    "LU",
    "LV",
    "MX",
    "NL",
    "NO",
    "NZ",
    "PL",
    "PT",
    "SE",
    "SI",
    "SK",
    "TR",
    "US",
}


class OutputData(TypedDict):
    results: list[Result]
    excluded: list[str]


def process_csv_files(input_dir: Path) -> int:
    file_count = 0
    for filename in listdir(input_dir):
        if filename.endswith(".csv") and not filename.endswith("_UNCODED.csv"):
            file_count += 1
            input_file = input_dir / filename
            try:
                with open(input_file, "r", encoding="utf-8") as file:
                    reader = DictReader(file)
                    for row in reader:
                        code = row["COUNTRY"]
                        score = float(row["SCORE"])
                        country = Country.get(code)
                        if country is None:
                            country = Country.create(code)
                        country.add_score(score)
            except IOError as e:
                logging.error(f"Error processing file {input_file}: {e}")
    return file_count


def save_results_as_json(output_file: Path, required_score_count: int):
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            results = sorted(
                [
                    country.to_json()
                    for country in Country.get_all()
                    if len(country.scores) == required_score_count
                    and country.code in OECD_COUNTRIES
                ],
                key=lambda x: round(x["score"], 3),
                reverse=True,
            )
            rank = 1
            for i, result in enumerate(results):
                if i > 0 and round(results[i - 1]["score"], 3) != round(
                    result["score"], 3
                ):
                    rank = i + 1
                result["score"] = round(result["score"], 3)
                result["rank"] = rank

            excluded_countries = [
                country.code
                for country in Country.get_all()
                if country.code in OECD_COUNTRIES
                and len(country.scores) != required_score_count
            ]

            output_data: OutputData = {
                "results": results,
                "excluded": excluded_countries,
            }

            dump(output_data, file, indent=2)
    except IOError as e:
        logging.error(f"Error writing to file {output_file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Process CSV files and generate results."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DATA_PATH,
        help="Input directory containing CSV files",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        help="Output file for results",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    file_count = process_csv_files(args.input_dir)

    output_file = Path(args.output_file) if args.output_file else OECD_ANALYSIS_PATH
    save_results_as_json(output_file, file_count)
    logging.info(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()
