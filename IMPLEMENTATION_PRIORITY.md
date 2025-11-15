# Implementation Priority Guide

## Quick Start: IDEAW + FrEIA Research Path

This document outlines the **immediate priority** implementation path for your research paper.

---

## 🎯 PHASE 1: IDEAW Base Implementation (Week 1-2)

### Goal: Get IDEAW working with your system

**Tasks 20.1 - 20.4** (Immediate Priority)

1. **Set up IDEAW environment** (Task 20.1)
   ```bash
   cd research/IDEAW
   pip install -r requirements.txt
   # torch==1.13.1, librosa==0.10.1, scipy, pydub, etc.
   ```

2. **Test IDEAW examples** (Task 20.2)
   - Review `embed_extract.py`
   - Test with sample 16kHz audio
   - Understand dual-embedding workflow
   - Document input/output formats

3. **Create IDEAW service wrapper** (Task 20.3)
   - File: `backend/services/ideaw_service.py`
   - Wrap IDEAW model for easy use
   - Implement encode/decode methods
   - Handle chunk processing (16000 + 8000)

4. **Test integration** (Task 20.4)
   - Write unit tests
   - Verify encoding/decoding accuracy
   - Test with various audio files

**Deliverable**: Working IDEAW baseline that you can encode/decode audio

---

## 🔬 PHASE 2: FrEIA Extensions (Week 3-5) - YOUR NOVELTY

### Goal: Create novel INN architecture variants using FrEIA

**Tasks 21.1 - 21.9** (Core Research Contribution)

### Step 1: Understand IDEAW Architecture (Task 21.1-21.2)
```bash
pip install FrEIA
```
- Study `research/IDEAW/models/innBlock.py`
- Understand coupling blocks (ρ, η, φ, ψ)
- Analyze DenseBlock structure
- Document current architecture

### Step 2: Create FrEIA Replacement (Task 21.3)
- File: `research/ideaw_freia/freia_innblock.py`
- Replace IDEAW's InnBlock with FrEIA coupling blocks
- Test: Affine, Spline, Rational Quadratic coupling
- Verify invertibility and gradient flow

### Step 3: Build FrEIA-MIHNET (Task 21.4-21.5)
- File: `research/ideaw_freia/freia_mihnet.py`
- Create Mihnet_s1 and Mihnet_s2 using FrEIA
- Make architecture configurable
- Integrate with IDEAW's training pipeline

### Step 4: Train FrEIA Variants (Task 21.6-21.7)
- Set up Google Colab for training
- Train baseline FrEIA-IDEAW
- Save checkpoints
- Evaluate baseline performance

### Step 5: Ablation Studies (Task 21.8) - **KEY NOVELTY**
Run systematic experiments:

1. **INN Block Count**: 4, 6, 8, 10, 12 blocks
2. **Coupling Types**: Affine vs Spline vs Rational Quadratic
3. **Dense Block Variants**: Different layer depths
4. **Activation Functions**: ReLU, LeakyReLU, ELU, etc.
5. **Normalization**: ActNorm, BatchNorm, LayerNorm

**Deliverable**: Multiple trained FrEIA-IDEAW variants with documented performance

---

## 💥 PHASE 3: Attack Suite (Week 6-7)

### Goal: Test robustness of your models

**Tasks 22.1 - 22.8**

### Priority Attacks (Implement First):
1. **Compression** (Task 22.2)
   - MP3: 64, 128, 192, 320 kbps
   - Most common real-world attack

2. **Noise** (Task 22.3)
   - Gaussian noise: 5-30 dB SNR
   - Tests basic robustness

3. **Filtering** (Task 22.4)
   - Low-pass, high-pass filters
   - Common in audio processing

4. **Temporal** (Task 22.5)
   - Speed changes (0.8x - 1.2x)
   - Sample rate conversion

### Advanced Attacks (If Time Permits):
5. **Re-recording** (Task 22.6)
   - Room impulse response
   - Most challenging attack

6. **Adversarial** (Task 22.7)
   - Gradient-based removal
   - Research-level attack

**Deliverable**: Attack suite that can test any watermarking method

---

## 📊 PHASE 4: Evaluation & Analysis (Week 8-9)

### Goal: Generate paper results

**Tasks 23.1 - 24.5**

### Metrics to Implement (Task 23.2-23.4):
1. **Robustness**: BER, Detection Rate, False Positive Rate
2. **Imperceptibility**: SNR, PESQ, STOI
3. **Performance**: Encoding/Decoding latency, Model size

### Experiments to Run (Task 24.1-24.4):
1. **Baseline Evaluation**: IDEAW original on clean audio
2. **Variant Comparison**: All FrEIA variants on clean audio
3. **Attack Robustness**: All variants against all attacks
4. **Statistical Analysis**: Significance testing, confidence intervals

### Generate Results (Task 24.5):
- Publication-ready figures
- LaTeX tables
- Results section for paper
- Supplementary materials

**Deliverable**: Complete experimental results for paper

---

## 📝 Research Paper Structure

### Sections You'll Write:

1. **Introduction**
   - Problem: Audio watermarking robustness
   - Solution: INN-based approach with FrEIA

2. **Related Work**
   - SilentCipher, WavMark, IDEAW
   - INN architectures in watermarking

3. **Methodology**
   - IDEAW baseline
   - FrEIA extensions
   - Ablation study design

4. **Experiments**
   - Dataset description
   - Attack suite
   - Evaluation metrics

5. **Results**
   - Baseline performance
   - Variant comparison
   - Attack robustness
   - Ablation study findings

6. **Discussion**
   - Best architecture
   - Trade-offs
   - Limitations

7. **Conclusion**
   - Novel contributions
   - Future work

---

## 🎓 Novel Contributions for Your Paper

### Primary Contributions:
1. **Systematic INN Architecture Study**: First comprehensive analysis of INN components for audio watermarking
2. **FrEIA-based IDEAW**: Novel implementation using modern INN framework
3. **Ablation Studies**: Detailed analysis of coupling types, block counts, etc.
4. **Comprehensive Evaluation**: Extensive attack suite and metrics

### What Makes This Publishable:
- ✅ Novel architectural exploration (FrEIA variants)
- ✅ Systematic ablation studies (not just one model)
- ✅ Comprehensive evaluation (multiple attacks, metrics)
- ✅ Reproducible research (open-source code, configs)
- ✅ Clear improvements or insights (from ablation studies)

---

## ⏱️ Timeline Summary

| Week | Phase | Tasks | Deliverable |
|------|-------|-------|-------------|
| 1-2  | IDEAW Base | 20.1-20.4 | Working IDEAW baseline |
| 3-5  | FrEIA Extensions | 21.1-21.9 | Trained FrEIA variants |
| 6-7  | Attack Suite | 22.1-22.8 | Comprehensive attacks |
| 8-9  | Evaluation | 23.1-24.5 | Paper results |
| 10-12 | Paper Writing | - | Draft paper |

**Total: 12 weeks to paper submission**

---

## 🚀 Getting Started TODAY

### Immediate Next Steps:

1. **Install IDEAW dependencies**
   ```bash
   cd research/IDEAW
   pip install -r requirements.txt
   ```

2. **Test IDEAW example**
   ```bash
   # Review embed_extract.py
   # Modify paths to your audio files
   # Run embedding and extraction
   ```

3. **Create service wrapper**
   ```bash
   # Create backend/services/ideaw_service.py
   # Start with basic load_model() method
   ```

4. **Document findings**
   - Keep notes on IDEAW behavior
   - Document any issues or insights
   - Track performance metrics

---

## 📚 Key Files to Focus On

### IDEAW Repository:
- `research/IDEAW/models/innBlock.py` - Core INN architecture
- `research/IDEAW/models/mihnet.py` - MIHNET structure
- `research/IDEAW/models/ideaw.py` - Full model
- `research/IDEAW/embed_extract.py` - Usage example
- `research/IDEAW/train.py` - Training pipeline

### Your Implementation:
- `backend/services/ideaw_service.py` - Service wrapper
- `research/ideaw_freia/freia_innblock.py` - FrEIA replacement
- `research/ideaw_freia/freia_mihnet.py` - FrEIA MIHNET
- `backend/research/attack_suite.py` - Attack implementations
- `backend/research/evaluation_metrics.py` - Metrics

---

## 💡 Tips for Success

1. **Start Simple**: Get IDEAW working first before FrEIA
2. **Document Everything**: Keep detailed notes for paper
3. **Version Control**: Git commit after each working feature
4. **Test Frequently**: Verify each component works before moving on
5. **Focus on Novelty**: The FrEIA ablation studies are your main contribution
6. **Reproducibility**: Save all configs, checkpoints, and results

---

## ❓ Questions to Answer Through Research

Your ablation studies should answer:
1. How many INN blocks are optimal for watermarking?
2. Which coupling type works best (affine, spline, etc.)?
3. What's the trade-off between imperceptibility and robustness?
4. How do architectural choices affect attack resistance?
5. Can FrEIA-based INN improve upon original IDEAW?

These answers = your paper's results section!

---

## 🎯 Success Criteria

You're ready for paper submission when you have:
- ✅ Working IDEAW baseline
- ✅ 5+ trained FrEIA-IDEAW variants
- ✅ Comprehensive attack evaluation
- ✅ Statistical analysis showing significance
- ✅ Publication-ready figures and tables
- ✅ Clear novel contributions documented
- ✅ Reproducible code and configs

**Good luck with your research! 🚀**
