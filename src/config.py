import os
from dataclasses import dataclass

@dataclass
class PipelineConfig:
    """Configuration for the ETL pipeline."""

    # Collection URL and ID for HDB resale flat data
    COLLECTION_ID: str = "189"
    COLLECTION_URL: str = "https://api-production.data.gov.sg/v2/public/api/collections/{}/metadata".format(COLLECTION_ID)

    # Dataset URL and ID for HDB resale flat data
    DATASET_ID: str = ""
    DATASET_URL: str = "https://data.gov.sg/api/action/datastore_search?resource_id="

    # Incremental extraction parameters
    OFFSET: int = 0
    LIMIT: int = 5000  # Maximum rows per request
    
    # HDB Lease Tenure
    HDB_LEASE_TENURE: int = 99

    # Date range
    START_DATE: str = "2012-01"
    END_DATE: str = "2016-12"

    # Output directory
    RAW_FOLDER: str = "./output/raw"
    CLEANED_FOLDER: str = "./output/cleaned"
    TRANSFORMED_FOLDER: str = "./output/transformed"
    FAILED_FOLDER: str = "./output/failed"
    HASHED_FOLDER: str = "./output/hashed"

    # Filename for the combined raw data
    RAW_COMBINED_FILENAME: str = "raw_all_dataset.csv"
    DATA_FILTERED_FILENAME: str = "filtered_all_data.csv"
    DATA_DEDUPLICATED_FILENAME: str = "deduplicated_all_data.csv"
    DATA_DUPLICATED_FILENAME: str = "duplicated_all_data.csv"
    DATA_HASHED_FILENAME: str = "hashed_all_data.csv"

config = PipelineConfig()