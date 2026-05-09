# Windows setup script for Credit Card Fraud Detection MLOps Project
# Run this in PowerShell

Write-Host "==========================================" -ForegroundColor Green
Write-Host "Setting up MLOps Project" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
. venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

# Create data directories if they don't exist
Write-Host "Creating data directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path data\raw -Force | Out-Null
New-Item -ItemType Directory -Path data\processed -Force | Out-Null

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the environment:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run tests:" -ForegroundColor Cyan
Write-Host "  pytest tests/" -ForegroundColor White
Write-Host ""
Write-Host "To run the API server:" -ForegroundColor Cyan
Write-Host "  python -m uvicorn src.inference.api:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "To run the Colab notebook:" -ForegroundColor Cyan
Write-Host "  Upload notebooks/colab_training_pipeline.ipynb to Google Colab" -ForegroundColor White
Write-Host ""
