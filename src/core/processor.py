"""
Main processor that orchestrates data processing operations.
"""

import os
from typing import List, Dict, Any, Optional
from ..config import Config
from ..models.data_models import ProcessingResult
from .data_processor import DataProcessor
from .batch_processor import BatchProcessor


class Processor:
    """Main processor that orchestrates all data processing operations."""
    
    def __init__(self, config: Config):
        """
        Initialize the main processor.
        
        Args:
            config: Configuration instance
        """
        self.config = config
        self.data_processor = DataProcessor(config)
        self.batch_processor = BatchProcessor(config)
    
    def process_file(self, input_file: str, output_dir: str,
                    custom_output_name: Optional[str] = None) -> ProcessingResult:
        """
        Process a single file.
        
        Args:
            input_file: Path to input file
            output_dir: Output directory
            custom_output_name: Custom output filename
            
        Returns:
            ProcessingResult object
        """
        return self.data_processor.process_file(input_file, output_dir, custom_output_name)
    
    def process_files(self, input_files: List[str], output_dir: str,
                    custom_output_names: Optional[List[str]] = None) -> List[ProcessingResult]:
        """
        Process multiple files.
        
        Args:
            input_files: List of input file paths
            output_dir: Output directory
            custom_output_names: Custom output filenames
            
        Returns:
            List of ProcessingResult objects
        """
        return self.batch_processor.process_files(input_files, output_dir, custom_output_names)
    
    def process_directory(self, input_dir: str, output_dir: str,
                         recursive: bool = True,
                         file_patterns: Optional[List[str]] = None,
                         custom_output_prefix: Optional[str] = None) -> List[ProcessingResult]:
        """
        Process all files in a directory.
        
        Args:
            input_dir: Input directory
            output_dir: Output directory
            recursive: Whether to process subdirectories
            file_patterns: File patterns to match
            custom_output_prefix: Custom output filename prefix
            
        Returns:
            List of ProcessingResult objects
        """
        return self.batch_processor.process_directory(
            input_dir, output_dir, recursive, file_patterns, custom_output_prefix
        )
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported input formats."""
        return self.data_processor.get_supported_formats()
    
    def validate_input_file(self, file_path: str) -> bool:
        """
        Validate if input file can be processed.
        
        Args:
            file_path: Path to input file
            
        Returns:
            True if file can be processed
        """
        return self.data_processor.validate_input_file(file_path)
    
    def get_processing_summary(self, results: List[ProcessingResult]) -> Dict[str, Any]:
        """
        Get summary of processing results.
        
        Args:
            results: List of ProcessingResult objects
            
        Returns:
            Summary dictionary
        """
        return self.batch_processor.get_processing_summary(results)
    
    def save_processing_report(self, results: List[ProcessingResult], 
                            output_dir: str, filename: str = "processing_report.txt"):
        """
        Save processing report to file.
        
        Args:
            results: List of ProcessingResult objects
            output_dir: Output directory
            filename: Report filename
        """
        self.batch_processor.save_processing_report(results, output_dir, filename)