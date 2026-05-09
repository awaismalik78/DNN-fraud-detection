# 🔄 API COMPARISON: api.py vs app.py

**Quick Reference**: Understanding the two fraud detection APIs

---

## 📋 OVERVIEW

| Feature | `api.py` | `app.py` | 
|---------|----------|---------|
| **Focus** | General-purpose (both models) | Transformer-specific |
| **Complexity** | Advanced | Educational |
| **Features** | Extended | Core |
| **Purpose** | Production | Learning/Reference |
| **Launch** | `python start_api.py` | `python run_inference_api.py` |

---

## 🎯 WHAT EACH API DOES

### api.py (Existing - General Purpose)

**Purpose**: Handle both autoencoders with full feature set

**Capabilities**:
- ✅ Choose between Standard or Transformer model
- ✅ Get embeddings for visualization
- ✅ Batch processing with configurable thresholds
- ✅ Percentile-based anomaly detection
- ✅ Multiple anomaly scoring methods
- ✅ Model comparison features
- ✅ Monitoring endpoints
- ✅ Caching support

**Endpoints**:
- `GET /health` - Status
- `GET /stats` - Statistics
- `POST /predict` - Single prediction with model selection
- `POST /predict-batch` - Batch scoring
- `GET /embeddings` - Extract bottleneck representations

**Use Case**: Production system needing flexibility

---

### app.py (New - Transformer-Focused)

**Purpose**: Focused inference using ONLY Transformer model

**Capabilities**:
- ✅ Streamlined single-model design
- ✅ Simple threshold-based detection
- ✅ Clean implementation for learning
- ✅ MSE-based anomaly scoring
- ✅ Confidence calculation
- ✅ Batch predictions
- ✅ Model statistics

**Endpoints**:
- `GET /health` - Status
- `GET /stats` - Model info
- `POST /predict` - Single prediction (Transformer only)
- `POST /predict-batch` - Batch predictions (Transformer only)
- `GET /` - API info

**Use Case**: Learning, demonstration, Transformer-specific deployments

---

## 🔍 TECHNICAL COMPARISON

### Model Loading

**api.py**:
```python
# Loads BOTH models
standard_model = load('standard_autoencoder.keras')
transformer_model = load('transformer_autoencoder.keras')
preprocessor = load('preprocessor.joblib')
```

**app.py**:
```python
# Loads TRANSFORMER only
model = load('transformer_autoencoder.keras')
preprocessor = load('preprocessor.joblib')
```

---

### Prediction Flow

**api.py**:
```python
def predict(features, model_name="transformer", threshold=None):
    # 1. Preprocess
    X = preprocessor.transform(features)
    
    # 2. Choose model
    if model_name == "standard":
        model = standard_model
    else:
        model = transformer_model
    
    # 3. Get reconstruction
    recon = model.predict(X)
    
    # 4. Calculate error
    mse = mean((X - recon)^2)
    
    # 5. Apply threshold (percentile or fixed)
    if threshold == "percentile":
        is_anomaly = mse > percentile_threshold
    else:
        is_anomaly = mse > fixed_threshold
    
    return result
```

**app.py**:
```python
def predict_single(features):
    # 1. Preprocess
    X = preprocessor.transform(features)
    
    # 2. Transformer (no choice)
    recon = model.predict(X)
    
    # 3. Calculate MSE
    mse = mean((X - recon)^2)
    
    # 4. Fixed threshold
    is_fraud = mse > 0.8
    
    # 5. Calculate confidence
    confidence = (mse - threshold) / threshold if is_fraud else (threshold - mse) / threshold
    
    return result
```

---

### Request Structure

**api.py**:
```json
{
  "Time": 0,
  "Amount": 149.62,
  "V1": -1.3598,
  ...,
  "V28": -0.1086,
  "model": "transformer",    // Choose model
  "threshold": 0.95,         // Percentile
  "method": "percentile"     // Threshold method
}
```

**app.py**:
```json
{
  "Time": 0,
  "Amount": 149.62,
  "V1": -1.3598,
  ...,
  "V28": -0.1086
  // Simple - no model choice needed
}
```

---

### Response Structure

**api.py**:
```json
{
  "is_anomaly": false,
  "reconstruction_error": 0.234,
  "confidence": 0.98,
  "model_used": "transformer",
  "threshold_used": 0.95,
  "method": "percentile"
}
```

**app.py**:
```json
{
  "fraud_detected": false,
  "anomaly_score": 0.234,
  "threshold": 0.8,
  "confidence": 0.71
}
```

---

## 🚀 WHICH ONE TO USE?

### Use **api.py** (Existing) if you need:
- ✅ Flexibility between two models
- ✅ Percentile-based detection
- ✅ Advanced features
- ✅ Production system with multiple models
- ✅ Embedding extraction
- ✅ Caching support

### Use **app.py** (New) if you need:
- ✅ Simple, focused Transformer inference
- ✅ Educational reference implementation
- ✅ Minimal dependencies
- ✅ Easiest to understand and modify
- ✅ Transformer model only
- ✅ Learning how to build inference APIs

---

## 📝 CODE STRUCTURE

### api.py Structure
```
src/inference/api.py
├── Imports & Setup
├── CONFIGURATION (detailed)
├── Pydantic Models (request/response)
├── AnomalyDetector Class
│   ├── __init__
│   ├── predict_reconstruction_error()
│   ├── predict_anomalies()
│   └── get_embeddings()
├── FastAPI App
│   ├── Startup/Shutdown
│   ├── Health endpoint
│   ├── Stats endpoint
│   ├── Predict endpoint
│   ├── Predict-batch endpoint
│   └── Error handlers
└── Main execution (uvicorn)
```

### app.py Structure
```
src/inference/app.py
├── Imports & Setup
├── CONFIGURATION
├── Pydantic Models (request/response)
├── Global State (model, preprocessor)
├── Utility Functions
│   ├── load_model_and_preprocessor()
│   ├── preprocess_transaction()
│   ├── calculate_reconstruction_error()
│   └── detect_fraud()
├── FastAPI App
│   ├── Startup/Shutdown
│   ├── Health endpoint
│   ├── Predict endpoint
│   ├── Predict-batch endpoint
│   ├── Stats endpoint
│   └── Root endpoint
├── Error handlers
└── Main execution (uvicorn)
```

---

## 📊 FEATURE COMPARISON TABLE

| Feature | api.py | app.py |
|---------|--------|--------|
| Standard Autoencoder support | ✅ | ❌ |
| Transformer support | ✅ | ✅ |
| Model selection | ✅ | ❌ |
| Percentile detection | ✅ | ❌ |
| Fixed threshold | ✅ | ✅ |
| Single predictions | ✅ | ✅ |
| Batch predictions | ✅ | ✅ |
| Get embeddings | ✅ | ❌ |
| Caching | ✅ | ❌ |
| Health check | ✅ | ✅ |
| Model stats | ✅ | ✅ |
| Error handling | ✅ | ✅ |
| Type hints | ✅ | ✅ |
| Pydantic validation | ✅ | ✅ |
| Swagger docs | ✅ | ✅ |
| Lines of code | ~450 | ~400 |

---

## 💡 LEARNING PROGRESSION

### Phase 1: Understanding (Start Here)
→ Read `app.py` to learn basic structure
→ Simple, clear, easy to follow

### Phase 2: Production Ready
→ Use `api.py` for real deployments
→ More features, more flexibility

### Phase 3: Advanced
→ Customize either based on needs
→ Add authentication, logging, etc.

---

## 🔧 RUNNING BOTH APIs

**Run api.py**:
```powershell
python start_api.py
# or
python -m uvicorn src.inference.api:app --reload
```

**Run app.py**:
```powershell
python run_inference_api.py
# or
python -m uvicorn src.inference.app:app --reload
```

**Note**: Can't run both on port 8000 simultaneously. Use different ports:
```powershell
# Terminal 1
python start_api.py

# Terminal 2
python -m uvicorn src.inference.app:app --port 8001
```

Then:
- api.py: http://localhost:8000/docs
- app.py: http://localhost:8001/docs

---

## 🎯 QUICK DECISION MATRIX

```
Question: What are you doing?

  Learning → Use app.py
  ↓
  "I want to understand how it works"
  → Simple, focused, educational

  Production → Use api.py
  ↓
  "I need a robust system now"
  → Flexible, feature-rich, proven

  Demo/Proof → Use either
  ↓
  "I need to show it works quickly"
  → Both work, app.py is simpler

  Research → Use app.py
  ↓
  "I want to experiment"
  → Easy to modify, understand changes

  Enterprise → Use api.py
  ↓
  "I need all features"
  → Caching, embeddings, flexibility
```

---

## 📚 RELATED FILES

| File | Purpose |
|------|---------|
| `src/inference/api.py` | General-purpose inference API |
| `src/inference/app.py` | Transformer-focused API (NEW) |
| `start_api.py` | Launcher for api.py |
| `run_inference_api.py` | Launcher for app.py (NEW) |
| `INFERENCE_API_GUIDE.md` | app.py documentation (NEW) |
| `src/inference/detector.py` | Inference engine used by api.py |

---

## ✅ RECOMMENDED WORKFLOW

### For Learning:
1. Start with `app.py`
2. Read the code
3. Follow the execution flow
4. Understand each step
5. Run it locally
6. Make small modifications
7. Graduate to `api.py`

### For Production:
1. Review both options
2. Choose `api.py` for flexibility
3. Customize as needed
4. Add authentication
5. Deploy with Docker
6. Monitor and scale

---

## 🚀 NEXT STEPS

**Option 1: Learning Path**
```powershell
# 1. Read the guide
code INFERENCE_API_GUIDE.md

# 2. Read the code
code src/inference/app.py

# 3. Run it
python run_inference_api.py

# 4. Test in browser
http://localhost:8001/docs
```

**Option 2: Production Path**
```powershell
# 1. Read the guide
code INFERENCE_API_GUIDE.md

# 2. Understand the differences
# (This file)

# 3. Run existing API
python start_api.py

# 4. Deploy
# Follow DEPLOYMENT_GUIDE.md
```

---

## 📖 DOCUMENTATION

- **api.py**: See existing code comments
- **app.py**: See `INFERENCE_API_GUIDE.md` and inline comments
- **Comparison**: This file (you are here)

---

**Choose your path and get started! Both APIs are production-ready.** ✨

