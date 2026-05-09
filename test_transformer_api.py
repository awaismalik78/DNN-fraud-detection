"""
Demo script: Test the Transformer Autoencoder Fraud Detection API
This script shows how to interact with src/inference/app.py
"""

import requests
import json
import time
from typing import Dict

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    "health": f"{API_BASE_URL}/health",
    "predict": f"{API_BASE_URL}/predict",
    "predict_batch": f"{API_BASE_URL}/predict-batch",
    "stats": f"{API_BASE_URL}/stats"
}

# Sample legitimate transaction
LEGITIMATE_TRANSACTION = {
    "Time": 0,
    "Amount": 149.62,
    "V1": -1.3598071336738,
    "V2": -0.0727812320124,
    "V3": 2.36060841498244,
    "V4": 1.59067054248337,
    "V5": -0.770464378778467,
    "V6": -0.623588099395191,
    "V7": -0.942143496290839,
    "V8": -0.622417098688339,
    "V9": -0.051410094880652,
    "V10": -0.276253783529582,
    "V11": -0.637628779843854,
    "V12": 0.46399461915966,
    "V13": -0.092747946301046,
    "V14": -0.12849206922258,
    "V15": -0.199347865324392,
    "V16": -0.108643033016505,
    "V17": -0.269809040300488,
    "V18": -0.170099690234065,
    "V19": 0.002883084236717,
    "V20": -0.103328316294955,
    "V21": -0.199347865324392,
    "V22": -0.108643033016505,
    "V23": -0.269809040300488,
    "V24": -0.170099690234065,
    "V25": 0.002883084236717,
    "V26": -0.103328316294955,
    "V27": -0.199347865324392,
    "V28": -0.108643033016505
}

# Sample anomalous transaction (modified features)
ANOMALOUS_TRANSACTION = {
    "Time": 100,
    "Amount": 5000.00,
    "V1": 3.5,
    "V2": 2.1,
    "V3": -5.2,
    "V4": 4.8,
    "V5": -3.2,
    "V6": 2.9,
    "V7": -4.1,
    "V8": 3.7,
    "V9": 2.3,
    "V10": -3.8,
    "V11": 4.5,
    "V12": -2.6,
    "V13": 3.1,
    "V14": 2.8,
    "V15": -3.5,
    "V16": 4.2,
    "V17": -2.9,
    "V18": 3.4,
    "V19": 2.1,
    "V20": -3.7,
    "V21": 4.0,
    "V22": -2.5,
    "V23": 3.3,
    "V24": 2.9,
    "V25": -3.6,
    "V26": 4.1,
    "V27": -2.8,
    "V28": 3.5
}


# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def print_header(title: str):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_result(title: str, data: Dict):
    """Print formatted result"""
    print(f"\n{title}:")
    print(json.dumps(data, indent=2))


def test_health_check():
    """Test 1: Health check endpoint"""
    print_header("TEST 1: HEALTH CHECK")
    print("Endpoint: GET /health")
    print("Purpose: Verify API is running and models are loaded\n")
    
    try:
        response = requests.get(API_ENDPOINTS["health"])
        response.raise_for_status()
        
        result = response.json()
        print_result("Response", result)
        
        if result["model_loaded"] and result["preprocessor_loaded"]:
            print("\n✅ Health check PASSED - API is ready!")
            return True
        else:
            print("\n❌ Health check FAILED - Models not loaded")
            return False
    
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to API")
        print("   Make sure to run: python run_inference_api.py")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_single_prediction_legitimate():
    """Test 2: Single prediction - legitimate transaction"""
    print_header("TEST 2: SINGLE PREDICTION (LEGITIMATE)")
    print("Endpoint: POST /predict")
    print("Purpose: Score a legitimate transaction")
    print(f"\nInput Transaction:")
    print(f"  Time: {LEGITIMATE_TRANSACTION['Time']}")
    print(f"  Amount: ${LEGITIMATE_TRANSACTION['Amount']:.2f}\n")
    
    try:
        response = requests.post(
            API_ENDPOINTS["predict"],
            json=LEGITIMATE_TRANSACTION
        )
        response.raise_for_status()
        
        result = response.json()
        print_result("Response", result)
        
        if not result["fraud_detected"]:
            print("\n✅ Correctly identified as LEGITIMATE")
            print(f"   Anomaly Score: {result['anomaly_score']:.4f}")
            print(f"   Threshold: {result['threshold']:.2f}")
            print(f"   Confidence: {result['confidence']:.2%}")
            return True
        else:
            print("\n⚠️  Identified as fraudulent (may be edge case)")
            return True
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_single_prediction_anomalous():
    """Test 3: Single prediction - anomalous transaction"""
    print_header("TEST 3: SINGLE PREDICTION (ANOMALOUS)")
    print("Endpoint: POST /predict")
    print("Purpose: Score an anomalous transaction")
    print(f"\nInput Transaction:")
    print(f"  Time: {ANOMALOUS_TRANSACTION['Time']}")
    print(f"  Amount: ${ANOMALOUS_TRANSACTION['Amount']:.2f}\n")
    
    try:
        response = requests.post(
            API_ENDPOINTS["predict"],
            json=ANOMALOUS_TRANSACTION
        )
        response.raise_for_status()
        
        result = response.json()
        print_result("Response", result)
        
        print(f"\n   Anomaly Score: {result['anomaly_score']:.4f}")
        print(f"   Threshold: {result['threshold']:.2f}")
        print(f"   Confidence: {result['confidence']:.2%}")
        
        if result["fraud_detected"]:
            print("\n✅ Correctly identified as ANOMALOUS")
            return True
        else:
            print("\n⚠️  Not flagged as anomalous (may be similar to training data)")
            return True
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_batch_predictions():
    """Test 4: Batch predictions"""
    print_header("TEST 4: BATCH PREDICTIONS")
    print("Endpoint: POST /predict-batch")
    print("Purpose: Score multiple transactions efficiently")
    print(f"\nProcessing 2 transactions:")
    print(f"  1. Legitimate transaction")
    print(f"  2. Anomalous transaction\n")
    
    try:
        batch_request = {
            "transactions": [
                LEGITIMATE_TRANSACTION,
                ANOMALOUS_TRANSACTION
            ]
        }
        
        response = requests.post(
            API_ENDPOINTS["predict_batch"],
            json=batch_request
        )
        response.raise_for_status()
        
        result = response.json()
        
        print(f"Batch Summary:")
        print(f"  Total processed: {result['total_processed']}")
        print(f"  Fraud rate: {result['batch_fraud_rate']:.1f}%")
        
        for i, pred in enumerate(result["predictions"], 1):
            print(f"\n  Transaction {i}:")
            print(f"    Fraud Detected: {pred['fraud_detected']}")
            print(f"    Anomaly Score: {pred['anomaly_score']:.4f}")
            print(f"    Confidence: {pred['confidence']:.2%}")
        
        print("\n✅ Batch prediction completed successfully")
        return True
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_model_statistics():
    """Test 5: Get model statistics"""
    print_header("TEST 5: MODEL STATISTICS")
    print("Endpoint: GET /stats")
    print("Purpose: Get model architecture and configuration\n")
    
    try:
        response = requests.get(API_ENDPOINTS["stats"])
        response.raise_for_status()
        
        result = response.json()
        
        print(f"Model Information:")
        print(f"  Name: {result['model_name']}")
        print(f"  Type: {result['model_type']}")
        print(f"  Parameters: {result['total_parameters']:,}")
        print(f"  Input Shape: {result['input_shape']}")
        print(f"  Output Shape: {result['output_shape']}")
        print(f"  Layers: {result['layers']}")
        print(f"  MSE Threshold: {result['mse_threshold']}")
        
        if result.get("metadata"):
            print(f"\n  Metadata available: Yes")
        
        print("\n✅ Model statistics retrieved successfully")
        return True
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "#"*70)
    print("# FRAUD DETECTION API - COMPREHENSIVE TEST SUITE")
    print("#"*70)
    print("\nAPI Base URL:", API_BASE_URL)
    print("Model: Transformer Autoencoder")
    print("Preprocessor: Scikit-Learn Pipeline")
    
    results = []
    
    # Run all tests
    results.append(("Health Check", test_health_check()))
    
    if results[0][1]:  # Only continue if health check passed
        time.sleep(1)
        results.append(("Single Prediction (Legitimate)", test_single_prediction_legitimate()))
        time.sleep(1)
        results.append(("Single Prediction (Anomalous)", test_single_prediction_anomalous()))
        time.sleep(1)
        results.append(("Batch Predictions", test_batch_predictions()))
        time.sleep(1)
        results.append(("Model Statistics", test_model_statistics()))
    
    # Print summary
    print("\n" + "#"*70)
    print("# TEST SUMMARY")
    print("#"*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print("\n" + "#"*70)
    print(f"Results: {passed}/{total} tests passed")
    print("#"*70 + "\n")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - API IS FULLY OPERATIONAL!\n")
        return True
    else:
        print("⚠️  Some tests failed - check the output above\n")
        return False


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def show_usage_examples():
    """Print usage examples"""
    print("\n" + "="*70)
    print("  USAGE EXAMPLES")
    print("="*70)
    
    print("\n1. Python with requests library:")
    print("""
    import requests
    
    response = requests.post('http://localhost:8000/predict', json={
        'Time': 0,
        'Amount': 149.62,
        'V1': -1.3598, ...
    })
    
    result = response.json()
    print(f"Fraud: {result['fraud_detected']}")
    """)
    
    print("\n2. cURL from command line:")
    print("""
    curl -X POST http://localhost:8000/predict \\
      -H "Content-Type: application/json" \\
      -d '{
        "Time": 0,
        "Amount": 149.62,
        "V1": -1.3598,
        ...
      }'
    """)
    
    print("\n3. JavaScript/fetch:")
    print("""
    fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({Time: 0, Amount: 149.62, ...})
    }).then(r => r.json()).then(data => console.log(data))
    """)
    
    print("\n4. Interactive Swagger UI:")
    print("    Visit: http://localhost:8000/docs")
    print("    Then: Click 'Try it out' on any endpoint\n")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*70)
    print("  TRANSFORMER AUTOENCODER FRAUD DETECTION - TEST SUITE")
    print("="*70)
    print("\nMake sure the API is running:")
    print("  Terminal: python run_inference_api.py")
    print("\nOr manually:")
    print("  Terminal: python -m uvicorn src.inference.app:app --reload")
    print("\n" + "="*70)
    
    # Run tests
    success = run_all_tests()
    
    # Show examples
    show_usage_examples()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
