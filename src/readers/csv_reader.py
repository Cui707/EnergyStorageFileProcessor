"""
CSV reader for data files.
"""

import pandas as pd
import os
from typing import Dict, Any, List, Optional
from .base import BaseReader


class CSVReader(BaseReader):
    """CSV file reader for battery data."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the CSV reader.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.encoding = config.get('encoding', 'utf-8')
        self.delimiter = config.get('delimiter', ',')
        self.skip_rows = config.get('skip_rows', 0)
        self.header_row = config.get('header_row', 0)
    
    def read(self, file_path: str) -> pd.DataFrame:
        """
        Read data from CSV file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            DataFrame containing the data
        """
        try:
            # Read CSV file
            df = pd.read_csv(
                file_path,
                encoding=self.encoding,
                delimiter=self.delimiter,
                skiprows=self.skip_rows,
                header=self.header_row,
                engine='python'
            )
            
            # Validate data
            if not self.validate(df):
                raise ValueError("Data validation failed")
            
            return df
            
        except Exception as e:
            raise Exception(f"Failed to read CSV file {file_path}: {e}")
    
    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate the CSV data.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            True if valid, False otherwise
        """
        if data.empty:
            return False
        
        # Check if DataFrame has columns
        if len(data.columns) == 0:
            return False
        
        # Check for required data types (basic validation)
        numeric_columns = data.select_dtypes(include=['number']).columns
        if len(numeric_columns) == 0:
            return False
        
        return True
    
    def get_supported_extensions(self) -> List[str]:
        """Get supported file extensions."""
        return ['csv']