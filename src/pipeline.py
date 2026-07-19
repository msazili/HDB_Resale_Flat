import logging
import pandas as pd

from src.config import config

from src.extract import DataExtractor
from src.validation import DataValidator
from src.transform import DataTransformer


logger = logging.getLogger(__name__)


class HDBDataPipeline:

    def __init__(self):
        """Initialize pipeline components."""
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()


    def run(self):
        logger.info("Starting HDB Data Pipeline")
        results = {}

        try:
            # # Step 1: Extract
            logger.info("Step 1: Extracting data")
            self.extractor.extract_data()

            # Step 2: Validate
            raw_filename = f"{config.CLEANED_FOLDER}/{config.DATA_FILTERED_FILENAME}"
            df = pd.read_csv(raw_filename, sep=',', header=0, encoding='utf-8')

            logger.info("Step 2: Validating data")
            self.validator = DataValidator(df)
            self.validator.run_all_checks()

            # Step 3: Transform
            logger.info("Step 3: Transforming data")
            self.transformer.transform_data()

            logger.info("Pipeline completed successfully")
            return results

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise