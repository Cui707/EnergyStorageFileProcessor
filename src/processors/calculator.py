"""
Data calculator for performing calculations on battery data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from ..models.data_models import BatteryData, ProcessedData
from ..config import Config


class DataCalculator:
    """Calculate system-level statistics from battery data."""
    
    def __init__(self, config: Config):
        """
        Initialize the data calculator.
        
        Args:
            config: Configuration instance
        """
        self.config = config
        self.calculation_rules = config.get_calculation_rules()
        self.insertion_rules = config.processor_settings.get('calculator', {}).get('insertion_rules', {})
    
    def calculate_system_statistics(self, battery_data: List[BatteryData]) -> ProcessedData:
        """
        Calculate system-level statistics from battery data.
        
        Args:
            battery_data: List of BatteryData objects
            
        Returns:
            ProcessedData object with calculated statistics
        """
        if not battery_data:
            return ProcessedData(
                cluster_data=[],
                system_max_voltage=0.0,
                system_min_voltage=0.0,
                voltage_diff=0.0,
                system_max_temperature=0.0,
                day_total_charge=0.0,
                day_total_discharge=0.0
            )
        
        # Extract data for calculations
        timestamps = [data.timestamp for data in battery_data]
        max_voltages = [data.max_voltage for data in battery_data]
        min_voltages = [data.min_voltage for data in battery_data]
        max_temperatures = [data.max_temperature for data in battery_data]
        total_charges = [data.total_charge for data in battery_data]
        total_discharges = [data.total_discharge for data in battery_data]
        this_charges = [data.this_charge for data in battery_data]
        this_discharges = [data.this_discharge for data in battery_data]
        
        # Calculate system voltage statistics
        system_max_voltage = max(max_voltages) if max_voltages else 0.0
        system_min_voltage = min(min_voltages) if min_voltages else 0.0
        
        # Apply voltage difference multiplier if specified
        voltage_diff_multiplier = self.calculation_rules.get('system_voltage', {}).get('diff_multiplier', 1)
        voltage_diff = (system_max_voltage - system_min_voltage) * voltage_diff_multiplier
        
        # Calculate system temperature statistics
        system_max_temperature = max(max_temperatures) if max_temperatures else 0.0
        
        # Calculate energy balance
        day_total_charge = self._calculate_daily_energy(this_charges)
        day_total_discharge = self._calculate_daily_energy(this_discharges)
        
        # Group data by cluster
        cluster_data = self._group_by_cluster(battery_data)
        
        return ProcessedData(
            cluster_data=cluster_data,
            system_max_voltage=system_max_voltage,
            system_min_voltage=system_min_voltage,
            voltage_diff=voltage_diff,
            system_max_temperature=system_max_temperature,
            day_total_charge=day_total_charge,
            day_total_discharge=day_total_discharge
        )
    
    def _calculate_daily_energy(self, energy_values: List[float]) -> float:
        """
        Calculate daily energy from energy values.
        
        Args:
            energy_values: List of energy values
            
        Returns:
            Daily energy total
        """
        if not energy_values:
            return 0.0
        
        # If we have multiple values, sum them up
        # This assumes energy_values contains cumulative values
        return sum(energy_values)
    
    def _group_by_cluster(self, battery_data: List[BatteryData]) -> List[BatteryData]:
        """
        Group battery data by cluster ID.
        
        Args:
            battery_data: List of BatteryData objects
            
        Returns:
            List of BatteryData objects grouped by cluster
        """
        # For now, return the original data
        # In a more complex implementation, we might want to group by cluster
        # and calculate cluster-specific statistics
        return battery_data
    
    def add_calculated_columns(self, df: pd.DataFrame, processed_data: ProcessedData) -> pd.DataFrame:
        """
        Add calculated columns to the DataFrame.
        
        Args:
            df: Original DataFrame
            processed_data: Processed data with calculated statistics
            
        Returns:
            DataFrame with added calculated columns
        """
        # Get calculation rules
        system_voltage_rules = self.calculation_rules.get('system_voltage', {})
        system_temperature_rules = self.calculation_rules.get('system_temperature', {})
        energy_balance_rules = self.calculation_rules.get('energy_balance', {})
        
        # Add system voltage columns
        if system_voltage_rules.get('max', False):
            df = self._insert_column(df, 'sysMaxU', processed_data.system_max_voltage, 
                                   self.insertion_rules.get('sys_max_u_after'))
        
        if system_voltage_rules.get('min', False):
            df = self._insert_column(df, 'sysMinU', processed_data.system_min_voltage,
                                   self.insertion_rules.get('sys_min_u_after'))
        
        if system_voltage_rules.get('diff', False):
            df = self._insert_column(df, 'MaxDiff', processed_data.voltage_diff,
                                   self.insertion_rules.get('max_diff_after'))
        
        # Add system temperature columns
        if system_temperature_rules.get('max', False):
            df = self._insert_column(df, 'sysMaxT', processed_data.system_max_temperature,
                                   self.insertion_rules.get('sys_max_t_after'))
        
        # Add energy balance columns
        if energy_balance_rules.get('charge', False):
            df = self._insert_column(df, 'DayTotalChargeKwh', processed_data.day_total_charge,
                                   self.insertion_rules.get('day_charge_after'))
        
        if energy_balance_rules.get('discharge', False):
            df = self._insert_column(df, 'DayTotalDischargeKwh', processed_data.day_total_discharge,
                                   self.insertion_rules.get('day_discharge_after'))
        
        return df
    
    def _insert_column(self, df: pd.DataFrame, column_name: str, value: float, 
                      after_column: Optional[str] = None) -> pd.DataFrame:
        """
        Insert a column into the DataFrame.
        
        Args:
            df: DataFrame to modify
            column_name: Name of the new column
            value: Value for the new column
            after_column: Name of column to insert after
            
        Returns:
            Modified DataFrame
        """
        # Create the new column
        df[column_name] = value
        
        if after_column and after_column in df.columns:
            # Move column after specified column
            col_index = df.columns.get_loc(after_column)
            df.insert(col_index + 1, column_name, df.pop(column_name))
        
        return df