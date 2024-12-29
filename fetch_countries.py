#!/usr/bin/env python3

import argparse
from json import dump, load
from os.path import abspath, dirname, exists
from pathlib import Path
from requests import get, RequestException
from typing import List, TypedDict, Dict
import logging

ROOT_PATH = Path(dirname(abspath(__file__)))
COUNTRIES_PATH = ROOT_PATH / "countries.json"
COUNTRIES_API_URL = "https://restcountries.com/v3.1/all"
FIELDS = "fields=name,cca2"


class Country(TypedDict):
    code: str
    names: List[str]


def fetch_countries(url: str, fields: str) -> List[Country]:
    try:
        response = get(f"{url}?{fields}")
        response.raise_for_status()
        countries_data = response.json()
        return sorted(
            [
                Country(code=country["cca2"], names=[country["name"]["common"]])
                for country in countries_data
            ],
            key=lambda country: country["code"],
        )
    except RequestException as e:
        logging.error(f"Error fetching countries data: {e}")
        return []


def load_existing_countries(file_path: Path) -> Dict[str, Country]:
    if exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                existing_countries = load(file)
                return {country["code"]: country for country in existing_countries}
        except IOError as e:
            logging.error(f"Error reading from file {file_path}: {e}")
    return {}


def merge_countries(
    existing: Dict[str, Country], fetched: List[Country]
) -> List[Country]:
    for country in fetched:
        if country["code"] in existing:
            existing[country["code"]]["names"].extend(
                name
                for name in country["names"]
                if name not in existing[country["code"]]["names"]
            )
            existing[country["code"]]["names"].sort()
        else:
            existing[country["code"]] = country
    return sorted(existing.values(), key=lambda country: country["code"])


def save_countries_to_file(
    countries: List[Country], file_path: Path, minify: bool
) -> None:
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            if minify:
                dump(countries, file, separators=(",", ":"), ensure_ascii=False)
            else:
                dump(countries, file, indent=2, ensure_ascii=False)
    except IOError as e:
        logging.error(f"Error writing to file {file_path}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch and save country data.")
    parser.add_argument(
        "--minify", action="store_true", help="Minify the output JSON file"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    existing_countries = load_existing_countries(COUNTRIES_PATH)
    fetched_countries = fetch_countries(COUNTRIES_API_URL, FIELDS)
    if fetched_countries:
        merged_countries = merge_countries(existing_countries, fetched_countries)
        save_countries_to_file(merged_countries, COUNTRIES_PATH, args.minify)
        logging.info(f"Countries data saved to {COUNTRIES_PATH}")


if __name__ == "__main__":
    main()
