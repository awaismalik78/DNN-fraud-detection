"""
Launcher script for the Fraud Detection API (Transformer-based)
Run this to start the inference API server
"""

import subprocess
import sys
import os

def main():
    """Start the API server"""
    print("\n" + "="*70)
    print("🚀 FRAUD DETECTION API SERVER (Transformer Autoencoder)")
    print("="*70)
    
    # FIX: Removed the extra os.path.dirname so it stays in the 'DNN project' folder
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    print("\n📍 Project Root:", project_root)
    print("📂 Models Location: saved_models/")
    print("🔧 Launching with uvicorn...")
    print("\n" + "="*70)
    print("API ENDPOINTS:")
    print("  • Health:         GET    http://localhost:8000/health")
    print("  • Predict:        POST   http://localhost:8000/predict")
    print("  • Predict Batch:  POST   http://localhost:8000/predict-batch")
    print("  • Statistics:     GET    http://localhost:8000/stats")
    print("  • Documentation:  HTTP   http://localhost:8000/docs")
    print("="*70)
    print("\n⏳ Initializing... This will:")
    print("  1. Load the Transformer Autoencoder model")
    print("  2. Load the preprocessing pipeline")
    print("  3. Start the API server on port 8000")
    print("\n")
    
    try:
        # Run the app with uvicorn
        subprocess.run(
            [sys.executable, "-m", "uvicorn", 
             "src.inference.app:app",
             "--host", "0.0.0.0",
             "--port", "8000",
             "--reload"],
            cwd=project_root
        )
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("🛑 API Server Stopped")
        print("="*70 + "\n")
    except Exception as e:
        print(f"\n✗ Error starting API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()