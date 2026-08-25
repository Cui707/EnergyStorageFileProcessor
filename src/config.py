"""
Configuration management for the energy storage processor.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for the energy storage processor."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to configuration file. If None, uses default config.
        """
        self.config_dir = Path(__file__).parent.parent / "configs"
        self.config_file = config_file or self.config_dir / "default.yaml"
        
        # Load configuration
        self.data_format = {}
        self.calculation_rules = {}
        self.parallel_settings = {}
        self.output_settings = {}
        self.reader_settings = {}
        self.processor_settings = {}
        
        self._load_config()
    
    def _load_config(self):
        """Load configuration from YAML files."""
        try:
            # Load main configuration
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                self.data_format = config.get('data_format', {})
                self.calculation_rules = config.get('calculation_rules', {})
                self.parallel_settings = config.get('parallel_settings', {})
                self.output_settings = config.get('output_settings', {})
                
                # Load reader settings
                readers_file = self.config_dir / "readers.yaml"
                if os.path.exists(readers_file):
                    with open(readers_file, 'r', encoding='utf-8') as f:
                        self.reader_settings = yaml.safe_load(f).get('readers', {})
                
                # Load processor settings
                processors_file = self.config_dir / "processors.yaml"
                if os.path.exists(processors_file):
                    with open(processors_file, 'r', encoding='utf-8') as f:
                        self.processor_settings = yaml.safe_load(f).get('processors', {})
            
        except Exception as e:
            raise Exception(f"Failed to load configuration: {e}")
    
    def get_data_format(self) -> Dict[str, Any]:
        """Get data format configuration."""
        return self.data_format
    
    def get_calculation_rules(self) -> Dict[str, Any]:
        """Get calculation rules configuration."""
        return self.calculation_rules
    
    def get_parallel_settings(self) -> Dict[str, Any]:
        """Get parallel processing settings."""
        return self.parallel_settings
    
    def get_output_settings(self) -> Dict[str, Any]:
        """Get output settings configuration."""
        return self.output_settings
    
    def get_reader_settings(self) -> Dict[str, Any]:
        """Get reader settings configuration."""
        return self.reader_settings
    
    def get_processor_settings(self) -> Dict[str, Any]:
        """Get processor settings configuration."""
        return self.processor_settings
    
    def get_max_workers(self) -> int:
        """Get maximum number of parallel workers."""
        return self.parallel_settings.get('max_workers', 4)
    
    def get_output_format(self) -> str:
        """Get output file format."""
        return self.output_settings.get('format', 'excel')
    
    def get_output_filename(self) -> str:
        """Get output filename."""
        return self.output_settings.get('filename', 'Processed_Data')
    
    def should_highlight_calculated(self) -> bool:
        """Whether to highlight calculated columns in output."""
        return self.output_settings.get('highlight_calculated', True)
    
    def get_filename_patterns(self) -> list:
        """Get filename patterns for file matching."""
        return self.processor_settings.get('extractor', {}).get('filename_patterns', ['*bms*', '*BMS*'])
    
    def get_column_patterns(self) -> Dict[str, str]:
        """Get column name patterns for data extraction."""
        return self.processor_settings.get('extractor', {}).get('column_patterns', {})