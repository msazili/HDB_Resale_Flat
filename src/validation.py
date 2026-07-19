import logging

import pandas as pd
import numpy as np

from src.config import config

from datetime import datetime
from typing import Dict, List, Tuple, Any

class DataValidator:
    """
    Data Quality Framework for HDB Resale Price Dataset
    """
    
    def __init__(self):
        # Filter dataset from Jan 2012 to Dec 2016
        raw_filename = f"{config.CLEANED_FOLDER}/{config.DATA_FILTERED_FILENAME}"
        df = pd.read_csv(raw_filename, sep=',', header=0, encoding='utf-8')

        self.df = df
        self.quality_report = {}
        self.validation_results = []
        
    def check_completeness(self) -> Dict[str, float]:
        """Check completeness of all columns"""
        completeness = {}
        for col in self.df.columns:
            complete_pct = (self.df[col].notna().sum() / len(self.df)) * 100
            completeness[col] = round(complete_pct, 2)
            if complete_pct < 100:
                self.validation_results.append({
                    'rule': 'COMPLETENESS',
                    'column': col,
                    'status': 'WARNING',
                    'message': f'Missing {100-complete_pct}% of values'
                })
        return completeness
    
    def check_uniqueness(self, id_col: str = '_id') -> Tuple[bool, int]:
        """Check if ID column is unique"""
        # is_unique = self.df[id_col].is_unique
        # duplicate_count = self.df[id_col].duplicated().sum()

        duplicate_columns = [col for col in self.df.columns if col not in ['_id', 'resale_price']]

        # Step 1: Remove duplicates keeping highest price
        df_cleaned = (
            self.df
            .sort_values('resale_price', ascending=False)
            .drop_duplicates(
                subset=duplicate_columns, 
                keep='first'
            ).sort_values('_id')
        )

        # Step 2: Get the duplicated records
        df_anti_join = self.df.merge(df_cleaned, on=list(self.df.columns), how='left', indicator=True)
        df_anti_join = df_anti_join[df_anti_join['_merge'] == 'left_only'].drop('_merge', axis=1)

        if len(df_anti_join) > 0:
            self.validation_results.append({
                'rule': 'UNIQUENESS',
                'column': duplicate_columns,
                'status': 'ERROR',
                'message': f'Found {len(df_anti_join)} duplicate {duplicate_columns}'
            })
        return (len(df_anti_join) > 0), len(df_anti_join)
    
    def check_price_range(self, price_col: str = 'resale_price') -> Dict[str, Any]:
        """Validate price range"""
        prices = self.df[price_col]
        invalid_prices = prices[(prices <= 0) | (prices > 2000000)]
        if len(invalid_prices) > 0:
            self.validation_results.append({
                'rule': 'PRICE_RANGE',
                'column': price_col,
                'status': 'ERROR',
                'message': f'Found {len(invalid_prices)} invalid prices'
            })
        return {
            'min': prices.min(),
            'max': prices.max(),
            'mean': prices.mean(),
            'invalid_count': len(invalid_prices)
        }
    
    def check_flat_types(self, flat_type_col: str = 'flat_type') -> Dict[str, Any]:
        """Validate flat types"""
        valid_types = ['1 ROOM', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', 'MULTI-GENERATION']
        invalid_types = self.df[~self.df[flat_type_col].isin(valid_types)]
        if len(invalid_types) > 0:
            self.validation_results.append({
                'rule': 'FLAT_TYPES',
                'column': flat_type_col,
                'status': 'ERROR',
                'message': f'Found {len(invalid_types)} invalid flat types'
            })
        return {
            'valid_types': valid_types,
            'invalid_count': len(invalid_types),
            'value_counts': self.df[flat_type_col].value_counts().to_dict()
        }
    
    def check_storey_ranges(self, storey_col: str = 'storey_range') -> Dict[str, Any]:
        """Validate storey range format"""
        pattern = r'^\d{2} TO \d{2}$'
        invalid_ranges = self.df[~self.df[storey_col].str.match(pattern, na=False)]
        return {
            'total': len(self.df),
            'invalid_count': len(invalid_ranges),
            'unique_ranges': self.df[storey_col].unique().tolist()
        }
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all data quality checks"""
        self.validation_results = []
        self.quality_report = {
            'timestamp': datetime.now().isoformat(),
            'total_records': len(self.df),
            'total_fields': len(self.df.columns),
            'completeness': self.check_completeness(),
            'uniqueness': self.check_uniqueness(),
            'price_validation': self.check_price_range(),
            'flat_type_validation': self.check_flat_types(),
            'storey_range_validation': self.check_storey_ranges(),
            'validation_results': self.validation_results,
            'quality_score': self.calculate_quality_score()
        }

        print(f"\nData Quality Report generated")
        for result in self.validation_results:
            print(f"[{result['status']}] {result['message']}")

        return self.quality_report
    
    def calculate_quality_score(self) -> int:
        """Calculate overall quality score"""
        score = 100
        for result in self.validation_results:
            if result['status'] == 'ERROR':
                score -= 10
            elif result['status'] == 'WARNING':
                score -= 5
        return max(0, min(100, score))

