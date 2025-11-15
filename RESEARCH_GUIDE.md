# 🎓 Audio Watermarking Research Guide

**Complete guide for implementing IDEAW + FrEIA research in Google Colab**

---

## 📋 Table of Contents

1. [Quick Start (5 minutes)](#quick-start)
2. [What You Need to Implement](#what-to-implement)
3. [Colab Training Setup](#colab-training)
4. [Implementation Timeline](#timeline)
5. [Research Plan Overview](#research-plan)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start {#quick-start}

### Step 1: Ensure Code is on GitHub (Already Done! ✅)
Your code is already at: https://github.com/Abdullahyassir007/audio-watermarking-demo

### Step 2: Upload Training Data to Google Drive (1 minute)
1. Open [Google Drive](https://drive.google.com)
2. Create folder: `IDEAW_Research`
3. Create subfolders: `data/`, `checkpoints/`, `results/`
4. Upload training audio files to `data/` folder

### Step 3: Open Colab (1 minute)
1. Go to [Google Colab](https://colab.research.google.com)
2. Upload `colab_notebooks/IDEAW_Training_Template.ipynb`
3. Runtime → Change runtime type → **GPU** → Save

### Step 4: Start Working (1 minute)
Run the setup cells in the notebook!

---

## 🔨 What You Need to Implement {#what-to-implement}

### The Colab Notebook is 80% Complete

✅ **Already Done (Just Run):**
- Setup (mount Drive, install packages, check GPU)
- Model loading
- Visualization
- Download results

❌ **You Need to Implement (Tasks 20.3 & 20.5):**

### 1. Training Loop (Task 20.3)

**First, check if IDEAW has a Solver:**
```python
# In Colab
!cat /content/IDEAW-Research/research/IDEAW/solver.py
```

**If Solver exists** → Easy:
```python
from solver import Solver
solver = Solver(config_path, ideaw, device)
solver.train(save_path=CHECKPOINT_PATH, log_path=RESULTS_PATH)
```

**If no Solver** → Copy from `train.py`:
- Look at `research/IDEAW/train.py`
- Copy their training loop
- Adapt for Colab notebook

### 2. Evaluation Code (Task 20.5)

Look at `research/IDEAW/embed_extract.py` for reference:
- Load trained checkpoint
- Test on validation audio
- Calculate BER, SNR, accuracy
- Save results

**Key Point:** Don't write from scratch - adapt IDEAW's existing code!

---

## 💻 Colab Training Setup {#colab-training}

### Three Approaches

#### Option 1: Google Drive Only (Easiest)
```python
from google.colab import drive
drive.mount('/content/drive')

CODE_PATH = '/content/drive/MyDrive/IDEAW_Research/code'
DATA_PATH = '/content/drive/MyDrive/IDEAW_Research/data'
```
**Best for:** Quick start, small projects

#### Option 2: GitHub + Drive (Recommended) ⭐
```python
!git clone https://github.com/Abdullahyassir007/audio-watermarking-demo.git
%cd audio-watermarking-demo

from google.colab import drive
drive.mount('/content/drive')
DATA_PATH = '/content/drive/MyDrive/IDEAW_Research/data'
```
**Best for:** Active development, version control, easy code updates

#### Option 3: Local Copy (Fastest Training)
```python
import shutil
shutil.copytree(
    '/content/drive/MyDrive/IDEAW_Research/data',
    '/content/data'
)
DATA_PATH = '/content/data'
```
**Best for:** Long training sessions

### Minimal Colab Setup (Copy-Paste)

```python
# Clone from GitHub
!git clone https://github.com/Abdullahyassir007/audio-watermarking-demo.git
%cd audio-watermarking-demo

# Mount Drive for data
from google.colab import drive
drive.mount('/content/drive')

# Install dependencies
!pip install -q -r research/IDEAW/requirements.txt
!pip install -q FrEIA

# Check GPU
import torch
print(f"GPU: {torch.cuda.is_available()}")
print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

# Load IDEAW
import sys
sys.path.insert(0, '/content/audio-watermarking-demo/research/IDEAW')
from models.ideaw import IDEAW

device = 'cuda' if torch.cuda.is_available() else 'cpu'
ideaw = IDEAW('research/IDEAW/models/config.yaml', device)
print("✓ IDEAW loaded!")
```

### Keep Session Alive

Open browser console (F12) and run:
```javascript
setInterval(() => {
    document.querySelector("colab-connect-button").click();
}, 60000);
```

### Resume After Disconnect

```python
checkpoint_path = '/content/drive/MyDrive/IDEAW_Research/checkpoints/latest.pth'
if os.path.exists(checkpoint_path):
    model.load_state_dict(torch.load(checkpoint_path))
    print("Resumed from checkpoint!")
```

---

## 📅 Implementation Timeline {#timeline}

### Week 1-2: IDEAW Baseline
- **Day 1**: Setup Colab, explore IDEAW code
- **Day 2**: Implement training loop
- **Day 3**: Test on small dataset
- **Day 4**: Upload full dataset
- **Day 5**: Start full training (overnight)
- **Day 6**: Evaluate baseline
- **Day 7**: Document results

**Deliverable:** Working IDEAW baseline model

### Week 3-5: FrEIA Extensions (YOUR NOVELTY)
- **Week 3**: 
  - Install FrEIA
  - Analyze IDEAW's InnBlock
  - Create FrEIA-based InnBlock
- **Week 4**:
  - Create FrEIA-MIHNET
  - Train baseline FrEIA-IDEAW
- **Week 5**:
  - Ablation studies (5+ variants)
  - Train all variants

**Deliverable:** 5+ trained FrEIA-IDEAW variants

### Week 6-7: Attack Suite
- Implement compression attacks (MP3, AAC, Opus)
- Implement noise attacks (Gaussian, environmental)
- Implement filtering attacks (low-pass, high-pass)
- Implement temporal attacks (speed, resampling)
- Implement re-recording simulation
- Test all variants against all attacks

**Deliverable:** Complete attack evaluation results

### Week 8-9: Evaluation & Analysis
- Calculate all metrics (BER, SNR, PESQ, STOI)
- Statistical analysis
- Generate publication-ready figures and tables
- Compile results

**Deliverable:** Paper results section

### Week 10-12: Paper Writing
- Write methodology section
- Write results section
- Create supplementary materials
- Prepare reproducibility package

**Deliverable:** Draft paper ready for submission


---

## 📊 Research Plan Overview {#research-plan}

### Research Goal
Develop novel INN-based audio watermarking variants using FrEIA framework and evaluate comprehensively for academic publication.

### Novel Contributions
1. **Systematic INN Architecture Study**: First comprehensive analysis of INN components for audio watermarking
2. **FrEIA-based IDEAW**: Novel implementation using modern INN framework
3. **Ablation Studies**: Detailed analysis of coupling types, block counts, etc.
4. **Comprehensive Evaluation**: Extensive attack suite and metrics

### Methods to Integrate

| Method | Status | Purpose |
|--------|--------|---------|
| **SilentCipher** | ✅ Done | Baseline comparison |
| **IDEAW** | 🔄 In Progress | Base INN implementation |
| **FrEIA-IDEAW** | ⏳ To Do | Novel contribution |
| **WavMark** | ⏳ Optional | Additional comparison |
| **Classical DSP** | ⏳ Optional | Baseline comparison |

### Ablation Studies (Your Novelty)

Test these FrEIA-IDEAW variants:
1. **Block Count**: 4, 6, 8, 10, 12 INN blocks
2. **Coupling Types**: Affine, Spline, Rational Quadratic
3. **Dense Blocks**: Different layer depths
4. **Activations**: ReLU, LeakyReLU, ELU
5. **Normalization**: ActNorm, BatchNorm, LayerNorm

### Attack Suite

| Attack Type | Variants |
|-------------|----------|
| Compression | MP3 (64, 128, 192, 320 kbps), AAC, Opus |
| Noise | Gaussian (5-30 dB SNR), Environmental, Colored |
| Filtering | Low-pass, High-pass, Band-pass |
| Temporal | Speed (0.8x-1.2x), Resampling |
| Re-recording | Room impulse response, Microphone simulation |
| Adversarial | Gradient-based removal (optional) |

### Evaluation Metrics

**Robustness:**
- Bit Error Rate (BER)
- Detection Rate
- False Positive Rate
- ROC curves

**Imperceptibility:**
- SNR (Signal-to-Noise Ratio)
- PESQ (Perceptual quality)
- STOI (Intelligibility)

**Performance:**
- Encoding/Decoding latency
- Model size
- Throughput

---

## 🆘 Troubleshooting {#troubleshooting}

### Common Issues

**"No GPU available"**
- Solution: Runtime → Change runtime type → GPU → Save

**"Session disconnected"**
- Solution: Checkpoints saved in Drive. Reconnect and resume.

**"Out of memory"**
- Solution: Reduce batch size: `BATCH_SIZE = 8`

**"Files not found"**
- Solution: Check paths: `!ls /content/drive/MyDrive/IDEAW_Research/`

**"I don't know how to implement training"**
- Solution: Look at `research/IDEAW/train.py` - copy their code!

**"IDEAW code is confusing"**
- Solution: Start with `embed_extract.py` - simpler workflow

**"Training fails"**
- Solution: Test with 1 audio file first, then scale up

### Training Times (Colab T4 GPU)

| Dataset Size | Epochs | Time |
|--------------|--------|------|
| 100 files | 50 | ~2 hours |
| 500 files | 50 | ~6 hours |
| 1000 files | 50 | ~12 hours |
| 1000 files | 100 | ~24 hours (need Pro) |

### Colab Limits

- **Free**: 12-hour sessions, may disconnect
- **Pro** ($10/month): 24-hour sessions, better GPUs
- **Pro+** ($50/month): Background execution

---

## 📁 File Organization

### Essential Files (Keep These)

```
project/
├── README.md                          # Project overview
├── RESEARCH_GUIDE.md                  # This file (complete guide)
├── .kiro/specs/                       # Specifications
│   └── audio-watermarking-demo/
│       ├── requirements.md            # Research requirements
│       ├── design.md                  # Architecture design
│       └── tasks.md                   # Implementation tasks
├── colab_notebooks/
│   └── IDEAW_Training_Template.ipynb  # Colab notebook
├── research/
│   ├── IDEAW/                         # IDEAW repository
│   └── wavmark/                       # WavMark repository
└── backend/                           # Demo application code
```

### Reference Files (Optional Reading)

- Backend documentation in `backend/README.md`
- Confidence scores explained in `backend/CONFIDENCE_SCORE_EXPLAINED.md`

---

## ✅ Success Checklist

### Phase 1: IDEAW Baseline
- [ ] IDEAW training working in Colab
- [ ] Baseline model trained (6-12 hours)
- [ ] Evaluation results documented
- [ ] Checkpoints saved to Drive
- [ ] Baseline metrics: SNR, BER, accuracy

### Phase 2: FrEIA Extensions
- [ ] FrEIA installed and tested
- [ ] FrEIA-InnBlock implemented
- [ ] FrEIA-MIHNET created
- [ ] Baseline FrEIA-IDEAW trained
- [ ] 5+ variants trained
- [ ] Ablation results documented

### Phase 3: Evaluation
- [ ] Attack suite implemented
- [ ] All variants tested against attacks
- [ ] All metrics calculated
- [ ] Statistical analysis complete
- [ ] Publication-ready figures generated

### Phase 4: Paper
- [ ] Methodology section written
- [ ] Results section written
- [ ] Figures and tables formatted
- [ ] Supplementary materials prepared
- [ ] Reproducibility package ready

---

## 🎯 Next Steps

1. **Right Now**: Read this guide (you're doing it!)
2. **Today**: Follow Quick Start section above
3. **This Week**: Implement training loop (Task 20.3)
4. **Next Week**: Train IDEAW baseline
5. **Week 3-5**: Implement FrEIA variants
6. **Week 6-9**: Attacks and evaluation
7. **Week 10-12**: Write paper

---

## 📞 Quick Reference

- **Main tasks**: `.kiro/specs/audio-watermarking-demo/tasks.md`
- **Colab template**: `colab_notebooks/IDEAW_Training_Template.ipynb`
- **This guide**: `RESEARCH_GUIDE.md`

**You've got everything you need. Start with the Quick Start section and begin training! 🚀**
