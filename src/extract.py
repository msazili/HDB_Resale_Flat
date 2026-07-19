import logging
import requests
import pandas as pd

from src.config import config

logger = logging.getLogger(__name__)

class DataExtractor:
    """Class responsible for extracting data from the source."""

    def extract_data(self):
        """Extract data from the source."""
        logger.info(f"Extracting data from {config.COLLECTION_URL}")

        try:
            all_records = []

            coll_url = config.COLLECTION_URL

            response = requests.get(coll_url)

            coll_data = response.json()

            childDatasets = coll_data['data']['collectionMetadata']['childDatasets']

            for dataset_id in childDatasets:

                dataset_records = []
    
                counter = 0
                count_total = 0
                
                offset = config.OFFSET
                limit = config.LIMIT

                while True:
                    config.DATASET_ID = dataset_id
                    dataset_url = f"{config.DATASET_URL}{config.DATASET_ID}&limit={limit}&offset={offset}"

                    dataset_output = requests.get(dataset_url)
                    dataset_data = dataset_output.json()

                    # Extract records from the response
                    if 'result' in dataset_data and 'records' in dataset_data['result']:
                        records = dataset_data['result']['records']
                        
                        # Add dataset_id using list comprehension
                        records = [{**record, 'dataset_id': config.DATASET_ID} for record in records]

                        total = dataset_data['result'].get('total', 0)

                        counter += 1
                        count_total += len(records)

                        if not records:  # No more records, exit loop
                            break

                        print(f"{counter} - Dataset: {config.DATASET_ID} - Count records: {len(records)} = {count_total} - Total records: {total}")

                        dataset_records.extend(records)
                        offset += limit  # Move to the next page

                    else:
                        print("No records found in the response")

                df_dataset = pd.DataFrame(dataset_records)
                filename = f"{config.RAW_FOLDER}/raw_{config.DATASET_ID}.csv"
                df_dataset.to_csv(filename, index=False)

                print(f"\nCSV file {filename} = {len(dataset_records)} saved successfully!\n")

                all_records.extend(dataset_records)


            # Combine all records into a single DataFrame and save to CSV
            df_all = pd.DataFrame(all_records)
            filename = f"{config.RAW_FOLDER}/{config.RAW_COMBINED_FILENAME}"
            df_all.to_csv(filename, index=False)
            print(f"CSV file {filename} = {len(all_records)} saved successfully!")

        except requests.RequestException as e:
            logger.error(f"Error during data extraction: {e}")
            raise

