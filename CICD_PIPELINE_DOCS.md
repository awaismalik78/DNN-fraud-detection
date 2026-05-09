# 🔄 CI/CD PIPELINE DOCUMENTATION

**Complete guide to GitHub Actions CI/CD automation for your MLOps project**

---

## 📋 TABLE OF CONTENTS

1. [Pipeline Overview](#pipeline-overview)
2. [Workflow File Structure](#workflow-file-structure)
3. [How It Works](#how-it-works)
4. [Monitoring & Results](#monitoring--results)
5. [Customization](#customization)
6. [Best Practices](#best-practices)

---

## 🏗️ PIPELINE OVERVIEW

### What is CI/CD?

**CI/CD** = Continuous Integration / Continuous Deployment

- **Continuous Integration**: Automatically test code whenever you push
- **Continuous Deployment**: Automatically deploy when tests pass

### Your Pipeline

```
Developer pushes code to GitHub
        ↓
GitHub Actions triggered
        ↓
3 parallel quality gates:
  1. Code Quality (flake8)
  2. Unit Tests (pytest)
  3. Integration Tests
        ↓
If all pass → API Validation
        ↓
✓ DEPLOYMENT READY
```

---

## 📂 WORKFLOW FILE STRUCTURE

### File Location
```
.github/
└── workflows/
    └── mlops.yml          ← Your CI/CD configuration
```

### What's Inside

```yaml
name: MLOps CI/CD Pipeline

on:
  push:
    branches: [main]       # Trigger on push to main
  pull_request:
    branches: [main]       # Trigger on PRs to main

jobs:
  quality-checks:          # Job 1: Linting
    runs-on: ubuntu-latest
    steps: [...]

  tests:                    # Job 2: Testing
    runs-on: ubuntu-latest
    needs: quality-checks   # Run after quality-checks
    steps: [...]

  api-validation:           # Job 3: API validation
    runs-on: ubuntu-latest
    needs: tests            # Run after tests
    steps: [...]

  summary:                  # Job 4: Summary
    runs-on: ubuntu-latest
    needs: [quality-checks, tests, api-validation]
    steps: [...]
```

---

## ⚙️ HOW IT WORKS

### Job 1: Code Quality Checks

**Purpose**: Verify code meets quality standards

**What it does:**
1. Checks out your code
2. Sets up Python 3.11
3. Installs dependencies
4. Runs flake8 linter
5. Reports any issues

**Checks**:
```python
# Syntax errors (always fail)
E9, F63, F7, F82

# Style issues (warnings)
PEP 8 compliance
Line length (max 127)
Complexity (max 10)
```

**Example Output**:
```
src/preprocessing/pipeline.py:45:1: W292 no newline at end of file
src/inference/app.py:120:80: E501 line too long (131 > 127 characters)
Total: 2 warnings (non-blocking)
```

### Job 2: Unit & Integration Tests

**Purpose**: Ensure all code works correctly

**What it runs:**
1. `pytest tests/` - All unit tests
2. `test_complete_pipeline.py` - Integration tests
3. `test_transformer_api.py` - API endpoint tests

**Expected Output**:
```
test_preprocessing.py::test_pipeline_load PASSED
test_preprocessing.py::test_transform_features PASSED
test_inference.py::test_model_loaded PASSED
test_inference.py::test_prediction_shape PASSED

tests: 4 passed in 2.34s
```

### Job 3: API Validation

**Purpose**: Verify /predict endpoint works correctly

**What it validates:**
1. JSON response structure
2. Field types and names
3. Mock transaction handling
4. Fraud/legitimate detection

**Example Validation**:
```python
# Tests this schema
{
  "fraud_detected": False,        # bool
  "anomaly_score": 0.45,          # float
  "threshold": 0.80,              # float
  "confidence": 0.4375            # float
}

# For both cases:
# ✓ Legitimate transaction
# ✓ Fraudulent transaction
```

### Job 4: Summary

**Purpose**: Final status report

**Output**:
```
=========================================
CI/CD Pipeline Execution Summary
=========================================
✓ Code Quality Checks: Completed
✓ Unit & Integration Tests: Completed
✓ API Validation: Completed
=========================================
Pipeline Status: All checks passed!
Ready for deployment
=========================================
```

---

## 📊 MONITORING & RESULTS

### Check Workflow Status

**On GitHub:**
1. Go to your repository
2. Click "Actions" tab
3. See list of workflow runs

### Workflow Status Indicators

| Icon | Status | Meaning |
|------|--------|---------|
| ✅ | Success | All tests passed, ready to deploy |
| ❌ | Failed | Tests failed, check logs |
| ⏳ | In Progress | Running now |
| ⊘ | Cancelled | Manually stopped |
| ⊗ | Skipped | Conditional not met |

### View Detailed Logs

```
1. Click on workflow run
2. Click on job (e.g., "Code Quality Checks")
3. Click on step to expand
4. See full logs and output
```

### Example Log Output

```log
Run flake8 linting
src/preprocessing/pipeline.py: 45 lines, 0 errors
src/inference/app.py: 450 lines, 2 warnings
...
Total: 25 files scanned, 2 warnings (non-blocking)
```

---

## 🔧 CUSTOMIZATION

### Change Trigger Events

**Edit `.github/workflows/mlops.yml`:**

```yaml
# Current (push and PRs)
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Add schedule (runs daily at 2 AM UTC)
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'

# Add manual trigger
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      reason:
        description: 'Reason for manual run'
```

### Change Python Version

```yaml
- name: Set up Python 3.11
  uses: actions/setup-python@v4
  with:
    python-version: '3.12'  # Change to 3.12
```

### Add More Tests

```yaml
- name: Run API stress test
  run: |
    python tests/stress_test.py

- name: Run performance benchmarks
  run: |
    python tests/benchmark.py
```

### Add Code Coverage

```yaml
- name: Generate coverage report
  run: |
    pytest --cov=src tests/

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

### Notify on Failure

```yaml
- name: Notify Slack on failure
  if: failure()
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -d '{"text":"CI/CD pipeline failed"}'
```

---

## 🎯 BEST PRACTICES

### 1. Keep Tests Fast

- Minimize external calls
- Use mock data
- Target <5 minutes for full suite

### 2. Fail Fast

- Run quick checks first (linting)
- Run unit tests before integration tests
- Skip slow tests on every commit (use tags)

### 3. Clear Commit Messages

```
Good:
git commit -m "Fix preprocessing DataFrame issue

- Convert dict to DataFrame before transform
- Fixes ColumnTransformer string column error
- Resolves API 400 error"

Bad:
git commit -m "fix"
git commit -m "update"
```

### 4. Use Branches for Features

```powershell
# Create feature branch
git checkout -b feature/batch-processing

# Make changes
# Test locally
# Push branch
git push origin feature/batch-processing

# Create Pull Request on GitHub
# PR will trigger CI/CD
# Merge only after tests pass
```

### 5. Monitor Pipeline

- Check Actions tab regularly
- Fix failures immediately
- Review logs for warnings
- Keep dependencies updated

### 6. Update Dependencies Regularly

```powershell
# Check for updates
pip list --outdated

# Update all
pip install --upgrade -r requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## 📈 PERFORMANCE TARGETS

| Stage | Target Time | Actual |
|-------|-------------|--------|
| Checkout | 5s | 3-5s |
| Setup Python | 10s | 5-15s |
| Install deps | 30s | 20-40s |
| Code Quality | 30s | 20-30s |
| Unit Tests | 60s | 30-60s |
| Integration Tests | 60s | 40-90s |
| API Validation | 30s | 20-30s |
| **Total** | **<5 min** | **5-8 min** |

---

## 🔐 SECURITY BEST PRACTICES

### Never Commit Secrets

```gitignore
# .gitignore - add sensitive files
.env
.env.local
secrets/
*.key
*.pem
credentials.json
```

### Use GitHub Secrets for Sensitive Data

1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add: `DATABASE_URL`, `API_KEYS`, etc.
4. Use in workflow: `${{ secrets.DATABASE_URL }}`

### Example with Secrets

```yaml
- name: Deploy to production
  env:
    API_KEY: ${{ secrets.PROD_API_KEY }}
    DB_URL: ${{ secrets.PROD_DB_URL }}
  run: |
    python deploy.py
```

---

## 🚀 WORKFLOW EXECUTION TIMELINE

### First Push
```
09:00 - Developer: git push origin main
09:00 - GitHub: Workflow triggered
09:01 - Job 1: Code Quality (1-2 min)
09:03 - Job 2: Tests (3-5 min)
09:08 - Job 3: API Validation (1 min)
09:09 - Job 4: Summary (5s)
09:09 - ✓ All passed!
```

### Multiple Jobs

Jobs run in order based on `needs`:
```
quality-checks (starts immediately)
        ↓ (after complete)
tests (starts)
        ↓ (after complete)
api-validation (starts)
        ↓ (after complete)
summary (starts)
```

---

## 🐛 TROUBLESHOOTING

### Workflow Not Running

**Check 1**: Is `.github/workflows/mlops.yml` committed?
```powershell
git add .github/workflows/mlops.yml
git commit -m "Add CI/CD workflow"
git push
```

**Check 2**: Is it on the main branch?
```powershell
git branch
# Should show: * main
```

**Check 3**: Go to Actions tab → Check for errors

### Tests Fail Locally But Pass in CI/CD

**Possible causes:**
- Different Python version
- Missing dependencies
- File path issues
- Environment variables

**Solution:**
```powershell
# Replicate CI/CD environment locally
python -m venv test_env
test_env\Scripts\Activate.ps1
pip install -r requirements.txt
pytest tests/
```

### Flake8 Complains About Line Length

**Solution 1**: Shorten line
```python
# Before (131 chars)
result = self.model.predict(preprocessed, verbose=0) + some_other_processing_function()

# After (120 chars)
result = self.model.predict(preprocessed, verbose=0)
result = result + some_other_processing_function()
```

**Solution 2**: Ignore specific errors
```yaml
- name: Run flake8 linting
  run: |
    flake8 src/ --ignore=E501 --max-line-length=127
```

### Tests Timeout in CI/CD

**Solution**: Increase timeout or skip slow tests
```yaml
- name: Run tests with timeout
  run: |
    timeout 600 pytest tests/ -v -x
    # 600 seconds = 10 minutes
```

---

## 📚 USEFUL GITHUB ACTIONS

### Status Badge

Add to your `README.md`:
```markdown
![CI/CD Pipeline](https://github.com/YOUR_USERNAME/DNN-fraud-detection/workflows/MLOps%20CI%2FCD%20Pipeline/badge.svg)
```

### Workflow Status

See in Actions tab:
- Number of runs
- Success/failure rate
- Execution time
- Commit messages

### Notifications

- GitHub notifications (default)
- Email notifications
- Slack integration (custom)
- Discord webhook (custom)

---

## ✅ VERIFICATION CHECKLIST

- [ ] `.github/workflows/mlops.yml` exists in repository
- [ ] Workflow file is properly formatted (YAML)
- [ ] Repository is on GitHub
- [ ] Tests run successfully locally
- [ ] CI/CD pipeline shows on Actions tab
- [ ] All tests pass on first push
- [ ] Code quality checks pass
- [ ] API validation passes
- [ ] Workflow completes in <10 minutes

---

## 🎉 YOU'RE DONE!

Your project now has:
✅ Automated code quality checks  
✅ Automated testing on every push  
✅ Automated API validation  
✅ Production-ready CI/CD pipeline  

Every push will automatically:
1. Check code quality
2. Run all tests
3. Validate API endpoints
4. Report results on GitHub

**You have a professional software engineering setup!** 🚀

---

## 📞 QUICK REFERENCE

```powershell
# View workflow status
# Go to: GitHub Actions tab

# Manually trigger workflow
# Go to: Actions → MLOps CI/CD Pipeline → Run workflow

# View workflow file
# File: .github/workflows/mlops.yml

# Edit workflow
# Edit .github/workflows/mlops.yml and push

# Check test results
# GitHub Actions → Click workflow run → View logs
```

