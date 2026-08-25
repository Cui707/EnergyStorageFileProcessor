"""
CSV writer for data files.
"""

import pandas as pd
from typing import Dict, Any, Optional
from .base import BaseWriter


class CSVWriter(BaseWriter):
    """CSV file writer for data."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the CSV writer.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.encoding = config.get('encoding', 'utf-8')
        self.delimiter = config.get('delimiter', ',')
    
    def write(self, data: pd.DataFrame, file_path: str) -> bool:
        """
        Write data to CSV file.
        
        Args:
            data: DataFrame to write
            file_path: Path to output file
            
        Returns:
            True if write successful
        """
        try:
            # Ensure output directory exists
            if not self.ensure_directory(file_path):
                raise Exception(f"Cannot create output directory: {Path(file_path).parent}")
            
            # Write to CSV
            data.to_csv(
                file_path,
                index=False,
                encoding=self.encoding,
                sep=self.delimiter
            )
            
            return True
            
        except Exception as e:
            print(f"Failed to write CSV file {file_path}: {e}")
            return False
    
    def get_supported_extensions(self) -> list:
        """Get supported file extensions."""
        return ['.csv']