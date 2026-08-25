"""
Batch processor for handling multiple files.
"""

import os
import time
from typing import List, Dict, Any, Optional
from ..config import Config
from ..models.data_models import ProcessingResult
from ..utils.parallel import ParallelProcessor
from ..utils.logger import Logger
from ..utils.file_utils import FileUtils
from .data_processor import DataProcessor


class BatchProcessor:
    """Batch processor for handling multiple files."""
    
    def __init__(self, config: Config):
        """
        Initialize the batch processor.
        
        Args:
            config: Configuration instance
        """
        self.config = config
        self.logger = Logger("BatchProcessor")
        self.parallel_processor = ParallelProcessor(config)
        self.data_processor = DataProcessor(config)
    
    def process_files(self, input_files: List[str], output_dir: str,
                    custom_output_names: Optional[List[str]] = None) -> List[ProcessingResult]:
        """
        Process multiple files.
        
        Args:
            input_files: List of input file paths
            output_dir: Output directory
            custom_output_names: Custom output filenames (optional)
            
        Returns:
            List of ProcessingResult objects
        """
        if not input_files:
            self.logger.warning("No input files provided")
            return []
        
        # Create output directory
        FileUtils.ensure_directory(output_dir)
        
        # Validate input files
        valid_files = []
        for file_path in input_files:
            if self.data_processor.validate_input_file(file_path):
                valid_files.append(file_path)
            else:
                self.logger.log_file_not_found(file_path)
        
        if not valid_files:
            self.logger.error("No valid input files found")
            return []
        
        self.logger.log_batch_start(len(valid_files))
        
        # Process files in parallel
        if custom_output_names:
            if len(custom_output_names) != len(valid_files):
                self.logger.warning("Number of custom output names doesn't match number of files")
                custom_output_names = None
        
        results = self.parallel_processor.process_files_parallel(
            valid_files,
            self._process_single_file,
            output_dir,
            custom_output_names=custom_output_names
        )
        
        # Log batch completion
        stats = self.parallel_processor.get_processing_stats()
        self.logger.log_batch_complete(stats)
        
        return results
    
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
        if not os.path.exists(input_dir):
            self.logger.error(f"Input directory not found: {input_dir}")
            return []
        
        # Create output directory
        FileUtils.ensure_directory(output_dir)
        
        # Set default file patterns if not provided
        if file_patterns is None:
            file_patterns = ['*.csv', '*.xlsx', '*.xls']
        
        # Find files to process
        file_paths = self.parallel_processor._find_files(input_dir, recursive, file_patterns)
        
        if not file_paths:
            self.logger.warning(f"No files found in directory: {input_dir}")
            return []
        
        # Filter valid files
        valid_files = []
        for file_path in file_paths:
            if self.data_processor.validate_input_file(file_path):
                valid_files.append(file_path)
        
        if not valid_files:
            self.logger.error("No valid input files found")
            return []
        
        self.logger.log_batch_start(len(valid_files))
        
        # Process files in parallel
        results = self.parallel_processor.process_directory(
            input_dir,
            self._process_single_file,
            output_dir,
            recursive=recursive,
            file_patterns=file_patterns,
            custom_output_prefix=custom_output_prefix
        )
        
        # Log batch completion
        stats = self.parallel_processor.get_processing_stats()
        self.logger.log_batch_complete(stats)
        
        return results
    
    def _process_single_file(self, file_path: str, output_dir: str,
                           custom_output_name: Optional[str] = None,
                           custom_output_prefix: Optional[str] = None) -> ProcessingResult:
        """
        Process a single file (called by parallel processor).
        
        Args:
            file_path: Path to input file
            output_dir: Output directory
            custom_output_name: Custom output filename
            custom_output_prefix: Custom output filename prefix
            
        Returns:
            ProcessingResult object
        """
        try:
            # Generate custom output name if prefix provided
            if custom_output_prefix:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                custom_output_name = f"{custom_output_prefix}_{base_name}.{self.config.get_output_format()}"
            
            # Process the file
            result = self.data_processor.process_file(file_path, output_dir, custom_output_name)
            
            return result
            
        except Exception as e:
            self.logger.log_processing_error(file_path, str(e))
            return ProcessingResult(
                input_file=file_path,
                output_file="",
                success=False,
                error_message=str(e)
            )
    
    def get_processing_summary(self, results: List[ProcessingResult]) -> Dict[str, Any]:
        """
        Get summary of processing results.
        
        Args:
            results: List of ProcessingResult objects
            
        Returns:
            Summary dictionary
        """
        if not results:
            return {
                'total_files': 0,
                'successful_files': 0,
                'failed_files': 0,
                'success_rate': 0.0,
                'total_processing_time': 0.0,
                'average_processing_time': 0.0,
                'total_records_processed': 0
            }
        
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]
        
        total_time = sum(r.processing_time or 0 for r in results)
        total_records = sum(r.records_processed for r in successful)
        
        return {
            'total_files': len(results),
            'successful_files': len(successful),
            'failed_files': len(failed),
            'success_rate': len(successful) / len(results) if results else 0.0,
            'total_processing_time': total_time,
            'average_processing_time': total_time / len(results) if results else 0.0,
            'total_records_processed': total_records
        }
    
    def save_processing_report(self, results: List[ProcessingResult], 
                            output_dir: str, filename: str = "processing_report.txt"):
        """
        Save processing report to file.
        
        Args:
            results: List of ProcessingResult objects
            output_dir: Output directory
            filename: Report filename
        """
        # Create output directory
        FileUtils.ensure_directory(output_dir)
        
        # Generate report
        report_path = os.path.join(output_dir, filename)
        summary = self.get_processing_summary(results)
        
        report_content = f"""
Energy Storage Processing Report
==============================

Processing Summary:
- Total Files Processed: {summary['total_files']}
- Successful Files: {summary['successful_files']}
- Failed Files: {summary['failed_files']}
- Success Rate: {summary['success_rate']:.2%}
- Total Processing Time: {summary['total_processing_time']:.2f} seconds
- Average Processing Time: {summary['average_processing_time']:.2f} seconds
- Total Records Processed: {summary['total_records_processed']}

Detailed Results:
"""
        
        for i, result in enumerate(results, 1):
            status = "SUCCESS" if result.success else "FAILED"
            report_content += f"""
{i}. {result.input_file} -> {result.output_file}
   Status: {status}
   Processing Time: {result.processing_time:.2f} seconds
   Records Processed: {result.records_processed}
"""
            if not result.success:
                report_content += f"   Error: {result.error_message}\n"
        
        # Save report
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            self.logger.info(f"Processing report saved to {report_path}")
        except Exception as e:
            self.logger.error(f"Failed to save processing report: {str(e)}")