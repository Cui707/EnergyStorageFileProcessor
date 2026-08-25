"""
Main entry point for the energy storage processor.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.cli import main

if __name__ == '__main__':
    sys.exit(main())