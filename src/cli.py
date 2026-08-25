"""
Command line interface for the energy storage processor.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Optional

from .config import Config
from .core.processor import Processor


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description='Energy Storage Data Processor - A tool for processing energy storage system data files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single file
  python -m energy_storage_processor process input.csv output/
  
  # Process multiple files
  python -m energy_storage_processor process file1.csv file2.csv output/
  
  # Process all files in a directory
  python -m energy_storage_processor batch input_dir/ output_dir/
  
  # Process directory with custom configuration
  python -m energy_storage_processor batch input_dir/ output_dir/ --config custom_config.yaml
  
  # Process directory with custom output prefix
  python -m energy_storage_processor batch input_dir/ output_dir/ --prefix processed_
  
  # Show configuration
  python -m energy_storage_processor config --show
  
  # Initialize new configuration
  python -m energy_storage_processor config --init my_config.yaml
        """
    )
    
    # Global options
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--log-dir', type=str, help='Directory for log files')
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Process command (single file)
    process_parser = subparsers.add_parser('process', help='Process a single file')
    process_parser.add_argument('input', type=str, help='Input file path')
    process_parser.add_argument('output', type=str, help='Output directory')
    process_parser.add_argument('--name', type=str, help='Custom output filename')
    
    # Batch command (multiple files)
    batch_parser = subparsers.add_parser('batch', help='Process multiple files or directory')
    batch_group = batch_parser.add_mutually_exclusive_group(required=True)
    batch_group.add_argument('--files', nargs='+', help='List of input files')
    batch_group.add_argument('--dir', type=str, help='Input directory')
    batch_parser.add_argument('output', type=str, help='Output directory')
    batch_parser.add_argument('--recursive', action='store_true', help='Process subdirectories recursively')
    batch_parser.add_argument('--patterns', nargs='+', help='File patterns to match (e.g., "*.csv")')
    batch_parser.add_argument('--prefix', type=str, help='Custom output filename prefix')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configuration management')
    config_parser.add_argument('--show', action='store_true', help='Show current configuration')
    config_parser.add_argument('--init', type=str, help='Initialize new configuration file')
    config_parser.add_argument('--validate', type=str, help='Validate configuration file')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show system information')
    info_parser.add_argument('--formats', action='store_true', help='Show supported file formats')
    info_parser.add_argument('--config-template', action='store_true', help='Show configuration template')
    
    return parser


def load_config(config_file: Optional[str] = None) -> Config:
    """Load configuration from file or use default."""
    try:
        if config_file and os.path.exists(config_file):
            return Config(config_file)
        else:
            # Use default configuration
            config_dir = Path(__file__).parent.parent / "configs"
            default_config = config_dir / "default.yaml"
            return Config(str(default_config))
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)


def setup_logging(verbose: bool = False, log_dir: Optional[str] = None):
    """Setup logging configuration."""
    from .utils.logger import get_logger
    
    log_level = "DEBUG" if verbose else "INFO"
    logger = get_logger("energy_storage_processor", log_level, log_dir)
    
    return logger


def cmd_process(args):
    """Handle process command."""
    # Load configuration
    config = load_config(args.config)
    
    # Setup logging
    logger = setup_logging(args.verbose, args.log_dir)
    
    # Create processor
    processor = Processor(config)
    
    # Validate input file
    if not os.path.exists(args.input):
        logger.error(f"Input file not found: {args.input}")
        return 1
    
    if not processor.validate_input_file(args.input):
        logger.error(f"Invalid input file format: {args.input}")
        return 1
    
    # Process file
    result = processor.process_file(args.input, args.output, args.name)
    
    if result.success:
        logger.info(f"Successfully processed {args.input} -> {result.output_file}")
        if args.verbose:
            logger.info(f"Processing time: {result.processing_time:.2f}s, Records: {result.records_processed}")
        return 0
    else:
        logger.error(f"Failed to process {args.input}: {result.error_message}")
        return 1


def cmd_batch(args):
    """Handle batch command."""
    # Load configuration
    config = load_config(args.config)
    
    # Setup logging
    logger = setup_logging(args.verbose, args.log_dir)
    
    # Create processor
    processor = Processor(config)
    
    # Determine input files
    if args.files:
        # Process specific files
        input_files = args.files
    else:
        # Process directory
        input_files = None
    
    # Process files
    if input_files:
        # Process specific files
        results = processor.process_files(input_files, args.output)
    else:
        # Process directory
        results = processor.process_directory(
            args.dir, 
            args.output, 
            args.recursive, 
            args.patterns, 
            args.prefix
        )
    
    # Generate summary
    summary = processor.get_processing_summary(results)
    
    # Print summary
    print(f"\nProcessing Summary:")
    print(f"  Total Files: {summary['total_files']}")
    print(f"  Successful: {summary['successful_files']}")
    print(f"  Failed: {summary['failed_files']}")
    print(f"  Success Rate: {summary['success_rate']:.2%}")
    print(f"  Total Time: {summary['total_processing_time']:.2f}s")
    print(f"  Avg Time: {summary['average_processing_time']:.2f}s")
    print(f"  Total Records: {summary['total_records_processed']}")
    
    # Save report
    if summary['total_files'] > 0:
        processor.save_processing_report(results, args.output)
        print(f"  Report saved to: {os.path.join(args.output, 'processing_report.txt')}")
    
    # Return appropriate exit code
    return 0 if summary['failed_files'] == 0 else 1


def cmd_config(args):
    """Handle config command."""
    if args.show:
        # Show current configuration
        config = load_config(args.config)
        print("Current Configuration:")
        print(f"  Output Format: {config.get_output_format()}")
        print(f"  Output Filename: {config.get_output_filename()}")
        print(f"  Max Workers: {config.get_max_workers()}")
        print(f"  Highlight Calculated: {config.should_highlight_calculated()}")
        return 0
    
    elif args.init:
        # Initialize new configuration
        if os.path.exists(args.init):
            print(f"Configuration file already exists: {args.init}")
            return 1
        
        try:
            # Create default configuration
            config_dir = Path(__file__).parent.parent / "configs"
            default_config = config_dir / "default.yaml"
            
            with open(args.init, 'w') as f:
                with open(default_config, 'r') as src:
                    f.write(src.read())
            
            print(f"Configuration file created: {args.init}")
            return 0
        except Exception as e:
            print(f"Failed to create configuration file: {e}")
            return 1
    
    elif args.validate:
        # Validate configuration file
        try:
            config = load_config(args.validate)
            print(f"Configuration file is valid: {args.validate}")
            return 0
        except Exception as e:
            print(f"Configuration file is invalid: {e}")
            return 1
    
    else:
        print("No action specified for config command")
        return 1


def cmd_info(args):
    """Handle info command."""
    config = load_config(args.config)
    processor = Processor(config)
    
    if args.formats:
        print("Supported File Formats:")
        for fmt in processor.get_supported_formats():
            print(f"  - {fmt}")
        return 0
    
    elif args.config_template:
        # Show configuration template
        print("Configuration Template:")
        print("""
# Data format configuration
data_format:
  time_columns:
    - occurTime
    - timestamp
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

# Calculation rules configuration
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

# Parallel processing configuration
parallel_settings:
  max_workers: 4
  chunk_size: 1000
  enable_multiprocessing: false

# Output configuration
output_settings:
  format: excel
  filename: "Processed_Data"
  highlight_calculated: true
""")
        return 0
    
    else:
        print("System Information:")
        print(f"  Supported Formats: {', '.join(processor.get_supported_formats())}")
        print(f"  Output Format: {config.get_output_format()}")
        print(f"  Max Workers: {config.get_max_workers()}")
        return 0


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Handle commands
    if args.command == 'process':
        return cmd_process(args)
    elif args.command == 'batch':
        return cmd_batch(args)
    elif args.command == 'config':
        return cmd_config(args)
    elif args.command == 'info':
        return cmd_info(args)
    else:
        print(f"Unknown command: {args.command}")
        return 1


if __name__ == '__main__':
    sys.exit(main())