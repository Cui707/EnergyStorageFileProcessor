"""
Tests for data processors.
"""

import pytest
import pandas as pd
import tempfile
import os
from datetime import datetime

from src.config import Config
from src.processors.extractor import DataExtractor
from src.processors.calculator import DataCalculator
from src.processors.validator import DataValidator


class TestDataExtractor:
    """Test data extractor functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = Config()
        self.extractor = DataExtractor(self.config)
    
    def test_should_process_file(self):
        """Test file processing decision."""
        assert self.extractor.should_process_file("bms1.csv")
        assert self.extractor.should_process_file("BMS_2.xlsx")
        assert not self.extractor.should_process_file("other_file.txt")
    
    def test_extract_time_columns(self):
        """Test extracting time columns."""
        df = pd.DataFrame({
            'occurTime': ['2023-01-01 10:00:00', '2023-01-01 10:01:00'],
            'timestamp': ['2023-01-01 10:00:00', '2023-01-01 10:01:00'],
            'maxU': [4.2, 4.3],
            'minU': [3.8, 3.9]
        })
        
        time_columns = self.extractor.extract_time_columns(df)
        assert 'occurTime' in time_columns
        assert 'timestamp' in time_columns
    
    def test_extract_voltage_columns(self):
        """Test extracting voltage columns."""
        df = pd.DataFrame({
            'maxU': [4.2, 4.3],
            'minU': [3.8, 3.9],
            'voltage': [4.0, 4.1],
            'current': [10.0, 10.5]
        })
        
        voltage_columns = self.extractor.extract_voltage_columns(df)
        assert 'maxU' in voltage_columns
        assert 'minU' in voltage_columns
        assert 'voltage' in voltage_columns
    
    def test_extract_battery_data(self):
        """Test extracting battery data."""
        df = pd.DataFrame({
            'occurTime': ['2023-01-01 10:00:00', '2023-01-01 10:01:00'],
            'maxU': [4.2, 4.3],
            'minU': [3.8, 3.9],
            'maxT': [25.0, 25.5],
            'current': [10.0, 10.5],
            'totalChargeKwh': [5.0, 5.1],
            'totalDischargeKwh': [2.0, 2.1],
            'thisChargeKwh': [0.1, 0.1],
            'thisDischargeKwh': [0.05, 0.05]
        })
        
        battery_data = self.extractor.extract_battery_data(df, "cluster_1")
        
        assert len(battery_data) == 2
        assert battery_data[0].cluster_id == "cluster_1"
        assert battery_data[0].max_voltage == 4.2
        assert battery_data[0].min_voltage == 3.8
        assert battery_data[0].max_temperature == 25.0
        assert battery_data[0].current == 10.0
        assert battery_data[0].total_charge == 5.0
        assert battery_data[0].total_discharge == 2.0
        assert battery_data[0].this_charge == 0.1
        assert battery_data[0].this_discharge == 0.05


class TestDataCalculator:
    """Test data calculator functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = Config()
        self.calculator = DataCalculator(self.config)
    
    def test_calculate_system_statistics(self):
        """Test calculating system statistics."""
        from src.models.data_models import BatteryData
        
        # Create test battery data
        battery_data = [
            BatteryData(
                cluster_id="cluster_1",
                timestamp=datetime(2023, 1, 1, 10, 0, 0),
                max_voltage=4.2,
                min_voltage=3.8,
                max_temperature=25.0,
                current=10.0,
                total_charge=5.0,
                total_discharge=2.0,
                this_charge=0.1,
                this_discharge=0.05
            ),
            BatteryData(
                cluster_id="cluster_2",
                timestamp=datetime(2023, 1, 1, 10, 1, 0),
                max_voltage=4.3,
                min_voltage=3.9,
                max_temperature=25.5,
                current=10.5,
                total_charge=5.1,
                total_discharge=2.1,
                this_charge=0.1,
                this_discharge=0.05
            )
        ]
        
        # Calculate system statistics
        processed_data = self.calculator.calculate_system_statistics(battery_data)
        
        assert processed_data.system_max_voltage == 4.3
        assert processed_data.system_min_voltage == 3.8
        assert processed_data.voltage_diff == 500.0  # (4.3 - 3.8) * 1000
        assert processed_data.system_max_temperature == 25.5
        assert processed_data.day_total_charge == 0.2
        assert processed_data.day_total_discharge == 0.1
        assert len(processed_data.cluster_data) == 2
    
    def test_add_calculated_columns(self):
        """Test adding calculated columns to DataFrame."""
        df = pd.DataFrame({
            'cluster_1_maxU': [4.2, 4.3],
            'cluster_1_minU': [3.8, 3.9],
            'cluster_1_maxT': [25.0, 25.5],
            'cluster_1_current': [10.0, 10.5],
            'cluster_1_charge': [5.0, 5.1],
            'cluster_1_discharge': [2.0, 2.1]
        })
        
        # Create mock processed data
        from src.models.data_models import ProcessedData, BatteryData
        processed_data = ProcessedData(
            cluster_data=[],
            system_max_voltage=4.3,
            system_min_voltage=3.8,
            voltage_diff=500.0,
            system_max_temperature=25.5,
            day_total_charge=0.2,
            day_total_discharge=0.1
        )
        
        # Add calculated columns
        df_with_calculated = self.calculator.add_calculated_columns(df, processed_data)
        
        # Check if calculated columns are added
        assert 'sysMaxU' in df_with_calculated.columns
        assert 'sysMinU' in df_with_calculated.columns
        assert 'MaxDiff' in df_with_calculated.columns
        assert 'sysMaxT' in df_with_calculated.columns
        assert 'DayTotalChargeKwh' in df_with_calculated.columns
        assert 'DayTotalDischargeKwh' in df_with_calculated.columns


class TestDataValidator:
    """Test data validator functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = Config()
        self.validator = DataValidator(self.config)
    
    def test_validate_valid_dataframe(self):
        """Test validating a valid DataFrame."""
        df = pd.DataFrame({
            'timestamp': ['2023-01-01 10:00:00', '2023-01-01 10:01:00'],
            'maxU': [4.2, 4.3],
            'minU': [3.8, 3.9],
            'maxT': [25.0, 25.5],
            'current': [10.0, 10.5],
            'charge': [5.0, 5.1],
            'discharge': [2.0, 2.1]
        })
        
        is_valid, errors = self.validator.validate_dataframe(df)
        assert is_valid
        assert len(errors) == 0
    
    def test_validate_empty_dataframe(self):
        """Test validating an empty DataFrame."""
        df = pd.DataFrame()
        
        is_valid, errors = self.validator.validate_dataframe(df)
        assert not is_valid
        assert len(errors) > 0
        assert any("empty" in error.lower() for error in errors)
    
    def test_validate_dataframe_no_columns(self):
        """Test validating a DataFrame with no columns."""
        df = pd.DataFrame(columns=['a', 'b'])
        df = df.drop(columns=['a', 'b'])  # Empty DataFrame with no columns
        
        is_valid, errors = self.validator.validate_dataframe(df)
        assert not is_valid
        assert len(errors) > 0
        assert any("columns" in error.lower() for error in errors)
    
    def test_validate_battery_data(self):
        """Test validating battery data."""
        from src.models.data_models import BatteryData
        
        # Create valid battery data
        battery_data = [
            BatteryData(
                cluster_id="cluster_1",
                timestamp=datetime(2023, 1, 1, 10, 0, 0),
                max_voltage=4.2,
                min_voltage=3.8,
                max_temperature=25.0,
                current=10.0,
                total_charge=5.0,
                total_discharge=2.0,
                this_charge=0.1,
                this_discharge=0.05
            )
        ]
        
        is_valid, errors = self.validator.validate_battery_data(battery_data)
        assert is_valid
        assert len(errors) == 0
    
    def test_validate_battery_data_empty(self):
        """Test validating empty battery data."""
        battery_data = []
        
        is_valid, errors = self.validator.validate_battery_data(battery_data)
        assert not is_valid
        assert len(errors) > 0
        assert any("No battery data" in error for error in errors)
    
    def test_validate_battery_data_unreasonable_values(self):
        """Test validating battery data with unreasonable values."""
        from src.models.data_models import BatteryData
        
        # Create battery data with unreasonable values
        battery_data = [
            BatteryData(
                cluster_id="cluster_1",
                timestamp=datetime(2023, 1, 1, 10, 0, 0),
                max_voltage=1500,  # Unreasonable voltage
                min_voltage=-100,  # Unreasonable voltage
                max_temperature=200,  # Unreasonable temperature
                current=5000,  # Unreasonable current
                total_charge=5.0,
                total_discharge=2.0,
                this_charge=0.1,
                this_discharge=0.05
            )
        ]
        
        is_valid, errors = self.validator.validate_battery_data(battery_data)
        assert not is_valid
        assert len(errors) > 0
        assert any("unreasonable" in error.lower() for error in errors)