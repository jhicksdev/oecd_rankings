from logging import INFO, basicConfig, error, info

from utils.country_manager import CountryManager
from utils.dataset_manager import DatasetManager
from utils.result_generator import ResultGenerator

basicConfig(level=INFO)

dataset_manager = DatasetManager()
country_manager = CountryManager()
result_generator = ResultGenerator(country_manager)

try:
    dataset_manager.load()
    dataset_manager.synchronize()
    dataset_manager.normalize()
    info("Dataset processing completed successfully.")
except Exception as e:
    error(f"Error processing datasets: {e}")

try:
    country_manager.load(dataset_manager)
    info("Country processing completed successfully.")
except Exception as e:
    error(f"Error processing countries: {e}")

try:
    result_generator.generate()
    info("Results generated successfully.")
except Exception as e:
    error(f"Error generating results: {e}")
