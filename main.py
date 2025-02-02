import logging

from utils.country_manager import CountryManager
from utils.dataset_manager import DatasetManager
from utils.paths import RESULTS_JSON

# Configure logging
logging.basicConfig(level=logging.INFO)

try:
    # Initialize dataset manager and process data
    dataset_manager = DatasetManager.get_instance()
    dataset_manager.load()
    dataset_manager.synchronize()
    dataset_manager.normalize()
    logging.info("Dataset processing completed successfully.")
except Exception as e:
    logging.error(f"Error processing datasets: {e}")

try:
    # Initialize country manager and process data
    country_manager = CountryManager.get_instance()
    country_manager.load()
    logging.info("Country processing completed successfully.")
    country_manager.save(RESULTS_JSON)
    logging.info(f"Results saved successfully to file: {RESULTS_JSON}")
except Exception as e:
    logging.error(f"Error processing countries: {e}")
