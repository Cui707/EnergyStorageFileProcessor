"""
Configuration models for the energy storage processor.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from pathlib import Path


@dataclass
class DataFormatConfig:
    """Configuration for data format specifications."""
    
    time_columns: List[str]
    voltage_columns: List[str]
    temperature_columns: List[str]
    current_columns: List[str]
    charge_columns: List[str]
    discharge_columns: List[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataFormatConfig':
        """Create from dictionary."""
        return cls(
            time_columns=data.get('time_columns', []),
            voltage_columns=data.get('voltage_columns', []),
            temperature_columns=data.get('temperature_columns', []),
            current_columns=data.get('current_columns', []),
            charge_columns=data.get('charge_columns', []),
            discharge_columns=data.get('discharge_columns', [])
        )


@dataclass
class CalculationRulesConfig:
    """Configuration for calculation rules."""
    
    system_voltage: Dict[str, Any]
    system_temperature: Dict[str, Any]
    energy_balance: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CalculationRulesConfig':
        """Create from dictionary."""
        return cls(
            system_voltage=data.get('system_voltage', {}),
            system_temperature=data.get('system_temperature', {}),
            energy_balance=data.get('energy_balance', {})
        )


@dataclass
class ParallelSettingsConfig:
    """Configuration for parallel processing settings."""
    
    max_workers: int
    chunk_size: int
    enable_multiprocessing: bool
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ParallelSettingsConfig':
        """Create from dictionary."""
        return cls(
            max_workers=data.get('max_workers', 4),
            chunk_size=data.get('chunk_size', 1000),
            enable_multiprocessing=data.get('enable_multiprocessing', False)
        )


@dataclass
class OutputSettingsConfig:
    """Configuration for output settings."""
    
    format: str
    filename: str
    highlight_calculated: bool
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OutputSettingsConfig':
        """Create from dictionary."""
        return cls(
            format=data.get('format', 'excel'),
            filename=data.get('filename', 'Processed_Data'),
            highlight_calculated=data.get('highlight_calculated', True)
        )


@dataclass
class ReaderSettingsConfig:
    """Configuration for reader settings."""
    
    csv: Dict[str, Any]
    excel: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReaderSettingsConfig':
        """Create from dictionary."""
        return cls(
            csv=data.get('csv', {}),
            excel=data.get('excel', {})
        )


@dataclass
class ProcessorSettingsConfig:
    """Configuration for processor settings."""
    
    extractor: Dict[str, Any]
    calculator: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProcessorSettingsConfig':
        """Create from dictionary."""
        return cls(
            extractor=data.get('extractor', {}),
            calculator=data.get('calculator', {})
        )


@dataclass
class FullConfig:
    """Full configuration for the processor."""
    
    data_format: DataFormatConfig
    calculation_rules: CalculationRulesConfig
    parallel_settings: ParallelSettingsConfig
    output_settings: OutputSettingsConfig
    reader_settings: ReaderSettingsConfig
    processor_settings: ProcessorSettingsConfig
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FullConfig':
        """Create from dictionary."""
        return cls(
            data_format=DataFormatConfig.from_dict(data.get('data_format', {})),
            calculation_rules=CalculationRulesConfig.from_dict(data.get('calculation_rules', {})),
            parallel_settings=ParallelSettingsConfig.from_dict(data.get('parallel_settings', {})),
            output_settings=OutputSettingsConfig.from_dict(data.get('output_settings', {})),
            reader_settings=ReaderSettingsConfig.from_dict(data.get('readers', {})),
            processor_settings=ProcessorSettingsConfig.from_dict(data.get('processors', {}))
        )