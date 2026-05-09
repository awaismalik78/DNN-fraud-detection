# Credit Card Fraud Detection MLOps Project

Advanced unsupervised anomaly detection using Deep Autoencoder and Tabular Transformer Autoencoder.

## Project Structure

```
DNN project/
├── data/                    # Raw and processed data
├── notebooks/              # Jupyter notebooks and Colab scripts
├── src/
│   ├── preprocessing/      # Data preprocessing pipeline
│   ├── models/            # Model architectures
│   └── inference/         # Inference utilities
├── saved_models/          # Trained models and preprocessors
├── tests/                 # Unit tests
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Setup Instructions

### 1. Clone/Setup Environment
```bash
cd "c:\Users\awais\Desktop\DNN project"
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python -c "import tensorflow as tf; print(f'TensorFlow version: {tf.__version__}')"
```

## Model Architectures

### Model 1: Standard Deep Autoencoder
- Input: 30 features
- Encoder: Dense layers with ReLU activation and batch normalization
- Bottleneck: Compressed latent representation
- Decoder: Mirror architecture for reconstruction
- Loss: Mean Squared Error (MSE)

### Model 2: Tabular Transformer Autoencoder
- Input: 30 features
- Multi-Head Attention: Captures feature interactions
- Transformer Encoder: Self-attention mechanism
- Bottleneck: Compressed latent representation
- Transformer Decoder: Reconstruct from latent space
- Loss: Mean Squared Error (MSE)

## Training (Colab)

Run `notebooks/colab_training_pipeline.ipynb` in Google Colab:
1. Connects to Kaggle ULB Credit Card Fraud dataset
2. Preprocesses data (StandardScaler on Time & Amount)
3. Trains both models on legitimate transactions
4. Exports models and preprocessor

## Outputs
- `saved_models/preprocessor.joblib` - Fitted preprocessing pipeline
- `saved_models/standard_autoencoder.keras` - Standard autoencoder model
- `saved_models/transformer_autoencoder.keras` - Transformer autoencoder model

## Inference

Use the trained models to detect anomalies in new transactions.
