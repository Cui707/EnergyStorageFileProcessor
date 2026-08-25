"""
Base writer class for data file writers.
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any, Optional
from pathlib import Path


class BaseWriter(ABC):
    """Base class for data file writers."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the writer.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
    
    @abstractmethod
    def write(self, data: pd.DataFrame, file_path: str) -> bool:
        """
        Write data to file.
        
        Args:
            data: DataFrame to write
            file_path: Path to output file
            
        Returns:
            True if write successful
        """
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> list:
        """Get supported file extensions."""
        pass
    
    def ensure_directory(self, file_path: str) -> bool:
        """
        Ensure output directory exists.
        
        Args:
            file_path: Path to output file
            
        Returns:
            True if directory exists or was created
        """
        try:
            directory = Path(file_path).parent
            directory.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    def get_file_extension(self, file_path: str) -> str:
        """Get file extension."""
        return Path(file_path).suffix.lower()