"""
Parallel processing utilities for batch operations.
"""

import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import Dict, Any, List, Optional, Callable
from tqdm import tqdm
import threading
from ..config import Config


class ParallelProcessor:
    """Handle parallel processing of data files."""
    
    def __init__(self, config: Config):
        """
        Initialize the parallel processor.
        
        Args:
            config: Configuration instance
        """
        self.config = config
        self.parallel_settings = config.get_parallel_settings()
        self.max_workers = self.parallel_settings.get('max_workers', 4)
        self.chunk_size = self.parallel_settings.get('chunk_size', 1000)
        self.enable_multiprocessing = self.parallel_settings.get('enable_multiprocessing', False)
        
        # Thread-safe progress tracking
        self.lock = threading.Lock()
        self.completed_tasks = 0
        self.total_tasks = 0
        self.failed_tasks = 0
    
    def process_files_parallel(self, file_paths: List[str], 
                             process_func: Callable,
                             output_dir: str,
                             **kwargs) -> List[Dict[str, Any]]:
        """
        Process multiple files in parallel.
        
        Args:
            file_paths: List of file paths to process
            process_func: Function to process each file
            output_dir: Output directory for results
            **kwargs: Additional arguments for process_func
            
        Returns:
            List of processing results
        """
        self.total_tasks = len(file_paths)
        self.completed_tasks = 0
        self.failed_tasks = 0
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Choose executor based on configuration
        if self.enable_multiprocessing:
            executor_class = ProcessPoolExecutor
        else:
            executor_class = ThreadPoolExecutor
        
        results = []
        
        with executor_class(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(process_func, file_path, output_dir, **kwargs): file_path
                for file_path in file_paths
            }
            
            # Process completed tasks with progress bar
            with tqdm(total=self.total_tasks, desc="Processing files") as pbar:
                for future in as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        result = future.result()
                        results.append(result)
                        
                        with self.lock:
                            self.completed_tasks += 1
                            pbar.update(1)
                            
                    except Exception as e:
                        with self.lock:
                            self.failed_tasks += 1
                            pbar.update(1)
                        
                        # Log error
                        error_result = {
                            'input_file': file_path,
                            'output_file': '',
                            'success': False,
                            'error_message': str(e),
                            'processing_time': 0,
                            'records_processed': 0
                        }
                        results.append(error_result)
        
        return results
    
    def process_directory(self, input_dir: str, 
                        process_func: Callable,
                        output_dir: str,
                        recursive: bool = True,
                        file_patterns: Optional[List[str]] = None,
                        **kwargs) -> List[Dict[str, Any]]:
        """
        Process all files in a directory.
        
        Args:
            input_dir: Input directory path
            process_func: Function to process each file
            output_dir: Output directory for results
            recursive: Whether to process subdirectories recursively
            file_patterns: List of file patterns to match
            **kwargs: Additional arguments for process_func
            
        Returns:
            List of processing results
        """
        # Find all files to process
        file_paths = self._find_files(input_dir, recursive, file_patterns)
        
        if not file_paths:
            print(f"No files found in directory: {input_dir}")
            return []
        
        print(f"Found {len(file_paths)} files to process")
        
        return self.process_files_parallel(file_paths, process_func, output_dir, **kwargs)
    
    def _find_files(self, directory: str, recursive: bool = True, 
                   file_patterns: Optional[List[str]] = None) -> List[str]:
        """
        Find files in directory matching patterns.
        
        Args:
            directory: Directory to search
            recursive: Whether to search recursively
            file_patterns: List of file patterns to match
            
        Returns:
            List of file paths
        """
        import glob
        
        if file_patterns is None:
            file_patterns = ['*.csv', '*.xlsx', '*.xls']
        
        file_paths = []
        
        for pattern in file_patterns:
            if recursive:
                # Recursive search
                pattern_path = os.path.join(directory, '**', pattern)
                files = glob.glob(pattern_path, recursive=True)
            else:
                # Non-recursive search
                pattern_path = os.path.join(directory, pattern)
                files = glob.glob(pattern_path)
            
            file_paths.extend(files)
        
        return list(set(file_paths))  # Remove duplicates
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """
        Get processing statistics.
        
        Returns:
            Dictionary with processing statistics
        """
        return {
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_tasks,
            'failed_tasks': self.failed_tasks,
            'success_rate': (self.completed_tasks - self.failed_tasks) / self.total_tasks if self.total_tasks > 0 else 0
        }
    
    def process_with_chunks(self, data_list: List[Any], 
                          process_func: Callable,
                          chunk_size: Optional[int] = None,
                          **kwargs) -> List[Any]:
        """
        Process data in chunks for better memory management.
        
        Args:
            data_list: List of data to process
            process_func: Function to process each chunk
            chunk_size: Size of each chunk (default from config)
            **kwargs: Additional arguments for process_func
            
        Returns:
            List of processing results
        """
        if chunk_size is None:
            chunk_size = self.chunk_size
        
        results = []
        
        # Process data in chunks
        for i in range(0, len(data_list), chunk_size):
            chunk = data_list[i:i + chunk_size]
            chunk_result = process_func(chunk, **kwargs)
            results.extend(chunk_result)
        
        return results