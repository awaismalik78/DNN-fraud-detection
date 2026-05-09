"""
FastAPI Application for Real-Time Credit Card Fraud Inference
Loads the Transformer Autoencoder model and preprocessing pipeline
Provides REST endpoints for fraud detection scoring
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import tensorflow as tf
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION
# ============================================================================

# Paths to saved models and preprocessing pipeline
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../saved_models/transformer_autoencoder.keras")
PREPROCESSOR_PATH = os.path.join(os.path.dirname(__file__), "../../saved_models/preprocessor.joblib")
METADATA_PATH = os.path.join(os.path.dirname(__file__), "../../saved_models/training_metadata.json")

# MSE threshold for anomaly detection
MSE_THRESHOLD = 0.8  # Configurable threshold for fraud detection

# ============================================================================
# PYDANTIC MODELS (Request/Response Schemas)
# ============================================================================

class TransactionInput(BaseModel):
    """Schema for a single raw transaction"""
    Time: float = Field(..., description="Transaction time in seconds")
    Amount: float = Field(..., description="Transaction amount in dollars")
    V1: float = Field(..., description="PCA-transformed feature 1")
    V2: float = Field(..., description="PCA-transformed feature 2")
    V3: float = Field(..., description="PCA-transformed feature 3")
    V4: float = Field(..., description="PCA-transformed feature 4")
    V5: float = Field(..., description="PCA-transformed feature 5")
    V6: float = Field(..., description="PCA-transformed feature 6")
    V7: float = Field(..., description="PCA-transformed feature 7")
    V8: float = Field(..., description="PCA-transformed feature 8")
    V9: float = Field(..., description="PCA-transformed feature 9")
    V10: float = Field(..., description="PCA-transformed feature 10")
    V11: float = Field(..., description="PCA-transformed feature 11")
    V12: float = Field(..., description="PCA-transformed feature 12")
    V13: float = Field(..., description="PCA-transformed feature 13")
    V14: float = Field(..., description="PCA-transformed feature 14")
    V15: float = Field(..., description="PCA-transformed feature 15")
    V16: float = Field(..., description="PCA-transformed feature 16")
    V17: float = Field(..., description="PCA-transformed feature 17")
    V18: float = Field(..., description="PCA-transformed feature 18")
    V19: float = Field(..., description="PCA-transformed feature 19")
    V20: float = Field(..., description="PCA-transformed feature 20")
    V21: float = Field(..., description="PCA-transformed feature 21")
    V22: float = Field(..., description="PCA-transformed feature 22")
    V23: float = Field(..., description="PCA-transformed feature 23")
    V24: float = Field(..., description="PCA-transformed feature 24")
    V25: float = Field(..., description="PCA-transformed feature 25")
    V26: float = Field(..., description="PCA-transformed feature 26")
    V27: float = Field(..., description="PCA-transformed feature 27")
    V28: float = Field(..., description="PCA-transformed feature 28")

    class Config:
        schema_extra = {
            "example": {
                "Time": 0,
                "Amount": 149.62,
                "V1": -1.3598071336738,
                "V2": -0.0727812320124,
                "V3": 2.36060841498244,
                "V4": 1.59067054248337,
                "V5": -0.770464378778467,
                "V6": -0.623588099395191,
                "V7": -0.942143496290839,
                "V8": -0.622417098688339,
                "V9": -0.051410094880652,
                "V10": -0.276253783529582,
                "V11": -0.637628779843854,
                "V12": 0.46399461915966,
                "V13": -0.092747946301046,
                "V14": -0.12849206922258,
                "V15": -0.199347865324392,
                "V16": -0.108643033016505,
                "V17": -0.269809040300488,
                "V18": -0.170099690234065,
                "V19": 0.002883084236717,
                "V20": -0.103328316294955,
                "V21": -0.199347865324392,
                "V22": -0.108643033016505,
                "V23": -0.269809040300488,
                "V24": -0.170099690234065,
                "V25": 0.002883084236717,
                "V26": -0.103328316294955,
                "V27": -0.199347865324392,
                "V28": -0.108643033016505
            }
        }


class FraudPredictionOutput(BaseModel):
    """Schema for fraud detection response"""
    fraud_detected: bool = Field(..., description="Whether transaction is fraudulent")
    anomaly_score: float = Field(..., description="MSE reconstruction error (anomaly score)")
    threshold: float = Field(..., description="MSE threshold used for detection")
    confidence: float = Field(..., description="Confidence score (0-1)")


class BatchTransactionInput(BaseModel):
    """Schema for batch transactions"""
    transactions: List[TransactionInput] = Field(..., description="List of transactions to score")


class BatchPredictionOutput(BaseModel):
    """Schema for batch fraud detection response"""
    predictions: List[FraudPredictionOutput]
    batch_fraud_rate: float = Field(..., description="Percentage of fraudulent transactions in batch")
    total_processed: int = Field(..., description="Total transactions processed")


class HealthResponse(BaseModel):
    """Schema for health check"""
    status: str
    model_loaded: bool
    preprocessor_loaded: bool
    threshold: float


# ============================================================================
# GLOBAL STATE
# ============================================================================

# Will be loaded on startup
model = None
preprocessor = None
metadata = None


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def load_model_and_preprocessor():
    """
    Load the trained Transformer Autoencoder model and preprocessing pipeline.
    Returns: (model, preprocessor, metadata) tuple
    """
    global model, preprocessor, metadata
    
    try:
        # Load the Transformer Autoencoder model
        print(f"Loading Transformer Autoencoder from {MODEL_PATH}...")
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✓ Transformer Autoencoder loaded successfully")
        
        # Load the preprocessing pipeline
        print(f"Loading preprocessing pipeline from {PREPROCESSOR_PATH}...")
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        print("✓ Preprocessing pipeline loaded successfully")
        
        # Load metadata if available
        if os.path.exists(METADATA_PATH):
            with open(METADATA_PATH, 'r') as f:
                metadata = json.load(f)
            print("✓ Training metadata loaded successfully")
        else:
            metadata = {}
            print("⚠ Training metadata not found")
        
        return model, preprocessor, metadata
    
    except FileNotFoundError as e:
        print(f"✗ Error: Model or preprocessor file not found: {e}")
        raise
    except Exception as e:
        print(f"✗ Error loading model or preprocessor: {e}")
        raise


def preprocess_transaction(raw_features: Dict) -> np.ndarray:
    """
    Preprocess raw transaction features using the fitted scikit-learn pipeline.
    
    Args:
        raw_features: Dictionary of raw transaction features
    
    Returns:
        Preprocessed feature array (1, 30)
    """
    # Create proper feature names list in order
    feature_names = ['Time', 'Amount'] + [f'V{i}' for i in range(1, 29)]
    
    # Convert dictionary to Pandas DataFrame with correct column names
    # This is CRITICAL because the preprocessor was trained on a DataFrame with these columns
    input_df = pd.DataFrame([raw_features], columns=feature_names)
    
    # Apply preprocessing pipeline (expects DataFrame with named columns)
    preprocessed = preprocessor.transform(input_df)
    
    return preprocessed


def calculate_reconstruction_error(original: np.ndarray, reconstructed: np.ndarray) -> float:
    """
    Calculate Mean Squared Error (MSE) between original and reconstructed.
    
    Args:
        original: Original preprocessed features (1, 30)
        reconstructed: Reconstructed features from autoencoder (1, 30)
    
    Returns:
        MSE value as float
    """
    mse = np.mean((original - reconstructed) ** 2)
    return float(mse)


def detect_fraud(mse_score: float, threshold: float = MSE_THRESHOLD) -> tuple:
    """
    Determine if transaction is fraudulent based on MSE threshold.
    
    Args:
        mse_score: Reconstruction error (MSE)
        threshold: MSE threshold for fraud detection
    
    Returns:
        (is_fraud: bool, confidence: float) tuple
    """
    is_fraud = mse_score > threshold
    
    # Confidence is normalized distance from threshold
    # Higher MSE = higher confidence in fraud detection
    if is_fraud:
        confidence = min(1.0, (mse_score - threshold) / threshold)
    else:
        confidence = min(1.0, (threshold - mse_score) / threshold)
    
    return is_fraud, confidence


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Fraud Detection API",
    description="Real-time credit card fraud detection using Transformer Autoencoder",
    version="1.0.0"
)


# ============================================================================
# STARTUP AND SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Load model and preprocessor on application startup"""
    print("\n" + "="*70)
    print("STARTING FRAUD DETECTION API")
    print("="*70)
    try:
        load_model_and_preprocessor()
        print("\n✓ API startup successful - ready for predictions")
        print("="*70 + "\n")
    except Exception as e:
        print(f"\n✗ API startup failed: {e}")
        print("="*70 + "\n")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    print("\n" + "="*70)
    print("SHUTTING DOWN FRAUD DETECTION API")
    print("="*70 + "\n")


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API and model status.
    
    Returns:
        HealthResponse with status and model information
    """
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        preprocessor_loaded=preprocessor is not None,
        threshold=MSE_THRESHOLD
    )


@app.post("/predict", response_model=FraudPredictionOutput, tags=["Predictions"])
async def predict_single(transaction: TransactionInput):
    """
    Predict fraud for a single transaction.
    
    Process:
    1. Receive raw transaction features
    2. Preprocess features using scikit-learn pipeline
    3. Pass through Transformer Autoencoder
    4. Calculate MSE reconstruction error
    5. Compare against threshold
    6. Return fraud detection result
    
    Args:
        transaction: Raw transaction features
    
    Returns:
        FraudPredictionOutput with fraud detection result
    """
    if model is None or preprocessor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert input to dictionary
        raw_features = transaction.dict()
        
        # Step 1: Preprocess the raw features
        preprocessed = preprocess_transaction(raw_features)
        
        # Step 2: Get reconstruction from Transformer Autoencoder
        reconstruction = model.predict(preprocessed, verbose=0)
        
        # Step 3: Calculate MSE reconstruction error
        mse_score = calculate_reconstruction_error(preprocessed, reconstruction)
        
        # Step 4: Detect fraud based on threshold
        is_fraud, confidence = detect_fraud(mse_score, MSE_THRESHOLD)
        
        return FraudPredictionOutput(
            fraud_detected=is_fraud,
            anomaly_score=mse_score,
            threshold=MSE_THRESHOLD,
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")


@app.post("/predict-batch", response_model=BatchPredictionOutput, tags=["Predictions"])
async def predict_batch(batch: BatchTransactionInput):
    """
    Predict fraud for a batch of transactions.
    
    Args:
        batch: List of transactions to score
    
    Returns:
        BatchPredictionOutput with results for all transactions
    """
    if model is None or preprocessor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        predictions = []
        fraud_count = 0
        
        for transaction in batch.transactions:
            # Preprocess
            raw_features = transaction.dict()
            preprocessed = preprocess_transaction(raw_features)
            
            # Get reconstruction
            reconstruction = model.predict(preprocessed, verbose=0)
            
            # Calculate MSE
            mse_score = calculate_reconstruction_error(preprocessed, reconstruction)
            
            # Detect fraud
            is_fraud, confidence = detect_fraud(mse_score, MSE_THRESHOLD)
            
            if is_fraud:
                fraud_count += 1
            
            predictions.append(FraudPredictionOutput(
                fraud_detected=is_fraud,
                anomaly_score=mse_score,
                threshold=MSE_THRESHOLD,
                confidence=confidence
            ))
        
        batch_fraud_rate = (fraud_count / len(batch.transactions)) * 100 if batch.transactions else 0
        
        return BatchPredictionOutput(
            predictions=predictions,
            batch_fraud_rate=batch_fraud_rate,
            total_processed=len(batch.transactions)
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Batch prediction error: {str(e)}")


@app.get("/stats", tags=["Information"])
async def get_stats():
    """
    Get model statistics and information.
    
    Returns:
        Model architecture, parameters, and training information
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    stats = {
        "model_name": model.name,
        "model_type": "Transformer Autoencoder",
        "total_parameters": model.count_params(),
        "input_shape": model.input_shape,
        "output_shape": model.output_shape,
        "layers": len(model.layers),
        "mse_threshold": MSE_THRESHOLD,
        "metadata": metadata
    }
    
    return stats


@app.get("/", tags=["Information"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": "Fraud Detection API",
        "version": "1.0.0",
        "description": "Real-time credit card fraud detection using Transformer Autoencoder",
        "endpoints": {
            "health": "GET /health",
            "predict": "POST /predict",
            "predict_batch": "POST /predict-batch",
            "stats": "GET /stats",
            "docs": "/docs"
        }
    }


# ============================================================================
# ERROR HANDLING
# ============================================================================

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=400,
        content={"detail": f"Validation error: {str(exc)}"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("Starting Fraud Detection API Server")
    print("="*70)
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative Docs: http://localhost:8000/redoc")
    print("="*70 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
