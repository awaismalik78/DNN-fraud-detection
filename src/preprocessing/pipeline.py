"""
Preprocessing Pipeline Module
Handles data cleaning, scaling, and feature engineering.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
import joblib
from typing import Tuple, Union


class PreprocessingPipeline:
    """Scikit-learn based preprocessing pipeline for credit card data."""
    
    def __init__(self):
        self.transformer = None
        self.feature_names = None
        
    def build(self, X: pd.DataFrame) -> None:
        """
        Build the preprocessing pipeline.
        
        Args:
            X: Input dataframe with features
        """
        self.feature_names = X.columns.tolist()
        
        # Scale Time and Amount, pass through other features
        self.transformer = ColumnTransformer(
            transformers=[
                ('scaler', StandardScaler(), ['Time', 'Amount']),
                ('passthrough', 'passthrough', 
                 [col for col in self.feature_names if col not in ['Time', 'Amount']])
            ],
            remainder='passthrough'
        )
        
        self.transformer.fit(X)
    
    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """
        Apply preprocessing to data.
        
        Args:
            X: Input dataframe
            
        Returns:
            Preprocessed numpy array
        """
        if self.transformer is None:
            raise ValueError("Pipeline not built. Call build() first.")
        
        X_processed = self.transformer.transform(X)
        
        # Convert to dense if sparse
        if hasattr(X_processed, 'toarray'):
            X_processed = X_processed.toarray()
        
        return np.array(X_processed, dtype=np.float32)
    
    def fit_transform(self, X: pd.DataFrame) -> np.ndarray:
        """Fit and transform data in one step."""
        self.build(X)
        return self.transform(X)
    
    def save(self, filepath: str) -> None:
        """Save pipeline to disk."""
        joblib.dump(self, filepath)
        print(f"Pipeline saved to {filepath}")
    
    @staticmethod
    def load(filepath: str) -> 'PreprocessingPipeline':
        """Load pipeline from disk."""
        pipeline = joblib.load(filepath)
        print(f"Pipeline loaded from {filepath}")
        return pipeline
