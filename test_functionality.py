#!/usr/bin/env python3
"""
Test script to verify the energy storage processor functionality.
This script creates sample data and tests the processing pipeline.
"""

import os
import sys
import tempfile
import pandas as pd
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.config import Config
from src.core.processor import Processor


def create_sample_data():
    """Create sample battery data for testing."""
    # Create timestamp range
    start_time = datetime(2023, 1, 1, 10, 0, 0)
    timestamps = [start_time + timedelta(minutes=i) for i in range(100)]
    
    # Create sample data for multiple clusters
    data = []
    for cluster in range(1, 6):  # 5 clusters
        for i, timestamp in enumerate(timestamps):
            # Simulate voltage variations
            base_voltage = 3.7 + (cluster * 0.1)
            max_voltage = base_voltage + 0.1 + (i * 0.001)
            min_voltage = base_voltage - 0.1 - (i * 0.001)
            
            # Simulate temperature variations
            base_temp = 25.0 + (cluster * 2)
            max_temp = base_temp + 5.0 + (i * 0.01)
            
            # Simulate current
            current = 10.0 + (cluster * 2) + (i * 0.1)
            
            # Simulate charge/discharge
            charge = 5.0 + (cluster * 0.5) + (i * 0.01)
            discharge = 2.0 + (cluster * 0.2) + (i * 0.005)
            
            data.append({
                'occurTime': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                f'bms_maxU_{cluster}': max_voltage,
                f'bms_minU_{cluster}': min_voltage,
                f'bms_mdMaxT_{cluster}': max_temp,
                f'bms_maxT_{cluster}': max_temp,
                f'bms_i_{cluster}': current,
                f'bms_totalChargeKwh_{cluster}': charge,
                f'bms_totalDischargeKwh_{cluster}': discharge,
                f'bms_thisChargeKwh_{cluster}': 0.01,
                f'bms_thislChargeKwh_{cluster}': 0.01,
                f'bms_thisDischargeKwh_{cluster}': 0.005
            })
    
    return pd.DataFrame(data)


def test_single_file_processing():
    """Test processing a single file."""
    print("Testing single file processing...")
    
    # Create sample data
    sample_data = create_sample_data()
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save sample data to CSV
        input_file = os.path.join(temp_dir, 'sample_data.csv')
        sample_data.to_csv(input_file, index=False)
        
        # Create processor
        config = Config()
        processor = Processor(config)
        
        # Process the file
        result = processor.process_file(input_file, temp_dir)
        
        # Verify result
        if result.success:
            print(f"✓ Successfully processed {result.input_file}")
            print(f"  Output file: {result.output_file}")
            print(f"  Processing time: {result.processing_time:.2f}s")
            print(f"  Records processed: {result.records_processed}")
            
            # Check if output file exists
            if os.path.exists(result.output_file):
                print("✓ Output file created successfully")
                
                # Read and verify output data
                output_data = pd.read_excel(result.output_file)
                print(f"  Output shape: {output_data.shape}")
                print(f"  Columns: {list(output_data.columns)}")
                
                # Check for calculated columns
                calculated_columns = ['sysMaxU', 'sysMinU', 'MaxDiff', 'sysMaxT', 
                                    'DayTotalChargeKwh', 'DayTotalDischargeKwh']
                for col in calculated_columns:
                    if col in output_data.columns:
                        print(f"  ✓ {col} column present")
                    else:
                        print(f"  ✗ {col} column missing")
            else:
                print("✗ Output file not found")
                return False
        else:
            print(f"✗ Failed to process file: {result.error_message}")
            return False
    
    return True


def test_batch_processing():
    """Test processing multiple files."""
    print("\nTesting batch processing...")
    
    # Create processor
    config = Config()
    processor = Processor(config)
    
    # Create temporary directory with multiple files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create multiple sample files
        input_files = []
        for i in range(3):
            sample_data = create_sample_data()
            input_file = os.path.join(temp_dir, f'sample_data_{i+1}.csv')
            sample_data.to_csv(input_file, index=False)
            input_files.append(input_file)
        
        # Process files
        results = processor.process_files(input_files, temp_dir)
        
        # Verify results
        if len(results) == len(input_files):
            print(f"✓ Processed {len(results)} files")
            
            successful = sum(1 for r in results if r.success)
            if successful == len(results):
                print("✓ All files processed successfully")
                
                # Check output files
                for i, result in enumerate(results):
                    if os.path.exists(result.output_file):
                        print(f"  ✓ Output file {i+1}: {result.output_file}")
                    else:
                        print(f"  ✗ Output file {i+1} not found")
                        return False
            else:
                print(f"✗ Only {successful}/{len(results)} files processed successfully")
                return False
        else:
            print(f"✗ Expected {len(input_files)} results, got {len(results)}")
            return False
    
    return True


def test_directory_processing():
    """Test processing a directory."""
    print("\nTesting directory processing...")
    
    # Create processor
    config = Config()
    processor = Processor(config)
    
    # Create temporary directory with files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create input directory
        input_dir = os.path.join(temp_dir, 'input')
        os.makedirs(input_dir)
        
        # Create sample files
        for i in range(5):
            sample_data = create_sample_data()
            input_file = os.path.join(input_dir, f'sample_data_{i+1}.csv')
            sample_data.to_csv(input_file, index=False)
        
        # Create output directory
        output_dir = os.path.join(temp_dir, 'output')
        
        # Process directory
        results = processor.process_directory(input_dir, output_dir)
        
        # Verify results
        if len(results) > 0:
            print(f"✓ Processed {len(results)} files")
            
            successful = sum(1 for r in results if r.success)
            if successful > 0:
                print(f"✓ {successful} files processed successfully")
                
                # Generate summary
                summary = processor.get_processing_summary(results)
                print(f"  Summary: {summary}")
            else:
                print("✗ No files processed successfully")
                return False
        else:
            print("✗ No results returned")
            return False
    
    return True


def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        # Test default configuration
        config = Config()
        print("✓ Default configuration loaded")
        
        # Test configuration access
        print(f"  Output format: {config.get_output_format()}")
        print(f"  Output filename: {config.get_output_filename()}")
        print(f"  Max workers: {config.get_max_workers()}")
        print(f"  Highlight calculated: {config.should_highlight_calculated()}")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def main():
    """Main test function."""
    print("Energy Storage Processor Test Suite")
    print("=" * 40)
    
    tests = [
        ("Configuration", test_configuration),
        ("Single File Processing", test_single_file_processing),
        ("Batch Processing", test_batch_processing),
        ("Directory Processing", test_directory_processing)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 40)
    print("Test Summary")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())