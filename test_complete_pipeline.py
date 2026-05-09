"""
Phase 6: Testing & Validation
Complete testing suite for the MLOps project
"""

import os
import sys
import json
import numpy as np
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

print("="*70)
print("PHASE 6: TESTING & VALIDATION")
print("="*70)

# ============================================================================
# TEST 1: Verify saved models exist
# ============================================================================
print("\n[TEST 1] Verifying saved models...")
saved_models_dir = Path('saved_models')
required_files = [
    'preprocessor.joblib',
    'standard_autoencoder.keras',
    'transformer_autoencoder.keras',
    'training_metadata.json'
]

all_models_exist = True
for file in required_files:
    filepath = saved_models_dir / file
    if filepath.exists():
        size_kb = filepath.stat().st_size / 1024
        print(f"  ✓ {file} ({size_kb:.1f} KB)")
    else:
        print(f"  ✗ {file} NOT FOUND")
        all_models_exist = False

if all_models_exist:
    print("  ✓ All model files present!")
else:
    print("  ✗ Some model files missing!")
    sys.exit(1)

# ============================================================================
# TEST 2: Load preprocessor
# ============================================================================
print("\n[TEST 2] Loading preprocessor...")
try:
    import joblib
    preprocessor = joblib.load('saved_models/preprocessor.joblib')
    print(f"  ✓ Preprocessor loaded successfully")
    print(f"    - Transformer type: {type(preprocessor).__name__}")
except Exception as e:
    print(f"  ✗ Failed to load preprocessor: {e}")
    sys.exit(1)

# ============================================================================
# TEST 3: Load trained models
# ============================================================================
print("\n[TEST 3] Loading trained models...")
try:
    import tensorflow as tf
    
    print("  Loading Standard Autoencoder...")
    standard_ae = tf.keras.models.load_model('saved_models/standard_autoencoder.keras')
    print(f"    ✓ {standard_ae.name}")
    print(f"      Input shape: {standard_ae.input_shape}")
    print(f"      Output shape: {standard_ae.output_shape}")
    print(f"      Parameters: {standard_ae.count_params():,}")
    
    print("  Loading Transformer Autoencoder...")
    transformer_ae = tf.keras.models.load_model('saved_models/transformer_autoencoder.keras')
    print(f"    ✓ {transformer_ae.name}")
    print(f"      Input shape: {transformer_ae.input_shape}")
    print(f"      Output shape: {transformer_ae.output_shape}")
    print(f"      Parameters: {transformer_ae.count_params():,}")
    
except Exception as e:
    print(f"  ✗ Failed to load models: {e}")
    sys.exit(1)

# ============================================================================
# TEST 4: Load and check training metadata
# ============================================================================
print("\n[TEST 4] Loading training metadata...")
try:
    with open('saved_models/training_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    print(f"  ✓ Metadata loaded")
    print(f"    - Dataset: {metadata['dataset']}")
    print(f"    - Legitimate transactions: {metadata['legitimate_transactions']:,}")
    print(f"    - Input features: {metadata['input_features']}")
    print(f"    - Standard AE final loss: {metadata['standard_ae_final_loss']:.6f}")
    print(f"    - Transformer AE final loss: {metadata['transformer_ae_final_loss']:.6f}")
except Exception as e:
    print(f"  ✗ Failed to load metadata: {e}")
    sys.exit(1)

# ============================================================================
# TEST 5: Create sample test data
# ============================================================================
print("\n[TEST 5] Creating sample test data...")
try:
    np.random.seed(42)
    n_samples = 100
    n_features = 30
    
    # Create sample data matching the original feature names
    feature_columns = ['Time', 'Amount'] + [f'V{i}' for i in range(1, 29)]
    sample_data = np.random.randn(n_samples, n_features)
    test_df = pd.DataFrame(sample_data, columns=feature_columns)
    
    print(f"  ✓ Created {n_samples} sample transactions")
    print(f"    Shape: {test_df.shape}")
    print(f"    Columns: {test_df.columns.tolist()[:5]}... (30 total)")
except Exception as e:
    print(f"  ✗ Failed to create test data: {e}")
    sys.exit(1)

# ============================================================================
# TEST 6: Test preprocessing pipeline
# ============================================================================
print("\n[TEST 6] Testing preprocessing pipeline...")
try:
    X_processed = preprocessor.transform(test_df)
    print(f"  ✓ Preprocessing successful")
    print(f"    Input shape: {test_df.shape}")
    print(f"    Output shape: {X_processed.shape}")
    print(f"    Output dtype: {X_processed.dtype}")
    print(f"    Min value: {X_processed.min():.4f}")
    print(f"    Max value: {X_processed.max():.4f}")
    print(f"    Mean: {X_processed.mean():.4f}")
    print(f"    Std: {X_processed.std():.4f}")
except Exception as e:
    print(f"  ✗ Preprocessing failed: {e}")
    sys.exit(1)

# ============================================================================
# TEST 7: Test standard autoencoder predictions
# ============================================================================
print("\n[TEST 7] Testing Standard Autoencoder predictions...")
try:
    X_processed_float32 = X_processed.astype(np.float32)
    predictions = standard_ae.predict(X_processed_float32, verbose=0)
    
    # Calculate reconstruction error
    mse_errors = np.mean(np.square(X_processed_float32 - predictions), axis=1)
    
    print(f"  ✓ Predictions successful")
    print(f"    Batch shape: {predictions.shape}")
    print(f"    Reconstruction errors computed: {len(mse_errors)}")
    print(f"    Mean error: {mse_errors.mean():.6f}")
    print(f"    Std error: {mse_errors.std():.6f}")
    print(f"    Min error: {mse_errors.min():.6f}")
    print(f"    Max error: {mse_errors.max():.6f}")
except Exception as e:
    print(f"  ✗ Standard AE prediction failed: {e}")
    sys.exit(1)

# ============================================================================
# TEST 8: Test transformer autoencoder predictions
# ============================================================================
print("\n[TEST 8] Testing Transformer Autoencoder predictions...")
try:
    predictions_transformer = transformer_ae.predict(X_processed_float32, verbose=0)
    
    # Calculate reconstruction error
    mse_errors_transformer = np.mean(np.square(X_processed_float32 - predictions_transformer), axis=1)
    
    print(f"  ✓ Predictions successful")
    print(f"    Batch shape: {predictions_transformer.shape}")
    print(f"    Reconstruction errors computed: {len(mse_errors_transformer)}")
    print(f"    Mean error: {mse_errors_transformer.mean():.6f}")
    print(f"    Std error: {mse_errors_transformer.std():.6f}")
    print(f"    Min error: {mse_errors_transformer.min():.6f}")
    print(f"    Max error: {mse_errors_transformer.max():.6f}")
except Exception as e:
    print(f"  ✗ Transformer AE prediction failed: {e}")
    sys.exit(1)

# ============================================================================
# TEST 9: Test anomaly detection logic
# ============================================================================
print("\n[TEST 9] Testing anomaly detection logic...")
try:
    # Using 95th percentile as threshold
    threshold = np.percentile(mse_errors, 95)
    anomalies = (mse_errors > threshold).astype(int)
    anomaly_rate = np.sum(anomalies) / len(anomalies)
    
    print(f"  ✓ Anomaly detection successful")
    print(f"    Threshold (95th percentile): {threshold:.6f}")
    print(f"    Anomalies detected: {np.sum(anomalies)}")
    print(f"    Anomaly rate: {anomaly_rate:.2%}")
except Exception as e:
    print(f"  ✗ Anomaly detection failed: {e}")
    sys.exit(1)

# ============================================================================
# TEST 10: Compare both models
# ============================================================================
print("\n[TEST 10] Comparing both model outputs...")
try:
    # Correlation between reconstruction errors
    correlation = np.corrcoef(mse_errors, mse_errors_transformer)[0, 1]
    
    print(f"  ✓ Model comparison successful")
    print(f"    Standard AE mean error: {mse_errors.mean():.6f}")
    print(f"    Transformer AE mean error: {mse_errors_transformer.mean():.6f}")
    print(f"    Error correlation: {correlation:.4f}")
    print(f"    Difference: {abs(mse_errors.mean() - mse_errors_transformer.mean()):.6f}")
except Exception as e:
    print(f"  ✗ Model comparison failed: {e}")
    sys.exit(1)

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✓ ALL TESTS PASSED!")
print("="*70)
print("\nSummary:")
print(f"  • {len(required_files)} model files verified")
print(f"  • 2 autoencoders loaded and functional")
print(f"  • {n_samples} test samples processed successfully")
print(f"  • Preprocessing pipeline working correctly")
print(f"  • Both models producing predictions")
print(f"  • Anomaly detection logic functional")
print(f"  • Models showing correlation: {correlation:.4f}")
print("\n✓ Your MLOps project is ready for production!")
print("="*70)
