# Energy Storage Data Processor

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/energy-storage/processor/releases)

A powerful, generic tool for processing energy storage system data files. This tool supports multiple file formats and provides batch processing capabilities with parallel execution.

## ✨ Features

- **📊 Multi-format Support**: Process CSV and Excel files with automatic format detection
- **⚡ Batch Processing**: Handle multiple files or entire directories with parallel execution
- **🔧 Configurable**: YAML-based configuration system for custom data processing rules
- **💻 Command Line Interface**: Easy-to-use CLI with comprehensive options
- **✅ Data Validation**: Built-in data validation and error handling
- **📈 Detailed Reporting**: Comprehensive processing reports and statistics
- **🚀 High Performance**: Multi-threaded/multi-process support for large datasets
- **🔌 Extensible**: Plugin architecture for adding new formats and processing rules

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/energy-storage/processor.git
cd processor

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Basic Usage

```bash
# Process a single file
python main.py process input.csv output/

# Process multiple files
python main.py process file1.csv file2.csv output/

# Process all files in a directory
python main.py batch --dir input_directory/ output_directory/

# Process directory recursively
python main.py batch --dir input_directory/ output_directory/ --recursive

# Use custom configuration
python main.py batch --dir input_directory/ output_directory/ --config custom_config.yaml

# Show help
python main.py --help
```

## 📋 Configuration

The tool uses YAML configuration files to define data formats and processing rules. Default configuration is provided in `configs/default.yaml`.

### Example Configuration

```yaml
# configs/default.yaml
data_format:
  time_columns:
    - timestamp
    - occurTime
    - time
  voltage_columns:
    - maxU
    - minU
    - voltage
    - voltage_
  temperature_columns:
    - maxT
    - minT
    - temp
    - temperature
  current_columns:
    - current
    - current_
  charge_columns:
    - charge
    - totalChargeKwh
    - charge_
  discharge_columns:
    - discharge
    - totalDischargeKwh
    - discharge_

calculation_rules:
  system_voltage:
    max: true
    min: true
    diff: true
    diff_multiplier: 1000
  system_temperature:
    max: true
  energy_balance:
    charge: true
    discharge: true

parallel_settings:
  max_workers: 4
  chunk_size: 1000
  enable_multiprocessing: false

output_settings:
  format: excel
  filename: "Processed_Data"
  highlight_calculated: true
```

### System-Specific Configurations

```bash
# Initialize EVE2502 configuration
python main.py config --init configs/battery_systems/ev2502_config.yaml

# Initialize generic configuration
python main.py config --init configs/battery_systems/my_system_config.yaml
```

## 📖 Detailed Usage

### Command Line Interface

#### Process Command

```bash
python main.py process [OPTIONS] INPUT OUTPUT

Options:
  --name TEXT     Custom output filename
  --config PATH   Configuration file path
  --verbose, -v   Enable verbose logging
  --log-dir PATH  Directory for log files
```

#### Batch Command

```bash
python main.py batch [OPTIONS] OUTPUT

Options:
  --files FILES   List of input files
  --dir PATH      Input directory
  --recursive     Process subdirectories recursively
  --patterns PATTERNS  File patterns to match (e.g., "*.csv")
  --prefix TEXT   Custom output filename prefix
  --config PATH   Configuration file path
  --verbose, -v   Enable verbose logging
  --log-dir PATH  Directory for log files
```

#### Config Command

```bash
python main.py config [OPTIONS]

Options:
  --show          Show current configuration
  --init PATH     Initialize new configuration file
  --validate PATH Validate configuration file
```

#### Info Command

```bash
python main.py info [OPTIONS]

Options:
  --formats       Show supported file formats
  --config-template  Show configuration template
```

### Programmatic Usage

```python
from src.config import Config
from src.core.processor import Processor

# Create processor
config = Config()
processor = Processor(config)

# Process a file
result = processor.process_file("input.csv", "output/")
if result.success:
    print(f"Processed successfully: {result.output_file}")
else:
    print(f"Error: {result.error_message}")

# Process directory
results = processor.process_directory("input_dir/", "output_dir/")
summary = processor.get_processing_summary(results)
print(f"Processed {summary['successful_files']}/{summary['total_files']} files")
```

## 📊 Sample Data Format

### CSV Input Format

```csv
occurTime,bms_maxU_1,bms_minU_1,bms_maxT_1,bms_current_1,bms_totalChargeKwh_1,bms_totalDischargeKwh_1
2023-01-01 10:00:00,4.2,3.8,25.0,10.0,5.0,2.0
2023-01-01 10:01:00,4.3,3.9,25.5,10.5,5.1,2.1
2023-01-01 10:02:00,4.1,3.7,24.8,9.8,4.9,1.9
```

### Expected Excel Output Format

The output includes:
- Original data columns from all clusters
- System calculations:
  - `sysMaxU`: System maximum voltage
  - `sysMinU`: System minimum voltage
  - `MaxDiff`: Voltage difference (in mV)
  - `sysMaxT`: System maximum temperature
  - `DayTotalChargeKwh`: Total daily charge
  - `DayTotalDischargeKwh`: Total daily discharge

## 🔧 Configuration Examples

### Basic Configuration

```yaml
# configs/basic_config.yaml
data_format:
  time_columns:
    - timestamp
    - occurTime
  voltage_columns:
    - maxU
    - minU
    - voltage
  temperature_columns:
    - maxT
    - minT
  current_columns:
    - current
  charge_columns:
    - charge
    - totalChargeKwh
  discharge_columns:
    - discharge
    - totalDischargeKwh

calculation_rules:
  system_voltage:
    max: true
    min: true
    diff: true
  system_temperature:
    max: true
  energy_balance:
    charge: true
    discharge: true

parallel_settings:
  max_workers: 4
  chunk_size: 1000
  enable_multiprocessing: false

output_settings:
  format: excel
  filename: "Processed_Data"
  highlight_calculated: true
```

### Advanced Configuration

```yaml
# configs/advanced_config.yaml
data_format:
  time_columns:
    - timestamp
    - occurTime
    - time
    - datetime
  voltage_columns:
    - maxU
    - minU
    - voltage
    - voltage_
  temperature_columns:
    - maxT
    - minT
    - temp
    - temperature
  current_columns:
    - current
    - current_
    - i_
  charge_columns:
    - charge
    - totalChargeKwh
    - totalcharge_
    - thisChargeKwh
  discharge_columns:
    - discharge
    - totalDischargeKwh
    - totaldischarge_
    - thisDischargeKwh

calculation_rules:
  system_voltage:
    max: true
    min: true
    diff: true
    diff_multiplier: 1000
  system_temperature:
    max: true
    min: false
  energy_balance:
    charge: true
    discharge: true
    daily_calculation: true

parallel_settings:
  max_workers: 8
  chunk_size: 2000
  enable_multiprocessing: true

output_settings:
  format: excel
  filename: "SystemData"
  highlight_calculated: true

processors:
  extractor:
    filename_patterns:
      - "*bms*"
      - "*BMS*"
      - "*cluster*"
    column_patterns:
      time: "(?i)occur.*time|timestamp|time"
      voltage: "(?i)max.*u|min.*u|voltage|volt"
      temperature: "(?i)max.*t|min.*t|temp|temperature"
      current: "(?i)current|i|amp"
      charge: "(?i)charge|totalcharge|thischarge"
      discharge: "(?i)discharge|totaldischarge|thisdischarge"
  
  calculator:
    system_voltage:
      max: true
      min: true
      diff: true
      diff_multiplier: 1000
    system_temperature:
      max: true
    energy_balance:
      charge: true
      discharge: true
      daily_calculation: true
    insertion_rules:
      sys_max_u_after: "maxU"
      sys_min_u_after: "minU"
      max_diff_after: "sysMinU"
      sys_max_t_after: "maxT"
      day_charge_after: "charge"
      day_discharge_after: "discharge"
```

## 🚀 Performance Optimization

### For Large Datasets

```yaml
# configs/performance_config.yaml
parallel_settings:
  max_workers: 8          # Match CPU cores
  chunk_size: 2000       # Larger chunks for better throughput
  enable_multiprocessing: true  # Use multiple processes for CPU-intensive tasks
```

### For Memory-Constrained Systems

```yaml
# configs/memory_config.yaml
parallel_settings:
  max_workers: 2          # Fewer workers to reduce memory usage
  chunk_size: 500        # Smaller chunks for better memory management
  enable_multiprocessing: false  # Use threads instead of processes
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Error**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **File Not Found**: Check file paths and permissions
   ```bash
   python main.py process input.csv output/
   ```

3. **Memory Issues**: Reduce chunk size or enable multiprocessing
   ```yaml
   parallel_settings:
     max_workers: 4
     chunk_size: 500
     enable_multiprocessing: true
   ```

4. **Configuration Error**: Validate YAML syntax
   ```bash
   python main.py config --validate my_config.yaml
   ```

### Debug Mode

Enable verbose logging for debugging:
```bash
python main.py --verbose process input.csv output/
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_processors.py

# Run functionality test
python test_functionality.py

# Validate project structure
python validate_structure.py
```

## 📊 API Reference

### Core Classes

#### Config
Configuration management class.
```python
from src.config import Config

config = Config("config.yaml")
print(config.get_output_format())
print(config.get_max_workers())
```

#### Processor
Main processing orchestrator.
```python
from src.core.processor import Processor

processor = Processor(config)
result = processor.process_file("input.csv", "output/")
```

### Data Models

#### ProcessingResult
Result of a processing operation.
```python
@dataclass
class ProcessingResult:
    input_file: str
    output_file: str
    success: bool
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    records_processed: int = 0
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [pandas](https://pandas.pydata.org/) for data manipulation
- Uses [PyYAML](https://pyyaml.org/) for configuration management
- Leverages [openpyxl](https://openpyxl.readthedocs.io/) for Excel file handling

## 📞 Support

- 📧 Email: support@energystorage.com
- 🐛 Issues: [GitHub Issues](https://github.com/energy-storage/processor/issues)
- 📖 Documentation: [Documentation](https://energy-storage-processor.readthedocs.io/)

## 🗺️ Roadmap

- [ ] Web-based interface
- [ ] Real-time data processing
- [ ] Cloud deployment options
- [ ] Additional output formats (JSON, Parquet)
- [ ] Advanced visualization features

---

**Made with ❤️ for the energy storage community**