"""
Base reader class for data file readers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import pandas as pd
from ..models.data_models import BatteryData


class BaseReader(ABC):
    """Base class for data file readers."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the reader.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
    
    @abstractmethod
    def read(self, file_path: str) -> pd.DataFrame:
        """
        Read data from file.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            DataFrame containing the data
        """
        pass
    
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate the read data.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def get_file_extension(self, file_path: str) -> str:
        """Get file extension."""
        return file_path.split('.')[-1].lower()
    
    def detect_file_type(self, file_path: str) -> str:
        """Detect file type based on extension."""
        extension = self.get_file_extension(file_path)
        
        if extension == 'csv':
            return 'csv'
        elif extension in ['xlsx', 'xls']:
            return 'excel'
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    
    def extract_cluster_id(self, file_path: str) -> str:
        """
        Extract cluster ID from file path.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Cluster ID string
        """
        import re
        
        # Extract numbers from filename (assuming bms1, bms2, etc.)
        filename = Path(file_path).name
        match = re.search(r'bms(\d+)', filename, re.IGNORECASE)
        
        if match:
            return f"cluster_{match.group(1)}"
        else:
            # Fallback to using file index
            return f"cluster_{hash(filename) % 1000}"