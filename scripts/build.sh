#!/bin/bash

# VeroctaAI Build Script for Render
# This script ensures proper build process for deployment

echo "🚀 Starting VeroctaAI build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Backend-only build script: installing Python dependencies and preparing environment"
pip install -r requirements.txt
echo "✅ Python dependencies installed"

echo "🎯 Backend build complete. Frontend has been removed from this repository."
