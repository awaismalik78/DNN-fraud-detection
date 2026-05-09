# 🚀 Phase 7 & 8: Deployment & Advanced Setup

## Phase 7: REST API Deployment

### Quick Start

**Option 1: Direct Start**
```powershell
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Start the API
python start_api.py
```

**Option 2: Manual Uvicorn**
```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Run API
python -m uvicorn src.inference.api:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

#### 1. **Health Check**
```bash
curl http://localhost:8000/health
```
Response:
```json
{"status": "healthy", "model_loaded": true}
```

#### 2. **Get Model Statistics**
```bash
curl http://localhost:8000/stats
```
Response:
```json
{
  "model_name": "Standard_Autoencoder",
  "input_shape": [null, 30],
  "output_shape": [null, 30],
  "total_parameters": 50432
}
```

#### 3. **Single Transaction Prediction**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Time": 0.0,
    "Amount": 149.62,
    "V1": -1.3598,
    "V2": -0.0747,
    "V3": 1.0000,
    "V4": -0.5516,
    "V5": -0.6179,
    "V6": -0.9913,
    "V7": -0.3110,
    "V8": 1.4686,
    "V9": -0.4536,
    "V10": 0.2053,
    "V11": 0.0258,
    "V12": 0.4038,
    "V13": 1.6045,
    "V14": 0.5605,
    "V15": 0.2696,
    "V16": -0.2565,
    "V17": -0.5869,
    "V18": -0.0299,
    "V19": -0.4676,
    "V20": 0.2600,
    "V21": 0.0896,
    "V22": 0.3798,
    "V23": 0.1113,
    "V24": -0.2694,
    "V25": -0.3473,
    "V26": -0.4045,
    "V27": 0.0973,
    "V28": 0.2750
  }'
```

Response:
```json
{
  "is_anomaly": false,
  "reconstruction_error": 0.235,
  "confidence": 0.52
}
```

#### 4. **Batch Predictions**
```bash
curl -X POST "http://localhost:8000/predict-batch" \
  -H "Content-Type: application/json" \
  -d '{
    "transactions": [
      {
        "Time": 0.0,
        "Amount": 149.62,
        "V1": -1.3598,
        ...
      },
      {
        "Time": 1.0,
        "Amount": 2.69,
        "V1": -0.5234,
        ...
      }
    ],
    "percentile": 95
  }'
```

Response:
```json
{
  "predictions": [
    {"is_anomaly": false, "reconstruction_error": 0.235, "confidence": 0.52},
    {"is_anomaly": true, "reconstruction_error": 1.543, "confidence": 0.98}
  ],
  "anomaly_rate": 0.5,
  "threshold_used": 0.87,
  "total_samples": 2,
  "anomalies_detected": 1
}
```

### Interactive API Documentation

Visit **http://localhost:8000/docs** for Swagger UI with:
- ✓ Endpoint descriptions
- ✓ Try-it-out functionality
- ✓ Request/response examples
- ✓ Schema definitions

---

## Phase 8: Production Deployment (Advanced)

### 8.1 Docker Containerization

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run API
CMD ["uvicorn", "src.inference.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
# Build image
docker build -t fraud-detection-api:latest .

# Run container
docker run -p 8000:8000 fraud-detection-api:latest

# Test
curl http://localhost:8000/health
```

### 8.2 Docker Compose (Multi-service)

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./saved_models:/app/saved_models
    environment:
      - PYTHONUNBUFFERED=1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Run with compose:
```bash
docker-compose up
```

### 8.3 AWS Lambda Deployment

1. **Install AWS CLI**
   ```bash
   pip install awscli
   ```

2. **Create Lambda handler** (`lambda_handler.py`):
   ```python
   import json
   import joblib
   import tensorflow as tf
   from src.inference.detector import AnomalyDetector
   
   detector = None
   
   def lambda_handler(event, context):
       global detector
       if detector is None:
           detector = AnomalyDetector(
               '/tmp/preprocessor.joblib',
               '/tmp/standard_autoencoder.keras'
           )
       
       # Parse input
       transaction = json.loads(event['body'])
       
       # Predict
       result = detector.predict_anomalies(pd.DataFrame([transaction]))
       
       return {
           'statusCode': 200,
           'body': json.dumps({
               'is_anomaly': bool(result['predictions'][0]),
               'error': float(result['reconstruction_errors'][0])
           })
       }
   ```

3. **Deploy to AWS**
   ```bash
   zip lambda.zip lambda_handler.py -r src
   aws lambda create-function \
     --function-name fraud-detection \
     --runtime python3.11 \
     --role arn:aws:iam::YOUR_ACCOUNT:role/service-role \
     --handler lambda_handler.lambda_handler \
     --zip-file fileb://lambda.zip
   ```

### 8.4 Google Cloud Run Deployment

1. **Create `main.py`** (for Cloud Run):
   ```python
   from src.inference.api import app
   
   if __name__ == "__main__":
       import uvicorn
       port = int(os.environ.get("PORT", 8000))
       uvicorn.run(app, host="0.0.0.0", port=port)
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy fraud-detection \
     --source . \
     --platform managed \
     --region us-central1
   ```

### 8.5 Kubernetes Deployment

Create `k8s-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fraud-detection-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fraud-detection
  template:
    metadata:
      labels:
        app: fraud-detection
    spec:
      containers:
      - name: api
        image: fraud-detection-api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: fraud-detection-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: fraud-detection
```

Deploy:
```bash
kubectl apply -f k8s-deployment.yaml
kubectl get pods
kubectl get service fraud-detection-service
```

### 8.6 Monitoring & Logging

**Add Prometheus metrics**:
```python
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
prediction_counter = Counter('predictions_total', 'Total predictions', ['model'])
anomaly_counter = Counter('anomalies_detected_total', 'Total anomalies', ['model'])
latency_histogram = Histogram('prediction_latency_seconds', 'Prediction latency')

@app.get("/metrics")
async def metrics():
    return generate_latest()
```

**Enable logging**:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Prediction made: anomaly={is_anomaly}, error={error:.4f}")
```

### 8.7 Performance Optimization

**Add caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=1)
def load_model():
    return tf.keras.models.load_model('saved_models/standard_autoencoder.keras')
```

**Batch processing**:
```python
@app.post("/predict-batch-optimized")
async def predict_batch_optimized(batch: BatchTransactionInput):
    # Process in chunks for memory efficiency
    chunk_size = 1000
    predictions = []
    
    for i in range(0, len(batch.transactions), chunk_size):
        chunk = batch.transactions[i:i+chunk_size]
        chunk_pred = detector.predict_anomalies(pd.DataFrame([t.dict() for t in chunk]))
        predictions.extend(chunk_pred['predictions'])
    
    return {'predictions': predictions}
```

---

## Deployment Checklist

- [ ] Phase 7: FastAPI running locally
- [ ] [ ] All endpoints tested with curl/Postman
- [ ] [ ] API documentation accessible at /docs
- [ ] [ ] Health check returning healthy status
- [ ] [ ] Phase 8a: Dockerfile created and tested
- [ ] [ ] Docker image builds successfully
- [ ] [ ] Container runs and serves requests
- [ ] [ ] Docker Compose tested
- [ ] [ ] AWS credentials configured
- [ ] [ ] Lambda function deployed
- [ ] [ ] Lambda tested via AWS Console
- [ ] [ ] Google Cloud credentials configured
- [ ] [ ] Cloud Run deployment successful
- [ ] [ ] Kubernetes cluster available
- [ ] [ ] K8s deployment applied
- [ ] [ ] Pods running and healthy
- [ ] [ ] Load balancer responding
- [ ] [ ] Monitoring metrics collecting
- [ ] [ ] Logging configured
- [ ] [ ] Performance optimizations deployed

---

## Quick Reference: API Testing

### Python Client
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Health check
r = requests.get(f"{BASE_URL}/health")
print(r.json())

# Single prediction
transaction = {
    "Time": 0.0,
    "Amount": 149.62,
    "V1": -1.3598,
    # ... all 30 features
}
r = requests.post(f"{BASE_URL}/predict", json=transaction)
print(r.json())

# Batch prediction
batch = {
    "transactions": [transaction, transaction],
    "percentile": 95
}
r = requests.post(f"{BASE_URL}/predict-batch", json=batch)
print(r.json())
```

---

**Next Step**: Run `python start_api.py` to launch the API server!

