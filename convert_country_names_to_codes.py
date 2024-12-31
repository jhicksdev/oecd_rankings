#!/usr/bin/env python3

import argparse
from csv import DictReader, DictWriter
from json import load
from os import listdir
from os.path import abspath, dirname, exists
from pathlib import Path
from typing import List, TypedDict
import logging

ROOT_PATH = Path(dirname(abspath(__file__)))
DATA_PATH = ROOT_PATH / "data"
UNCODED_PATH = DATA_PATH / "uncoded"
COUNTRIES_PATH = ROOT_PATH / "countries.json"


class Country(TypedDict):
    code: str
    names: List[str]


def load_countries(file_path: Path) -> List[Country]:
    if exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return load(file)
        except IOError as e:
            logging.error(f"Error reading from file {file_path}: {e}")
    return []


def get_country_code(name: str, countries: List[Country]) -> str | None:
    for country in countries:
        if name in country["names"]:
            return country["code"]
    return None


def convert_file(input_file: Path, output_file: Path, countries: List[Country]) -> None:
    try:
        with open(input_file, "r", encoding="utf-8") as uncoded_file:
            reader = DictReader(uncoded_file)
            rows = list(reader)
            for row in rows:
                name = row["COUNTRY"]
                code = get_country_code(name, countries)
                if code:
                    row["COUNTRY"] = code
                logging.info(f"Converted {name} to {code}")
            with open(output_file, "w", encoding="utf-8") as coded_file:
                fieldnames = reader.fieldnames
                if fieldnames:
                    writer = DictWriter(coded_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
    except IOError as e:
        logging.error(f"Error processing file {input_file}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert country names to codes in CSV files."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=UNCODED_PATH,
        help="Input directory containing uncoded CSV files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DATA_PATH,
        help="Output directory for coded CSV files",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    countries = load_countries(COUNTRIES_PATH)
    if not countries:
        logging.error(f"No countries data found in {COUNTRIES_PATH}")
        return

    for filename in listdir(Path(args.input_dir)):
        if filename.endswith("_UNCODED.csv"):
            input_file = Path(args.input_dir) / filename
            output_file = Path(args.output_dir) / filename.replace("_UNCODED", "")
            convert_file(input_file, output_file, countries)
            logging.info(f"Processed file {input_file}")


if __name__ == "__main__":
    main()
