# Implementation Plan

## 🎯 CURRENT PRIORITY: IDEAW Research (All in Google Colab)

**Note**: All IDEAW training and experimentation will be done in Google Colab. No local installation required for IDEAW work.

---

## Research Framework Implementation - PRIORITY ORDER

### PHASE 1: IDEAW + FrEIA in Google Colab (IMMEDIATE - Weeks 1-5)

- [x] 20. Set up IDEAW in Google Colab
  - [x] 20.1 Prepare Google Colab environment
    - ✅ Created Google Drive folder structure: `audio-watermarking-demo/{Dataset, checkpoints, results}`
    - ✅ Uploaded training audio files to Drive/Dataset folder (2707 files, used 50 for testing)
    - ✅ Code pushed to GitHub: https://github.com/Abdullahyassir007/audio-watermarking-demo
    - ✅ Created Colab notebook: `colab_notebooks/IDEAW_Colab_Training.ipynb`
    - ✅ Enabled GPU in Colab (Tesla T4, 15GB)
    - _Requirements: 14.1, 14.10_
  
  - [x] 20.2 Test IDEAW baseline in Colab
    - ✅ Used code directly from Drive (no cloning needed)
    - ✅ Mounted Google Drive for data and checkpoints
    - ✅ Installed dependencies with PyTorch 2.x compatibility fixes
    - ✅ Loaded IDEAW model successfully (8.4M parameters)
    - ✅ Verified GPU availability (Tesla T4)
    - ✅ Reviewed IDEAW's embed_extract.py workflow
    - ✅ Tested model initialization and structure
    - ✅ Documented IDEAW's input/output formats (16kHz, 1-second chunks, 16-bit message, 10-bit location code)
    - _Requirements: 14.1, 14.2, 14.10_
  
  - [x] 20.3 Implement IDEAW training in Colab
    - ✅ Verified IDEAW has Solver class
    - ✅ Used existing Solver for training
    - ✅ Implemented data loading: processed 50 audio files → 532 segments (pickle file)
    - ✅ Configured checkpoint saving to Drive (every 100 iterations)
    - ✅ Training metrics logged (loss, SNR, accuracy displayed every 10 iterations)
    - ✅ Implemented resume from checkpoint functionality
    - ✅ Tested training successfully
    - ✅ Fixed PyTorch 2.x compatibility issues (STFT/iSTFT, metrics, attackLayer)
    - ✅ Pushed fixes to GitHub
    - _Requirements: 14.5, 14.6, 14.8_
  
  - [x] 20.4 Train IDEAW baseline model in Colab
    - ✅ Prepared training dataset (532 segments from 50 files, 8.9 minutes)
    - ✅ Configured hyperparameters (batch size=1 due to memory, 1000 iterations)
    - ✅ Successfully trained for 500+ iterations
    - ✅ Reached Stage II (robustness training with attacks)
    - ✅ Checkpoints saved to Drive at iterations 100, 200, 300, 400, 500
    - ✅ Documented performance: SNR ~16-28 dB, accuracy improving from ~45% to ~60%
    - ✅ Model shows learning progress
    - _Requirements: 14.5, 14.6, 14.8_
  
  - [x] 20.5 Implement evaluation in Colab
    - ✅ Added checkpoint loading cell to notebook
    - ✅ Successfully loaded trained model checkpoint
    - ✅ Verified checkpoint structure is valid
    - ✅ Documented that full evaluation requires using standalone_demo.py or continuing training
    - ✅ Checkpoints saved to Drive for future use
    - _Requirements: 14.8, 14.9_

- [-] 21. Implement FrEIA-based IDEAW in Colab (NOVELTY)



  - [ ] 21.1 Set up FrEIA in Colab
    - Install FrEIA in Colab: `!pip install FrEIA`
    - Study FrEIA documentation and examples in Colab
    - Test FrEIA coupling blocks (affine, spline, rational quadratic)
    - Create new Colab notebook: `FrEIA_IDEAW_Development.ipynb`
    - _Requirements: 14.3, 14.7_
  
  - [ ] 21.2 Analyze IDEAW architecture in Colab
    - **TASK**: Create analysis notebook cells
    - Load and inspect `research/IDEAW/models/innBlock.py`
    - Visualize InnBlock structure (ρ, η, φ, ψ networks)
    - Analyze DenseBlock implementation
    - Document coupling block forward/reverse operations
    - Identify components for FrEIA replacement
    - _Requirements: 14.3_
  
  - [ ] 21.3 Create FrEIA-based InnBlock in Colab
    - **TASK**: Implement in Colab notebook
    - Create `FrEIA_InnBlock` class matching IDEAW's interface
    - Implement using FrEIA's coupling blocks
    - Test different coupling types (affine, spline, rational quadratic)
    - Verify forward/reverse operations match IDEAW
    - Test gradient flow and invertibility
    - Save implementation to Drive
    - _Requirements: 14.3, 14.4, 14.7_
  
  - [ ] 21.4 Create FrEIA-based MIHNET in Colab
    - **TASK**: Implement in Colab notebook
    - Create `FrEIA_Mihnet_s1` and `FrEIA_Mihnet_s2` classes
    - Make INN block count configurable
    - Make coupling type configurable
    - Test with IDEAW's training pipeline
    - Verify compatibility with attack layer and discriminator
    - _Requirements: 14.3, 14.4, 14.5_
  
  - [ ] 21.5 Integrate FrEIA-MIHNET with IDEAW in Colab
    - **TASK**: Create complete FrEIA-IDEAW model in Colab
    - Replace IDEAW's MIHNET with FrEIA version
    - Keep attack layer, discriminator, balance block unchanged
    - Test forward/backward pass
    - Verify training works with FrEIA blocks
    - Save FrEIA-IDEAW implementation to Drive
    - _Requirements: 14.4, 14.7_
  
  - [ ] 21.6 Train FrEIA-IDEAW baseline in Colab
    - Configure FrEIA-IDEAW with default settings (8 blocks, affine)
    - Start training in Colab (6-12 hours)
    - Monitor training metrics
    - Save checkpoints to Drive
    - Evaluate baseline FrEIA-IDEAW performance
    - Compare with original IDEAW baseline
    - _Requirements: 14.5, 14.6, 14.10_
  
  - [ ] 21.7 Conduct ablation studies in Colab (NOVELTY CONTRIBUTION)
    - **Experiment 1**: Train with 4, 6, 8, 10, 12 INN blocks
    - **Experiment 2**: Compare affine vs spline vs rational quadratic coupling
    - **Experiment 3**: Test different dense block architectures
    - **Experiment 4**: Experiment with activation functions
    - **Experiment 5**: Test normalization layers (ActNorm, BatchNorm)
    - Run each variant training in Colab (6-12 hours each)
    - Save all checkpoints and results to Drive
    - Document performance of each variant
    - _Requirements: 14.3, 14.7_
  
  - [ ] 21.8 Analyze ablation results in Colab
    - **TASK**: Create analysis notebook
    - Load all variant checkpoints
    - Compare metrics across all variants
    - Generate comparison tables and plots
    - Identify best-performing architecture
    - Document architectural insights
    - Prepare results for paper
    - _Requirements: 14.7, 14.9_
  
  - [ ] 21.9 Sync trained models and push code updates
    - All checkpoints automatically saved to Google Drive
    - Push any FrEIA implementation code to GitHub
    - Commit Colab notebooks with results to GitHub
    - Download key checkpoints from Drive to local if needed for evaluation
    - Organize in `research/trained_models/` directory locally
    - Create model inventory with performance metrics
    - Prepare models for attack evaluation (next phase)
    - _Requirements: 14.9_

### PHASE 2: Attack Suite Implementation (Local - Weeks 6-7)

- [ ] 22. Implement comprehensive attack suite (LOCAL)
  - [ ] 22.1 Set up attack suite infrastructure
    - Create `backend/research/attack_suite.py`
    - Design AttackSuite class with configurable parameters
    - Implement attack result logging and tracking
    - Create attack configuration system (YAML or JSON)
    - _Requirements: 15.9, 15.10_
  
  - [ ] 22.2 Implement compression attacks
    - Add MP3 compression using pydub or ffmpeg (64, 128, 192, 320 kbps)
    - Implement AAC compression at multiple bitrates
    - Implement Opus compression at multiple bitrates
    - Create compression parameter sweep functionality
    - Test compression attacks on sample audio
    - _Requirements: 15.1_
  
  - [ ] 22.3 Implement noise attacks
    - Add Gaussian noise at various SNR levels (5, 10, 15, 20, 25, 30 dB)
    - Implement environmental noise addition (use noise samples)
    - Add colored noise generation (pink, brown, blue noise)
    - Create noise intensity parameter sweeps
    - Test noise attacks on watermarked audio
    - _Requirements: 15.2_
  
  - [ ] 22.4 Implement filtering attacks
    - Add low-pass filter with configurable cutoff frequencies
    - Implement high-pass filter with configurable cutoff frequencies
    - Add band-pass filter with configurable frequency ranges
    - Use scipy.signal for filter implementations
    - Test filtering attacks on watermarked audio
    - _Requirements: 15.3_
  
  - [ ] 22.5 Implement temporal attacks
    - Add time-scale modification (speed changes 0.8x to 1.2x)
    - Implement sample rate conversion (8kHz, 16kHz, 22kHz, 44.1kHz, 48kHz)
    - Add pitch-preserving time stretching using librosa
    - Test temporal attacks on watermarked audio
    - _Requirements: 15.4, 15.5_
  
  - [ ] 22.6 Implement re-recording simulation
    - Download or create room impulse response (RIR) database
    - Implement RIR convolution for acoustic simulation
    - Add microphone frequency response simulation
    - Implement full playback-capture chain simulation
    - Test re-recording attacks on watermarked audio
    - _Requirements: 15.6_
  
  - [ ] 22.7 Implement adversarial attacks (optional - advanced)
    - Create gradient-based watermark removal using PyTorch
    - Implement overwriting attacks with conflicting watermarks
    - Add adversarial optimization for watermark destruction
    - Test adversarial attacks on watermarked audio
    - _Requirements: 15.7, 15.8_
  
  - [ ] 22.8 Create attack evaluation workflow
    - Implement batch attack processing for multiple audio files
    - Create systematic attack evaluation pipeline
    - Add detailed attack logging (parameters, results, timing)
    - Generate attack result summaries and statistics
    - _Requirements: 15.11, 15.12_

### PHASE 3: Evaluation Metrics and Analysis (Local or Colab - Weeks 8-9)

- [ ] 23. Implement evaluation metrics system
  - [ ] 23.1 Set up evaluation metrics infrastructure
    - Create `backend/research/evaluation_metrics.py`
    - Design EvaluationMetrics class
    - Implement result storage and tracking system
    - Create metrics configuration system
    - _Requirements: 16.11_
  
  - [ ] 23.2 Implement robustness metrics
    - Create Bit Error Rate (BER) calculation
    - Implement detection rate (true positive rate) calculation
    - Add false positive rate calculation
    - Create accuracy metric for watermark recovery
    - Implement ROC curve generation and AUC calculation
    - _Requirements: 16.1, 16.3_
  
  - [ ] 23.3 Implement imperceptibility metrics
    - Add SNR (Signal-to-Noise Ratio) calculation
    - Implement PESQ score evaluation using pesq library
    - Add STOI score calculation using pystoi library
    - Create spectral distortion analysis
    - Implement perceptual quality metrics
    - _Requirements: 16.2_
  
  - [ ] 23.4 Implement performance metrics
    - Add encoding latency measurement (time per second of audio)
    - Add decoding latency measurement
    - Implement model size analysis (parameters, memory)
    - Add throughput measurement for batch processing
    - Track GPU/CPU usage during processing
    - _Requirements: 16.4, 16.5_
  
  - [ ] 23.5 Implement statistical analysis
    - Add t-test for comparing two methods
    - Implement Mann-Whitney U test for non-parametric comparison
    - Create ANOVA for multi-group comparisons
    - Implement confidence interval calculation using bootstrap
    - Add correlation analysis between metrics
    - _Requirements: 16.6, 16.7, 16.8_
  
  - [ ] 23.6 Create visualization and reporting
    - Generate robustness curves (BER vs attack intensity)
    - Create comparative bar charts for different methods
    - Generate ROC curves for detection performance
    - Create heatmaps for attack resistance analysis
    - Implement publication-quality plot generation (matplotlib)
    - _Requirements: 16.9, 16.10_
  
  - [ ] 23.7 Create evaluation reporting system
    - Generate comparative performance tables
    - Export results in LaTeX table format
    - Create CSV/JSON exports for further analysis
    - Generate comprehensive evaluation reports (PDF/HTML)
    - Maintain detailed experimental logs for reproducibility
    - _Requirements: 16.10, 16.11, 16.12_

- [ ] 24. Run comprehensive evaluation experiments
  - [ ] 24.1 Evaluate IDEAW baseline (original architecture)
    - Load IDEAW baseline checkpoint from Drive
    - Test on clean audio (no attacks)
    - Measure imperceptibility metrics (SNR, PESQ, STOI)
    - Measure performance metrics (latency, throughput)
    - Document baseline results
    - _Requirements: 14.8, 16.1, 16.2, 16.4_
  
  - [ ] 24.2 Evaluate FrEIA-IDEAW variants
    - Load all FrEIA variant checkpoints from Drive
    - Test each variant on clean audio
    - Compare imperceptibility across variants
    - Compare performance across variants
    - Identify best-performing architecture
    - _Requirements: 14.7, 16.1, 16.2, 16.4_
  
  - [ ] 24.3 Evaluate robustness against attacks
    - Run all attacks on IDEAW baseline
    - Run all attacks on best FrEIA-IDEAW variant
    - Calculate BER for each attack type and intensity
    - Generate robustness curves
    - Compare robustness between variants
    - _Requirements: 15.1-15.8, 16.1, 16.3_
  
  - [ ] 24.4 Statistical analysis and comparison
    - Perform statistical tests comparing variants
    - Calculate confidence intervals for all metrics
    - Identify statistically significant improvements
    - Generate comparison tables and plots
    - _Requirements: 16.6, 16.7, 16.8_
  
  - [ ] 24.5 Generate research results package
    - Compile all experimental results
    - Generate publication-ready figures and tables
    - Create supplementary materials
    - Write results section for paper
    - Prepare reproducibility package
    - _Requirements: 16.10, 16.11, 16.12, 18.1-18.10_

### PHASE 4: Additional Methods and Ensemble (Optional - After Core Research)

- [ ] 25. Implement additional watermarking methods (OPTIONAL)
  - [ ] 25.1 Implement WavMark integration
    - Install WavMark via pip
    - Create WavMarkService wrapper
    - Test WavMark encoding/decoding
    - Add to evaluation framework
    - _Requirements: 12.1_
  
  - [ ] 25.2 Implement Classical DSP baselines
    - Implement echo hiding method
    - Implement spread spectrum method
    - Test DSP methods
    - Add to evaluation framework
    - _Requirements: 12.3_

- [ ] 26. Implement ensemble learning (OPTIONAL)
  - [ ] 26.1 Create ensemble framework
    - Design ensemble architecture
    - Implement fusion strategies
    - Test ensemble approaches
    - _Requirements: 13.1-13.10_

---

## ✅ COMPLETED TASKS (Demo Application)

## Frontend UI Guidelines
All frontend components must follow these design principles:
- **Modern Design**: Use gradients, shadows, rounded corners, and smooth transitions
- **Intuitive UX**: Clear labels, helpful placeholders, visual feedback, and logical flow
- **Responsive**: Mobile-first approach with proper breakpoints (sm, md, lg, xl)
- **Accessible**: Proper contrast ratios, keyboard navigation, and ARIA labels
- **Consistent**: Unified color scheme, typography, and spacing throughout

- [x] 0. Implement website navigation and authentication
  - [x] 0.1 Install React Router and set up routing
    - Install react-router-dom package
    - Configure BrowserRouter in App.tsx
    - Set up route definitions for all pages
    - Implement protected routes for authenticated pages
    - _Requirements: 0.1, 0.7, 0.8_
  - [x] 0.2 Create Navbar component
    - Implement responsive navigation with mobile menu
    - Add authentication-based conditional rendering
    - Implement active route highlighting
    - Add smooth transitions and hover effects
    - **UI**: Follow Frontend UI Guidelines - modern, responsive, accessible
    - _Requirements: 0.1, 0.2, 0.3, 0.4, 0.12, 0.13, 0.14_
  - [x] 0.3 Create Footer component
    - Design footer with brand information
    - Add navigation links and resources
    - Implement social media links
    - Add copyright information
    - **UI**: Follow Frontend UI Guidelines - consistent styling
    - _Requirements: 0.11, 0.12, 0.13_
  - [x] 0.4 Create HomePage
    - Design hero section with gradient background
    - Implement features showcase grid
    - Add "How it works" section
    - Create CTA section for unauthenticated users
    - **UI**: Follow Frontend UI Guidelines - engaging, modern, responsive
    - _Requirements: 0.9, 0.12, 0.13, 0.14_
  - [x] 0.5 Create LoginPage
    - Design login form with email and password inputs
    - Implement form validation
    - Add loading states for submission
    - Include social login placeholders
    - Add demo mode notice
    - **UI**: Follow Frontend UI Guidelines - clean, secure-looking, intuitive
    - _Requirements: 0.5, 0.6, 0.12, 0.13, 0.14_
  - [x] 0.6 Create AboutPage
    - Write technology overview section
    - Add use cases with visual cards
    - Include technical specifications
    - Add team section
    - **UI**: Follow Frontend UI Guidelines - informative, professional
    - _Requirements: 0.10, 0.12, 0.13_
  - [x] 0.7 Create EncodePage and DecodePage
    - Set up page layouts with headers
    - Add placeholders for audio upload components
    - Integrate MessageInput component in EncodePage
    - Add action buttons with disabled states
    - **UI**: Follow Frontend UI Guidelines - clear workflow, modern design
    - _Requirements: 0.7, 0.12, 0.13, 0.14_
  - [x] 0.8 Implement authentication state management
    - Add authentication state in App component
    - Implement login and logout handlers
    - Add route protection logic
    - Implement redirect to login for protected routes
    - _Requirements: 0.3, 0.4, 0.6, 0.7, 0.8_

- [x] 1. Set up project structure and dependencies






  - Create root directory with frontend and backend folders
  - Initialize React TypeScript project with Vite
  - Initialize Flask backend with virtual environment
  - Install frontend dependencies (React, TypeScript, Tailwind CSS, Axios, Socket.IO Client, Wavesurfer.js)
  - Install backend dependencies (Flask, Flask-CORS, Flask-SocketIO, SilentCipher, Librosa)
  - Create .gitignore files for both frontend and backend
  - Set up environment configuration files
  - _Requirements: 10.1, 10.2_

- [x] 2. Implement backend message conversion utilities





  - [x] 2.1 Create MessageConverter class with format conversion methods


    - Implement text_to_numeric() to convert text strings to 5-integer array
    - Implement binary_to_numeric() to convert 40-bit binary string to 5-integer array
    - Implement numeric_to_text() for reverse conversion
    - Implement numeric_to_binary() for reverse conversion
    - Implement validate_message() to validate message formats
    - _Requirements: 2.1, 2.3, 2.4_

  - [x] 2.2 Write unit tests for message conversion

    - Test text to numeric conversion with various inputs
    - Test binary to numeric conversion with edge cases
    - Test validation logic for all formats
    - _Requirements: 2.1, 2.3, 2.4_

- [x] 3. Implement backend audio processing service





  - [x] 3.1 Create AudioProcessor class for audio operations


    - Implement load_audio() using librosa
    - Implement save_audio() to write audio files
    - Implement validate_format() to check WAV format and sample rates
    - Implement get_metadata() to extract duration, sample rate, channels
    - _Requirements: 1.1, 1.2_

  - [x] 3.2 Add distortion methods to AudioProcessor

    - Implement apply_noise() to add Gaussian noise
    - Implement apply_compression() to simulate MP3 compression
    - Implement resample_audio() to change sample rates
    - _Requirements: 5.2, 5.3_

  - [x] 3.3 Write unit tests for audio processing

    - Test audio loading with valid and invalid files
    - Test metadata extraction accuracy
    - Test distortion application
    - _Requirements: 1.1, 5.2, 5.3_

- [x] 4. Implement SilentCipher integration service






  - [x] 4.1 Create SilentCipherService class

    - Implement get_model() to load 16kHz and 44.1kHz models
    - Implement encode_audio() to embed watermarks using SilentCipher
    - Implement decode_audio() to extract watermarks
    - Handle model caching to avoid reloading
    - Calculate and return SDR values
    - _Requirements: 3.1, 3.2, 3.4, 4.1, 4.2_

  - [x] 4.2 Write integration tests for SilentCipher

    - Test encoding with sample audio files
    - Test decoding accuracy
    - Test with both 16kHz and 44.1kHz audio
    - _Requirements: 3.1, 4.1_

- [ ] 5. Implement Flask API endpoints
  - [ ] 5.1 Create Flask app with CORS configuration
    - Set up Flask application factory
    - Configure CORS for frontend origin
    - Set up file upload limits (50MB)
    - Configure temporary storage directory
    - _Requirements: 10.1, 10.5_
  - [ ] 5.2 Implement /api/encode endpoint
    - Accept audio file and message payload
    - Validate file format and message
    - Call SilentCipherService to encode
    - Return encoded audio with SDR value
    - Handle errors and return appropriate status codes
    - _Requirements: 3.1, 3.2, 3.5, 10.1, 10.3_
  - [ ] 5.3 Implement /api/decode endpoint
    - Accept audio file
    - Call SilentCipherService to decode
    - Return decoded message and confidence scores
    - Handle no-watermark-detected case
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 10.2, 10.3_
  - [ ] 5.4 Implement /api/distort endpoint
    - Accept audio file and distortion parameters
    - Call AudioProcessor to apply distortion
    - Return distorted audio file
    - _Requirements: 5.2, 5.3_
  - [ ] 5.5 Implement /api/providers endpoint
    - Return list of available backend providers
    - Include SilentCipher as default provider
    - _Requirements: 9.1, 9.2_
  - [ ] 5.6 Implement /api/health endpoint
    - Check if SilentCipher models are loaded
    - Return service status
    - _Requirements: 10.5_

- [ ] 6. Implement WebSocket functionality for audio sharing
  - [ ] 6.1 Set up Flask-SocketIO server
    - Initialize Socket.IO with Flask app
    - Configure CORS for WebSocket connections
    - _Requirements: 8.1, 8.2_
  - [ ] 6.2 Create ShareManager service
    - Implement create_share_session() to generate unique share codes
    - Implement get_share_session() to retrieve shared audio
    - Implement cleanup_expired_sessions() with 1-hour timeout
    - Store sessions in memory with expiration tracking
    - _Requirements: 8.2, 8.3_
  - [ ] 6.3 Implement Socket.IO event handlers
    - Handle 'connect' event for client connections
    - Handle 'join_session' to assign device sessions
    - Handle 'share_audio' to create and broadcast share sessions
    - Handle 'request_audio' to retrieve shared audio
    - Handle 'disconnect' for cleanup
    - _Requirements: 8.1, 8.3, 8.5_
  - [ ] 6.4 Write integration tests for WebSocket
    - Test session creation and joining
    - Test audio sharing between mock clients
    - Test session expiration
    - _Requirements: 8.1, 8.3_

- [x] 7. Implement frontend message input component





  - [x] 7.1 Create MessageInput component with format switching


    - Create UI with tabs for numeric, text, and binary modes
    - Implement numeric array input with 5 number fields (0-255)
    - Implement text input with character limit
    - Implement binary input with 40-bit validation
    - Add format switching logic
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [x] 7.2 Add validation and conversion logic


    - Implement validateNumeric() for range checking
    - Implement convertTextToPayload() using backend API or local logic
    - Implement convertBinaryToPayload() for binary string conversion
    - Display validation errors inline

    - _Requirements: 2.5, 2.8_
  - [x] 7.3 Add random message generation


    - Implement generateRandom() to create random 5-integer array
    - Add button to trigger random generation
    - _Requirements: 2.6_

- [ ] 8. Implement frontend audio upload and player components
  - [ ] 8.1 Create AudioUploader component
    - Create file input with drag-and-drop support (modern, animated drop zone)
    - Implement validateFile() for format and size checking
    - Implement extractMetadata() using Web Audio API
    - Display file name, duration, and sample rate with visual cards
    - Show upload errors with helpful messages and icons
    - **UI**: Follow Frontend UI Guidelines - modern design with gradients, smooth animations, responsive layout
    - _Requirements: 1.1, 1.2, 1.4, 1.5_
  - [ ] 8.2 Create AudioPlayer component with waveform
    - Integrate Wavesurfer.js for waveform visualization with modern styling
    - Implement play/pause controls with smooth icon transitions
    - Implement seek functionality with visual feedback
    - Display current time and duration with clear typography
    - Add volume control with slider and mute button
    - **UI**: Follow Frontend UI Guidelines - intuitive controls, responsive waveform, accessible buttons
    - _Requirements: 1.3, 7.2, 7.3_

- [ ] 9. Implement frontend encoder panel
  - [ ] 9.1 Create EncoderPanel component
    - Integrate AudioUploader for original audio
    - Integrate MessageInput for message entry
    - Add "Encode" button with loading state and animated spinner
    - Display encoding progress indicator with percentage and visual feedback
    - **UI**: Follow Frontend UI Guidelines - clear workflow steps, visual hierarchy, responsive layout
    - _Requirements: 3.1, 3.2_
  - [ ] 9.2 Implement encoding API call
    - Create encodeAudio() method using Axios
    - Send audio file and message to /api/encode
    - Handle response with encoded audio blob
    - Handle errors with user-friendly messages
    - _Requirements: 3.1, 10.1, 10.3, 10.4_
  - [ ] 9.3 Display encoding results
    - Show AudioPlayer for encoded audio with modern player controls
    - Display SDR value prominently with visual indicator (good/fair/poor)
    - Add download button for encoded file with icon and hover effects
    - Show side-by-side comparison with original using responsive grid
    - **UI**: Follow Frontend UI Guidelines - clear result presentation, visual metrics, intuitive actions
    - _Requirements: 3.3, 3.4, 3.5, 7.1, 7.2, 7.4_
  - [ ] 9.4 Add share functionality
    - Add "Share to Device" button
    - Integrate with SharePanel component
    - _Requirements: 8.1_

- [ ] 10. Implement frontend decoder panel
  - [ ] 10.1 Create DecoderPanel component
    - Integrate AudioUploader for watermarked audio
    - Add "Decode" button with loading state and animated spinner
    - Display decoding progress indicator with visual feedback
    - **UI**: Follow Frontend UI Guidelines - clear call-to-action, loading states, responsive design
    - _Requirements: 4.1, 4.5_
  - [ ] 10.2 Implement decoding API call
    - Create decodeAudio() method using Axios
    - Send audio file to /api/decode
    - Handle response with decoded message
    - Handle no-watermark-detected case
    - Handle errors appropriately
    - _Requirements: 4.1, 10.2, 10.3, 10.4_
  - [ ] 10.3 Display decoding results
    - Show decoded message in all formats (numeric, text, binary) with tabbed interface
    - Display confidence scores for each value with visual bars/indicators
    - Show detection status clearly with success/warning/error states and icons
    - Handle and display "no watermark found" state with helpful message
    - **UI**: Follow Frontend UI Guidelines - clear result presentation, visual confidence indicators, intuitive format switching
    - _Requirements: 4.2, 4.3, 4.4_

- [ ] 11. Implement frontend distortion testing panel
  - [ ] 11.1 Create DistortionPanel component with toggle
    - Add toggle switch to enable/disable distortion testing with smooth animation
    - Show distortion controls only when enabled with slide-in animation
    - Create UI for distortion type selection (noise, compression, resample) with visual cards
    - Add parameter inputs for each distortion type with sliders and real-time preview
    - **UI**: Follow Frontend UI Guidelines - progressive disclosure, visual feedback, intuitive controls
    - _Requirements: 5.1, 5.2, 5.7_
  - [ ] 11.2 Implement distortion API call
    - Create applyDistortion() method using Axios
    - Send audio and distortion parameters to /api/distort
    - Handle response with distorted audio blob
    - Handle errors
    - _Requirements: 5.2, 5.3_
  - [ ] 11.3 Display distortion results
    - Show AudioPlayer for distorted audio with waveform comparison
    - Add "Decode Distorted" button with clear call-to-action styling
    - Display comparison of detection results with before/after cards
    - Show robustness metrics with visual charts and color-coded indicators
    - **UI**: Follow Frontend UI Guidelines - clear comparisons, visual metrics, data visualization
    - _Requirements: 5.3, 5.4, 5.5, 5.6_

- [ ] 12. Implement frontend audio sharing functionality
  - [ ] 12.1 Create SharePanel component
    - Add "Generate Share Code" button with icon and loading state
    - Display generated share code prominently with copy-to-clipboard functionality
    - Generate and display QR code using qrcode library with modern styling
    - Show shareable link with one-click copy button
    - **UI**: Follow Frontend UI Guidelines - clear sharing flow, visual QR code, easy copy actions
    - _Requirements: 8.1, 8.2_
  - [ ] 12.2 Implement WebSocket client for sharing
    - Initialize Socket.IO client connection
    - Implement generateShareCode() to create unique ID
    - Emit 'share_audio' event with audio blob and metadata
    - Handle connection status and errors
    - _Requirements: 8.1, 8.3_
  - [ ] 12.3 Create ReceivePanel component
    - Add input for entering share code with clear placeholder and validation
    - Add "Receive Audio" button with loading state and icon
    - Display receiving status with progress indicator and visual feedback
    - **UI**: Follow Frontend UI Guidelines - clear input validation, loading states, status feedback
    - _Requirements: 8.3_
  - [ ] 12.4 Implement WebSocket client for receiving
    - Listen for 'audio_shared' events
    - Emit 'request_audio' with share code
    - Handle received audio blob
    - Pass received audio to decoder or player
    - _Requirements: 8.3, 8.4_
  - [ ] 12.5 Display device session identifier
    - Generate unique device session ID on app load
    - Display session ID in UI header or footer with badge styling
    - Persist session ID in sessionStorage
    - **UI**: Follow Frontend UI Guidelines - subtle but visible, copy functionality, consistent placement
    - _Requirements: 8.5_

- [ ] 13. Implement backend provider abstraction
  - [ ] 13.1 Create BackendProvider interface
    - Define abstract base class for backend providers
    - Define methods: encode(), decode(), get_capabilities()
    - _Requirements: 9.3_
  - [ ] 13.2 Implement SilentCipherProvider
    - Create concrete implementation of BackendProvider
    - Wrap SilentCipherService methods
    - Return provider metadata (name, features, etc.)
    - _Requirements: 9.2, 9.3_
  - [ ] 13.3 Create ProviderManager
    - Implement provider registration system
    - Implement get_provider() to retrieve active provider
    - Implement list_providers() for /api/providers endpoint
    - _Requirements: 9.1, 9.4_

- [ ] 14. Implement frontend backend selector
  - [ ] 14.1 Create BackendSelector component
    - Fetch available providers from /api/providers
    - Display provider options in dropdown or radio buttons
    - Show provider description and features
    - _Requirements: 9.1, 9.2_
  - [ ] 14.2 Implement provider switching
    - Update global state when provider changes
    - Persist selection in localStorage
    - Update encoder and decoder panels with new provider
    - _Requirements: 9.4, 9.5_

- [ ] 15. Implement main app layout and routing
  - [ ] 15.1 Create App component with global state
    - Set up React Context for global state (backend provider, device session, socket)
    - Initialize Socket.IO connection on mount
    - Generate and store device session ID
    - _Requirements: 8.5, 9.5_
  - [ ] 15.2 Create main layout with Tailwind CSS
    - Design header with app title and BackendSelector
    - Create tabbed or sectioned layout for Encoder, Decoder, and Share panels
    - Add footer with device session ID
    - Implement responsive design
    - _Requirements: 6.1, 6.2, 6.6_
  - [ ] 15.3 Wire up all components
    - Integrate EncoderPanel with share functionality
    - Integrate DecoderPanel with receive functionality
    - Connect DistortionPanel to encoder output
    - Ensure proper data flow between components
    - _Requirements: 6.3, 6.4_

- [ ] 16. Add error handling and user feedback
  - [ ] 16.1 Create ErrorBoundary component
    - Catch React errors and display fallback UI
    - Log errors for debugging
    - _Requirements: 6.4_
  - [ ] 16.2 Implement toast notification system
    - Add toast library (react-hot-toast or similar)
    - Show success messages for completed operations
    - Show error messages with retry options
    - Show info messages for status updates
    - _Requirements: 6.3, 6.4_
  - [ ] 16.3 Add loading states throughout UI
    - Show spinners during API calls
    - Disable buttons during processing
    - Show progress indicators for long operations
    - _Requirements: 3.2, 4.5_

- [ ] 17. Implement file cleanup and resource management
  - [ ] 17.1 Add backend file cleanup service
    - Create cleanup task to remove files older than 1 hour
    - Implement automatic cleanup on server startup
    - Add cleanup on session expiration
    - _Requirements: 8.4_
  - [ ] 17.2 Add frontend memory management
    - Revoke object URLs when components unmount
    - Clear audio blobs when no longer needed
    - Implement cleanup on page unload
    - _Requirements: 7.3_

- [ ] 18. Create configuration and documentation files
  - [ ] 18.1 Create backend configuration
    - Create config.py with environment variables
    - Create requirements.txt with all dependencies
    - Create README.md with setup instructions
    - Add example .env file
    - _Requirements: 10.5_
  - [ ] 18.2 Create frontend configuration
    - Create .env.example with API URL
    - Update package.json with scripts
    - Create README.md with development instructions
    - _Requirements: 10.5_
  - [ ] 18.3 Create root README
    - Document project overview
    - Add setup instructions for both frontend and backend
    - Include usage examples
    - Add screenshots or demo links
    - _Requirements: 6.1, 6.5_

- [x] 19. Implement standalone demo interface




  - [x] 19.1 Create standalone_demo.py CLI script


    - Set up argparse for command-line argument parsing
    - Define 'encode' and 'decode' subcommands
    - Add arguments: --input, --output, --message, --format, --model, --play
    - Implement argument validation
    - _Requirements: 11.1, 11.2, 11.3, 11.9_
  - [x] 19.2 Implement standalone encode workflow


    - Import and use AudioProcessor to load input audio
    - Import and use MessageConverter to convert message based on format
    - Import and use SilentCipherService to encode watermark
    - Save watermarked audio to output path
    - Display output file path and SDR value to console
    - _Requirements: 11.2, 11.3, 11.4, 11.5, 11.10_
  - [x] 19.3 Implement standalone decode workflow


    - Import and use AudioProcessor to load input audio
    - Import and use SilentCipherService to decode watermark
    - Display decoded message and confidence scores to console
    - Format output for readability
    - _Requirements: 11.6, 11.7, 11.10_
  - [x] 19.4 Add optional audio playback feature


    - Implement play_audio() method using pygame or similar
    - Add --play flag to trigger playback after encoding
    - Handle playback errors gracefully
    - _Requirements: 11.8_
  - [x] 19.5 Create optional Tkinter GUI interface


    - Create simple GUI with file selection dialogs
    - Add message input fields
    - Add encode/decode buttons
    - Display results in GUI
    - _Requirements: 11.1, 11.9_
  - [x] 19.6 Write tests for standalone interface


    - Test CLI argument parsing
    - Test encode workflow with sample audio
    - Test decode workflow with watermarked audio
    - Test all message formats (numeric, text, binary)
    - Test both model types (16k, 44.1k)
    - _Requirements: 11.2, 11.3, 11.4, 11.6, 11.7_
  - [x] 19.7 Create documentation for standalone interface


    - Add usage examples to README
    - Document all CLI arguments and options
    - Provide sample commands for common use cases
    - Document dependencies and setup
    - _Requirements: 11.9_

## Research Framework Implementation - PRIORITY ORDER

### PHASE 1: IDEAW + FrEIA Implementation (IMMEDIATE PRIORITY)

- [x] 20. Set up IDEAW in Google Colab
  - [x] 20.1 Prepare Google Colab environment
    - ✅ Created Google Drive folder structure for IDEAW training
    - ✅ Set up Colab notebook with GPU support (T4)
    - ✅ Installed IDEAW dependencies (PyTorch 2.x, librosa, scipy, pydub, etc.)
    - ✅ Fixed PyTorch 2.x compatibility issues (STFT/iSTFT, metrics, attackLayer)
    - ✅ Verified IDEAW repository structure and imports
    - _Requirements: 14.1_
  
  - [x] 20.2 Test IDEAW baseline in Colab
    - ✅ Reviewed IDEAW's embed_extract.py workflow
    - ✅ Loaded IDEAW model successfully (8.4M parameters)
    - ✅ Tested model initialization and GPU allocation
    - ✅ Documented IDEAW's input/output formats (16kHz, 1-second chunks, 16-bit message, 10-bit location code)
    - ✅ Verified model structure and checkpoint loading
    - _Requirements: 14.1, 14.10_
  
  - [x] 20.3 Prepare training data
    - ✅ Processed 50 audio files into 532 training segments
    - ✅ Resampled audio to 16kHz and split into 1-second segments
    - ✅ Created pickle file (32.5 MB) for training
    - ✅ Set up checkpoint and results directories on Google Drive
    - _Requirements: 14.1_
  
  - [x] 20.4 Train IDEAW model in Colab
    - ✅ Configured training with batch size 1 (memory constraints)
    - ✅ Successfully trained for 500+ iterations
    - ✅ Reached Stage II (robustness training with attacks)
    - ✅ Saved checkpoints to Google Drive
    - ✅ Verified checkpoint can be loaded
    - ✅ Model shows learning progress (accuracy improving from ~45% to ~60%)
    - _Requirements: 14.2, 14.9_
  
  - [ ] 20.5 Create IDEAW service wrapper (Future work)
    - Create backend/services/ideaw_service.py
    - Implement IDEAWService class wrapping IDEAW model
    - Implement load_model(config_path, checkpoint_path) method
    - Implement encode_audio(audio, message, location_code) method
    - Implement decode_audio(audio) method returning (message, location_code, confidence)
    - Handle chunk-based processing (16000 samples + 8000 intervals)
    - Add SNR calculation and timing metrics
    - _Requirements: 14.2, 14.4, 14.8_

- [ ] 21. Implement FrEIA-based IDEAW extensions (NOVELTY)
  - [x] 21.1 Set up FrEIA framework


    - Install FrEIA: pip install FrEIA
    - Install additional dependencies (PyTorch, etc.)
    - Study FrEIA documentation and examples
    - Review FrEIA coupling block types (affine, spline, GLOWCouplingBlock, etc.)
    - _Requirements: 14.3, 14.7_
  
  - [ ] 21.2 Analyze IDEAW's InnBlock architecture
    - Study research/IDEAW/models/innBlock.py implementation
    - Understand the coupling block structure (ρ, η, φ, ψ networks)
    - Analyze DenseBlock implementation in research/IDEAW/models/dense.py
    - Document current InnBlock forward/reverse operations
    - Identify components suitable for FrEIA replacement
    - _Requirements: 14.3_
  
  - [ ] 21.3 Create FrEIA-based InnBlock replacement
    - Create research/ideaw_freia/freia_innblock.py
    - Implement FrEIA-based coupling blocks matching IDEAW's interface
    - Test different FrEIA coupling types (affine, spline, rational quadratic)
    - Ensure forward/reverse operations match IDEAW's behavior
    - Verify gradient flow and invertibility
    - _Requirements: 14.3, 14.4, 14.7_
  
  - [ ] 21.4 Create FrEIA-based MIHNET variants
    - Create research/ideaw_freia/freia_mihnet.py
    - Implement Mihnet_s1 using FrEIA blocks
    - Implement Mihnet_s2 using FrEIA blocks
    - Make INN block count configurable (num_inn_1, num_inn_2)
    - Make coupling block type configurable (affine, spline, etc.)
    - _Requirements: 14.3, 14.4, 14.5_
  
  - [ ] 21.5 Integrate FrEIA-MIHNET with IDEAW
    - Create research/ideaw_freia/ideaw_freia.py
    - Replace IDEAW's MIHNET with FrEIA-based version
    - Maintain compatibility with IDEAW's training pipeline
    - Keep attack layer, discriminator, and balance block unchanged
    - Test forward/backward pass with FrEIA blocks
    - _Requirements: 14.4, 14.7_
  
  - [ ] 21.6 Set up training pipeline for FrEIA-IDEAW
    - Adapt IDEAW's training script for FrEIA variant
    - Configure training parameters (learning rates, batch size, etc.)
    - Implement two-stage training (stage I and stage II)
    - Add checkpointing and model saving
    - Set up Google Colab notebook for training
    - _Requirements: 14.5, 14.6, 14.10_
  
  - [ ] 21.7 Train baseline FrEIA-IDEAW model
    - Prepare training dataset (audio files at 16kHz)
    - Train FrEIA-IDEAW with default configuration
    - Monitor training metrics (loss, SNR, accuracy)
    - Save trained model checkpoints
    - Evaluate baseline performance
    - _Requirements: 14.5, 14.6_
  
  - [ ] 21.8 Conduct ablation studies (NOVELTY CONTRIBUTION)
    - **Experiment 1**: Vary number of INN blocks (4, 6, 8, 10, 12)
    - **Experiment 2**: Compare coupling types (affine vs spline vs rational quadratic)
    - **Experiment 3**: Modify dense block architectures (layers, hidden units)
    - **Experiment 4**: Test different activation functions
    - **Experiment 5**: Experiment with normalization layers (ActNorm, BatchNorm)
    - Document performance of each variant
    - _Requirements: 14.3, 14.7_
  
  - [ ] 21.9 Create research documentation for FrEIA-IDEAW
    - Document architectural modifications and rationale
    - Create comparison tables (original IDEAW vs FrEIA variants)
    - Generate architecture visualization diagrams
    - Write methodology section for paper
    - Document novel contributions clearly
    - _Requirements: 14.7, 14.9_

### PHASE 2: Attack Suite Implementation

- [ ] 22. Implement comprehensive attack suite

- [ ] 22. Implement comprehensive attack suite
  - [ ] 22.1 Set up attack suite infrastructure
    - Create backend/research/attack_suite.py
    - Design AttackSuite class with configurable parameters
    - Implement attack result logging and tracking
    - Create attack configuration system (YAML or JSON)
    - _Requirements: 15.9, 15.10_
  
  - [ ] 22.2 Implement compression attacks
    - Add MP3 compression using pydub or ffmpeg (64, 128, 192, 320 kbps)
    - Implement AAC compression at multiple bitrates
    - Implement Opus compression at multiple bitrates
    - Create compression parameter sweep functionality
    - Test compression attacks on sample audio
    - _Requirements: 15.1_
  
  - [ ] 22.3 Implement noise attacks
    - Add Gaussian noise at various SNR levels (5, 10, 15, 20, 25, 30 dB)
    - Implement environmental noise addition (use noise samples)
    - Add colored noise generation (pink, brown, blue noise)
    - Create noise intensity parameter sweeps
    - Test noise attacks on watermarked audio
    - _Requirements: 15.2_
  
  - [ ] 22.4 Implement filtering attacks
    - Add low-pass filter with configurable cutoff frequencies
    - Implement high-pass filter with configurable cutoff frequencies
    - Add band-pass filter with configurable frequency ranges
    - Use scipy.signal for filter implementations
    - Test filtering attacks on watermarked audio
    - _Requirements: 15.3_
  
  - [ ] 22.5 Implement temporal attacks
    - Add time-scale modification (speed changes 0.8x to 1.2x)
    - Implement sample rate conversion (8kHz, 16kHz, 22kHz, 44.1kHz, 48kHz)
    - Add pitch-preserving time stretching using librosa
    - Test temporal attacks on watermarked audio
    - _Requirements: 15.4, 15.5_
  
  - [ ] 22.6 Implement re-recording simulation
    - Download or create room impulse response (RIR) database
    - Implement RIR convolution for acoustic simulation
    - Add microphone frequency response simulation
    - Implement full playback-capture chain simulation
    - Test re-recording attacks on watermarked audio
    - _Requirements: 15.6_
  
  - [ ] 22.7 Implement adversarial attacks (optional - advanced)
    - Create gradient-based watermark removal using PyTorch
    - Implement overwriting attacks with conflicting watermarks
    - Add adversarial optimization for watermark destruction
    - Test adversarial attacks on watermarked audio
    - _Requirements: 15.7, 15.8_
  
  - [ ] 22.8 Create attack evaluation workflow
    - Implement batch attack processing for multiple audio files
    - Create systematic attack evaluation pipeline
    - Add detailed attack logging (parameters, results, timing)
    - Generate attack result summaries and statistics
    - _Requirements: 15.11, 15.12_

### PHASE 3: Evaluation Metrics and Analysis

- [ ] 23. Implement evaluation metrics system
  - [ ] 23.1 Set up evaluation metrics infrastructure
    - Create backend/research/evaluation_metrics.py
    - Design EvaluationMetrics class
    - Implement result storage and tracking system
    - Create metrics configuration system
    - _Requirements: 16.11_
  
  - [ ] 23.2 Implement robustness metrics
    - Create Bit Error Rate (BER) calculation
    - Implement detection rate (true positive rate) calculation
    - Add false positive rate calculation
    - Create accuracy metric for watermark recovery
    - Implement ROC curve generation and AUC calculation
    - _Requirements: 16.1, 16.3_
  
  - [ ] 23.3 Implement imperceptibility metrics
    - Add SNR (Signal-to-Noise Ratio) calculation
    - Implement PESQ score evaluation using pesq library
    - Add STOI score calculation using pystoi library
    - Create spectral distortion analysis
    - Implement perceptual quality metrics
    - _Requirements: 16.2_
  
  - [ ] 23.4 Implement performance metrics
    - Add encoding latency measurement (time per second of audio)
    - Add decoding latency measurement
    - Implement model size analysis (parameters, memory)
    - Add throughput measurement for batch processing
    - Track GPU/CPU usage during processing
    - _Requirements: 16.4, 16.5_
  
  - [ ] 23.5 Implement statistical analysis
    - Add t-test for comparing two methods
    - Implement Mann-Whitney U test for non-parametric comparison
    - Create ANOVA for multi-group comparisons
    - Implement confidence interval calculation using bootstrap
    - Add correlation analysis between metrics
    - _Requirements: 16.6, 16.7, 16.8_
  
  - [ ] 23.6 Create visualization and reporting
    - Generate robustness curves (BER vs attack intensity)
    - Create comparative bar charts for different methods
    - Generate ROC curves for detection performance
    - Create heatmaps for attack resistance analysis
    - Implement publication-quality plot generation (matplotlib)
    - _Requirements: 16.9, 16.10_
  
  - [ ] 23.7 Create evaluation reporting system
    - Generate comparative performance tables
    - Export results in LaTeX table format
    - Create CSV/JSON exports for further analysis
    - Generate comprehensive evaluation reports (PDF/HTML)
    - Maintain detailed experimental logs for reproducibility
    - _Requirements: 16.10, 16.11, 16.12_

- [ ] 24. Run comprehensive evaluation experiments
  - [ ] 24.1 Evaluate IDEAW baseline (original architecture)
    - Test IDEAW on clean audio (no attacks)
    - Measure imperceptibility metrics (SNR, PESQ, STOI)
    - Measure performance metrics (latency, throughput)
    - Document baseline results
    - _Requirements: 14.8, 16.1, 16.2, 16.4_
  
  - [ ] 24.2 Evaluate FrEIA-IDEAW variants
    - Test each FrEIA variant on clean audio
    - Compare imperceptibility across variants
    - Compare performance across variants
    - Identify best-performing architecture
    - _Requirements: 14.7, 16.1, 16.2, 16.4_
  
  - [ ] 24.3 Evaluate robustness against attacks
    - Run all attacks on IDEAW baseline
    - Run all attacks on best FrEIA-IDEAW variant
    - Calculate BER for each attack type and intensity
    - Generate robustness curves
    - Compare robustness between variants
    - _Requirements: 15.1-15.8, 16.1, 16.3_
  
  - [ ] 24.4 Statistical analysis and comparison
    - Perform statistical tests comparing variants
    - Calculate confidence intervals for all metrics
    - Identify statistically significant improvements
    - Generate comparison tables and plots
    - _Requirements: 16.6, 16.7, 16.8_
  
  - [ ] 24.5 Generate research results package
    - Compile all experimental results
    - Generate publication-ready figures and tables
    - Create supplementary materials
    - Write results section for paper
    - Prepare reproducibility package
    - _Requirements: 16.10, 16.11, 16.12, 18.1-18.10_

### PHASE 4: Additional Methods and Ensemble (Optional - After Core Research)

- [ ] 25. Implement additional watermarking methods (OPTIONAL)
  - [ ] 25.1 Implement WavMark integration
    - Install WavMark via pip
    - Create WavMarkService wrapper
    - Test WavMark encoding/decoding
    - Add to evaluation framework
    - _Requirements: 12.1_
  
  - [ ] 25.2 Implement Classical DSP baselines
    - Implement echo hiding method
    - Implement spread spectrum method
    - Test DSP methods
    - Add to evaluation framework
    - _Requirements: 12.3_

- [ ] 26. Implement ensemble learning (OPTIONAL)
  - [ ] 26.1 Create ensemble framework
    - Design ensemble architecture
    - Implement fusion strategies
    - Test ensemble approaches
    - _Requirements: 13.1-13.10_



## Demo Application Integration and Testing

- [ ] 29. Final demo application integration and testing
  - [ ] 29.1 Test complete encoding workflow
    - Upload audio, enter message, encode, play result
    - Verify SDR display and download functionality
    - Test with different audio formats and sample rates
    - _Requirements: 1.1, 2.1, 3.1, 3.3, 3.4, 3.5_
  - [ ] 29.2 Test complete decoding workflow
    - Upload watermarked audio and decode
    - Verify message display and confidence scores
    - Test with non-watermarked audio
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  - [ ] 29.3 Test distortion workflow
    - Enable distortion testing
    - Apply various distortions
    - Decode distorted audio
    - Verify robustness results
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_
  - [ ] 29.4 Test cross-device sharing
    - Share audio from one device
    - Receive on another device
    - Decode received audio
    - Verify audio integrity
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
  - [ ] 29.5 Test backend provider switching
    - Switch between providers (when multiple available)
    - Verify UI updates correctly
    - Test encoding/decoding with different providers
    - _Requirements: 9.1, 9.4, 9.5_
  - [ ] 29.6 Test standalone demo interface
    - Test CLI encoding with all message formats
    - Test CLI decoding with watermarked audio
    - Verify output matches web application results
    - Test error handling and validation
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.6, 11.7, 11.9_
  - [ ] 29.7 Perform end-to-end testing
    - Test all workflows in sequence
    - Test error scenarios
    - Test with various audio files
    - Verify performance and responsiveness
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_
