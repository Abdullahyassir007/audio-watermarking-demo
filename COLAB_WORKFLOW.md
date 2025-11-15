# 🔄 GitHub + Colab Workflow

## Overview

Your research workflow now uses **GitHub for code** and **Google Drive for data/checkpoints**.

---

## 📋 Workflow Diagram

```
Local Machine (Windows)
    ↓ Write code
    ↓ git push
    ↓
GitHub Repository
    ↓ git clone/pull
    ↓
Google Colab (Training)
    ↓ Save checkpoints
    ↓
Google Drive (Data & Results)
    ↓ Download
    ↓
Local Machine (Evaluation)
```

---

## 🚀 Quick Start in Colab

### 1. Clone Repository
```python
!git clone https://github.com/Abdullahyassir007/audio-watermarking-demo.git
%cd audio-watermarking-demo
```

### 2. Mount Drive for Data
```python
from google.colab import drive
drive.mount('/content/drive')

DATA_PATH = '/content/drive/MyDrive/IDEAW_Research/data'
CHECKPOINT_PATH = '/content/drive/MyDrive/IDEAW_Research/checkpoints'
RESULTS_PATH = '/content/drive/MyDrive/IDEAW_Research/results'
```

### 3. Install Dependencies
```python
!pip install -q -r research/IDEAW/requirements.txt
!pip install -q FrEIA
```

### 4. Start Training
```python
import sys
sys.path.insert(0, '/content/audio-watermarking-demo/research/IDEAW')
from models.ideaw import IDEAW

device = 'cuda' if torch.cuda.is_available() else 'cpu'
ideaw = IDEAW('research/IDEAW/models/config.yaml', device)
# ... training code ...
```

---

## 🔄 Development Cycle

### Making Changes Locally

```bash
# On your local machine
# 1. Make code changes
# 2. Test locally (optional)
# 3. Commit and push
git add .
git commit -m "Implemented FrEIA coupling blocks"
git push
```

### Pulling Changes in Colab

```python
# In Colab
!git pull origin main
print("✓ Code updated!")
```

### Making Changes in Colab

```python
# If you edit code in Colab
!git config --global user.email "your.email@example.com"
!git config --global user.name "Your Name"

!git add .
!git commit -m "Updated training parameters"
!git push  # You'll need GitHub token for authentication
```

---

## 📁 File Organization

### On GitHub (Code Only)
```
audio-watermarking-demo/
├── research/IDEAW/          # IDEAW code
├── research/wavmark/        # WavMark code
├── colab_notebooks/         # Colab templates
├── backend/                 # Demo app
└── docs/                    # Documentation
```

### On Google Drive (Data & Results)
```
IDEAW_Research/
├── data/                    # Training audio files
│   ├── train/
│   └── val/
├── checkpoints/             # Model checkpoints
│   ├── ideaw_baseline/
│   └── freia_variants/
└── results/                 # Training logs & plots
    ├── training_log.csv
    └── training_curves.png
```

---

## 💡 Best Practices

### 1. Separate Code and Data
- ✅ **Code** → GitHub (version controlled)
- ✅ **Data** → Google Drive (large files)
- ✅ **Checkpoints** → Google Drive (large files)

### 2. Commit Often
```bash
# After implementing a feature
git add .
git commit -m "Descriptive message"
git push
```

### 3. Pull Before Starting Work
```python
# In Colab, always pull latest code first
!git pull origin main
```

### 4. Use Branches for Experiments
```bash
# For experimental features
git checkout -b experiment-freia-spline
# ... make changes ...
git push -u origin experiment-freia-spline
```

---

## 🔧 Common Tasks

### Update Code in Colab
```python
# Pull latest changes
!git pull origin main

# Or clone fresh (if issues)
!rm -rf audio-watermarking-demo
!git clone https://github.com/Abdullahyassir007/audio-watermarking-demo.git
%cd audio-watermarking-demo
```

### Copy Data to Local Storage (Faster Training)
```python
import shutil

# Copy from Drive to Colab local storage
shutil.copytree(
    '/content/drive/MyDrive/IDEAW_Research/data',
    '/content/data'
)

# Use local path for training (much faster!)
DATA_PATH = '/content/data'
```

### Save Checkpoints to Drive
```python
import torch

# Save checkpoint
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}

torch.save(
    checkpoint,
    f'/content/drive/MyDrive/IDEAW_Research/checkpoints/checkpoint_epoch_{epoch}.pth'
)
```

### Push Code Changes from Colab
```python
# Configure git (first time only)
!git config --global user.email "your.email@example.com"
!git config --global user.name "Your Name"

# Check changes
!git status

# Commit and push
!git add .
!git commit -m "Updated from Colab"
!git push

# Note: You'll need GitHub personal access token
# Generate at: https://github.com/settings/tokens
```

---

## 🎯 Typical Research Session

### Morning (Local Machine)
```bash
# 1. Write new FrEIA coupling block code
# 2. Update documentation
# 3. Commit and push
git add .
git commit -m "Added spline coupling block"
git push
```

### Afternoon (Google Colab)
```python
# 1. Open Colab notebook
# 2. Clone/pull latest code
!git clone https://github.com/Abdullahyassir007/audio-watermarking-demo.git
%cd audio-watermarking-demo

# 3. Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# 4. Start training
# ... training code ...
# Training runs for 6-12 hours
```

### Evening (Check Progress)
```
# 1. Open Google Drive on phone/computer
# 2. Check IDEAW_Research/results/training_log.csv
# 3. View training_curves.png
# 4. Monitor progress
```

### Next Morning (Local Machine)
```bash
# 1. Download checkpoints from Drive
# 2. Evaluate model locally
# 3. Analyze results
# 4. Plan next experiment
```

---

## 🆘 Troubleshooting

### "Repository not found"
```python
# Check URL is correct
!git remote -v

# Update if needed
!git remote set-url origin https://github.com/Abdullahyassir007/audio-watermarking-demo.git
```

### "Authentication failed"
```python
# Use personal access token instead of password
# Generate at: https://github.com/settings/tokens
# When prompted for password, paste token
```

### "Merge conflict"
```python
# If you edited same file locally and in Colab
!git status  # Check conflicts
!git diff    # See differences

# Option 1: Keep Colab version
!git checkout --theirs filename.py
!git add filename.py
!git commit -m "Resolved conflict"

# Option 2: Keep local version
!git checkout --ours filename.py
!git add filename.py
!git commit -m "Resolved conflict"
```

### "Out of sync"
```python
# If local and Colab diverged
!git fetch origin
!git reset --hard origin/main  # WARNING: Loses local changes
```

---

## ✅ Advantages of This Workflow

1. **Version Control**: All code changes tracked
2. **Collaboration**: Easy to share with collaborators
3. **Backup**: Code backed up on GitHub
4. **Flexibility**: Work from anywhere (local, Colab, other machines)
5. **Reproducibility**: Exact code version for each experiment
6. **No Manual Uploads**: No need to zip/upload code manually

---

## 📚 Resources

- **Your Repository**: https://github.com/Abdullahyassir007/audio-watermarking-demo
- **GitHub Tokens**: https://github.com/settings/tokens
- **Git Basics**: https://git-scm.com/doc
- **Colab Guide**: https://colab.research.google.com/

**Happy researching! 🚀**
