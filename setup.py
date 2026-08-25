"""
Setup script for the energy storage processor.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text().strip().split('\n')

setup(
    name="energy-storage-processor",
    version="1.0.0",  # Will be updated to 1.0.0 for release
    author="Energy Storage Processor Team",
    author_email="team@energystorage.com",
    description="A generic tool for processing energy storage system data files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/energy-storage/processor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
    },
    entry_points={
        "console_scripts": [
            "energy-storage-processor=src.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "energy_storage_processor": ["configs/*.yaml"],
    },
    keywords="energy storage, battery data, data processing, csv, excel, analysis",
    project_urls={
        "Bug Reports": "https://github.com/energy-storage/processor/issues",
        "Source": "https://github.com/energy-storage/processor",
        "Documentation": "https://energy-storage-processor.readthedocs.io/",
    },
)