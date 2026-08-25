@echo off
REM Energy Storage Data Processor - Quick Start Script
REM This script helps you get started with the energy storage processor

echo Energy Storage Data Processor - Quick Start
echo ===========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip is not installed or not in PATH
    echo Please install pip
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM Install the package
echo Installing the package...
pip install -e .

if %errorlevel% neq 0 (
    echo Error: Failed to install the package
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.
echo Quick Start Examples:
echo ====================
echo.
echo 1. Test the installation:
echo    python test_functionality.py
echo.
echo 2. Process a single file:
echo    echo timestamp,maxU,minU,current,charge,discharge > sample.csv
echo    echo 2023-01-01 10:00:00,4.2,3.8,10.0,5.0,2.0 >> sample.csv
echo    python main.py process sample.csv output/
echo.
echo 3. Process a directory:
echo    python main.py batch --dir input_directory/ output_directory/
echo.
echo 4. Show help:
echo    python main.py --help
echo.
echo For more information, refer to INSTALL.md and README.md
echo.

pause