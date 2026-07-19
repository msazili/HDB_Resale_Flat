import logging
import requests
import pandas as pd

from src.config import config
from src.utils import PipelineUtils

logger = logging.getLogger(__name__)
utils = PipelineUtils()

class DataTransformer:
    """Class responsible for transforming data from the source."""


    def filter_data(self):
        # Filter dataset from Jan 2012 to Dec 2016
    
        raw_filename = f"{config.RAW_FOLDER}/{config.RAW_COMBINED_FILENAME}"

        df = pd.read_csv(raw_filename, sep=',', header=0, encoding='utf-8')

        print(f"Get Raw CSV file {raw_filename} = {len(df)} successfully!")        

        start_date = pd.to_datetime(f"{config.START_DATE}", format='%Y-%m')
        end_date = pd.to_datetime(f"{config.END_DATE}", format='%Y-%m')

        data_month = pd.to_datetime(df['month'], format='%Y-%m')

        # Step 1: Filter the DataFrame based on the date range
        filtered_df = df[(data_month >= start_date) & (data_month <= end_date)]

        print(f"\nStep 1: Filtered data between {config.START_DATE} and {config.END_DATE}:")

        # Step 2: Update the remaining_lease column
        filtered_df['remaining_lease'] = filtered_df['lease_commence_date'].apply(utils.calculate_remaining_lease)

        print(f"\nStep 2: Calculate remaining lease")

        # Step 3: Calculate Average Resale Price group by month, town, and flat_type
        filtered_df['avg_resale_price'] = filtered_df.groupby(['month', 'town', 'flat_type'])['resale_price'].transform('mean')
        filtered_df['avg_resale_price'] = filtered_df['avg_resale_price'].round(2)

        print(f"\nStep 3: Calculate average resale prices")

        # print(filtered_df)

        # Store the filtered data to a new CSV file
        filtered_filename = f"{config.CLEANED_FOLDER}/{config.DATA_FILTERED_FILENAME}"
        filtered_df.to_csv(filtered_filename, index=False)

        print(f"CSV file {filtered_filename} = {len(filtered_df)} saved successfully!")        
        

    def remove_duplicates(self):
        # Remove duplicates based on specific columns
        filtered_filename = f"{config.CLEANED_FOLDER}/{config.DATA_FILTERED_FILENAME}"
        df = pd.read_csv(filtered_filename, sep=',', header=0, encoding='utf-8')

        print(f"Get Filtered CSV file {filtered_filename} = {len(df)} successfully!")        

        # Define columns to check for duplicates (exclude _id and resale_price)
        duplicate_columns = [col for col in df.columns if col not in ['_id', 'resale_price']]

        # Step 1: Remove duplicates keeping highest price
        df_cleaned = (
            df
            .sort_values('resale_price', ascending=False)
            .drop_duplicates(
                subset=duplicate_columns, 
                keep='first'
            ).sort_values('_id')
        )

        print(f"\nStep 1: Remove duplicates keeping highest price")

        # Step 2: Get the duplicated records
        df_anti_join = df.merge(df_cleaned, on=list(df.columns), how='left', indicator=True)
        df_anti_join = df_anti_join[df_anti_join['_merge'] == 'left_only'].drop('_merge', axis=1)

        print(f"\nStep 2: Get the duplicated records")

        # Step 3: Remove _id and dataset_id columns
        df_cleaned.drop(['_id', 'dataset_id'], axis=1, inplace=True)
        df_anti_join.drop(['_id', 'dataset_id'], axis=1, inplace=True)

        print(f"\nStep 3: Remove _id and dataset_id columns")

        # Step 4: Store the cleaned data to a new CSV file
        filename = f"{config.CLEANED_FOLDER}/{config.DATA_DEDUPLICATED_FILENAME}"
        df_cleaned.to_csv(filename, index=False)

        print(f"Step 4: Cleaned Data store to CSV file {filename} = {len(df_cleaned)} saved successfully!")        

        print(f"Original: {len(df)} records")
        print(f"Cleaned: {len(df_cleaned)} records")
        print(f"Removed: {len(df) - len(df_cleaned)} duplicates")

        # Step 5: Store the duplicated records to a new CSV file
        failed_filename = f"{config.FAILED_FOLDER}/{config.DATA_DUPLICATED_FILENAME}"
        df_anti_join.to_csv(failed_filename, index=False)

        print(f"Step 5: Duplicated Data store to CSV file {failed_filename} = {len(df_anti_join)} saved successfully!")        


    def generate_hashed_identifiers(self):
        # Generate hashed identifiers for the cleaned data
        filtered_filename = f"{config.CLEANED_FOLDER}/{config.DATA_DEDUPLICATED_FILENAME}"
        df = pd.read_csv(filtered_filename, sep=',', header=0, encoding='utf-8')

        print(f"Get Cleaned Data CSV file {filtered_filename} = {len(df)} successfully!")        

        # Step 1: Add column Resale Identifier to the cleaned data
        df['resale_identifier'] = df.apply(utils.create_identifier, axis=1)

        print(f"\nStep 1: Add column Resale Identifier to the cleaned data")

        # Step 2: Apply hashing to column resale_identifier
        df['hashed_identifier'] = df['resale_identifier'].apply(utils.hash_identifier)

        print(f"\nStep 2: Apply hashing to column resale_identifier")

        # Step 3: Store the data with hashed identifiers to a new CSV file
        hashed_filename = f"{config.HASHED_FOLDER}/{config.DATA_HASHED_FILENAME}"
        df.to_csv(hashed_filename, index=False)

        print(f"Step 3: Data with Hashed Identifiers stored to CSV file {hashed_filename} = {len(df)} saved successfully!")


    def transform_data(self):
        """Transform data from the source."""
        logger.info(f"Transforming data from {config.RAW_FOLDER}")

        self.filter_data()
        self.remove_duplicates()
        self.generate_hashed_identifiers()

