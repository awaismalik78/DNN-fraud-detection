"""
Inference Module
Handles model loading, prediction, and anomaly scoring.
"""

import numpy as np
import pandas as pd
from tensorflow import keras
import joblib
from typing import Tuple, Dict, Union


class AnomalyDetector:
    """Unified anomaly detection using autoencoders."""
    
    def __init__(self, preprocessor_path: str, model_path: str):
        """
        Initialize the detector.
        
        Args:
            preprocessor_path: Path to saved preprocessor.joblib
            model_path: Path to saved .keras model
        """
        self.preprocessor = joblib.load(preprocessor_path)
        self.model = keras.models.load_model(model_path)
        self.reconstruction_errors = None
        
    def predict_reconstruction_error(self, X: pd.DataFrame) -> np.ndarray:
        """
        Compute reconstruction errors for samples.
        
        Args:
            X: Input dataframe
            
        Returns:
            Array of reconstruction errors (MSE per sample)
        """
        # Preprocess
        X_processed = self.preprocessor.transform(X)
        
        # Get predictions
        predictions = self.model.predict(X_processed, verbose=0)
        
        # Compute MSE per sample
        errors = np.mean(np.square(X_processed - predictions), axis=1)
        
        return errors
    
    def predict_anomalies(self, X: pd.DataFrame, threshold: float = None,
                         percentile: float = 95) -> Dict:
        """
        Detect anomalies in data.
        
        Args:
            X: Input dataframe
            threshold: Fixed anomaly threshold. If None, uses percentile.
            percentile: Percentile for dynamic threshold (default: 95)
            
        Returns:
            Dictionary with predictions, errors, and threshold used
        """
        errors = self.predict_reconstruction_error(X)
        
        if threshold is None:
            threshold = np.percentile(errors, percentile)
        
        predictions = (errors > threshold).astype(int)
        
        return {
            'predictions': predictions,
            'reconstruction_errors': errors,
            'threshold_used': threshold,
            'anomaly_count': np.sum(predictions),
            'anomaly_rate': np.sum(predictions) / len(predictions)
        }
    
    def get_embeddings(self, X: pd.DataFrame) -> np.ndarray:
        """
        Extract bottleneck embeddings for clustering/visualization.
        
        Args:
            X: Input dataframe
            
        Returns:
            Embeddings from bottleneck layer
        """
        X_processed = self.preprocessor.transform(X)
        
        # Create embedding model (input to bottleneck)
        embedding_model = keras.Model(
            inputs=self.model.input,
            outputs=self.model.get_layer('bottleneck').output
        )
        
        embeddings = embedding_model.predict(X_processed, verbose=0)
        return embeddings


def batch_predict(detector: AnomalyDetector, X: pd.DataFrame,
                 batch_size: int = 10000) -> np.ndarray:
    """
    Predict on large datasets in batches to avoid memory issues.
    
    Args:
        detector: AnomalyDetector instance
        X: Input dataframe
        batch_size: Batch size for processing
        
    Returns:
        Array of predictions
    """
    predictions = []
    
    for i in range(0, len(X), batch_size):
        batch = X.iloc[i:i+batch_size]
        batch_pred = detector.predict_anomalies(batch)
        predictions.append(batch_pred['predictions'])
    
    return np.concatenate(predictions)
