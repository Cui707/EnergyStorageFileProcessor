"""
File utilities for the energy storage processor.
"""

import os
import shutil
import glob
from pathlib import Path
from typing import List, Optional, Dict, Any
import hashlib


class FileUtils:
    """File handling utilities."""
    
    @staticmethod
    def ensure_directory(directory: str) -> bool:
        """
        Ensure directory exists, create if necessary.
        
        Args:
            directory: Directory path
            
        Returns:
            True if directory exists or was created
        """
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: Path to file
            
        Returns:
            File size in bytes
        """
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0
    
    @staticmethod
    def get_file_hash(file_path: str, algorithm: str = 'md5') -> str:
        """
        Calculate file hash.
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm (md5, sha1, sha256)
            
        Returns:
            File hash
        """
        hash_func = hashlib.new(algorithm)
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception:
            return ""
    
    @staticmethod
    def find_files(directory: str, pattern: str, recursive: bool = True) -> List[str]:
        """
        Find files matching pattern.
        
        Args:
            directory: Directory to search
            pattern: File pattern (e.g., '*.csv')
            recursive: Whether to search recursively
            
        Returns:
            List of file paths
        """
        try:
            if recursive:
                pattern_path = os.path.join(directory, '**', pattern)
                return glob.glob(pattern_path, recursive=True)
            else:
                pattern_path = os.path.join(directory, pattern)
                return glob.glob(pattern_path)
        except Exception:
            return []
    
    @staticmethod
    def copy_file(src: str, dst: str) -> bool:
        """
        Copy file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            True if copy successful
        """
        try:
            shutil.copy2(src, dst)
            return True
        except Exception:
            return False
    
    @staticmethod
    def move_file(src: str, dst: str) -> bool:
        """
        Move file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            True if move successful
        """
        try:
            shutil.move(src, dst)
            return True
        except Exception:
            return False
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Delete file.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if deletion successful
        """
        try:
            os.remove(file_path)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """
        Get file information.
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary with file information
        """
        try:
            stat = os.stat(file_path)
            return {
                'path': file_path,
                'size': stat.st_size,
                'modified_time': stat.st_mtime,
                'created_time': stat.st_ctime,
                'extension': Path(file_path).suffix.lower(),
                'filename': Path(file_path).name,
                'directory': Path(file_path).parent
            }
        except Exception:
            return {}
    
    @staticmethod
    def get_unique_filename(file_path: str) -> str:
        """
        Get unique filename by adding number suffix if file exists.
        
        Args:
            file_path: Desired file path
            
        Returns:
            Unique file path
        """
        if not os.path.exists(file_path):
            return file_path
        
        base_path = Path(file_path).stem
        extension = Path(file_path).suffix
        directory = Path(file_path).parent
        
        counter = 1
        while True:
            new_path = os.path.join(directory, f"{base_path}_{counter}{extension}")
            if not os.path.exists(new_path):
                return new_path
            counter += 1
    
    @staticmethod
    def get_relative_path(file_path: str, base_path: str) -> str:
        """
        Get relative path from base path.
        
        Args:
            file_path: File path
            base_path: Base path
            
        Returns:
            Relative path
        """
        try:
            return os.path.relpath(file_path, base_path)
        except Exception:
            return file_path
    
    @staticmethod
    def is_file_accessible(file_path: str) -> bool:
        """
        Check if file is accessible.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file is accessible
        """
        try:
            with open(file_path, 'r') as f:
                f.read()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_directory_size(directory: str) -> int:
        """
        Get total size of directory in bytes.
        
        Args:
            directory: Directory path
            
        Returns:
            Total size in bytes
        """
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(file_path)
        except Exception:
            pass
        return total_size
    
    @staticmethod
    def clean_directory(directory: str, keep_patterns: Optional[List[str]] = None) -> int:
        """
        Clean directory by removing files not matching patterns.
        
        Args:
            directory: Directory to clean
            keep_patterns: List of file patterns to keep
            
        Returns:
            Number of files removed
        """
        if keep_patterns is None:
            keep_patterns = []
        
        removed_count = 0
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Check if file should be kept
                    should_keep = False
                    for pattern in keep_patterns:
                        if glob.fnmatch.fnmatch(file, pattern):
                            should_keep = True
                            break
                    
                    if not should_keep:
                        if FileUtils.delete_file(file_path):
                            removed_count += 1
        except Exception:
            pass
        
        return removed_count