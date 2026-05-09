"""
FastAPI Service for Fraud Detection
RESTful API for real-time anomaly detection.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
import logging
from src.inference.detector import AnomalyDetector

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="Real-time anomaly detection using Deep Autoencoder and Transformer Autoencoder",
    version="1.0.0"
)

# Global detector (will be initialized on startup)
detector = None


class TransactionInput(BaseModel):
    """Single transaction input schema."""
    Time: float
    Amount: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float


class BatchTransactionInput(BaseModel):
    """Batch transactions input schema."""
    transactions: List[TransactionInput]
    threshold: Optional[float] = None
    percentile: Optional[float] = 95


class PredictionOutput(BaseModel):
    """Single prediction output."""
    is_anomaly: bool
    reconstruction_error: float
    confidence: float


class BatchPredictionOutput(BaseModel):
    """Batch prediction output."""
    predictions: List[PredictionOutput]
    anomaly_rate: float
    threshold_used: float
    total_samples: int
    anomalies_detected: int


@app.on_event("startup")
async def startup_event():
    """Initialize detector on startup."""
    global detector
    try:
        detector = AnomalyDetector(
            preprocessor_path="saved_models/preprocessor.joblib",
            model_path="saved_models/standard_autoencoder.keras"
        )
        logger.info("Detector initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize detector: {e}")
        raise


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "model_loaded": detector is not None}


@app.post("/predict", response_model=PredictionOutput)
async def predict_single(transaction: TransactionInput):
    """Predict anomaly for a single transaction."""
    if detector is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert to dataframe
        df = pd.DataFrame([transaction.dict()])
        
        # Get prediction
        result = detector.predict_anomalies(df)
        
        error = float(result['reconstruction_errors'][0])
        is_anomaly = bool(result['predictions'][0])
        confidence = min(error / (result['threshold_used'] + 1e-6), 1.0)
        
        return PredictionOutput(
            is_anomaly=is_anomaly,
            reconstruction_error=error,
            confidence=confidence
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict-batch", response_model=BatchPredictionOutput)
async def predict_batch(batch_input: BatchTransactionInput):
    """Predict anomalies for multiple transactions."""
    if detector is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert to dataframe
        transactions_data = [t.dict() for t in batch_input.transactions]
        df = pd.DataFrame(transactions_data)
        
        # Get predictions
        result = detector.predict_anomalies(
            df,
            threshold=batch_input.threshold,
            percentile=batch_input.percentile
        )
        
        # Format output
        predictions = []
        for i, (pred, error) in enumerate(
            zip(result['predictions'], result['reconstruction_errors'])
        ):
            confidence = min(error / (result['threshold_used'] + 1e-6), 1.0)
            predictions.append(
                PredictionOutput(
                    is_anomaly=bool(pred),
                    reconstruction_error=float(error),
                    confidence=float(confidence)
                )
            )
        
        return BatchPredictionOutput(
            predictions=predictions,
            anomaly_rate=float(result['anomaly_rate']),
            threshold_used=float(result['threshold_used']),
            total_samples=len(df),
            anomalies_detected=int(result['anomaly_count'])
        )
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/stats")
async def get_stats():
    """Get model statistics."""
    if detector is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_name": detector.model.name,
        "input_shape": detector.model.input_shape,
        "output_shape": detector.model.output_shape,
        "total_parameters": detector.model.count_params()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
