"""
Data models for the energy storage processor.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class BatteryData:
    """Represents battery data from a single cluster."""
    
    cluster_id: str
    timestamp: datetime
    max_voltage: float
    min_voltage: float
    max_temperature: float
    current: float
    total_charge: float
    total_discharge: float
    this_charge: float
    this_discharge: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'cluster_id': self.cluster_id,
            'timestamp': self.timestamp,
            'max_voltage': self.max_voltage,
            'min_voltage': self.min_voltage,
            'max_temperature': self.max_temperature,
            'current': self.current,
            'total_charge': self.total_charge,
            'total_discharge': self.total_discharge,
            'this_charge': self.this_charge,
            'this_discharge': self.this_discharge
        }


@dataclass
class ProcessedData:
    """Represents processed data from multiple clusters."""
    
    cluster_data: List[BatteryData]
    system_max_voltage: float
    system_min_voltage: float
    voltage_diff: float
    system_max_temperature: float
    day_total_charge: float
    day_total_discharge: float
    
    def to_dataframe(self):
        """Convert to pandas DataFrame."""
        import pandas as pd
        
        # Create cluster data DataFrame
        cluster_dfs = []
        for data in self.cluster_data:
            cluster_df = pd.DataFrame([data.to_dict()])
            for col in cluster_df.columns:
                cluster_df[f'cluster_{data.cluster_id}_{col}'] = cluster_df[col]
                cluster_df = cluster_df.drop(col, axis=1)
            cluster_dfs.append(cluster_df)
        
        # Merge cluster data
        if cluster_dfs:
            result_df = pd.concat(cluster_dfs, axis=1)
        else:
            result_df = pd.DataFrame()
        
        # Add system calculations
        system_data = {
            'system_max_voltage': self.system_max_voltage,
            'system_min_voltage': self.system_min_voltage,
            'voltage_diff': self.voltage_diff,
            'system_max_temperature': self.system_max_temperature,
            'day_total_charge': self.day_total_charge,
            'day_total_discharge': self.day_total_discharge
        }
        
        for key, value in system_data.items():
            result_df[key] = value
        
        return result_df


@dataclass
class ProcessingResult:
    """Represents the result of data processing."""
    
    input_file: str
    output_file: str
    success: bool
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    records_processed: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'input_file': self.input_file,
            'output_file': self.output_file,
            'success': self.success,
            'error_message': self.error_message,
            'processing_time': self.processing_time,
            'records_processed': self.records_processed
        }