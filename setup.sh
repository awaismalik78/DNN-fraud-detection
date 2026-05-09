#!/bin/bash
# Setup script for Credit Card Fraud Detection MLOps Project

echo "=========================================="
echo "Setting up MLOps Project"
echo "=========================================="

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # On macOS/Linux
# For Windows: venv\Scripts\activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directories if they don't exist
mkdir -p data/raw
mkdir -p data/processed

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To activate the environment:"
echo "  source venv/bin/activate  # On macOS/Linux"
echo "  venv\Scripts\activate     # On Windows"
echo ""
echo "To run tests:"
echo "  pytest tests/"
echo ""
echo "To run the API server:"
echo "  python -m uvicorn src.inference.api:app --reload"
echo ""
echo "To run the Colab notebook:"
echo "  Upload notebooks/colab_training_pipeline.ipynb to Google Colab"
echo ""
