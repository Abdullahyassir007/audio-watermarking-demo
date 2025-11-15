# Audio Watermarking Research Plan

## Overview
This document outlines the comprehensive research plan for developing an ensemble audio watermarking system with multiple state-of-the-art methods for academic publication.

## Research Objectives

### Primary Goal
Develop and evaluate an ensemble audio watermarking system that combines multiple SOTA methods to achieve superior robustness and imperceptibility compared to individual methods.

### Novel Contributions
1. **Ensemble Learning Framework**: Novel fusion strategies combining deep learning and classical methods
2. **IDEAW Architecture Extensions**: Experimental INN modifications using FrEIA framework
3. **Comprehensive Evaluation**: Systematic robustness analysis across 8+ attack categories
4. **Comparative Study**: First comprehensive comparison of SilentCipher, WavMark, IDEAW, and classical DSP methods

## Integrated Watermarking Methods

### 1. SilentCipher (Sony) - Baseline ✅ IMPLEMENTED
- **Status**: Already integrated in current project
- **Capacity**: 40 bits (5 × 8-bit integers)
- **Sample Rates**: 16kHz, 44.1kHz
- **Strengths**: High imperceptibility, psychoacoustic modeling
- **Usage**: Pre-trained models via pip install

### 2. WavMark (ByteDance) - To Implement
- **Repository**: https://github.com/wavmark/wavmark
- **Status**: Cloned to research/wavmark
- **Capacity**: 32 bits (16-bit pattern + 16-bit payload)
- **Sample Rate**: 16kHz
- **Strengths**: 29× robustness vs traditional, 38dB SNR, 4.3 PESQ
- **Installation**: `pip install wavmark`
- **Key Features**:
  - Automatic model download from HuggingFace
  - Fixed pattern for watermark detection (1/65536 false positive rate)
  - Optimized for speech and generative audio
  - Chunk-based processing (1 second chunks)

### 3. IDEAW (INN-based) - To Implement
- **Repository**: https://github.com/PecholaL/IDEAW
- **Status**: Cloned to research/IDEAW
- **Capacity**: 26 bits (16-bit message + 10-bit location code)
- **Sample Rate**: 16kHz
- **Strengths**: Re-recording resistance, dual-embedding for localization
- **Architecture**:
  - Dual MIHNET structure (Mihnet_s1 + Mihnet_s2)
  - Multiple InnBlock layers (invertible coupling blocks)
  - STFT/ISTFT frequency domain processing
  - Attack layer for robustness training
  - Balance block for attack compensation
  - Discriminator for perceptual quality
- **Key Features**:
  - Invertible Neural Network architecture
  - Dual-embedding (message + location code)
  - Efficient watermark localization
  - Configurable INN block depth
  - Two-stage training process

### 4. Classical DSP Baselines - To Implement
- **Methods**: Echo Hiding, Spread Spectrum
- **Purpose**: Baseline comparison, lightweight processing
- **Strengths**: Fast, interpretable, no training required

### 5. IDEAW-FrEIA Extensions - Research Contribution
- **Purpose**: Novel architectural experimentation
- **Framework**: FrEIA (Framework for Easily Invertible Architectures)
- **Approach**: 
  - Replace IDEAW's custom InnBlock with FrEIA coupling layers
  - Experiment with different coupling types (affine, spline, etc.)
  - Ablation studies on INN components
  - Maintain compatibility with IDEAW's training pipeline
- **Novel Contributions**:
  - Systematic INN architecture analysis
  - Improved coupling block designs
  - Architectural optimization for watermarking

## Ensemble Learning Strategies

### Fusion Approaches
1. **Majority Voting**: Simple consensus across methods
2. **Confidence Weighting**: Weight by individual confidence scores
3. **Adaptive Selection**: Choose best method based on audio characteristics
4. **Consensus Decoding**: Require agreement threshold across methods

### Encoding Strategies
1. **Parallel Encoding**: Embed with multiple methods simultaneously
2. **Sequential Encoding**: Chain methods (one method's output → next method's input)
3. **Hybrid Approach**: Combine parallel and sequential strategies

## Comprehensive Attack Suite

### 1. Compression Attacks
- MP3: 64, 128, 192, 320 kbps
- AAC: Multiple bitrates
- Opus: Multiple bitrates

### 2. Noise Attacks
- Gaussian noise: Various SNR levels
- Environmental noise: Real-world samples
- Colored noise: Pink, brown, blue

### 3. Filtering Attacks
- Low-pass filter: Various cutoff frequencies
- High-pass filter: Various cutoff frequencies
- Band-pass filter: Various frequency ranges

### 4. Temporal Attacks
- Time-scale modification: 0.8× to 1.2× speed
- Sample rate conversion: 8kHz, 16kHz, 22kHz, 44.1kHz, 48kHz
- Pitch-preserving time stretching

### 5. Re-recording Simulation
- Room impulse response convolution
- Microphone response simulation
- Full playback-capture chain

### 6. Adversarial Attacks
- Gradient-based watermark removal
- Overwriting with conflicting watermarks

## Evaluation Metrics

### Robustness Metrics
- **Bit Error Rate (BER)**: Primary accuracy metric
- **Detection Rate**: True positive rate
- **False Positive Rate**: False alarm rate
- **ROC Analysis**: ROC curves and AUC

### Imperceptibility Metrics
- **SNR**: Signal-to-Noise Ratio
- **PESQ**: Perceptual Evaluation of Speech Quality
- **STOI**: Short-Time Objective Intelligibility
- **Spectral Distortion**: Frequency domain analysis

### Performance Metrics
- **Encoding Latency**: Processing time for embedding
- **Decoding Latency**: Processing time for extraction
- **Model Size**: Memory footprint
- **Computational Complexity**: FLOPS analysis

### Statistical Analysis
- **Significance Testing**: T-tests, Mann-Whitney U, ANOVA
- **Confidence Intervals**: Bootstrap CI calculation
- **Correlation Analysis**: Metric relationships

## Implementation Roadmap

### Phase 1: Multi-Method Integration (Weeks 1-3)
- [x] SilentCipher baseline (already done)
- [ ] WavMark integration and testing
- [ ] IDEAW integration and testing
- [ ] Classical DSP implementation
- [ ] Unified interface for all methods

### Phase 2: Ensemble Framework (Weeks 4-5)
- [ ] Ensemble engine implementation
- [ ] Fusion strategy development
- [ ] Ensemble evaluation framework
- [ ] Performance comparison

### Phase 3: Attack Suite Development (Weeks 6-7)
- [ ] Compression attacks
- [ ] Noise and filtering attacks
- [ ] Temporal attacks
- [ ] Re-recording simulation
- [ ] Adversarial attacks

### Phase 4: IDEAW-FrEIA Extensions (Weeks 8-10)
- [ ] FrEIA framework setup
- [ ] InnBlock replacement with FrEIA
- [ ] Architecture experimentation
- [ ] Ablation studies
- [ ] Novel architecture training

### Phase 5: Comprehensive Evaluation (Weeks 11-12)
- [ ] Full attack suite evaluation
- [ ] Statistical analysis
- [ ] Comparative study
- [ ] Ensemble performance analysis

### Phase 6: Paper Writing (Weeks 13-14)
- [ ] Results compilation
- [ ] Publication-ready figures and tables
- [ ] Paper drafting
- [ ] Reproducibility package

## Expected Research Outcomes

### Academic Contributions
1. **Novel Ensemble Framework**: First comprehensive ensemble approach for audio watermarking
2. **Systematic Comparison**: Detailed comparison of 4+ watermarking methods
3. **INN Architecture Analysis**: Systematic study of INN components for watermarking
4. **Robustness Benchmark**: Comprehensive evaluation across 8+ attack categories

### Publication Targets
- Conference: INTERSPEECH, ICASSP, EMNLP
- Journal: IEEE/ACM Transactions on Audio, Speech, and Language Processing

### Deliverables
1. **Research Paper**: 8-10 pages with comprehensive evaluation
2. **Open-Source Code**: Full implementation with documentation
3. **Reproducibility Package**: Datasets, configs, trained models
4. **Supplementary Materials**: Extended results, ablation studies

## Technical Requirements

### Hardware
- GPU: NVIDIA GPU with 8GB+ VRAM (for training)
- CPU: Multi-core processor for parallel processing
- RAM: 16GB+ recommended
- Storage: 50GB+ for datasets and models

### Software
- Python 3.8+
- PyTorch 1.13+
- Libraries: librosa, scipy, numpy, matplotlib
- Frameworks: SilentCipher, WavMark, IDEAW, FrEIA

### Development Environment
- Google Colab: For IDEAW training and experimentation
- Local Development: For integration and testing
- Version Control: Git for experiment tracking

## Repository Structure
```
audio-watermarking-demo/
├── backend/
│   ├── services/
│   │   ├── silentcipher_service.py      ✅ Done
│   │   ├── wavmark_service.py           ⏳ To Do
│   │   ├── ideaw_service.py             ⏳ To Do
│   │   └── classical_dsp_service.py     ⏳ To Do
│   └── research/
│       ├── ensemble_engine.py           ⏳ To Do
│       ├── attack_suite.py              ⏳ To Do
│       ├── evaluation_metrics.py        ⏳ To Do
│       └── automated_workflows.py       ⏳ To Do
├── research/
│   ├── IDEAW/                           ✅ Cloned
│   ├── wavmark/                         ✅ Cloned
│   └── ideaw_freia_extension/           ⏳ To Do
└── experiments/
    ├── configs/                         ⏳ To Do
    ├── results/                         ⏳ To Do
    └── notebooks/                       ⏳ To Do
```

## Key Insights from Repository Analysis

### IDEAW Architecture
- **Dual-Embedding Design**: Separate networks for message and location code
- **InnBlock Structure**: Custom invertible blocks with dense networks
- **Training Pipeline**: Two-stage training with configurable ratios
- **Attack Layer**: Built-in attack simulation for robustness
- **Chunk Processing**: 16000 samples + 8000 intervals for long audio

### WavMark Architecture
- **Pattern-Based Detection**: 16-bit fixed pattern reduces false positives
- **HuggingFace Integration**: Automatic model download
- **Simple API**: Easy encode/decode interface
- **Chunk-Based**: 1-second chunks for scalability

### Integration Strategy
1. **Unified Interface**: Abstract base class for all methods
2. **Format Conversion**: Standardize message formats across methods
3. **Chunk Alignment**: Handle different chunk sizes consistently
4. **Metric Standardization**: Common evaluation metrics for all methods

## Next Steps

1. **Immediate**: Implement WavMark service integration
2. **Short-term**: Implement IDEAW service integration
3. **Medium-term**: Develop ensemble framework and attack suite
4. **Long-term**: IDEAW-FrEIA extensions and paper writing

## References

1. SilentCipher: https://github.com/sony/silentcipher
2. WavMark: https://github.com/wavmark/wavmark
3. IDEAW: https://github.com/PecholaL/IDEAW
4. FrEIA: https://github.com/vislearn/FrEIA
