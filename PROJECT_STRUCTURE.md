# Energy Storage Data Processor - Project Structure

```
energy_storage_processor/
├── src/                          # Source code directory
│   ├── __init__.py               # Package initialization
│   ├── cli.py                    # Command line interface
│   ├── config.py                 # Configuration management
│   ├── core/                     # Core processing modules
│   │   ├── __init__.py
│   │   ├── processor.py          # Main processor orchestrator
│   │   ├── data_processor.py     # Single file processor
│   │   └── batch_processor.py    # Batch processor
│   ├── readers/                  # File reader modules
│   │   ├── __init__.py
│   │   ├── base.py               # Base reader class
│   │   ├── csv_reader.py         # CSV file reader
│   │   ├── excel_reader.py       # Excel file reader
│   │   └── factory.py            # Reader factory
│   ├── processors/               # Data processing modules
│   │   ├── __init__.py
│   │   ├── extractor.py          # Data extraction
│   │   ├── calculator.py         # Data calculation
│   │   └── validator.py         # Data validation
│   ├── writers/                  # File writer modules
│   │   ├── __init__.py
│   │   ├── base.py               # Base writer class
│   │   ├── excel_writer.py       # Excel file writer
│   │   ├── csv_writer.py         # CSV file writer
│   │   └── factory.py            # Writer factory
│   ├── utils/                    # Utility modules
│   │   ├── __init__.py
│   │   ├── file_utils.py         # File handling utilities
│   │   ├── parallel.py           # Parallel processing utilities
│   │   └── logger.py             # Logging utilities
│   └── models/                   # Data models
│       ├── __init__.py
│       ├── data_models.py        # Data models
│       └── config_models.py      # Configuration models
├── configs/                      # Configuration files directory
│   ├── default.yaml              # Default configuration
│   ├── readers.yaml              # Reader configuration
│   ├── processors.yaml           # Processor configuration
│   └── battery_systems/          # Battery system specific configs
│       ├── ev2502_example.yaml   # EVE2502 example configuration
│       └── generic.yaml          # Generic configuration
├── tests/                        # Test files directory
│   ├── __init__.py
│   ├── test_config.py            # Configuration tests
│   ├── test_readers.py           # Reader tests
│   └── test_processors.py        # Processor tests
├── main.py                       # Main entry point
├── setup.py                      # Package setup script
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── INSTALL.md                    # Installation guide
├── test_functionality.py         # Functionality test script
├── example_usage.py              # Programmatic usage examples
├── quick_start.bat               # Windows quick start script
└── .gitignore                    # Git ignore file
```

## Key Components

### 1. Core Modules (`src/core/`)
- **processor.py**: Main orchestrator that coordinates all operations
- **data_processor.py**: Handles single file processing
- **batch_processor.py**: Handles batch processing with parallel execution

### 2. Data Readers (`src/readers/`)
- **base.py**: Abstract base class for all readers
- **csv_reader.py**: CSV file reader with configurable options
- **excel_reader.py**: Excel file reader (supports .xlsx and .xls)
- **factory.py**: Factory pattern for creating appropriate readers

### 3. Data Processors (`src/processors/`)
- **extractor.py**: Extracts relevant data from raw files based on patterns
- **calculator.py**: Performs system-level calculations (voltage, temperature, energy)
- **validator.py**: Validates data integrity and consistency

### 4. Data Writers (`src/writers/`)
- **base.py**: Abstract base class for all writers
- **excel_writer.py**: Excel file writer with formatting support
- **csv_writer.py**: CSV file writer with configurable options
- **factory.py**: Factory pattern for creating appropriate writers

### 5. Utilities (`src/utils/`)
- **file_utils.py**: File handling utilities (copy, move, find, etc.)
- **parallel.py**: Parallel processing utilities with thread/process pool management
- **logger.py**: Logging utilities with configurable output

### 6. Models (`src/models/`)
- **data_models.py**: Data models for battery data and processing results
- **config_models.py**: Configuration models for type-safe configuration handling

### 7. Configuration (`configs/`)
- **default.yaml**: Default configuration for processing
- **readers.yaml**: Reader-specific configuration
- **processors.yaml**: Processor-specific configuration
- **battery_systems/**: System-specific configurations (EVE2502, generic, etc.)

## Design Patterns Used

1. **Factory Pattern**: For creating readers and writers based on file type
2. **Strategy Pattern**: For different processing strategies
3. **Observer Pattern**: For logging and progress tracking
4. **Template Method**: For base classes with customizable implementations
5. **Command Pattern**: For command line interface

## Key Features

1. **Multi-format Support**: CSV and Excel files
2. **Batch Processing**: Parallel processing of multiple files
3. **Configurable**: YAML-based configuration system
4. **Extensible**: Plugin architecture for adding new formats
5. **Error Handling**: Comprehensive error handling and logging
6. **Validation**: Built-in data validation
7. **Reporting**: Detailed processing reports and statistics

## Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **PyYAML**: YAML configuration parsing
- **openpyxl**: Excel file handling
- **click**: Command line interface (optional)
- **tqdm**: Progress bars

## Installation

The project can be installed using pip:
```bash
pip install -e .
```

## Usage

### Command Line Interface
```bash
# Process single file
python main.py process input.csv output/

# Process multiple files
python main.py process file1.csv file2.csv output/

# Process directory
python main.py batch --dir input_dir/ output_dir/

# Use custom configuration
python main.py batch --dir input_dir/ output_dir/ --config custom_config.yaml
```

### Programmatic Usage
```python
from src.config import Config
from src.core.processor import Processor

# Create processor
config = Config()
processor = Processor(config)

# Process file
result = processor.process_file("input.csv", "output/")
```

## Configuration System

The configuration system uses YAML files to define:
- Data formats and column patterns
- Calculation rules
- Parallel processing settings
- Output formatting options

## Testing

The project includes comprehensive tests:
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_processors.py

# Run functionality test
python test_functionality.py
```

## Extensibility

The project is designed to be extensible:
- Add new file formats by extending BaseReader/BaseWriter
- Add new processing rules by modifying configuration
- Add new calculations by extending DataCalculator
- Add new output formats by implementing new writers

## Performance

The project supports:
- Multi-threaded processing for I/O-bound tasks
- Multi-process processing for CPU-bound tasks
- Configurable chunk sizes for memory management
- Progress tracking for large batches

## Error Handling

Comprehensive error handling includes:
- File validation before processing
- Data validation during processing
- Graceful handling of corrupt files
- Detailed error logging
- Progress reporting with failure information

## Logging

Configurable logging system supports:
- Console output
- File output with timestamps
- Verbose mode for debugging
- Progress tracking
- Error reporting

This architecture provides a solid foundation for a robust, maintainable, and extensible energy storage data processing tool.