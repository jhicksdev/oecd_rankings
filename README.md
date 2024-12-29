# OECD Rankings

This project aims to provide a comprehensive analysis of OECD member countries based on various international rankings. By normalizing and comparing data from different sources, the project helps identify areas where countries excel and areas that need improvement. The results can be used by policymakers, researchers, and the general public to gain insights into the performance of OECD countries across different metrics.

For more information about the OECD, please visit the [Organisation for Economic Co-operation and Development (OECD) website](https://www.oecd.org/).

## Table of Contents

- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
  - [Human Development Index (HDI)](#human-development-index-hdi)
  - [World Happiness Report](#world-happiness-report)
  - [Global Peace Index](#global-peace-index)
  - [Corruption Perceptions Index](#corruption-perceptions-index)
  - [Data Coverage](#data-coverage)
- [Data Calculation](#data-calculation)
  - [Explanation](#explanation)
  - [Note](#note)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
  - [Fetch Country Data](#fetch-country-data)
  - [Convert Country Names to Codes](#convert-country-names-to-codes)
  - [Process OECD Results](#process-oecd-results)
  - [Command-Line Arguments](#command-line-arguments)
- [Example](#example)
- [Missing OECD Countries](#missing-oecd-countries)
- [Contributing](#contributing)
- [Contact](#contact)
- [License](#license)

## Project Structure

- `process_oecd_results.py`: Processes CSV files in the `data` directory, generates results for OECD member countries, and exports the results in JSON and/or CSV formats. It also identifies missing OECD member countries.
- `convert_country_names_to_codes.py`: Converts country names in uncoded CSV files to country codes using data from `countries.json`.
- `fetch_countries.py`: Fetches country data from an external API and merges it with existing data in `countries.json`.
- `country.py`: Defines the `Country` class used to manage country data and calculate average scores.
- `data/`: Directory containing CSV files with international rankings data.
- `results.json`: JSON file containing the processed results for OECD member countries.
- `results.csv`: CSV file containing the processed results for OECD member countries.
- `countries.json`: JSON file containing country codes and names.

## Data Sources

The data used in this project is sourced from the following reports:

### Human Development Index (HDI)

The HDI ranks countries based on life expectancy, education, and per capita income. It provides a measure of well-being and development beyond economic performance. For more information, visit the [UNDP HDI page](http://hdr.undp.org/en/content/human-development-index-hdi).

### World Happiness Report

This report ranks countries based on citizens' well-being and happiness, considering factors like GDP per capita, social support, and life expectancy. For more information, visit the [World Happiness Report website](https://worldhappiness.report/).

### Global Peace Index

The Global Peace Index ranks countries based on peace and stability, considering factors like conflicts, militarization, and societal safety. For more information, visit the [IEP Global Peace Index page](http://visionofhumanity.org/indexes/global-peace-index/).

### Corruption Perceptions Index

The Corruption Perceptions Index ranks countries based on perceived levels of public sector corruption. For more information, visit the [Transparency International CPI page](https://www.transparency.org/en/cpi).

### Data Coverage

The data used in this project covers the following years:

| Dataset                       | Year |
| ----------------------------- | ---- |
| Human Development Index (HDI) | 2022 |
| World Happiness Report        | 2024 |
| Global Peace Index            | 2024 |
| Corruption Perceptions Index  | 2023 |

## Data Calculation

The scores in the CSV files in the `data` directory have been normalized to values between 0 and 1. This normalization allows for a standardized comparison across different datasets. The normalization is done using the following formula:

```python
normalized_score = (original_score - worst_score) / (best_score - worst_score)
```

### Explanation

- `original_score`: The original score assigned to a country in the dataset.
- `worst_score`: The worst score observed in the dataset.
- `best_score`: The best score observed in the dataset.
- `normalized_score`: The score adjusted to a range between 0 and 1 for standardized comparison.

This process ensures that all scores are on a common scale, making it easier to compare different countries across various metrics such as human development, safety, happiness, etc.

### Note

The normalization process has been done manually using third-party software unrelated to this project. The normalized scores are then used in this project to generate the final rankings and results.

By using normalized scores, the project can provide a more accurate and fair comparison of how each OECD member country excels in different areas.

## Prerequisites

- Python 3.6 or higher
- Internet connection (for fetching country data)

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/jhicksdev/oecd_rankings.git
   cd oecd_rankings
   ```

2. Create a virtual environment and activate it:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Fetch Country Data

Fetch country data from an external API and merge it with existing data in `countries.json`:

```sh
./fetch_countries.py --minify
```

### Convert Country Names to Codes

Convert country names in uncoded CSV files to country codes using data from `countries.json`:

```sh
./convert_country_names_to_codes.py --input-dir data/uncoded --output-dir data
```

### Process OECD Results

Process CSV files in the `data` directory, generate results for OECD member countries, and export the results in JSON and/or CSV formats. It also identifies missing OECD member countries:

```sh
./process_oecd_results.py --format both
```

### Command-Line Arguments

- `fetch_countries.py`:

  - `--minify`: Minify the output JSON file.

- `convert_country_names_to_codes.py`:

  - `--input-dir`: Input directory containing uncoded CSV files (default: `data/uncoded`).
  - `--output-dir`: Output directory for coded CSV files (default: `data`).

- `process_oecd_results.py`:
  - `--input-dir`: Input directory containing CSV files (default: `data`).
  - `--output-file`: Output file for results.
  - `--format`: Output format (`json`, `csv`, or `both`).

## Example

To process the OECD results and export them in both JSON and CSV formats, run:

```sh
./process_oecd_results.py --format both
```

This will generate `results.json` and `results.csv` files in the root directory, and if any OECD member countries are missing from the results, a `MISSING_COUNTRIES.txt` file will be created listing those countries.

## Missing OECD Countries

The following OECD member countries were excluded from the results due to incomplete data:

- Luxembourg (LU)

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request. For major changes, please discuss them in an issue first to ensure they align with the project's goals.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## Contact

For questions or support, please contact Joseph Hicks at [jhicksdev@gmail.com](mailto:jhicksdev@gmail.com).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
