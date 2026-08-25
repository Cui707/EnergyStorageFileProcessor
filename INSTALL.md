# Energy Storage Data Processor - Installation Guide

## Installation Steps

### 1. Install Dependencies

```bash
# Navigate to the project directory
cd energy_storage_processor

# Install required packages
pip install -r requirements.txt
```

### 2. Install the Package

```bash
# Install in development mode
pip install -e .
```

### 3. Verify Installation

```bash
# Test the installation
python test_functionality.py

# Check if CLI is working
python main.py info --formats
```

## Quick Start

### 1. Process a Single File

```bash
# Create a sample CSV file with battery data
echo "timestamp,maxU,minU,maxT,current,charge,discharge" > sample.csv
echo "2023-01-01 10:00:00,4.2,3.8,25.0,10.0,5.0,2.0" >> sample.csv

# Process the file
python main.py process sample.csv output/
```

### 2. Process Multiple Files

```bash
# Process multiple files
python main.py process file1.csv file2.csv file3.csv output/
```

### 3. Process Directory

```bash
# Process all CSV files in a directory
python main.py batch --dir input_directory/ output_directory/

# Process files recursively
python main.py batch --dir input_directory/ output_directory/ --recursive

# Process with custom patterns
python main.py batch --dir input_directory/ output_directory/ --patterns "*.csv" "*.xlsx"
```

### 4. Use Custom Configuration

```bash
# Create custom configuration
python main.py config --init my_config.yaml

# Use custom configuration
python main.py batch --dir input_directory/ output_directory/ --config my_config.yaml
```

## Configuration Examples

### Basic Configuration

```yaml
# configs/my_config.yaml
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
    - occurTime
    - timestamp
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

## Sample Data Format

### CSV Input Format

```csv
occurTime,bms_maxU_1,bms_minU_1,bms_maxT_1,bms_current_1,bms_totalChargeKwh_1,bms_totalDischargeKwh_1
2023-01-01 10:00:00,4.2,3.8,25.0,10.0,5.0,2.0
2023-01-01 10:01:00,4.3,3.9,25.5,10.5,5.1,2.1
2023-01-01 10:02:00,4.1,3.7,24.8,9.8,4.9,1.9
```

### Expected Excel Output Format

The output will include:
- Original data columns
- System calculations:
  - `sysMaxU`: System maximum voltage
  - `sysMinU`: System minimum voltage
  - `MaxDiff`: Voltage difference (in mV)
  - `sysMaxT`: System maximum temperature
  - `DayTotalChargeKwh`: Total daily charge
  - `DayTotalDischargeKwh`: Total daily discharge

## Troubleshooting

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

### Performance Optimization

1. **Increase workers** for CPU-intensive tasks:
   ```yaml
   parallel_settings:
     max_workers: 8
     enable_multiprocessing: true
   ```

2. **Adjust chunk size** based on memory:
   ```yaml
   parallel_settings:
     chunk_size: 2000
   ```

3. **Filter files** to process only relevant data:
   ```bash
   python main.py batch --dir input/ output/ --patterns "*.csv"
   ```

## Getting Help

- Check the README.md for detailed usage instructions
- Run `python main.py --help` for command line options
- Run `python main.py info --config-template` for configuration template
- Test with `python test_functionality.py` to verify installation