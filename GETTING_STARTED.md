# Getting Started Guide

## Project Overview

This is an advanced MLOps project for Credit Card Fraud Detection using:
- **Standard Deep Autoencoder** for unsupervised anomaly detection
- **Tabular Transformer Autoencoder** for feature interaction modeling

Both models are trained on legitimate transactions only and detect fraud by measuring reconstruction error.

---

## Quick Start

### 1. Windows Setup

```powershell
# Run PowerShell as Administrator
.\setup.ps1
```

### 2. macOS/Linux Setup

```bash
chmod +x setup.sh
./setup.sh
```

### 3. Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate environment (choose one)
source venv/bin/activate          # Linux/macOS
venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Project Structure

```
DNN project/
├── data/                          # Data storage
│   ├── raw/                      # Raw dataset
│   └── processed/                # Processed data
├── notebooks/                    # Jupyter notebooks
│   └── colab_training_pipeline.ipynb  # Main training script
├── src/                          # Source code
│   ├── preprocessing/
│   │   └── pipeline.py           # Data preprocessing
│   ├── models/
│   │   └── autoencoders.py       # Model architectures
│   └── inference/
│       ├── detector.py           # Anomaly detection
│       └── api.py                # FastAPI service
├── saved_models/                 # Trained models
│   ├── preprocessor.joblib       # (after training)
│   ├── standard_autoencoder.keras
│   └── transformer_autoencoder.keras
├── tests/                        # Unit tests
├── config.py                     # Configuration
├── requirements.txt              # Dependencies
└── README.md                     # Documentation
```

---

## Training Phase (Google Colab)

### Step 1: Prepare Kaggle API
1. Go to [kaggle.com](https://www.kaggle.com/settings/account)
2. Click "Create New API Token" → saves `kaggle.json`

### Step 2: Run Colab Notebook
1. Open [Google Colab](https://colab.research.google.com)
2. Upload `notebooks/colab_training_pipeline.ipynb`
3. Follow the notebook steps:
   - Install dependencies
   - Upload your `kaggle.json`
   - Download the dataset
   - Train both models
   - Export models and preprocessor

### Step 3: Download Models
After training completes:
1. Download `preprocessor.joblib`
2. Download `standard_autoencoder.keras`
3. Download `transformer_autoencoder.keras`
4. Save to your `saved_models/` folder

---

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_models.py -v

# Run with coverage
pytest tests/ --cov=src
```

---

## Using Trained Models

### Option 1: Python Script

```python
from src.inference.detector import AnomalyDetector
import pandas as pd

# Load detector
detector = AnomalyDetector(
    preprocessor_path="saved_models/preprocessor.joblib",
    model_path="saved_models/standard_autoencoder.keras"
)

# Predict on new data
transactions = pd.read_csv("new_transactions.csv")
results = detector.predict_anomalies(
    transactions,
    threshold=None,  # Uses 95th percentile
    percentile=95
)

print(f"Anomalies detected: {results['anomaly_count']}")
print(f"Anomaly rate: {results['anomaly_rate']:.2%}")
```

### Option 2: FastAPI Service

```bash
# Start API server
python -m uvicorn src.inference.api:app --reload

# API will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

**Example API call:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Time": 0.0,
    "Amount": 149.62,
    "V1": -1.3598,
    "V2": -0.0747,
    ...
  }'
```

---

## Model Architecture Details

### Standard Autoencoder
```
Input (30)
  ↓
Dense(64) → BatchNorm → ReLU
  ↓
Dense(32) → BatchNorm → ReLU
  ↓
Dense(16) → BatchNorm → ReLU
  ↓
Bottleneck (8) ← [Compressed representation]
  ↓
Dense(16) → BatchNorm → ReLU
  ↓
Dense(32) → BatchNorm → ReLU
  ↓
Dense(64) → BatchNorm → ReLU
  ↓
Output (30)
```

### Transformer Autoencoder
```
Input (30)
  ↓
Embedding Layer (32)
  ↓
Multi-Head Attention (4 heads)
  ↓
Feed-Forward Network
  ↓
Bottleneck (8) ← [Compressed representation]
  ↓
Multi-Head Attention (4 heads)
  ↓
Feed-Forward Network
  ↓
Reconstruction Layer (30)
  ↓
Output (30)
```

---

## Configuration

Edit `config.py` to customize:
- Model hyperparameters
- Anomaly detection thresholds
- Data paths
- API settings

---

## Troubleshooting

### Issue: Models not found
**Solution:** Ensure saved models are in `saved_models/` folder after training

### Issue: Memory errors during training
**Solution:** Reduce batch size in config.py or split data into smaller chunks

### Issue: API won't start
**Solution:** Check port 8000 is not in use, or specify different port:
```bash
python -m uvicorn src.inference.api:app --port 8001
```

---

## Next Steps

1. ✅ Run setup script
2. ✅ Train models in Google Colab
3. ✅ Download trained models to `saved_models/`
4. ✅ Run tests: `pytest tests/`
5. ✅ Test predictions with Python or FastAPI
6. ✅ Deploy to production

---

## Support & Resources

- **TensorFlow Docs**: https://www.tensorflow.org/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Scikit-Learn**: https://scikit-learn.org/
- **Kaggle Dataset**: https://www.kaggle.com/mlg-ulb/creditcardfraud

