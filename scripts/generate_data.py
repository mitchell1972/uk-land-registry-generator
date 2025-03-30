#!/usr/bin/env python3
"""
UK Land Registry Data Generator

Entry point script for generating UK Land Registry application data.
"""
import os
import sys

# Add parent directory to path to allow importing the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from uklandregistry.cli import run_cli

if __name__ == "__main__":
    sys.exit(run_cli()) 