"""
Phase 7: FastAPI Service Starter
Quick start script for the REST API
"""

import subprocess
import sys
from pathlib import Path

def start_api():
    """Start the FastAPI server."""
    
    print("="*70)
    print("PHASE 7: STARTING FASTAPI SERVICE")
    print("="*70)
    
    # Check if models exist
    saved_models = Path('saved_models')
    required_files = [
        'preprocessor.joblib',
        'standard_autoencoder.keras'
    ]
    
    print("\n[Step 1] Checking model files...")
    for file in required_files:
        if not (saved_models / file).exists():
            print(f"  ✗ {file} not found!")
            print("\nPlease ensure models are downloaded from Colab to saved_models/")
            return False
        print(f"  ✓ {file}")
    
    print("\n[Step 2] Starting FastAPI server...")
    print("\n  API will be available at: http://localhost:8000")
    print("  API documentation at: http://localhost:8000/docs")
    print("  Swagger UI at: http://localhost:8000/redoc")
    print("\n  Press Ctrl+C to stop the server\n")
    
    # Start uvicorn
    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn',
            'src.inference.api:app',
            '--reload',
            '--host', '0.0.0.0',
            '--port', '8000'
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n  Server stopped.")
    except FileNotFoundError:
        print("\n  ✗ uvicorn not found. Install FastAPI first:")
        print("    pip install fastapi uvicorn")
        return False
    
    return True

if __name__ == '__main__':
    success = start_api()
    sys.exit(0 if success else 1)
