"""
Project initialization and verification script
"""

import os
import sys
from pathlib import Path

def verify_project_structure():
    """Verify project structure is correctly set up."""
    
    project_root = Path(__file__).parent
    
    required_dirs = [
        'data',
        'data/raw',
        'data/processed',
        'notebooks',
        'src',
        'src/preprocessing',
        'src/models',
        'src/inference',
        'saved_models',
        'tests',
    ]
    
    required_files = [
        'requirements.txt',
        'README.md',
        'GETTING_STARTED.md',
        'config.py',
        '.gitignore',
        'setup.sh',
        'setup.ps1',
        'src/__init__.py',
        'src/preprocessing/__init__.py',
        'src/preprocessing/pipeline.py',
        'src/models/__init__.py',
        'src/models/autoencoders.py',
        'src/inference/__init__.py',
        'src/inference/detector.py',
        'src/inference/api.py',
        'tests/test_models.py',
        'notebooks/colab_training_pipeline.ipynb',
    ]
    
    print("=" * 60)
    print("PROJECT STRUCTURE VERIFICATION")
    print("=" * 60)
    
    # Check directories
    print("\n✓ CHECKING DIRECTORIES:")
    all_dirs_ok = True
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        exists = full_path.exists() and full_path.is_dir()
        status = "✓" if exists else "✗"
        print(f"  {status} {dir_path}")
        if not exists:
            all_dirs_ok = False
    
    # Check files
    print("\n✓ CHECKING FILES:")
    all_files_ok = True
    for file_path in required_files:
        full_path = project_root / file_path
        exists = full_path.exists() and full_path.is_file()
        status = "✓" if exists else "✗"
        print(f"  {status} {file_path}")
        if not exists:
            all_files_ok = False
    
    print("\n" + "=" * 60)
    if all_dirs_ok and all_files_ok:
        print("✓ PROJECT STRUCTURE VERIFIED SUCCESSFULLY!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run setup script (setup.ps1 for Windows, setup.sh for macOS/Linux)")
        print("2. Upload notebooks/colab_training_pipeline.ipynb to Google Colab")
        print("3. Follow GETTING_STARTED.md for detailed instructions")
        return 0
    else:
        print("✗ SOME FILES/DIRECTORIES ARE MISSING!")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(verify_project_structure())
