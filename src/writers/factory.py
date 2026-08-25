"""
Writer factory for creating appropriate writers based on file type.
"""

from typing import Dict, Any, Optional
from .base import BaseWriter
from .excel_writer import ExcelWriter
from .csv_writer import CSVWriter


class WriterFactory:
    """Factory class for creating file writers."""
    
    _writers = {
        'excel': ExcelWriter,
        'csv': CSVWriter
    }
    
    @classmethod
    def create_writer(cls, file_type: str, config: Dict[str, Any]) -> BaseWriter:
        """
        Create a writer for the specified file type.
        
        Args:
            file_type: Type of file ('excel' or 'csv')
            config: Configuration dictionary
            
        Returns:
            Appropriate writer instance
            
        Raises:
            ValueError: If file type is not supported
        """
        if file_type not in cls._writers:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        writer_class = cls._writers[file_type]
        return writer_class(config)
    
    @classmethod
    def get_supported_types(cls) -> list:
        """Get list of supported file types."""
        return list(cls._writers.keys())
    
    @classmethod
    def auto_detect_writer(cls, file_path: str, config: Dict[str, Any]) -> BaseWriter:
        """
        Automatically detect file type and create appropriate writer.
        
        Args:
            file_path: Path to the file
            config: Configuration dictionary
            
        Returns:
            Appropriate writer instance
        """
        # Extract file extension
        extension = Path(file_path).suffix.lower()
        
        # Map extension to file type
        extension_map = {
            '.xlsx': 'excel',
            '.xls': 'excel',
            '.csv': 'csv'
        }
        
        if extension not in extension_map:
            raise ValueError(f"Unsupported file extension: {extension}")
        
        file_type = extension_map[extension]
        return cls.create_writer(file_type, config)