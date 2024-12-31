#!/bin/bash

# Fetch country data and minify the output JSON file
./fetch_countries.py --minify

# Convert country names to codes in CSV files
./convert_country_names_to_codes.py

# Process OECD results and export them in JSON format
./process_oecd_results.py