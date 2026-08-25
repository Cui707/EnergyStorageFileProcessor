"""
Logging utilities for the energy storage processor.
"""

import os
import logging
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path


class Logger:
    """Logger for the energy storage processor."""
    
    def __init__(self, name: str = "energy_storage_processor", 
                 log_level: str = "INFO",
                 log_file: Optional[str] = None,
                 console_output: bool = True):
        """
        Initialize the logger.
        
        Args:
            name: Logger name
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file (optional)
            console_output: Whether to output to console
        """
        self.name = name
        self.log_level = getattr(logging, log_level.upper())
        self.log_file = log_file
        self.console_output = console_output
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Add console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # Add file handler
        if log_file:
            # Create log directory if it doesn't exist
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)
    
    def log_processing_start(self, file_path: str, total_files: int):
        """Log processing start."""
        self.info(f"Starting processing of file {file_path} ({total_files} total)")
    
    def log_processing_complete(self, file_path: str, output_file: str, 
                               processing_time: float, records_processed: int):
        """Log processing completion."""
        self.info(f"Completed processing {file_path} -> {output_file} "
                 f"({processing_time:.2f}s, {records_processed} records)")
    
    def log_processing_error(self, file_path: str, error: str):
        """Log processing error."""
        self.error(f"Error processing {file_path}: {error}")
    
    def log_batch_start(self, total_files: int):
        """Log batch processing start."""
        self.info(f"Starting batch processing of {total_files} files")
    
    def log_batch_complete(self, stats: dict):
        """Log batch processing completion."""
        self.info(f"Batch processing completed. "
                 f"Total: {stats['total_tasks']}, "
                 f"Success: {stats['completed_tasks'] - stats['failed_tasks']}, "
                 f"Failed: {stats['failed_tasks']}, "
                 f"Success rate: {stats['success_rate']:.2%}")
    
    def log_config_loaded(self, config_file: str):
        """Log configuration loading."""
        self.info(f"Configuration loaded from {config_file}")
    
    def log_file_not_found(self, file_path: str):
        """Log file not found error."""
        self.warning(f"File not found: {file_path}")
    
    def log_validation_error(self, file_path: str, errors: list):
        """Log validation error."""
        self.error(f"Validation failed for {file_path}: {', '.join(errors)}")


def get_logger(name: str = "energy_storage_processor", 
               log_level: str = "INFO",
               log_dir: Optional[str] = None) -> Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name
        log_level: Logging level
        log_dir: Directory for log files (optional)
        
    Returns:
        Logger instance
    """
    if log_dir:
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"energy_storage_processor_{timestamp}.log")
        
        return Logger(name, log_level, log_file)
    else:
        return Logger(name, log_level)