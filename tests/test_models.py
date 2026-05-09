"""
Unit Tests for Fraud Detection Models
"""

import pytest
import numpy as np
import pandas as pd
from src.preprocessing.pipeline import PreprocessingPipeline
from src.models.autoencoders import StandardAutoencoder, TransformerAutoencoder


@pytest.fixture
def sample_data():
    """Create sample credit card data for testing."""
    np.random.seed(42)
    n_samples = 100
    n_features = 30
    
    data = np.random.randn(n_samples, n_features)
    columns = ['Time', 'Amount'] + [f'V{i}' for i in range(1, 29)]
    
    df = pd.DataFrame(data, columns=columns)
    return df


class TestPreprocessingPipeline:
    """Test preprocessing pipeline."""
    
    def test_pipeline_build_and_transform(self, sample_data):
        """Test pipeline building and transformation."""
        pipeline = PreprocessingPipeline()
        
        # Build pipeline
        pipeline.build(sample_data)
        assert pipeline.transformer is not None
        assert pipeline.feature_names is not None
        
        # Transform data
        X_processed = pipeline.transform(sample_data)
        assert X_processed.shape == sample_data.shape
        assert X_processed.dtype == np.float32
    
    def test_pipeline_fit_transform(self, sample_data):
        """Test fit_transform method."""
        pipeline = PreprocessingPipeline()
        X_processed = pipeline.fit_transform(sample_data)
        
        assert X_processed.shape == sample_data.shape
        assert isinstance(X_processed, np.ndarray)


class TestStandardAutoencoder:
    """Test Standard Autoencoder."""
    
    def test_model_build(self):
        """Test model architecture."""
        model = StandardAutoencoder.build(input_dim=30, bottleneck_dim=8)
        
        assert model is not None
        assert model.input_shape == (None, 30)
        assert model.output_shape == (None, 30)
        
        # Check bottleneck layer
        bottleneck_layer = model.get_layer('bottleneck')
        assert bottleneck_layer.output_shape == (None, 8)
    
    def test_model_prediction(self, sample_data):
        """Test model prediction."""
        model = StandardAutoencoder.build(input_dim=30, bottleneck_dim=8)
        
        X = sample_data.values.astype(np.float32)
        predictions = model.predict(X, verbose=0)
        
        assert predictions.shape == X.shape
        assert predictions.dtype == np.float32


class TestTransformerAutoencoder:
    """Test Transformer Autoencoder."""
    
    def test_model_build(self):
        """Test model architecture."""
        model = TransformerAutoencoder.build(input_dim=30, num_heads=4, 
                                            bottleneck_dim=8, ff_dim=32)
        
        assert model is not None
        assert model.input_shape == (None, 30)
        assert model.output_shape == (None, 30)
        
        # Check bottleneck layer
        bottleneck_layer = model.get_layer('bottleneck')
        assert bottleneck_layer.output_shape == (None, 8)
    
    def test_model_prediction(self, sample_data):
        """Test model prediction."""
        model = TransformerAutoencoder.build(input_dim=30, num_heads=4,
                                            bottleneck_dim=8, ff_dim=32)
        
        X = sample_data.values.astype(np.float32)
        predictions = model.predict(X, verbose=0)
        
        assert predictions.shape == X.shape
        assert predictions.dtype == np.float32
