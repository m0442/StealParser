#!/usr/bin/env python3
"""
Setup script for Leaked Data Parser & Analyzer
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="leaked-data-parser",
    version="2.0.0",
    author="Cybersecurity Research Team",
    author_email="security@example.com",
    description="Advanced tool for parsing and analyzing leaked data from various sources",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/leaked-data-parser",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "leaked-data-parser=run_parser:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.json", "*.yaml", "*.yml"],
    },
    keywords="security, forensics, data, parser, analysis, research, leaked, darkweb, breach",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/leaked-data-parser/issues",
        "Source": "https://github.com/yourusername/leaked-data-parser",
        "Documentation": "https://github.com/yourusername/leaked-data-parser/wiki",
    },
)
