import logging

from src.config import config
from src.extract import DataExtractor
from src.validation import DataValidator
from src.transform import DataTransformer


logger = logging.getLogger(__name__)


class HDBDataPipeline:

    def __init__(self):
        """Initialize pipeline components."""
        self.extractor = DataExtractor()
        self.validator = DataValidator()
        self.transformer = DataTransformer()


    def run(self):
        logger.info("Starting HDB Data Pipeline")
        results = {}

        try:
            # # Step 1: Extract
            # logger.info("Step 1: Extracting data")
            # self.extractor.extract_data()

            # Step 2: Validate
            logger.info("Step 2: Validating data")
            self.validator.run_all_checks()

            # Step 3: Transform
            logger.info("Step 3: Transforming data")
            self.transformer.transform_data()

            # if not downloaded_files:
            #     raise ValueError("No files downloaded")

            # raw_df = DataExtractor.combine_raw_data(downloaded_files)
            # results["raw_count"] = len(raw_df)

            logger.info("Pipeline completed successfully")
            return results

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise