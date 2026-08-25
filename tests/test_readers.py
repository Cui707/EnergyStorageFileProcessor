"""
Tests for data readers.
"""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path

from src.readers.csv_reader import CSVReader
from src.readers.excel_reader import ExcelReader
from src.readers.factory import ReaderFactory


class TestCSVReader:
    """Test CSV reader functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = {
            'encoding': 'utf-8',
            'delimiter': ',',
            'skip_rows': 0,
            'header_row': 0
        }
        self.reader = CSVReader(self.config)
    
    def test_read_valid_csv(self):
        """Test reading a valid CSV file."""
        # Create test CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("timestamp,maxU,minU,maxT,current\n")
            f.write("2023-01-01 10:00:00,4.2,3.8,25.0,10.0\n")
            f.write("2023-01-01 10:01:00,4.3,3.9,25.5,10.5\n")
            temp_file = f.name
        
        try:
            # Read CSV file
            df = self.reader.read(temp_file)
            
            # Validate DataFrame
            assert not df.empty
            assert len(df.columns) == 5
            assert len(df) == 2
            assert 'timestamp' in df.columns
            assert 'maxU' in df.columns
            assert 'minU' in df.columns
            assert 'maxT' in df.columns
            assert 'current' in df.columns
            
        finally:
            os.unlink(temp_file)
    
    def test_read_invalid_csv(self):
        """Test reading an invalid CSV file."""
        # Create invalid CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("invalid,csv,content\n")
            f.write("test,data\n")
            temp_file = f.name
        
        try:
            # Read CSV file
            df = self.reader.read(temp_file)
            
            # Validate DataFrame
            assert not df.empty
            assert len(df.columns) == 3
            
        finally:
            os.unlink(temp_file)
    
    def test_validate_empty_dataframe(self):
        """Test validation of empty DataFrame."""
        df = pd.DataFrame()
        is_valid = self.reader.validate(df)
        assert not is_valid
    
    def test_validate_valid_dataframe(self):
        """Test validation of valid DataFrame."""
        df = pd.DataFrame({
            'timestamp': ['2023-01-01 10:00:00', '2023-01-01 10:01:00'],
            'maxU': [4.2, 4.3],
            'minU': [3.8, 3.9],
            'maxT': [25.0, 25.5],
            'current': [10.0, 10.5]
        })
        
        is_valid = self.reader.validate(df)
        assert is_valid
    
    def test_get_supported_extensions(self):
        """Test getting supported extensions."""
        extensions = self.reader.get_supported_extensions()
        assert 'csv' in extensions


class TestExcelReader:
    """Test Excel reader functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = {
            'sheet_name': 0,
            'header_row': 0,
            'skip_rows': 0
        }
        self.reader = ExcelReader(self.config)
    
    def test_read_valid_excel(self):
        """Test reading a valid Excel file."""
        # Create test Excel file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_file = f.name
        
        try:
            # Create DataFrame and save to Excel
            df = pd.DataFrame({
                'timestamp': ['2023-01-01 10:00:00', '2023-01-01 10:01:00'],
                'maxU': [4.2, 4.3],
                'minU': [3.8, 3.9],
                'maxT': [25.0, 25.5],
                'current': [10.0, 10.5]
            })
            df.to_excel(temp_file, index=False)
            
            # Read Excel file
            df_read = self.reader.read(temp_file)
            
            # Validate DataFrame
            assert not df_read.empty
            assert len(df_read.columns) == 5
            assert len(df_read) == 2
            assert 'timestamp' in df_read.columns
            assert 'maxU' in df_read.columns
            assert 'minU' in df_read.columns
            assert 'maxT' in df_read.columns
            assert 'current' in df_read.columns
            
        finally:
            os.unlink(temp_file)
    
    def test_validate_empty_dataframe(self):
        """Test validation of empty DataFrame."""
        df = pd.DataFrame()
        is_valid = self.reader.validate(df)
        assert not is_valid
    
    def test_get_supported_extensions(self):
        """Test getting supported extensions."""
        extensions = self.reader.get_supported_extensions()
        assert 'xlsx' in extensions
        assert 'xls' in extensions


class TestReaderFactory:
    """Test reader factory functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = {
            'encoding': 'utf-8',
            'delimiter': ',',
            'skip_rows': 0,
            'header_row': 0
        }
    
    def test_create_csv_reader(self):
        """Test creating CSV reader."""
        reader = ReaderFactory.create_reader('csv', self.config)
        assert isinstance(reader, CSVReader)
    
    def test_create_excel_reader(self):
        """Test creating Excel reader."""
        reader = ReaderFactory.create_reader('excel', self.config)
        assert isinstance(reader, ExcelReader)
    
    def test_create_invalid_reader(self):
        """Test creating invalid reader type."""
        with pytest.raises(ValueError):
            ReaderFactory.create_reader('invalid', self.config)
    
    def test_get_supported_types(self):
        """Test getting supported types."""
        types = ReaderFactory.get_supported_types()
        assert 'csv' in types
        assert 'excel' in types
    
    def test_auto_detect_csv(self):
        """Test auto-detecting CSV reader."""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            reader = ReaderFactory.auto_detect_reader(temp_file, self.config)
            assert isinstance(reader, CSVReader)
        finally:
            os.unlink(temp_file)
    
    def test_auto_detect_excel(self):
        """Test auto-detecting Excel reader."""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_file = f.name
        
        try:
            reader = ReaderFactory.auto_detect_reader(temp_file, self.config)
            assert isinstance(reader, ExcelReader)
        finally:
            os.unlink(temp_file)
    
    def test_auto_detect_invalid_extension(self):
        """Test auto-detecting invalid extension."""
        with pytest.raises(ValueError):
            ReaderFactory.auto_detect_reader('invalid.txt', self.config)