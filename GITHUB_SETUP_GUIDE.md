# 🚀 GITHUB SETUP & CI/CD DEPLOYMENT GUIDE

**Complete instructions for setting up your GitHub repository and enabling CI/CD automation**

---

## 📋 TABLE OF CONTENTS

1. [GitHub Repository Setup](#github-repository-setup)
2. [Local Git Configuration](#local-git-configuration)
3. [Pushing Your Project](#pushing-your-project)
4. [CI/CD Pipeline Overview](#cicd-pipeline-overview)
5. [Monitoring Workflows](#monitoring-workflows)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 GITHUB REPOSITORY SETUP

### Step 1: Create GitHub Account (If You Don't Have One)
1. Go to https://github.com/signup
2. Sign up with your email
3. Verify your email address
4. Complete profile setup

### Step 2: Create a New Repository on GitHub

**Method A: Via GitHub Website (Recommended)**

1. Go to https://github.com/new
2. Fill in the repository details:
   ```
   Repository name: DNN-fraud-detection
   (or any name you prefer)
   
   Description: Credit Card Fraud Detection MLOps System with 
                Transformer Autoencoder and FastAPI Backend
   
   Visibility: Public (or Private if you prefer)
   
   Initialize repository: Choose "Add a README" (optional)
   
   .gitignore: Select "Python"
   
   License: MIT (optional but recommended)
   ```
3. Click "Create repository"
4. Copy the repository URL (e.g., `https://github.com/YOUR_USERNAME/DNN-fraud-detection.git`)

---

## 🖥️ LOCAL GIT CONFIGURATION

### Step 1: Install Git (If Not Already Installed)

**Windows:**
```powershell
# Check if git is installed
git --version

# If not installed, download from:
# https://git-scm.com/download/win
```

**Verify Installation:**
```powershell
git --version
# Output: git version 2.x.x
```

### Step 2: Configure Git Globally

```powershell
# Set your name (use your GitHub username)
git config --global user.name "Your Name"

# Set your email (use your GitHub account email)
git config --global user.email "your.email@example.com"

# Verify configuration
git config --global user.name
git config --global user.email
```

**Example:**
```powershell
git config --global user.name "awais"
git config --global user.email "awais@example.com"
```

### Step 3: Set Up SSH or HTTPS Authentication

**Option A: HTTPS (Simpler, Recommended for Beginners)**

```powershell
# Nothing extra needed - GitHub will prompt for token
# when you first push
```

**Option B: SSH (More Secure, Recommended for Production)**

1. Generate SSH key:
```powershell
ssh-keygen -t ed25519 -C "your.email@example.com"
```

2. Press Enter for all prompts (accept defaults)

3. Start SSH agent:
```powershell
# For PowerShell
Start-Service ssh-agent

# For CMD
net start ssh-agent
```

4. Add SSH key to agent:
```powershell
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

5. Add public key to GitHub:
   - Copy your public key: `cat $env:USERPROFILE\.ssh\id_ed25519.pub`
   - Go to https://github.com/settings/keys
   - Click "New SSH key"
   - Paste your key and save

---

## 📤 PUSHING YOUR PROJECT

### Step 1: Initialize Local Repository

Navigate to your project directory:

```powershell
cd "c:\Users\awais\Desktop\DNN project"
```

Check if git is already initialized:
```powershell
ls -la
# If you see .git folder, skip to Step 2
```

If no `.git` folder exists, initialize it:
```powershell
git init
```

### Step 2: Create .gitignore File

**If you created the repo on GitHub with Python .gitignore:** Skip this step.

**If you didn't:**
```powershell
# PowerShell - Create .gitignore
@'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/
*.egg-info/
dist/
build/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# IDE
.vscode/
.idea/
*.swp
*.swo

# Machine Learning
*.h5
*.keras
*.joblib
saved_models/
data/raw/

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Logs
*.log
'@ | Set-Content .gitignore
```

### Step 3: Add Remote Repository

Get your repository URL from GitHub (HTTPS or SSH):

```powershell
# Using HTTPS (GitHub will ask for credentials on first push)
git remote add origin https://github.com/YOUR_USERNAME/DNN-fraud-detection.git

# OR using SSH (if you set up SSH keys)
git remote add origin git@github.com:YOUR_USERNAME/DNN-fraud-detection.git
```

**Verify remote was added:**
```powershell
git remote -v
# Should show fetch and push URLs
```

### Step 4: Add Files to Staging Area

```powershell
# Add all files (respects .gitignore)
git add .

# Verify files to be committed
git status
```

**Expected output:**
```
On branch main

Initial commit

Changes to be committed:
  (use "rm --cached <file>..." to unstage)
        new file:   .github/workflows/mlops.yml
        new file:   README.md
        new file:   requirements.txt
        ... (40+ files)
```

### Step 5: Create Initial Commit

```powershell
git commit -m "Initial commit: Credit Card Fraud Detection MLOps System

- Transformer Autoencoder model (45K parameters)
- FastAPI backend with /predict endpoint
- Streamlit interactive dashboard
- Complete preprocessing pipeline
- GitHub Actions CI/CD workflow"
```

### Step 6: Rename Branch to 'main' (If Needed)

```powershell
# Check current branch
git branch

# If on 'master', rename to 'main'
git branch -M main

# Verify
git branch
# Should show: * main
```

### Step 7: Push to GitHub

**First Time Push (Set Upstream):**
```powershell
git push -u origin main
```

**Subsequent Pushes:**
```powershell
git push
```

**Authentication:**
- **HTTPS**: GitHub will open browser for authentication (GitHub.com login)
- **SSH**: Should work automatically if SSH keys are configured

---

## 🔄 CI/CD PIPELINE OVERVIEW

### What Happens When You Push

Your GitHub Actions workflow (`.github/workflows/mlops.yml`) automatically:

```
Push to main branch
        ↓
GitHub Actions Triggered
        ↓
┌─────────────────────────────────────────┐
│  Job 1: Code Quality Checks             │
│  • Install Python 3.11                  │
│  • Install dependencies                 │
│  • Run flake8 linting                   │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│  Job 2: Unit & Integration Tests        │
│  • Run pytest                           │
│  • Run integration tests                │
│  • Run API endpoint tests               │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│  Job 3: API Validation                  │
│  • Validate /predict endpoint           │
│  • Test JSON response structure         │
│  • Verify mock transaction handling     │
└─────────────────────────────────────────┘
        ↓
✓ All Tests Pass
        ↓
Ready for Deployment!
```

### Pipeline Components

**1. Code Quality Checks (flake8)**
- Syntax error detection
- Code style enforcement
- Max complexity checking
- Report generation

**2. Unit Tests (pytest)**
- Test files in `tests/` directory
- Coverage reporting
- Failure highlighting

**3. Integration Tests**
- `test_complete_pipeline.py` execution
- End-to-end workflow validation
- Model loading verification

**4. API Endpoint Tests**
- `test_transformer_api.py` execution
- Mock transaction handling
- Response schema validation

**5. API Structure Validation**
- Pydantic model validation
- JSON response format checking
- Fraud/legitimate response testing

---

## 📊 MONITORING WORKFLOWS

### View Workflow Runs

1. Go to your GitHub repository
2. Click "Actions" tab
3. See list of workflow runs with status:
   - ✅ **Success** (All tests passed)
   - ❌ **Failed** (Check logs)
   - ⏳ **In Progress** (Running now)

### Check Detailed Logs

1. Click on a workflow run
2. Click on a job (e.g., "Code Quality Checks")
3. See detailed output and any errors
4. Scroll through logs to find issues

### Example Successful Run

```
✓ Checkout code
✓ Set up Python 3.11
✓ Install dependencies
✓ Run flake8 linting
  - src/preprocessing/pipeline.py: OK
  - src/inference/app.py: OK
✓ Run unit tests
  - test_preprocessing.py: PASSED
  - test_inference.py: PASSED
✓ API validation
  - Response structure: Valid
  - Mock transactions: OK

Pipeline Status: All checks passed! ✓
```

---

## 🔐 AUTHENTICATION SETUP

### GitHub Personal Access Token (PAT)

If HTTPS push fails, use a Personal Access Token:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: "MLOps Project Token"
4. Select scopes: `repo` (full control)
5. Click "Generate token"
6. **Copy the token immediately** (won't show again)

**Use token when Git prompts for password:**
```
Username: your-github-username
Password: <paste-your-token-here>
```

---

## 📝 MAKING CHANGES AFTER INITIAL PUSH

### Simple Git Workflow

```powershell
# 1. Make changes to files
# (edit Python files, etc.)

# 2. Stage changes
git add .

# 3. Commit changes
git commit -m "Fix API preprocessing issue

- Convert dict to DataFrame before preprocessing
- Fixes ColumnTransformer string column error"

# 4. Push to GitHub
git push

# CI/CD pipeline automatically runs!
```

### Creating a Branch for Features

```powershell
# Create new branch
git checkout -b feature/add-batch-processing

# Make your changes
# ... edit files ...

# Stage and commit
git add .
git commit -m "Add batch processing endpoint"

# Push branch to GitHub
git push -u origin feature/add-batch-processing

# Create Pull Request on GitHub website
```

---

## 🐛 TROUBLESHOOTING

### Problem: "fatal: not a git repository"

**Solution:**
```powershell
# Navigate to project root
cd "c:\Users\awais\Desktop\DNN project"

# Initialize git
git init
```

### Problem: "fatal: remote origin already exists"

**Solution:**
```powershell
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/YOUR_USERNAME/repo-name.git
```

### Problem: "rejected push because the remote contains work"

**Solution:**
```powershell
# Pull latest changes
git pull origin main

# Resolve conflicts if any, then push again
git push origin main
```

### Problem: GitHub Actions workflow not running

**Solutions:**
1. Check `.github/workflows/mlops.yml` file exists
2. Verify file is in correct directory structure
3. Commit and push the workflow file:
   ```powershell
   git add .github/workflows/mlops.yml
   git commit -m "Add GitHub Actions CI/CD workflow"
   git push
   ```
4. Go to GitHub > Actions tab to verify

### Problem: Authentication fails on push

**Solution - Use Personal Access Token:**
```powershell
# When Git prompts for password, paste your PAT token
# (Generate at https://github.com/settings/tokens)
```

---

## ✅ QUICK START CHECKLIST

- [ ] Create GitHub account
- [ ] Create new repository on GitHub
- [ ] Copy repository URL
- [ ] Configure local git (`git config --global user.name ...`)
- [ ] Navigate to project directory
- [ ] Run `git init` (if needed)
- [ ] Create `.gitignore` file
- [ ] Run `git remote add origin <your-repo-url>`
- [ ] Run `git add .`
- [ ] Run `git commit -m "Initial commit..."`
- [ ] Run `git branch -M main`
- [ ] Run `git push -u origin main`
- [ ] Go to GitHub Actions tab to see workflow run
- [ ] Verify all tests pass ✓

---

## 🚀 FIRST PUSH - STEP BY STEP

Here's the exact sequence of commands:

```powershell
# 1. Navigate to project
cd "c:\Users\awais\Desktop\DNN project"

# 2. Initialize git (if not already done)
git init

# 3. Configure git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 4. Add remote
git remote add origin https://github.com/YOUR_USERNAME/DNN-fraud-detection.git

# 5. Add all files
git add .

# 6. Create commit
git commit -m "Initial commit: MLOps fraud detection system

- Transformer Autoencoder model
- FastAPI backend with CI/CD
- Streamlit dashboard
- Complete test suite
- GitHub Actions workflow"

# 7. Rename to main (if needed)
git branch -M main

# 8. Push to GitHub
git push -u origin main

# 9. GitHub will ask for authentication
# HTTPS: Paste Personal Access Token when prompted
# SSH: Should work automatically
```

---

## 📊 CI/CD WORKFLOW DETAILS

### When Workflow Triggers

- ✅ Push to `main` branch
- ✅ Pull requests to `main`
- ❌ NOT on other branches (unless configured)

### Workflow Jobs

**Job 1: Code Quality**
- Language: Python 3.11
- Tools: flake8
- Time: ~1-2 minutes

**Job 2: Tests**
- Unit tests: pytest
- Integration tests: test_complete_pipeline.py
- API tests: test_transformer_api.py
- Time: ~3-5 minutes

**Job 3: API Validation**
- Validates /predict endpoint
- Tests response schema
- Tests mock transactions
- Time: ~1 minute

**Total Time:** 5-8 minutes per push

---

## 🎯 NEXT STEPS AFTER SUCCESSFUL PUSH

1. **Verify on GitHub**: Go to your repository URL and confirm files appear
2. **Check Actions**: Click Actions tab to see workflow status
3. **Monitor Runs**: Watch the CI/CD pipeline execute
4. **Review Results**: Click on workflow runs to see detailed logs
5. **Make Changes**: Edit code locally and push again
6. **Track Progress**: GitHub shows commit history and workflow runs

---

## 📚 USEFUL COMMANDS

```powershell
# View git status
git status

# View commit history
git log

# View remote repositories
git remote -v

# See what will be committed
git diff --cached

# Unstage a file
git reset <filename>

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View current branch
git branch

# Switch branch
git checkout <branch-name>

# Pull latest changes
git pull origin main

# Force push (use carefully!)
git push --force origin main
```

---

## 🎉 YOU'RE READY!

Your MLOps project is now:
✅ Version controlled with Git  
✅ Hosted on GitHub  
✅ Automated with CI/CD pipeline  
✅ Monitored and validated  

**Every push will:**
- Run code quality checks
- Execute all tests
- Validate API endpoints
- Report results on GitHub

**Congratulations!** You now have a professional software engineering setup! 🚀

---

## 📞 REFERENCE LINKS

- GitHub Help: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- GitHub Actions: https://github.com/features/actions
- SSH Setup: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

