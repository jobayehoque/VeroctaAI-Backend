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
    # Use port 5002 to avoid conflicts with Apple AirPlay on port 5000
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)