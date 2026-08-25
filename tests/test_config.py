"""
Tests for configuration management.
"""

import pytest
import tempfile
import os
import yaml
from pathlib import Path

from src.config import Config
from src.models.config_models import FullConfig, DataFormatConfig, CalculationRulesConfig


class TestConfig:
    """Test configuration management."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config_data = {
            'data_format': {
                'time_columns': ['occurTime', 'timestamp'],
                'voltage_columns': ['maxU', 'minU', 'voltage'],
                'temperature_columns': ['maxT', 'minT', 'temp'],
                'current_columns': ['current'],
                'charge_columns': ['charge', 'totalChargeKwh'],
                'discharge_columns': ['discharge', 'totalDischargeKwh']
            },
            'calculation_rules': {
                'system_voltage': {
                    'max': True,
                    'min': True,
                    'diff': True,
                    'diff_multiplier': 1000
                },
                'system_temperature': {
                    'max': True
                },
                'energy_balance': {
                    'charge': True,
                    'discharge': True
                }
            },
            'parallel_settings': {
                'max_workers': 4,
                'chunk_size': 1000,
                'enable_multiprocessing': False
            },
            'output_settings': {
                'format': 'excel',
                'filename': 'Processed_Data',
                'highlight_calculated': True
            }
        }
    
    def test_load_config_from_dict(self):
        """Test loading configuration from dictionary."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.config_data, f)
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            
            # Test data format
            data_format = config.get_data_format()
            assert 'time_columns' in data_format
            assert 'voltage_columns' in data_format
            assert 'occurTime' in data_format['time_columns']
            
            # Test calculation rules
            calc_rules = config.get_calculation_rules()
            assert 'system_voltage' in calc_rules
            assert calc_rules['system_voltage']['max'] is True
            
            # Test parallel settings
            parallel_settings = config.get_parallel_settings()
            assert parallel_settings['max_workers'] == 4
            
            # Test output settings
            output_settings = config.get_output_settings()
            assert output_settings['format'] == 'excel'
            
        finally:
            os.unlink(temp_file)
    
    def test_load_config_nonexistent_file(self):
        """Test loading configuration from non-existent file."""
        config = Config()  # Should load default config
        assert config is not None
    
    def test_get_max_workers(self):
        """Test getting max workers."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.config_data, f)
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            assert config.get_max_workers() == 4
        finally:
            os.unlink(temp_file)
    
    def test_get_output_format(self):
        """Test getting output format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.config_data, f)
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            assert config.get_output_format() == 'excel'
        finally:
            os.unlink(temp_file)
    
    def test_get_output_filename(self):
        """Test getting output filename."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.config_data, f)
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            assert config.get_output_filename() == 'Processed_Data'
        finally:
            os.unlink(temp_file)
    
    def test_should_highlight_calculated(self):
        """Test should highlight calculated."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.config_data, f)
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            assert config.should_highlight_calculated() is True
        finally:
            os.unlink(temp_file)
    
    def test_get_filename_patterns(self):
        """Test getting filename patterns."""
        processor_config = {
            'extractor': {
                'filename_patterns': ['*bms*', '*BMS*', '*cluster*']
            }
        }
        
        full_config = {**self.config_data, 'processors': processor_config}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(full_config, f)
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            patterns = config.get_filename_patterns()
            assert '*bms*' in patterns
            assert '*BMS*' in patterns
            assert '*cluster*' in patterns
        finally:
            os.unlink(temp_file)
    
    def test_get_column_patterns(self):
        """Test getting column patterns."""
        processor_config = {
            'extractor': {
                'column_patterns': {
                    'time': '(?i)occur.*time|timestamp',
                    'voltage': '(?i)max.*u|min.*u|voltage',
                    'temperature': '(?i)max.*t|min.*t|temp'
                }
            }
        }
        
        full_config = {**self.config_data, 'processors': processor_config}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(full_config, f)
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            patterns = config.get_column_patterns()
            assert 'time' in patterns
            assert 'voltage' in patterns
            assert 'temperature' in patterns
        finally:
            os.unlink(temp_file)


class TestConfigModels:
    """Test configuration models."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.data_format = {
            'time_columns': ['occurTime', 'timestamp'],
            'voltage_columns': ['maxU', 'minU', 'voltage'],
            'temperature_columns': ['maxT', 'minT', 'temp'],
            'current_columns': ['current'],
            'charge_columns': ['charge', 'totalChargeKwh'],
            'discharge_columns': ['discharge', 'totalDischargeKwh']
        }
        
        self.calculation_rules = {
            'system_voltage': {
                'max': True,
                'min': True,
                'diff': True
            },
            'system_temperature': {
                'max': True
            },
            'energy_balance': {
                'charge': True,
                'discharge': True
            }
        }
        
        self.parallel_settings = {
            'max_workers': 4,
            'chunk_size': 1000,
            'enable_multiprocessing': False
        }
        
        self.output_settings = {
            'format': 'excel',
            'filename': 'Processed_Data',
            'highlight_calculated': True
        }
    
    def test_data_format_config(self):
        """Test DataFormatConfig model."""
        config = DataFormatConfig.from_dict(self.data_format)
        
        assert config.time_columns == ['occurTime', 'timestamp']
        assert config.voltage_columns == ['maxU', 'minU', 'voltage']
        assert config.temperature_columns == ['maxT', 'minT', 'temp']
        assert config.current_columns == ['current']
        assert config.charge_columns == ['charge', 'totalChargeKwh']
        assert config.discharge_columns == ['discharge', 'totalDischargeKwh']
    
    def test_calculation_rules_config(self):
        """Test CalculationRulesConfig model."""
        config = CalculationRulesConfig.from_dict(self.calculation_rules)
        
        assert config.system_voltage['max'] is True
        assert config.system_voltage['min'] is True
        assert config.system_voltage['diff'] is True
        assert config.system_temperature['max'] is True
        assert config.energy_balance['charge'] is True
        assert config.energy_balance['discharge'] is True
    
    def test_full_config(self):
        """Test FullConfig model."""
        full_config_dict = {
            'data_format': self.data_format,
            'calculation_rules': self.calculation_rules,
            'parallel_settings': self.parallel_settings,
            'output_settings': self.output_settings,
            'readers': {
                'csv': {'encoding': 'utf-8'},
                'excel': {'sheet_name': 0}
            },
            'processors': {
                'extractor': {'filename_patterns': ['*bms*']},
                'calculator': {'system_voltage': {'max': True}}
            }
        }
        
        config = FullConfig.from_dict(full_config_dict)
        
        assert config.data_format.time_columns == ['occurTime', 'timestamp']
        assert config.calculation_rules.system_voltage['max'] is True
        assert config.parallel_settings.max_workers == 4
        assert config.output_settings.format == 'excel'
        assert config.reader_settings.csv['encoding'] == 'utf-8'
        assert config.processor_settings.extractor['filename_patterns'] == ['*bms*']