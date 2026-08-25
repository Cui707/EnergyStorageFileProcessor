#!/usr/bin/env python3
"""
Example script demonstrating how to use the energy storage processor programmatically.
This shows how to integrate the processor into other Python applications.
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config import Config
from src.core.processor import Processor


def create_example_data():
    """Create example battery data for demonstration."""
    print("Creating example battery data...")
    
    # Create timestamp range
    start_time = datetime(2023, 1, 1, 10, 0, 0)
    timestamps = [start_time + timedelta(minutes=i) for i in range(50)]
    
    # Create example data for 3 clusters
    data = []
    for cluster in range(1, 4):  # 3 clusters
        for i, timestamp in enumerate(timestamps):
            # Simulate realistic battery data
            base_voltage = 3.6 + (cluster * 0.05)  # Different voltage levels
            max_voltage = base_voltage + 0.05 + (i * 0.0002)
            min_voltage = base_voltage - 0.05 - (i * 0.0002)
            
            # Simulate temperature
            base_temp = 22.0 + (cluster * 3)
            max_temp = base_temp + 3.0 + (i * 0.005)
            
            # Simulate current
            current = 8.0 + (cluster * 1.5) + (i * 0.05)
            
            # Simulate charge/discharge
            charge = 3.0 + (cluster * 0.3) + (i * 0.005)
            discharge = 1.5 + (cluster * 0.1) + (i * 0.002)
            
            data.append({
                'occurTime': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                f'bms_maxU_{cluster}': max_voltage,
                f'bms_minU_{cluster}': min_voltage,
                f'bms_mdMaxT_{cluster}': max_temp,
                f'bms_maxT_{cluster}': max_temp,
                f'bms_i_{cluster}': current,
                f'bms_totalChargeKwh_{cluster}': charge,
                f'bms_totalDischargeKwh_{cluster}': discharge,
                f'bms_thisChargeKwh_{cluster}': 0.005,
                f'bms_thislChargeKwh_{cluster}': 0.005,
                f'bms_thisDischargeKwh_{cluster}': 0.002
            })
    
    df = pd.DataFrame(data)
    print(f"Created example data with {len(df)} rows and {len(df.columns)} columns")
    return df


def demonstrate_single_file_processing():
    """Demonstrate single file processing."""
    print("\n" + "="*50)
    print("Demonstrating Single File Processing")
    print("="*50)
    
    # Create example data
    df = create_example_data()
    
    # Create temporary directory
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save example data to CSV
        input_file = os.path.join(temp_dir, 'example_data.csv')
        df.to_csv(input_file, index=False)
        print(f"Saved example data to: {input_file}")
        
        # Create processor
        config = Config()
        processor = Processor(config)
        
        # Process the file
        print("\nProcessing file...")
        result = processor.process_file(input_file, temp_dir)
        
        # Display results
        if result.success:
            print(f"✓ Successfully processed: {result.input_file}")
            print(f"  Output file: {result.output_file}")
            print(f"  Processing time: {result.processing_time:.2f} seconds")
            print(f"  Records processed: {result.records_processed}")
            
            # Read and display output data summary
            output_df = pd.read_excel(result.output_file)
            print(f"  Output data shape: {output_df.shape}")
            
            # Show some calculated columns
            calculated_cols = ['sysMaxU', 'sysMinU', 'MaxDiff', 'sysMaxT', 
                             'DayTotalChargeKwh', 'DayTotalDischargeKwh']
            for col in calculated_cols:
                if col in output_df.columns:
                    print(f"  {col} range: {output_df[col].min():.3f} - {output_df[col].max():.3f}")
        else:
            print(f"✗ Processing failed: {result.error_message}")


def demonstrate_batch_processing():
    """Demonstrate batch processing."""
    print("\n" + "="*50)
    print("Demonstrating Batch Processing")
    print("="*50)
    
    # Create processor
    config = Config()
    processor = Processor(config)
    
    # Create temporary directory with multiple files
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create multiple example files
        input_files = []
        for i in range(3):
            df = create_example_data()
            input_file = os.path.join(temp_dir, f'example_data_{i+1}.csv')
            df.to_csv(input_file, index=False)
            input_files.append(input_file)
            print(f"Created example file: {input_file}")
        
        # Process files
        print("\nProcessing multiple files...")
        results = processor.process_files(input_files, temp_dir)
        
        # Display results
        print(f"\nProcessed {len(results)} files:")
        successful = sum(1 for r in results if r.success)
        print(f"  Successful: {successful}")
        print(f"  Failed: {len(results) - successful}")
        
        # Show processing summary
        if successful > 0:
            summary = processor.get_processing_summary(results)
            print(f"\nProcessing Summary:")
            print(f"  Total Files: {summary['total_files']}")
            print(f"  Successful: {summary['successful_files']}")
            print(f"  Failed: {summary['failed_files']}")
            print(f"  Success Rate: {summary['success_rate']:.2%}")
            print(f"  Total Time: {summary['total_processing_time']:.2f}s")
            print(f"  Average Time: {summary['average_processing_time']:.2f}s")
            print(f"  Total Records: {summary['total_records_processed']}")
            
            # Save processing report
            processor.save_processing_report(results, temp_dir)
            print(f"  Processing report saved to: {os.path.join(temp_dir, 'processing_report.txt')}")


def demonstrate_custom_configuration():
    """Demonstrate using custom configuration."""
    print("\n" + "="*50)
    print("Demonstrating Custom Configuration")
    print("="*50)
    
    # Create custom configuration
    custom_config_data = {
        'data_format': {
            'time_columns': ['occurTime'],
            'voltage_columns': ['maxU', 'minU'],
            'temperature_columns': ['maxT'],
            'current_columns': ['i'],
            'charge_columns': ['totalChargeKwh'],
            'discharge_columns': ['totalDischargeKwh']
        },
        'calculation_rules': {
            'system_voltage': {
                'max': True,
                'min': True,
                'diff': True,
                'diff_multiplier': 1000
            },
            'system_temperature': {
                'max': True
            },
            'energy_balance': {
                'charge': True,
                'discharge': True
            }
        },
        'parallel_settings': {
            'max_workers': 2,
            'chunk_size': 1000,
            'enable_multiprocessing': False
        },
        'output_settings': {
            'format': 'excel',
            'filename': 'Custom_Processed_Data',
            'highlight_calculated': True
        }
    }
    
    # Create temporary config file
    import tempfile
    import yaml
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = os.path.join(temp_dir, 'custom_config.yaml')
        with open(config_file, 'w') as f:
            yaml.dump(custom_config_data, f)
        
        print(f"Created custom configuration: {config_file}")
        
        # Create processor with custom config
        config = Config(config_file)
        processor = Processor(config)
        
        # Create and process example data
        df = create_example_data()
        input_file = os.path.join(temp_dir, 'custom_example.csv')
        df.to_csv(input_file, index=False)
        
        print("\nProcessing with custom configuration...")
        result = processor.process_file(input_file, temp_dir)
        
        if result.success:
            print(f"✓ Successfully processed with custom config")
            print(f"  Output file: {result.output_file}")
            
            # Show configuration values
            print(f"\nConfiguration Values:")
            print(f"  Output Format: {config.get_output_format()}")
            print(f"  Output Filename: {config.get_output_filename()}")
            print(f"  Max Workers: {config.get_max_workers()}")
            print(f"  Highlight Calculated: {config.should_highlight_calculated()}")
        else:
            print(f"✗ Processing failed: {result.error_message}")


def demonstrate_programmatic_usage():
    """Demonstrate programmatic usage."""
    print("\n" + "="*50)
    print("Demonstrating Programmatic Usage")
    print("="*50)
    
    # Create processor
    config = Config()
    processor = Processor(config)
    
    # Get system information
    print("System Information:")
    print(f"  Supported Formats: {processor.get_supported_formats()}")
    print(f"  Output Format: {config.get_output_format()}")
    print(f"  Max Workers: {config.get_max_workers()}")
    
    # Create example data
    df = create_example_data()
    
    # Process data programmatically
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = os.path.join(temp_dir, 'programmatic_example.csv')
        df.to_csv(input_file, index=False)
        
        # Validate input file
        is_valid = processor.validate_input_file(input_file)
        print(f"\nInput file validation: {'✓ Valid' if is_valid else '✗ Invalid'}")
        
        # Process the file
        result = processor.process_file(input_file, temp_dir)
        
        if result.success:
            print("✓ Programmatic processing successful")
            print(f"  Output file: {result.output_file}")
            
            # Read and analyze results
            output_df = pd.read_excel(result.output_file)
            print(f"  Output shape: {output_df.shape}")
            
            # Calculate some statistics
            if 'sysMaxU' in output_df.columns:
                print(f"  System Max Voltage: {output_df['sysMaxU'].mean():.3f} ± {output_df['sysMaxU'].std():.3f}")
            if 'sysMaxT' in output_df.columns:
                print(f"  System Max Temperature: {output_df['sysMaxT'].mean():.1f} ± {output_df['sysMaxT'].std():.1f}")
        else:
            print(f"✗ Programmatic processing failed: {result.error_message}")


def main():
    """Main demonstration function."""
    print("Energy Storage Processor - Programmatic Usage Examples")
    print("=" * 60)
    
    try:
        # Run demonstrations
        demonstrate_single_file_processing()
        demonstrate_batch_processing()
        demonstrate_custom_configuration()
        demonstrate_programmatic_usage()
        
        print("\n" + "="*60)
        print("All demonstrations completed successfully!")
        print("For more information, refer to the README.md file.")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()