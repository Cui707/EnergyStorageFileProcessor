"""
Reader factory for creating appropriate readers based on file type.
"""

from typing import Dict, Any, Optional
from .base import BaseReader
from .csv_reader import CSVReader
from .excel_reader import ExcelReader


class ReaderFactory:
    """Factory class for creating file readers."""
    
    _readers = {
        'csv': CSVReader,
        'excel': ExcelReader
    }
    
    @classmethod
    def create_reader(cls, file_type: str, config: Dict[str, Any]) -> BaseReader:
        """
        Create a reader for the specified file type.
        
        Args:
            file_type: Type of file ('csv' or 'excel')
            config: Configuration dictionary
            
        Returns:
            Appropriate reader instance
            
        Raises:
            ValueError: If file type is not supported
        """
        if file_type not in cls._readers:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        reader_class = cls._readers[file_type]
        return reader_class(config)
    
    @classmethod
    def get_supported_types(cls) -> list:
        """Get list of supported file types."""
        return list(cls._readers.keys())
    
    @classmethod
    def auto_detect_reader(cls, file_path: str, config: Dict[str, Any]) -> BaseReader:
        """
        Automatically detect file type and create appropriate reader.
        
        Args:
            file_path: Path to the file
            config: Configuration dictionary
            
        Returns:
            Appropriate reader instance
        """
        # Extract file extension
        extension = file_path.split('.')[-1].lower()
        
        # Map extension to file type
        extension_map = {
            'csv': 'csv',
            'xlsx': 'excel',
            'xls': 'excel'
        }
        
        if extension not in extension_map:
            raise ValueError(f"Unsupported file extension: {extension}")
        
        file_type = extension_map[extension]
        return cls.create_reader(file_type, config)