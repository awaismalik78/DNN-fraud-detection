"""
Autoencoder Model Architectures
Defines Standard Deep Autoencoder and Tabular Transformer Autoencoder.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from typing import Tuple, List


class StandardAutoencoder:
    """Standard fully-connected Deep Autoencoder for anomaly detection."""
    
    @staticmethod
    def build(input_dim: int = 30, bottleneck_dim: int = 8) -> Model:
        """
        Build Standard Deep Autoencoder.
        
        Architecture:
        Input (input_dim) -> Dense(64) -> Dense(32) -> Dense(16) -> 
        Bottleneck (bottleneck_dim) -> Dense(16) -> Dense(32) -> Dense(64) -> Output (input_dim)
        
        Args:
            input_dim: Number of input features (default: 30)
            bottleneck_dim: Bottleneck dimension (default: 8)
            
        Returns:
            Compiled Keras model
        """
        # Encoder
        inputs = layers.Input(shape=(input_dim,))
        
        encoded = layers.Dense(64, activation='relu')(inputs)
        encoded = layers.BatchNormalization()(encoded)
        
        encoded = layers.Dense(32, activation='relu')(encoded)
        encoded = layers.BatchNormalization()(encoded)
        
        encoded = layers.Dense(16, activation='relu')(encoded)
        encoded = layers.BatchNormalization()(encoded)
        
        # Bottleneck
        bottleneck = layers.Dense(bottleneck_dim, activation='relu', name='bottleneck')(encoded)
        
        # Decoder
        decoded = layers.Dense(16, activation='relu')(bottleneck)
        decoded = layers.BatchNormalization()(decoded)
        
        decoded = layers.Dense(32, activation='relu')(decoded)
        decoded = layers.BatchNormalization()(decoded)
        
        decoded = layers.Dense(64, activation='relu')(decoded)
        decoded = layers.BatchNormalization()(decoded)
        
        # Output
        outputs = layers.Dense(input_dim, activation='linear')(decoded)
        
        # Create and compile model
        model = Model(inputs, outputs, name='Standard_Autoencoder')
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        return model


class TransformerAutoencoder:
    """Tabular Transformer Autoencoder with Multi-Head Attention."""
    
    @staticmethod
    def build(input_dim: int = 30, num_heads: int = 4, 
              bottleneck_dim: int = 8, ff_dim: int = 32) -> Model:
        """
        Build Tabular Transformer Autoencoder.
        
        Uses Multi-Head Attention to capture feature interactions.
        
        Args:
            input_dim: Number of input features (default: 30)
            num_heads: Number of attention heads (default: 4)
            bottleneck_dim: Bottleneck dimension (default: 8)
            ff_dim: Feed-forward dimension (default: 32)
            
        Returns:
            Compiled Keras model
        """
        # Encoder
        inputs = layers.Input(shape=(input_dim,))
        
        # Project to embedding
        embedding_dim = 32
        x = layers.Dense(embedding_dim, activation='relu')(inputs)
        x = layers.LayerNormalization()(x)
        
        # Reshape for attention
        x = layers.Reshape((input_dim, 1))(x)
        
        # Transformer encoder block
        attention_output = layers.MultiHeadAttention(
            num_heads=num_heads,
            key_dim=8
        )(x, x)
        x = layers.Add()([x, attention_output])
        x = layers.LayerNormalization()(x)
        
        # Feed-forward network
        ff_output = layers.Dense(ff_dim, activation='relu')(x)
        ff_output = layers.Dense(1)(ff_output)
        x = layers.Add()([x, ff_output])
        x = layers.LayerNormalization()(x)
        
        # Compress to bottleneck
        x = layers.Flatten()(x)
        bottleneck = layers.Dense(bottleneck_dim, activation='relu', name='bottleneck')(x)
        
        # Decoder
        x = layers.Dense(input_dim * 1, activation='relu')(bottleneck)
        x = layers.Reshape((input_dim, 1))(x)
        
        # Transformer decoder block
        attention_output = layers.MultiHeadAttention(
            num_heads=num_heads,
            key_dim=8
        )(x, x)
        x = layers.Add()([x, attention_output])
        x = layers.LayerNormalization()(x)
        
        # Feed-forward network
        ff_output = layers.Dense(ff_dim, activation='relu')(x)
        ff_output = layers.Dense(1)(ff_output)
        x = layers.Add()([x, ff_output])
        x = layers.LayerNormalization()(x)
        
        # Reconstruct
        x = layers.Flatten()(x)
        outputs = layers.Dense(input_dim, activation='linear')(x)
        
        # Create and compile model
        model = Model(inputs, outputs, name='Transformer_Autoencoder')
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        return model
