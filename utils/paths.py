from pathlib import Path

# /
ROOT_DIR = Path(__file__).resolve().parent.parent

# /countries.json
COUNTRIES_JSON = ROOT_DIR / "countries.json"

# /data.csv
DATA_CSV = ROOT_DIR / "data.csv"

# /results.csv
RESULTS_CSV = ROOT_DIR / "results.csv"

# /results.json
RESULTS_JSON = ROOT_DIR / "results.json"

# /assets
ASSETS_DIR = ROOT_DIR / "assets"

# /assets/results.png
RESULTS_PNG = ASSETS_DIR / "results.png"
