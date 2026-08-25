"""
Data validator for validating battery data integrity.
"""

import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from ..models.data_models import BatteryData
from ..config import Config


class DataValidator:
    """Validate battery data for integrity and completeness."""
    
    def __init__(self, config: Config):
        """
        Initialize the data validator.
        
        Args:
            config: Configuration instance
        """
        self.config = config
        self.data_format = config.get_data_format()
    
    def validate_dataframe(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate a DataFrame for data integrity.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check if DataFrame is empty
        if df.empty:
            errors.append("DataFrame is empty")
            return False, errors
        
        # Check if DataFrame has columns
        if len(df.columns) == 0:
            errors.append("DataFrame has no columns")
            return False, errors
        
        # Check for required column types
        self._validate_column_types(df, errors)
        
        # Check for data consistency
        self._validate_data_consistency(df, errors)
        
        # Check for null values
        self._validate_null_values(df, errors)
        
        # Check for reasonable value ranges
        self._validate_value_ranges(df, errors)
        
        return len(errors) == 0, errors
    
    def _validate_column_types(self, df: pd.DataFrame, errors: List[str]):
        """Validate column types."""
        # Check for numeric columns
        numeric_columns = df.select_dtypes(include=['number']).columns
        if len(numeric_columns) == 0:
            errors.append("No numeric columns found")
        
        # Check for time columns
        time_columns = self._find_time_columns(df)
        if len(time_columns) == 0:
            errors.append("No time columns found")
    
    def _validate_data_consistency(self, df: pd.DataFrame, errors: List[str]):
        """Validate data consistency."""
        # Check for duplicate rows
        if df.duplicated().any():
            errors.append("Duplicate rows found")
        
        # Check for consistent data types
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check if object columns contain numeric data
                try:
                    pd.to_numeric(df[col], errors='raise')
                except:
                    pass  # It's okay to have non-numeric data
    
    def _validate_null_values(self, df: pd.DataFrame, errors: List[str]):
        """Validate null values."""
        # Check for excessive null values
        null_threshold = 0.5  # 50% null values threshold
        
        for col in df.columns:
            null_percentage = df[col].isnull().sum() / len(df)
            if null_percentage > null_threshold:
                errors.append(f"Column '{col}' has {null_percentage:.1%} null values")
    
    def _validate_value_ranges(self, df: pd.DataFrame, errors: List[str]):
        """Validate value ranges."""
        # Check voltage values (should be reasonable)
        voltage_columns = self._find_voltage_columns(df)
        for col in voltage_columns:
            if df[col].dtype in ['int64', 'float64']:
                min_voltage = df[col].min()
                max_voltage = df[col].max()
                
                # Voltage should be between 0 and 1000V (reasonable range)
                if min_voltage < 0 or max_voltage > 1000:
                    errors.append(f"Voltage column '{col}' has unreasonable values: {min_voltage}-{max_voltage}")
        
        # Check temperature values (should be reasonable)
        temperature_columns = self._find_temperature_columns(df)
        for col in temperature_columns:
            if df[col].dtype in ['int64', 'float64']:
                min_temp = df[col].min()
                max_temp = df[col].max()
                
                # Temperature should be between -50°C and 100°C (reasonable range)
                if min_temp < -50 or max_temp > 100:
                    errors.append(f"Temperature column '{col}' has unreasonable values: {min_temp}-{max_temp}")
        
        # Check current values (should be reasonable)
        current_columns = self._find_current_columns(df)
        for col in current_columns:
            if df[col].dtype in ['int64', 'float64']:
                max_current = df[col].max()
                
                # Current should be reasonable (not extremely high)
                if abs(max_current) > 1000:  # 1000A threshold
                    errors.append(f"Current column '{col}' has unreasonable value: {max_current}")
    
    def _find_time_columns(self, df: pd.DataFrame) -> List[str]:
        """Find time-related columns."""
        time_keywords = ['time', 'timestamp', 'date', 'occur']
        time_columns = []
        
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in time_keywords):
                time_columns.append(col)
        
        return time_columns
    
    def _find_voltage_columns(self, df: pd.DataFrame) -> List[str]:
        """Find voltage-related columns."""
        voltage_keywords = ['voltage', 'volt', 'u', 'v']
        voltage_columns = []
        
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in voltage_keywords):
                voltage_columns.append(col)
        
        return voltage_columns
    
    def _find_temperature_columns(self, df: pd.DataFrame) -> List[str]:
        """Find temperature-related columns."""
        temp_keywords = ['temp', 'temperature', 't']
        temp_columns = []
        
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in temp_keywords):
                temp_columns.append(col)
        
        return temp_columns
    
    def _find_current_columns(self, df: pd.DataFrame) -> List[str]:
        """Find current-related columns."""
        current_keywords = ['current', 'i', 'amp', 'a']
        current_columns = []
        
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in current_keywords):
                current_columns.append(col)
        
        return current_columns
    
    def validate_battery_data(self, battery_data: List[BatteryData]) -> Tuple[bool, List[str]]:
        """
        Validate battery data objects.
        
        Args:
            battery_data: List of BatteryData objects
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        if not battery_data:
            errors.append("No battery data to validate")
            return False, errors
        
        # Check for consistent cluster IDs
        cluster_ids = [data.cluster_id for data in battery_data]
        if len(set(cluster_ids)) != len(cluster_ids):
            errors.append("Duplicate cluster IDs found")
        
        # Check for reasonable values
        for i, data in enumerate(battery_data):
            if data.max_voltage < 0 or data.max_voltage > 1000:
                errors.append(f"Battery data {i}: unreasonable max voltage {data.max_voltage}")
            
            if data.min_voltage < 0 or data.min_voltage > 1000:
                errors.append(f"Battery data {i}: unreasonable min voltage {data.min_voltage}")
            
            if data.max_temperature < -50 or data.max_temperature > 100:
                errors.append(f"Battery data {i}: unreasonable max temperature {data.max_temperature}")
            
            if abs(data.current) > 1000:
                errors.append(f"Battery data {i}: unreasonable current {data.current}")
        
        return len(errors) == 0, errors