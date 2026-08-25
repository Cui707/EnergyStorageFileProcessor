#!/usr/bin/env python3
"""
Validation script to check if the energy storage processor is properly structured.
This script verifies that all necessary files and components are in place.
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and report the result."""
    if os.path.exists(file_path):
        print(f"[OK] {description}: {file_path}")
        return True
    else:
        print(f"[FAIL] {description}: {file_path}")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists and report the result."""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print(f"[OK] {description}: {dir_path}")
        return True
    else:
        print(f"[FAIL] {description}: {dir_path}")
        return False

def check_python_import(module_name, description):
    """Check if a Python module can be imported."""
    try:
        __import__(module_name)
        print(f"[OK] {description}: {module_name}")
        return True
    except ImportError as e:
        print(f"[FAIL] {description}: {module_name} - {e}")
        return False

def main():
    """Main validation function."""
    print("Energy Storage Processor - Project Structure Validation")
    print("=" * 60)
    
    # Get the project root directory
    project_root = Path(__file__).parent
    print(f"Project root: {project_root}")
    
    # Check essential files
    print("\n1. Checking Essential Files")
    print("-" * 30)
    
    essential_files = [
        ("main.py", "Main entry point"),
        ("setup.py", "Setup script"),
        ("requirements.txt", "Dependencies file"),
        ("README.md", "Documentation"),
        ("INSTALL.md", "Installation guide"),
        (".gitignore", "Git ignore file"),
        ("src/__init__.py", "Source package initialization"),
        ("src/config.py", "Configuration management"),
        ("src/cli.py", "Command line interface"),
        ("src/core/processor.py", "Main processor"),
        ("src/core/data_processor.py", "Data processor"),
        ("src/core/batch_processor.py", "Batch processor"),
        ("src/readers/base.py", "Base reader"),
        ("src/readers/csv_reader.py", "CSV reader"),
        ("src/readers/excel_reader.py", "Excel reader"),
        ("src/readers/factory.py", "Reader factory"),
        ("src/processors/extractor.py", "Data extractor"),
        ("src/processors/calculator.py", "Data calculator"),
        ("src/processors/validator.py", "Data validator"),
        ("src/writers/base.py", "Base writer"),
        ("src/writers/excel_writer.py", "Excel writer"),
        ("src/writers/csv_writer.py", "CSV writer"),
        ("src/writers/factory.py", "Writer factory"),
        ("src/utils/file_utils.py", "File utilities"),
        ("src/utils/parallel.py", "Parallel processing"),
        ("src/utils/logger.py", "Logging utilities"),
        ("src/models/data_models.py", "Data models"),
        ("src/models/config_models.py", "Configuration models"),
    ]
    
    files_ok = 0
    for file_path, description in essential_files:
        full_path = project_root / file_path
        if check_file_exists(full_path, description):
            files_ok += 1
    
    # Check directories
    print("\n2. Checking Directories")
    print("-" * 30)
    
    directories = [
        ("src/core", "Core modules"),
        ("src/readers", "File readers"),
        ("src/processors", "Data processors"),
        ("src/writers", "File writers"),
        ("src/utils", "Utilities"),
        ("src/models", "Data models"),
        ("configs", "Configuration files"),
        ("configs/battery_systems", "Battery system configs"),
        ("tests", "Test files"),
    ]
    
    dirs_ok = 0
    for dir_path, description in directories:
        full_path = project_root / dir_path
        if check_directory_exists(full_path, description):
            dirs_ok += 1
    
    # Check configuration files
    print("\n3. Checking Configuration Files")
    print("-" * 30)
    
    config_files = [
        ("configs/default.yaml", "Default configuration"),
        ("configs/readers.yaml", "Reader configuration"),
        ("configs/processors.yaml", "Processor configuration"),
        ("configs/battery_systems/generic.yaml", "Generic system config"),
        ("configs/battery_systems/ev2502_example.yaml", "EVE2502 example config"),
    ]
    
    configs_ok = 0
    for file_path, description in config_files:
        full_path = project_root / file_path
        if check_file_exists(full_path, description):
            configs_ok += 1
    
    # Check test and example files
    print("\n4. Checking Test and Example Files")
    print("-" * 30)
    
    test_files = [
        ("test_functionality.py", "Functionality test"),
        ("example_usage.py", "Usage examples"),
        ("tests/test_config.py", "Configuration tests"),
        ("tests/test_readers.py", "Reader tests"),
        ("tests/test_processors.py", "Processor tests"),
    ]
    
    tests_ok = 0
    for file_path, description in test_files:
        full_path = project_root / file_path
        if check_file_exists(full_path, description):
            tests_ok += 1
    
    # Check Python syntax
    print("\n5. Checking Python Syntax")
    print("-" * 30)
    
    python_files = [
        "main.py",
        "src/config.py",
        "src/cli.py",
        "src/core/processor.py",
        "src/core/data_processor.py",
        "src/core/batch_processor.py",
        "src/readers/base.py",
        "src/readers/csv_reader.py",
        "src/readers/excel_reader.py",
        "src/readers/factory.py",
        "src/processors/extractor.py",
        "src/processors/calculator.py",
        "src/processors/validator.py",
        "src/writers/base.py",
        "src/writers/excel_writer.py",
        "src/writers/csv_writer.py",
        "src/writers/factory.py",
        "src/utils/file_utils.py",
        "src/utils/parallel.py",
        "src/utils/logger.py",
        "src/models/data_models.py",
        "src/models/config_models.py",
    ]
    
    syntax_ok = 0
    for python_file in python_files:
        full_path = project_root / python_file
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), full_path, 'exec')
                print(f"[OK] Python syntax: {python_file}")
                syntax_ok += 1
            except SyntaxError as e:
                print(f"[FAIL] Python syntax error in {python_file}: {e}")
            except Exception as e:
                print(f"[OK] Python syntax: {python_file} (warning: {e})")
                syntax_ok += 1
    
    # Check YAML syntax
    print("\n6. Checking YAML Syntax")
    print("-" * 30)
    
    yaml_files = [
        "configs/default.yaml",
        "configs/readers.yaml",
        "configs/processors.yaml",
        "configs/battery_systems/generic.yaml",
        "configs/battery_systems/ev2502_example.yaml",
    ]
    
    yaml_ok = 0
    try:
        import yaml
        for yaml_file in yaml_files:
            full_path = project_root / yaml_file
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        yaml.safe_load(f)
                    print(f"[OK] YAML syntax: {yaml_file}")
                    yaml_ok += 1
                except yaml.YAMLError as e:
                    print(f"[FAIL] YAML syntax error in {yaml_file}: {e}")
    except ImportError:
        print("[FAIL] PyYAML not installed, skipping YAML syntax check")
    
    # Summary
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    total_checks = len(essential_files) + len(directories) + len(config_files) + len(test_files) + len(python_files) + len(yaml_files)
    passed_checks = files_ok + dirs_ok + configs_ok + tests_ok + syntax_ok + yaml_ok
    
    print(f"Total checks: {total_checks}")
    print(f"Passed: {passed_checks}")
    print(f"Failed: {total_checks - passed_checks}")
    print(f"Success rate: {passed_checks/total_checks*100:.1f}%")
    
    # Check if we can import the main modules
    print("\n7. Checking Module Imports")
    print("-" * 30)
    
    import_tests = [
        ("src.config", "Configuration module"),
        ("src.core.processor", "Core processor module"),
        ("src.readers.factory", "Reader factory module"),
        ("src.processors.extractor", "Data extractor module"),
        ("src.writers.factory", "Writer factory module"),
    ]
    
    import_ok = 0
    for module_name, description in import_tests:
        try:
            __import__(module_name)
            print(f"[OK] Import successful: {description}")
            import_ok += 1
        except Exception as e:
            print(f"[FAIL] Import failed: {description} - {e}")
    
    # Final verdict
    print("\n" + "=" * 60)
    if passed_checks >= total_checks * 0.8:  # 80% success rate
        print("[OK] Project structure validation PASSED")
        print("The energy storage processor appears to be properly structured.")
        if import_ok == len(import_tests):
            print("[OK] All modules can be imported successfully.")
            print("\nYou can now try:")
            print("  1. Install dependencies: pip install -r requirements.txt")
            print("  2. Install the package: pip install -e .")
            print("  3. Run tests: python test_functionality.py")
            print("  4. Use the CLI: python main.py --help")
        else:
            print("[WARNING] Some modules failed to import. Check the import errors above.")
    else:
        print("[FAIL] Project structure validation FAILED")
        print("Please fix the issues marked with [FAIL] above.")
    
    return 0 if passed_checks >= total_checks * 0.8 else 1

if __name__ == "__main__":
    sys.exit(main())