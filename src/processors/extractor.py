"""
Data extractor for extracting relevant information from raw data.
"""

import re
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from ..models.data_models import BatteryData
from ..config import Config


class DataExtractor:
    """Extract relevant data from raw data files."""
    
    def __init__(self, config: Config):
        """
        Initialize the data extractor.
        
        Args:
            config: Configuration instance
        """
        self.config = config
        self.filename_patterns = config.get_filename_patterns()
        self.column_patterns = config.get_column_patterns()
    
    def should_process_file(self, filename: str) -> bool:
        """
        Check if file should be processed based on filename patterns.
        
        Args:
            filename: Name of the file to check
            
        Returns:
            True if file should be processed
        """
        import fnmatch
        
        for pattern in self.filename_patterns:
            if fnmatch.fnmatch(filename, pattern):
                return True
        
        return False
    
    def extract_columns_by_pattern(self, df: pd.DataFrame, pattern: str) -> List[str]:
        """
        Extract columns matching a specific pattern.
        
        Args:
            df: DataFrame to search
            pattern: Regular expression pattern to match
            
        Returns:
            List of matching column names
        """
        try:
            return [col for col in df.columns if re.search(pattern, col, re.IGNORECASE)]
        except Exception:
            return []
    
    def extract_time_columns(self, df: pd.DataFrame) -> List[str]:
        """Extract time-related columns."""
        patterns = self.column_patterns.get('time', '')
        if isinstance(patterns, str):
            patterns = [patterns]
        
        matching_columns = []
        for pattern in patterns:
            matching_columns.extend(self.extract_columns_by_pattern(df, pattern))
        
        return list(set(matching_columns))
    
    def extract_voltage_columns(self, df: pd.DataFrame) -> List[str]:
        """Extract voltage-related columns."""
        patterns = self.column_patterns.get('voltage', '')
        if isinstance(patterns, str):
            patterns = [patterns]
        
        matching_columns = []
        for pattern in patterns:
            matching_columns.extend(self.extract_columns_by_pattern(df, pattern))
        
        return list(set(matching_columns))
    
    def extract_temperature_columns(self, df: pd.DataFrame) -> List[str]:
        """Extract temperature-related columns."""
        patterns = self.column_patterns.get('temperature', '')
        if isinstance(patterns, str):
            patterns = [patterns]
        
        matching_columns = []
        for pattern in patterns:
            matching_columns.extend(self.extract_columns_by_pattern(df, pattern))
        
        return list(set(matching_columns))
    
    def extract_current_columns(self, df: pd.DataFrame) -> List[str]:
        """Extract current-related columns."""
        patterns = self.column_patterns.get('current', '')
        if isinstance(patterns, str):
            patterns = [patterns]
        
        matching_columns = []
        for pattern in patterns:
            matching_columns.extend(self.extract_columns_by_pattern(df, pattern))
        
        return list(set(matching_columns))
    
    def extract_charge_columns(self, df: pd.DataFrame) -> List[str]:
        """Extract charge-related columns."""
        patterns = self.column_patterns.get('charge', '')
        if isinstance(patterns, str):
            patterns = [patterns]
        
        matching_columns = []
        for pattern in patterns:
            matching_columns.extend(self.extract_columns_by_pattern(df, pattern))
        
        return list(set(matching_columns))
    
    def extract_discharge_columns(self, df: pd.DataFrame) -> List[str]:
        """Extract discharge-related columns."""
        patterns = self.column_patterns.get('discharge', '')
        if isinstance(patterns, str):
            patterns = [patterns]
        
        matching_columns = []
        for pattern in patterns:
            matching_columns.extend(self.extract_columns_by_pattern(df, pattern))
        
        return list(set(matching_columns))
    
    def extract_battery_data(self, df: pd.DataFrame, cluster_id: str) -> List[BatteryData]:
        """
        Extract battery data from DataFrame.
        
        Args:
            df: DataFrame containing battery data
            cluster_id: ID of the battery cluster
            
        Returns:
            List of BatteryData objects
        """
        battery_data = []
        
        # Extract columns
        time_columns = self.extract_time_columns(df)
        voltage_columns = self.extract_voltage_columns(df)
        temperature_columns = self.extract_temperature_columns(df)
        current_columns = self.extract_current_columns(df)
        charge_columns = self.extract_charge_columns(df)
        discharge_columns = self.extract_discharge_columns(df)
        
        # If no time columns found, use DataFrame index
        if not time_columns:
            time_data = df.index
        else:
            time_data = df[time_columns[0]] if time_columns else df.index
        
        # Process each row
        for idx, row in df.iterrows():
            try:
                # Parse time
                if len(time_columns) > 0:
                    timestamp = pd.to_datetime(row[time_columns[0]])
                else:
                    timestamp = pd.to_datetime('now')
                
                # Extract values
                max_voltage = self._extract_max_value(row, voltage_columns) if voltage_columns else 0.0
                min_voltage = self._extract_min_value(row, voltage_columns) if voltage_columns else 0.0
                max_temperature = self._extract_max_value(row, temperature_columns) if temperature_columns else 0.0
                current = self._extract_value(row, current_columns) if current_columns else 0.0
                total_charge = self._extract_value(row, charge_columns) if charge_columns else 0.0
                total_discharge = self._extract_value(row, discharge_columns) if discharge_columns else 0.0
                this_charge = self._extract_value(row, [c for c in charge_columns if 'this' in c.lower()]) if charge_columns else 0.0
                this_discharge = self._extract_value(row, [c for c in discharge_columns if 'this' in c.lower()]) if discharge_columns else 0.0
                
                # Create BatteryData object
                battery = BatteryData(
                    cluster_id=cluster_id,
                    timestamp=timestamp,
                    max_voltage=max_voltage,
                    min_voltage=min_voltage,
                    max_temperature=max_temperature,
                    current=current,
                    total_charge=total_charge,
                    total_discharge=total_discharge,
                    this_charge=this_charge,
                    this_discharge=this_discharge
                )
                
                battery_data.append(battery)
                
            except Exception as e:
                # Skip rows with errors
                continue
        
        return battery_data
    
    def _extract_max_value(self, row: pd.Series, columns: List[str]) -> float:
        """Extract maximum value from specified columns."""
        if not columns:
            return 0.0
        
        values = []
        for col in columns:
            if col in row and pd.notna(row[col]):
                try:
                    values.append(float(row[col]))
                except (ValueError, TypeError):
                    continue
        
        return max(values) if values else 0.0
    
    def _extract_min_value(self, row: pd.Series, columns: List[str]) -> float:
        """Extract minimum value from specified columns."""
        if not columns:
            return 0.0
        
        values = []
        for col in columns:
            if col in row and pd.notna(row[col]):
                try:
                    values.append(float(row[col]))
                except (ValueError, TypeError):
                    continue
        
        return min(values) if values else 0.0
    
    def _extract_value(self, row: pd.Series, columns: List[str]) -> float:
        """Extract value from specified columns."""
        if not columns:
            return 0.0
        
        for col in columns:
            if col in row and pd.notna(row[col]):
                try:
                    return float(row[col])
                except (ValueError, TypeError):
                    continue
        
        return 0.0