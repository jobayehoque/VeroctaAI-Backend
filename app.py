#!/usr/bin/env python3
"""
VeroctaAI Backend Application
AI-Powered Financial Intelligence Platform

This is the main entry point for the VeroctaAI backend application.
It imports and configures the Flask app from the organized src structure.
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the main application
from src.core.app import app

if __name__ == '__main__':
    # This will use the configuration from src/core/app.py
    app.run()