# 📂 Project Directory Tree & File Guide

```
DNN project/
│
├── 📄 CHECKLIST.md                      ← Your progress tracking (read this first!)
├── 📄 PROJECT_SUMMARY.md                ← Complete project overview
├── 📄 README.md                         ← What this project does
├── 📄 GETTING_STARTED.md                ← Setup & usage guide
├── 📄 requirements.txt                  ← Python dependencies
├── 📄 config.py                         ← Configuration settings
├── 📄 verify_setup.py                   ← Verify project structure
│
├── 🪟 setup.ps1                         ← Windows setup script
├── 🐧 setup.sh                          ← Linux/macOS setup script
│
├── 🔐 .gitignore                        ← Git exclusions
│
│
├── 📁 data/                             ← DATA DIRECTORY
│   ├── raw/                             ← Raw dataset (from Kaggle)
│   └── processed/                       ← Processed/cleaned data
│
│
├── 📁 notebooks/                        ← JUPYTER NOTEBOOKS
│   └── colab_training_pipeline.ipynb    ← ⭐ MAIN: Colab training script
│       │                                   (Train 2 autoencoders here)
│       │
│       ├── Kaggle API setup
│       ├── Download credit card dataset
│       ├── Preprocessing pipeline
│       ├── Standard Autoencoder (train)
│       ├── Transformer Autoencoder (train)
│       ├── Export models & preprocessor
│       └── Download files back to PC
│
│
├── 📁 src/                              ← SOURCE CODE
│   ├── __init__.py
│   │
│   ├── 📁 preprocessing/                ← Data preprocessing
│   │   ├── __init__.py
│   │   └── pipeline.py                  ← PreprocessingPipeline class
│   │       ├── StandardScaler for Time & Amount
│   │       ├── ColumnTransformer
│   │       └── save/load via joblib
│   │
│   ├── 📁 models/                       ← Model architectures
│   │   ├── __init__.py
│   │   └── autoencoders.py              ← Two autoencoder classes
│   │       ├── StandardAutoencoder.build()
│   │       │   ├── Input → Dense(64) → Dense(32) → Dense(16)
│   │       │   ├── Bottleneck(8)
│   │       │   └── Mirror decoder → Output
│   │       │
│   │       └── TransformerAutoencoder.build()
│   │           ├── Input → Embedding(32)
│   │           ├── MultiHeadAttention + FFN
│   │           ├── Bottleneck(8)
│   │           └── MultiHeadAttention + FFN → Output
│   │
│   └── 📁 inference/                    ← Inference & serving
│       ├── __init__.py
│       │
│       ├── detector.py                  ← AnomalyDetector class
│       │   ├── Load preprocessor + model
│       │   ├── predict_reconstruction_error()
│       │   ├── predict_anomalies()
│       │   ├── get_embeddings()
│       │   └── batch_predict()
│       │
│       └── api.py                       ← FastAPI REST service
│           ├── /health - Health check
│           ├── /predict - Single prediction
│           ├── /predict-batch - Batch predictions
│           └── /stats - Model statistics
│
│
├── 📁 saved_models/                     ← TRAINED MODELS (post-Colab)
│   ├── preprocessor.joblib              ← (add after Colab training)
│   ├── standard_autoencoder.keras       ← (add after Colab training)
│   └── transformer_autoencoder.keras    ← (add after Colab training)
│
│
├── 📁 tests/                            ← UNIT TESTS
│   └── test_models.py                   ← Test suite
│       ├── TestPreprocessingPipeline
│       │   ├── test_pipeline_build_and_transform()
│       │   └── test_pipeline_fit_transform()
│       │
│       ├── TestStandardAutoencoder
│       │   ├── test_model_build()
│       │   └── test_model_prediction()
│       │
│       └── TestTransformerAutoencoder
│           ├── test_model_build()
│           └── test_model_prediction()
│
│
└── .git/                                ← Git repository (after git init)

```

---

## 📋 File Type Legend

| Symbol | Meaning |
|--------|---------|
| 📄 | Documentation/Config file |
| 📁 | Directory/Folder |
| 🐧 | Linux/macOS script |
| 🪟 | Windows script |
| 🔐 | Hidden/System file |
| ⭐ | Important/Main file |
| 📓 | Jupyter Notebook |

---

## 🎯 Key Files Explained

### **Setup & Configuration**
| File | Purpose | Usage |
|------|---------|-------|
| `setup.ps1` | Automate Windows setup | `.\setup.ps1` |
| `setup.sh` | Automate Linux/macOS setup | `bash setup.sh` |
| `config.py` | Central configuration | `from config import *` |
| `requirements.txt` | Python packages | `pip install -r requirements.txt` |

### **Documentation**
| File | Purpose | When to Read |
|------|---------|-------------|
| `CHECKLIST.md` | Progress tracking | ⭐ Start here! |
| `PROJECT_SUMMARY.md` | Complete overview | Before starting |
| `README.md` | Project description | For context |
| `GETTING_STARTED.md` | Detailed guide | During setup |

### **Core Modules**
| Module | Classes | Purpose |
|--------|---------|---------|
| `preprocessing/pipeline.py` | `PreprocessingPipeline` | Normalize Time & Amount |
| `models/autoencoders.py` | `StandardAutoencoder`, `TransformerAutoencoder` | Define model architectures |
| `inference/detector.py` | `AnomalyDetector` | Run inference & detect anomalies |
| `inference/api.py` | FastAPI app | REST API service |

---

## 🔄 File Relationships

```
config.py
├── Loaded by: models/autoencoders.py
├── Used by: inference/api.py
└── Referenced by: test_models.py

preprocessing/pipeline.py
├── Created/used in: colab_training_pipeline.ipynb
├── Exported to: saved_models/preprocessor.joblib
├── Loaded by: inference/detector.py
└── Tested by: tests/test_models.py

models/autoencoders.py
├── Architectures used in: colab_training_pipeline.ipynb
├── Models saved to: saved_models/*.keras
├── Loaded by: inference/detector.py
└── Tested by: tests/test_models.py

inference/detector.py
├── Uses: saved_models/preprocessor.joblib
├── Uses: saved_models/*.keras models
├── Called by: inference/api.py
└── Tested by: CHECKLIST.md manual tests

inference/api.py
├── Uses: inference/detector.py
├── Depends on: saved_models/ files
└── Started with: uvicorn

colab_training_pipeline.ipynb
├── Produces: saved_models/ files
└── Produces: training_metadata.json
```

---

## 📊 Project Phases & Files

### Phase 1: Setup ✅
- ✓ Folder structure created
- ✓ All .py modules created
- ✓ Configuration files created
- ✓ Documentation written
- ✓ Setup scripts created

### Phase 2: Environment
- ⏳ Run setup script
- ⏳ Install dependencies
- ⏳ Verify installation

### Phase 3: Training
- ⏳ Use `colab_training_pipeline.ipynb`
- ⏳ Generate files in `saved_models/`

### Phase 4: Testing
- ⏳ Run `tests/test_models.py`
- ⏳ Verify predictions work

### Phase 5: Deployment (Optional)
- ⏳ Start `inference/api.py`
- ⏳ Make API requests

---

## 💾 Generated Files (After Colab)

After running the Colab notebook, these files will be created:

```
saved_models/
├── preprocessor.joblib           (size: ~2 KB)
├── standard_autoencoder.keras    (size: ~2.5 MB)
├── transformer_autoencoder.keras (size: ~2.3 MB)
└── training_metadata.json        (size: ~1 KB)
```

**These files are needed for:**
- Running `tests/test_models.py`
- Using `inference/detector.py`
- Starting `inference/api.py`

---

## 🔍 Quick Navigation

### Want to...
| Task | File to Check |
|------|--------------|
| Understand the project | `README.md` |
| Track your progress | `CHECKLIST.md` |
| See what's installed | `requirements.txt` |
| Configure settings | `config.py` |
| Train models | `notebooks/colab_training_pipeline.ipynb` |
| Test models locally | `tests/test_models.py` |
| Make predictions | `src/inference/detector.py` |
| Use REST API | `src/inference/api.py` |
| Change model architecture | `src/models/autoencoders.py` |
| Modify preprocessing | `src/preprocessing/pipeline.py` |

---

## 📈 File Sizes Reference

| File | Expected Size |
|------|---------------|
| `requirements.txt` | ~200 bytes |
| `config.py` | ~2 KB |
| `pipeline.py` | ~2 KB |
| `autoencoders.py` | ~4 KB |
| `detector.py` | ~3 KB |
| `api.py` | ~5 KB |
| `test_models.py` | ~3 KB |
| `colab_training_pipeline.ipynb` | ~30 KB |
| **After Colab training:** |
| `preprocessor.joblib` | ~2 KB |
| `standard_autoencoder.keras` | ~2.5 MB |
| `transformer_autoencoder.keras` | ~2.3 MB |

---

## ✨ Total Project Stats

- **Total Folders**: 8 (src + 3 subfolders, data + 2 subfolders, notebooks, saved_models, tests)
- **Total .py Files**: 10 (modules + tests + config + verify)
- **Total .md Files**: 5 (guides + checklists)
- **Total .ipynb Files**: 1 (Colab notebook)
- **Total Config Files**: 2 (requirements.txt, .gitignore)
- **Total Scripts**: 2 (setup.ps1, setup.sh)
- **Lines of Code**: ~2000+ across all modules

---

## 🎯 How to Use This Tree

1. **Reference for file locations**: Check the tree to find what you need
2. **Understanding relationships**: See how files depend on each other
3. **Progress tracking**: Mark sections as you complete them
4. **Module organization**: See the logical grouping of functionality

---

## 📌 Pro Tips

- Keep this file open while setting up for quick reference
- Use `Ctrl+F` to search for specific files or folders
- Notice the symbol legend to quickly identify file types
- File relationships show dependencies for debugging

---

**Print or bookmark this page for quick reference!**

