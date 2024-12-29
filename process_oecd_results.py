#!/usr/bin/env python3

import argparse
import logging
from csv import DictReader, DictWriter
from json import dump
from os import listdir
from os.path import abspath, dirname
from pathlib import Path

from country import Country

ROOT_PATH = Path(dirname(abspath(__file__)))
DATA_PATH = ROOT_PATH / "data"
RESULTS_PATH_JSON = ROOT_PATH / "results.json"
RESULTS_PATH_CSV = ROOT_PATH / "results.csv"
MISSING_COUNTRIES_PATH = ROOT_PATH / "MISSING_COUNTRIES.txt"

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
                key=lambda x: x["score"],
                reverse=True,
            )
            dump(results, file, indent=2)
    except IOError as e:
        logging.error(f"Error writing to file {output_file}: {e}")


def save_results_as_csv(output_file: Path, required_score_count: int):
    try:
        with open(output_file, "w", encoding="utf-8", newline="") as file:
            fieldnames = ["country", "score"]
            writer = DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            results = sorted(
                [
                    country.to_json()
                    for country in Country.get_all()
                    if len(country.scores) == required_score_count
                    and country.code in OECD_COUNTRIES
                ],
                key=lambda x: x["score"],
                reverse=True,
            )
            for result in results:
                writer.writerow(result)
    except IOError as e:
        logging.error(f"Error writing to file {output_file}: {e}")


def save_missing_countries(required_score_count: int):
    missing_countries = [
        country.code
        for country in Country.get_all()
        if country.code in OECD_COUNTRIES
        and len(country.scores) != required_score_count
    ]
    if missing_countries:
        try:
            with open(MISSING_COUNTRIES_PATH, "w", encoding="utf-8") as file:
                for country_code in missing_countries:
                    file.write(f"{country_code}\n")
        except IOError as e:
            logging.error(f"Error writing to file {MISSING_COUNTRIES_PATH}: {e}")


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
        type=Path,
        help="Output file for results",
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv", "both"],
        default="json",
        help="Output format (json, csv, or both)",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    file_count = process_csv_files(args.input_dir)

    if args.format in ["json", "both"]:
        output_file = args.output_file or RESULTS_PATH_JSON
        save_results_as_json(output_file, file_count)
        logging.info(f"Results saved to {output_file}")

    if args.format in ["csv", "both"]:
        output_file = args.output_file or RESULTS_PATH_CSV
        save_results_as_csv(output_file, file_count)
        logging.info(f"Results saved to {output_file}")

    save_missing_countries(file_count)


if __name__ == "__main__":
    main()
