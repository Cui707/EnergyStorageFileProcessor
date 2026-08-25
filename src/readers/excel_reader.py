"""
Excel reader for data files.
"""

import pandas as pd
import os
from typing import Dict, Any, List, Optional
from .base import BaseReader


class ExcelReader(BaseReader):
    """Excel file reader for battery data."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Excel reader.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.sheet_name = config.get('sheet_name', 0)
        self.header_row = config.get('header_row', 0)
        self.skip_rows = config.get('skip_rows', 0)
    
    def read(self, file_path: str) -> pd.DataFrame:
        """
        Read data from Excel file.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            DataFrame containing the data
        """
        try:
            # Read Excel file
            df = pd.read_excel(
                file_path,
                sheet_name=self.sheet_name,
                header=self.header_row,
                skiprows=self.skip_rows
            )
            
            # Validate data
            if not self.validate(df):
                raise ValueError("Data validation failed")
            
            return df
            
        except Exception as e:
            raise Exception(f"Failed to read Excel file {file_path}: {e}")
    
    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate the Excel data.
        
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
        return ['xlsx', 'xls']