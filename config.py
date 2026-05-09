"""
Configuration file for the MLOps project
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "saved_models"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Create directories if they don't exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Model configuration
MODEL_CONFIG = {
    "standard_autoencoder": {
        "input_dim": 30,
        "bottleneck_dim": 8,
        "epochs": 100,
        "batch_size": 256,
        "validation_split": 0.2,
        "early_stopping_patience": 10,
    },
    "transformer_autoencoder": {
        "input_dim": 30,
        "num_heads": 4,
        "bottleneck_dim": 8,
        "ff_dim": 32,
        "epochs": 100,
        "batch_size": 256,
        "validation_split": 0.2,
        "early_stopping_patience": 10,
    }
}

# Anomaly detection thresholds
ANOMALY_DETECTION = {
    "method": "percentile",  # "percentile" or "fixed_threshold"
    "percentile": 95,  # Use 95th percentile as threshold
    "fixed_threshold": None,  # Set if using fixed threshold
}

# API configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": False,
    "reload": True,
}

# Dataset information
DATASET_CONFIG = {
    "name": "Kaggle ULB Credit Card Fraud",
    "url": "https://www.kaggle.com/mlg-ulb/creditcardfraud",
    "columns": 31,  # 30 features + 1 class label
    "feature_columns": 30,
    "scaled_features": ["Time", "Amount"],
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}
