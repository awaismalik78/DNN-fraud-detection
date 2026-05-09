# 🚀 TWO-PART SYSTEM - QUICK START GUIDE

## Your Credit Card Fraud Detection MLOps Platform

**Status**: ✅ **READY TO RUN**

This guide walks you through running both the backend API server and the frontend Streamlit dashboard.

---

## 🎯 THE TWO-PART SYSTEM

```
┌──────────────────────────────────────────────────────────────┐
│               CREDIT CARD FRAUD DETECTION SYSTEM              │
├─────────────────────────────────────┬──────────────────────────┤
│   BACKEND (FastAPI)                 │  FRONTEND (Streamlit)    │
│   • Transformer Model               │  • Interactive Dashboard │
│   • Preprocessing Pipeline          │  • Real-time Alerts      │
│   • Fraud Detection Scoring         │  • Visualization         │
│   • REST API (Port 8000)            │  • Feature Analysis      │
│   • Swagger Documentation          │  • User Interface        │
│                                     │    (Port 8501)           │
└─────────────────────────────────────┴──────────────────────────┘
```

---

## 📋 PREREQUISITES

Before you start, make sure you have:

```
✅ Python 3.11 virtual environment activated
✅ All packages installed (pip install -r requirements.txt)
✅ Model files in saved_models/:
   • transformer_autoencoder.keras
   • preprocessor.joblib
✅ Two terminal windows (for both services)
```

### Check Your Setup
```powershell
# Terminal - Verify Python version
python --version
# Output: Python 3.11.x

# Terminal - Verify virtual environment
Get-Command python
# Should show: c:\Users\awais\Desktop\DNN project\venv\Scripts\python.exe

# Terminal - Verify package installation
pip list | findstr streamlit
# Should show: streamlit (version)
```

---

## 🚀 STEP-BY-STEP STARTUP (5 MINUTES)

### Step 0: Activate Virtual Environment (If Not Already Done)

**PowerShell**:
```powershell
.\venv\Scripts\Activate.ps1
```

**CMD**:
```cmd
.\venv\Scripts\activate.bat
```

**Expected Output**:
```
(venv) C:\Users\awais\Desktop\DNN project>
```

---

### Step 1: Start Backend API (Terminal 1)

**Command**:
```powershell
uvicorn src.inference.app:app --reload
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 [Ctrl+C to quit]
INFO:     Started server process [12345]
INFO:     Application startup complete
```

**What this means**:
- ✅ FastAPI server started
- ✅ Transformer model loaded
- ✅ Preprocessor pipeline loaded
- ✅ Ready to accept predictions on port 8000

**Access API documentation**:
- Browser: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

**Keep this terminal running!** Leave it open while using the dashboard.

---

### Step 2: Start Frontend Dashboard (Terminal 2)

**Open a new terminal window** and ensure venv is activated:

```powershell
.\venv\Scripts\Activate.ps1
```

**Command**:
```powershell
streamlit run src/frontend/dashboard.py
```

**Expected Output**:
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  For better performance, install Pyarrow: pip install pyarrow
```

**What this means**:
- ✅ Streamlit server started
- ✅ Dashboard loaded on port 8501
- ✅ Browser should open automatically
- ⚠️ Ignore pyarrow warning (optional dependency)

**If browser doesn't open**:
```
Open manually: http://localhost:8501
```

---

### Step 3: Verify Both Are Running

| Component | Port | Check URL |
|-----------|------|-----------|
| Backend API | 8000 | http://localhost:8000/health |
| Frontend Dashboard | 8501 | http://localhost:8501 |

**Terminal 1 (Backend)**: Shows Uvicorn running  
**Terminal 2 (Frontend)**: Shows Streamlit running  
**Browser**: Shows dashboard with "✅ Backend Connected"

---

## 🎮 USING THE DASHBOARD

### Dashboard Layout

```
┌────────────────────────────────────────────────────────┐
│  FRAUD DETECTION ANALYZER                              │
│  Status: ✅ Backend Connected                          │
├─────────────────┬──────────────────────────────────────┤
│  SIDEBAR        │  MAIN AREA                           │
│  ┌────────────┐ │  ┌──────────────────────────────────┐│
│  │ Generate   │ │  │  🚀 Analyze Transaction Button   ││
│  │ Transaction│ │  │                                  ││
│  ├────────────┤ │  │  Results Display                 ││
│  │ Amount: $  │ │  │  🚨 FRAUD DETECTED              ││
│  │ [slider]   │ │  │                                  ││
│  ├────────────┤ │  │  Metrics:                        ││
│  │ Time: HH:MM│ │  │  • Anomaly Score: 1.2345        ││
│  │ [slider]   │ │  │  • Threshold: 0.80              ││
│  ├────────────┤ │  │  • Confidence: 85%              ││
│  │ Settings   │ │  │                                  ││
│  │ Display    │ │  │  [Gauge Chart]                  ││
│  └────────────┘ │  │                                  ││
│                 │  │  [Feature Distribution]          ││
│                 │  │                                  ││
│                 │  │  📋 Tab: Details | Info          ││
│                 │  └──────────────────────────────────┘│
└─────────────────┴──────────────────────────────────────┘
```

---

### Workflow: Analyzing a Transaction

#### 1️⃣ Generate Random Transaction
```
Click: "🎲 Generate Random Transaction"
Result: Creates realistic 30-feature transaction data
        • Time: 0-86,400 seconds (24 hours)
        • Amount: $0.99-$1,000.00
        • V1-V28: Normal distribution features
Updates in Sidebar: Shows current Amount and Time
```

#### 2️⃣ Adjust Sliders (Optional)
```
Slider 1: "Transaction Amount"
          Range: $0 to $10,000
          Step: $10
          Effect: Overrides generated amount

Slider 2: "Time of Day"
          Range: 0 to 86,400 seconds
          Step: 3,600 (1 hour)
          Display: HH:MM format
          Effect: Overrides generated time
```

#### 3️⃣ Click "Analyze Transaction"
```
Button: "🚀 Analyze Transaction" (large, prominent)
Action: Sends 30 features to backend API
Result: Loading spinner appears...
```

#### 4️⃣ View Results
```
🔴 FRAUD DETECTED
━━━━━━━━━━━━━━━━━
High Risk Transaction Identified

Metrics:
• Anomaly Score: 1.2345 (vs 0.80 threshold)
• Confidence: 85%
• Status: 🔴 FRAUD

Visualizations:
• Gauge Chart: Shows score vs threshold
• Red threshold line at 0.80
• Needle position indicates anomaly score
```

#### 5️⃣ Explore Details Tab
```
Tab: "Details"
View:
• Complete transaction data (JSON)
• Feature values (all 30 features)
• Feature distribution bar chart
• Color-coded feature importance
```

---

## 📊 UNDERSTANDING THE RESULTS

### What the Dashboard Shows

#### Alert Boxes
```
🟢 LEGITIMATE TRANSACTION        🔴 FRAUD DETECTED
✅ Low Risk                       🚨 High Risk
Transaction Approved             Alert! Suspicious Activity
Color: Green gradient             Color: Red gradient
```

#### Gauge Chart
```
Displays: Anomaly Score (MSE reconstruction error)
Range: 0 to 2.0
Threshold: Red line at 0.80
Colors:
  • Green zone: 0 to 0.80 (Safe)
  • Red zone: 0.80 to 2.0 (Fraud)
Needle: Points to actual score
Delta: Shows distance from threshold
```

#### Metrics Cards
```
┌─────────────────┐  ┌──────────────┐  ┌────────────┐  ┌───────┐
│ Anomaly Score   │  │ Threshold    │  │ Confidence │  │Status │
│ 1.2345          │  │ 0.80         │  │ 85%        │  │ 🔴    │
│ vs 0.80 ▲       │  │ (MSE limit)  │  │ (accuracy) │  │FRAUD  │
└─────────────────┘  └──────────────┘  └────────────┘  └───────┘
```

#### Feature Distribution
```
Bar Chart: 15 selected features (V1, V3, V5, ... V28)
Colors: RdYlGn_r (Red-Yellow-Green reversed)
        • Red: Extreme/unusual values
        • Yellow: Moderate values
        • Green: Normal/expected values
Interactivity: Hover for exact values
```

---

## 🔄 EXAMPLE SCENARIOS

### Scenario 1: Legitimate Transaction
```
Input:
  • Amount: $49.99
  • Time: 14:30 (afternoon)
  • Features: Normal distribution

Output:
  • Anomaly Score: 0.35
  • Status: ✅ LEGITIMATE
  • Confidence: 92%
  • Gauge: Green, needle low
```

### Scenario 2: Suspicious Transaction
```
Input:
  • Amount: $5,000
  • Time: 03:00 (night)
  • Features: Extreme values

Output:
  • Anomaly Score: 1.45
  • Status: 🚨 FRAUD DETECTED
  • Confidence: 88%
  • Gauge: Red zone, needle high
```

### Scenario 3: Edge Case
```
Input:
  • Amount: $999.99
  • Time: 12:00 (noon)
  • Features: Unusual but plausible

Output:
  • Anomaly Score: 0.78
  • Status: ⚠️ BORDERLINE
  • Confidence: 3%
  • Gauge: Needle near red line
```

---

## 🛠️ TROUBLESHOOTING

### Problem 1: Backend Won't Start
```
Error: "Address already in use"

Solutions:
  Option A: Kill existing process
    netstat -ano | findstr :8000
    taskkill /PID <PID> /F
    
  Option B: Use different port
    uvicorn src.inference.app:app --port 9000 --reload
    (Update dashboard config to use 9000)

  Option C: Wait 30 seconds and retry
    ports sometimes need time to release
```

### Problem 2: Dashboard Won't Load
```
Error: "Cannot connect to API"

Solutions:
  1. Verify backend is running (Terminal 1)
  2. Check port 8000: http://localhost:8000/health
  3. Restart frontend: Ctrl+C then re-run
  4. Check firewall: Allow localhost:8000

Expected: {"status":"healthy","threshold":0.8}
```

### Problem 3: API Returns Error
```
Error: "Internal Server Error"

Check backend terminal for:
  • Model loading errors
  • Preprocessor loading errors
  • Feature dimension mismatches
  
Verify in saved_models/:
  • transformer_autoencoder.keras exists
  • preprocessor.joblib exists
```

### Problem 4: Dashboard Port Already Used
```
Error: "Port 8501 already in use"

Solution:
  streamlit run src/frontend/dashboard.py --server.port 8502
  Then open: http://localhost:8502
```

### Problem 5: "Module not found" errors
```
Error: "No module named 'streamlit'"

Solution:
  pip install -r requirements.txt
  (or) pip install streamlit requests plotly
```

---

## 🔌 API HEALTH CHECKS

### Check Backend Status
```powershell
# Terminal - Check if backend is responding
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "preprocessor_loaded": true,
  "threshold": 0.8
}
```

### Check API Documentation
```
Browser: http://localhost:8000/docs
         Shows interactive Swagger UI with all endpoints
```

### Test API Manually
```powershell
# Terminal - Send test request
$body = @{
  Time = 30000
  Amount = 100.50
  V1 = -1.35
  V2 = -0.73
  # ... (V3 through V28)
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/predict" `
  -Method POST -Body $body `
  -ContentType "application/json"

$response.Content | ConvertFrom-Json
```

---

## 📈 PERFORMANCE METRICS

| Metric | Expected Time |
|--------|---------------|
| Backend startup | 3-5 seconds |
| Dashboard startup | 2-3 seconds |
| API response time | 50-150 ms |
| Prediction latency | 100-200 ms |
| Gauge chart render | <100 ms |
| Dashboard interaction | <500 ms |

---

## 🎯 WORKFLOW CHECKLIST

### Startup (First Time)
- [ ] Terminal 1: Activate venv
- [ ] Terminal 1: Start backend API
- [ ] Verify: Backend running on :8000
- [ ] Terminal 2: Activate venv
- [ ] Terminal 2: Start dashboard
- [ ] Verify: Dashboard at http://localhost:8501
- [ ] Browser: See "✅ Backend Connected"

### Daily Use
- [ ] Open Terminal 1: Start backend
- [ ] Wait for: "Application startup complete"
- [ ] Open Terminal 2: Start dashboard
- [ ] Wait for: Browser to open
- [ ] Use: Generate → Adjust → Analyze
- [ ] Review: Results and metrics

### Shutdown
- [ ] Dashboard: Refresh clears state
- [ ] Backend: Ctrl+C to stop
- [ ] Dashboard: Ctrl+C to stop
- [ ] Terminals: Close windows

---

## 💻 COMMAND REFERENCE

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start backend API
uvicorn src.inference.app:app --reload

# Start frontend dashboard
streamlit run src/frontend/dashboard.py

# Check backend health
curl http://localhost:8000/health

# View API documentation
# Open: http://localhost:8000/docs

# Kill process on port (if stuck)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Run tests
python test_transformer_api.py
```

---

## 📚 DOCUMENTATION REFERENCES

For more information, see:

| Document | Purpose |
|----------|---------|
| STREAMLIT_DASHBOARD_GUIDE.md | Dashboard features and design |
| INFERENCE_API_GUIDE.md | API endpoints and usage |
| API_COMPARISON.md | Comparing two API implementations |
| TRANSFORMER_API_IMPLEMENTATION.md | Technical details |
| README.md | Project overview |

---

## 🎉 YOU'RE READY!

Your fraud detection system is complete and production-ready:

### What You Have
```
✅ Transformer Autoencoder Model (45K parameters)
✅ Scikit-learn Preprocessing Pipeline
✅ FastAPI REST Backend with Swagger docs
✅ Streamlit Interactive Dashboard
✅ Real-time Fraud Detection
✅ Modern UI with Visualizations
✅ Complete Documentation
```

### What You Can Do
```
✅ Analyze single transactions
✅ Get fraud/legitimate predictions
✅ View anomaly scores and confidence
✅ See interactive gauge charts
✅ Explore feature distributions
✅ Monitor API health
✅ Scale to batch processing
```

---

## 🚀 LET'S GO!

**Terminal 1**:
```powershell
.\venv\Scripts\Activate.ps1
uvicorn src.inference.app:app --reload
```

**Terminal 2**:
```powershell
.\venv\Scripts\Activate.ps1
streamlit run src/frontend/dashboard.py
```

**Browser**:
```
http://localhost:8501
```

---

## 📞 NEED HELP?

If something goes wrong:

1. **Check backend terminal** for error messages
2. **Check browser console** (F12) for frontend errors
3. **Verify API health**: http://localhost:8000/health
4. **Review logs** in both terminals
5. **See troubleshooting section** above
6. **Restart both services** (stop and re-run)

---

**Status**: ✅ **Ready to Launch!**

**Next Step**: Start both services and open the dashboard!

Enjoy your fraud detection system! 🎊

