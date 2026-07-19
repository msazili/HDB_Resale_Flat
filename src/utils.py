import hashlib
import logging
from datetime import datetime
import pandas as pd

from src.config import config

logger = logging.getLogger(__name__)

class PipelineUtils:
    """Class responsible for utility functions."""

    # Update the remaining_lease column
    current_date = datetime.now()

    def calculate_remaining_lease(self, lease_year):
        lease_tenure = config.HDB_LEASE_TENURE
        years_elapsed = self.current_date.year - lease_year
        remaining = lease_tenure - years_elapsed

        return max(0, int(remaining))  # Ensure non-negative
    

    def create_identifier(self,row):
        # Block digits
        block_str = str(row['block'])
        block_digits = ''.join(filter(str.isdigit, block_str))
        block_digits = block_digits.zfill(3)[:3]
        
        # Average price prefix
        avg_prefix = str(int(row['avg_resale_price']))[:2]
        
        # Month digits
        month_digits = row['month'].split('-')[1]
        
        # Town first character
        town_char = row['town'][0]
        
        return f"S{block_digits}{avg_prefix}{month_digits}{town_char}"
    

    # Function to hash using SHA-256
    def hash_identifier(self, identifier):
        """Hash the identifier using SHA-256 algorithm"""
        return hashlib.sha256(identifier.encode('utf-8')).hexdigest()


