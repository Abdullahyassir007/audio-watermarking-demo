# Requirements Document

## Introduction

This document specifies the requirements for a comprehensive audio watermarking research platform that showcases multiple state-of-the-art watermarking techniques. The platform serves dual purposes: (1) a front-end demo application for interactive watermarking demonstrations, and (2) a research framework for academic evaluation of ensemble watermarking methods, novel INN-based approaches, and comprehensive robustness analysis. The system integrates multiple watermarking libraries including SilentCipher, WavMark, IDEAW, and classical DSP methods to enable comparative studies and ensemble learning approaches.

## Glossary

### Core System Components
- **Demo Application**: The web-based front-end application that provides the user interface for audio watermarking operations
- **Research Framework**: The backend system supporting multiple watermarking methods for academic evaluation and ensemble learning
- **Ensemble Engine**: The component that combines multiple watermarking methods using various fusion strategies
- **Attack Suite**: The comprehensive testing framework that simulates various audio attacks and distortions
- **Evaluation Metrics**: The standardized measurement system for imperceptibility, robustness, and performance analysis

### Watermarking Methods
- **SilentCipher**: Sony's deep learning-based audio watermarking library (primary baseline)
- **WavMark**: ByteDance's robust watermarking method optimized for speech and generative audio
- **IDEAW/DeAR**: Invertible Neural Network-based watermarking methods for re-recording resistance
- **Classical DSP**: Traditional echo hiding and spread spectrum methods for baseline comparison
- **Custom INN**: Novel Invertible Neural Network implementation using FrEIA framework

### Technical Components
- **Watermark Encoder**: Multi-method component that embeds messages using selected watermarking algorithms
- **Watermark Decoder**: Multi-method component that extracts embedded messages from watermarked audio files
- **Message Payload**: Standardized message format supporting various bit capacities across different methods
- **Audio Player**: UI component for playback and waveform visualization
- **Backend Provider**: Abstracted interface for different watermarking service implementations
- **Attack Simulator**: Component that applies systematic distortions for robustness testing

### Research & Evaluation
- **Bit Error Rate (BER)**: Primary metric for payload recovery accuracy
- **Imperceptibility Metrics**: SNR, PESQ, STOI measurements for perceptual quality
- **Detection Metrics**: True/false positive rates for watermark presence detection
- **Performance Metrics**: Latency, runtime, and model size measurements
- **Statistical Analysis**: Significance testing and confidence interval reporting

### System Infrastructure
- **Audio Transfer**: Cross-device sharing mechanism for watermarked audio
- **Device Session**: Unique identifier for device instances
- **User**: Person interacting with the demo application or research framework

## Requirements

### Requirement 0

**User Story:** As a user, I want to navigate through a modern website interface with authentication, so that I can access the watermarking features securely

#### Acceptance Criteria

1. THE Demo Application SHALL provide a navigation bar with links to Home, Encode, Decode, and About pages
2. THE Demo Application SHALL display a responsive navigation menu that adapts to mobile and desktop screen sizes
3. WHEN the User is not authenticated, THE Demo Application SHALL display a Login button in the navigation bar
4. WHEN the User is authenticated, THE Demo Application SHALL display a Logout button in the navigation bar
5. THE Demo Application SHALL provide a login page with email and password input fields
6. WHEN the User submits valid credentials on the login page, THE Demo Application SHALL authenticate the User and redirect to the Encode page
7. THE Demo Application SHALL restrict access to Encode and Decode pages for unauthenticated users
8. WHEN an unauthenticated User attempts to access protected pages, THE Demo Application SHALL redirect to the login page
9. THE Demo Application SHALL provide a Home page with feature highlights and call-to-action buttons
10. THE Demo Application SHALL provide an About page with information about the technology and use cases
11. THE Demo Application SHALL display a footer with links and branding information on all pages
12. THE Demo Application SHALL use gradient backgrounds and modern UI design throughout the interface
13. THE Demo Application SHALL maintain consistent styling with rounded corners, shadows, and smooth transitions
14. THE Demo Application SHALL provide visual feedback for all interactive elements with hover effects and animations

### Requirement 1

**User Story:** As a user, I want to upload an audio file to the demo application, so that I can embed a watermark into it

#### Acceptance Criteria

1. WHEN the User selects an audio file from their device, THE Demo Application SHALL accept WAV format files with 16kHz or 44.1kHz sampling rates
2. WHEN the User uploads an audio file, THE Demo Application SHALL display the file name and duration
3. WHEN the User uploads an audio file, THE Demo Application SHALL provide an Audio Player for previewing the original audio
4. IF the uploaded file format is not supported, THEN THE Demo Application SHALL display an error message indicating supported formats
5. THE Demo Application SHALL limit uploaded file size to 50 megabytes maximum

### Requirement 2

**User Story:** As a user, I want to specify a custom message to embed in the audio, so that I can demonstrate the watermarking capability

#### Acceptance Criteria

1. THE Demo Application SHALL provide three input modes: numeric array mode, text message mode, and binary message mode
2. WHEN the User selects numeric array mode, THE Demo Application SHALL provide an input interface for entering five integer values between 0 and 255
3. WHEN the User selects text message mode, THE Demo Application SHALL convert the text string to a Message Payload format compatible with the Backend Provider
4. WHEN the User selects binary message mode, THE Demo Application SHALL accept a 40-bit binary string and convert it to Message Payload format
5. WHEN the User enters a message value outside the valid range, THE Demo Application SHALL display a validation error
6. THE Demo Application SHALL provide a random message generation option for quick testing
7. WHEN the User submits valid message values, THE Demo Application SHALL store the Message Payload for encoding
8. THE Demo Application SHALL display the entered message values clearly to the User in the selected format

### Requirement 3

**User Story:** As a user, I want to encode a watermark into my audio file, so that I can create a watermarked version

#### Acceptance Criteria

1. WHEN the User initiates encoding with a valid audio file and Message Payload, THE Watermark Encoder SHALL embed the watermark using SilentCipher
2. WHILE encoding is in progress, THE Demo Application SHALL display a loading indicator
3. WHEN encoding completes successfully, THE Demo Application SHALL provide an Audio Player for the watermarked audio
4. WHEN encoding completes successfully, THE Demo Application SHALL display the Signal-to-Distortion Ratio (SDR) value in decibels
5. WHEN encoding completes successfully, THE Demo Application SHALL provide a download option for the watermarked audio file

### Requirement 4

**User Story:** As a user, I want to decode a watermark from an audio file, so that I can verify the embedded message

#### Acceptance Criteria

1. WHEN the User uploads a watermarked audio file for decoding, THE Watermark Decoder SHALL extract the embedded Message Payload
2. WHEN decoding completes successfully, THE Demo Application SHALL display the decoded message values
3. WHEN decoding completes successfully, THE Demo Application SHALL display confidence scores for the decoded message
4. IF no watermark is detected, THEN THE Demo Application SHALL display a message indicating no watermark was found
5. WHILE decoding is in progress, THE Demo Application SHALL display a loading indicator

### Requirement 5

**User Story:** As a user, I want to optionally apply distortions to watermarked audio, so that I can test the robustness of the watermark

#### Acceptance Criteria

1. THE Demo Application SHALL provide an optional distortion testing mode that the User can enable
2. WHERE the User enables distortion testing and has a watermarked audio file, THE Distortion Module SHALL provide options for noise addition, compression, and resampling
3. WHEN the User applies a distortion, THE Demo Application SHALL generate a distorted version of the audio
4. WHEN distortion is applied, THE Demo Application SHALL provide an Audio Player for the distorted audio
5. WHEN the User decodes a distorted audio file, THE Watermark Decoder SHALL attempt to extract the watermark
6. THE Demo Application SHALL allow the User to compare detection results between original watermarked and distorted audio
7. WHEN distortion testing is disabled, THE Demo Application SHALL not apply any distortions to the audio

### Requirement 6

**User Story:** As a user, I want an intuitive,modern and responsive interface, so that I can easily navigate and use the demo application

#### Acceptance Criteria

1. THE Demo Application SHALL provide a clean, modern user interface with clear visual hierarchy
2. THE Demo Application SHALL organize features into logical sections for encoding, decoding, and distortion testing
3. WHEN the User performs any action, THE Demo Application SHALL provide immediate visual feedback
4. THE Demo Application SHALL display error messages in a user-friendly format with actionable guidance
5. THE Demo Application SHALL be responsive and functional on desktop browsers with minimum 1280x720 resolution

### Requirement 7

**User Story:** As a user, I want to compare original and watermarked audio side-by-side, so that I can verify the imperceptibility of the watermark

#### Acceptance Criteria

1. WHEN encoding completes, THE Demo Application SHALL display both original and watermarked audio players simultaneously
2. THE Demo Application SHALL provide waveform visualizations for both original and watermarked audio
3. THE Demo Application SHALL allow the User to play original and watermarked audio independently
4. THE Demo Application SHALL display the SDR metric to quantify the imperceptibility
5. THE Demo Application SHALL provide a visual indication that the watermark is imperceptible to human hearing

### Requirement 8

**User Story:** As a user, I want to send watermarked audio to another device, so that I can demonstrate cross-device watermark verification

#### Acceptance Criteria

1. WHEN the User has a watermarked audio file, THE Demo Application SHALL provide an option to share the audio to another device
2. THE Demo Application SHALL generate a unique shareable link or QR code for the watermarked audio
3. WHEN another device accesses the shared link, THE Demo Application SHALL allow downloading or direct decoding of the watermarked audio
4. THE Demo Application SHALL maintain the audio quality and watermark integrity during transfer
5. THE Demo Application SHALL display the Device Session identifier to help users identify different devices

### Requirement 9

**User Story:** As a developer, I want the application to support multiple backend providers, so that different watermarking services can be used interchangeably

#### Acceptance Criteria

1. THE Demo Application SHALL provide a backend provider selection interface
2. THE Demo Application SHALL support SilentCipher as the initial Backend Provider
3. THE Demo Application SHALL abstract backend communication through a common interface
4. WHEN the User switches Backend Provider, THE Demo Application SHALL update the available features and options accordingly
5. THE Demo Application SHALL persist the selected Backend Provider preference for the User session

### Requirement 10

**User Story:** As a developer, I want the application to communicate with a backend API, so that watermarking processing can be performed server-side

#### Acceptance Criteria

1. THE Demo Application SHALL send audio files and Message Payload to the Backend API for encoding
2. THE Demo Application SHALL send audio files to the Backend API for decoding
3. WHEN the Backend API returns results, THE Demo Application SHALL parse and display the response data
4. IF the Backend API returns an error, THEN THE Demo Application SHALL display an appropriate error message to the User
5. THE Demo Application SHALL handle network timeouts gracefully with retry options or clear error messages

### Requirement 11

**User Story:** As a developer, I want a simple standalone demo interface that runs within the IDE, so that I can quickly test watermarking functionality without running the full web application

#### Acceptance Criteria

1. THE Demo Application SHALL provide a CLI-based or Tkinter-based standalone demo interface
2. THE standalone demo interface SHALL allow the User to upload an audio file by providing a file path
3. THE standalone demo interface SHALL allow the User to input a message for encoding (numeric array, text, or binary format)
4. WHEN the User initiates encoding through the standalone interface, THE system SHALL embed the watermark and save the watermarked audio file
5. THE standalone demo interface SHALL display the output file path and SDR value after successful encoding
6. THE standalone demo interface SHALL allow the User to upload a watermarked audio file for decoding
7. WHEN the User initiates decoding through the standalone interface, THE system SHALL extract and display the decoded message and confidence scores
8. THE standalone demo interface SHALL provide an option to play the encoded audio (lowest priority feature)
9. THE standalone demo interface SHALL be runnable directly from the IDE terminal without additional setup beyond backend dependencies
10. THE standalone demo interface SHALL use the same backend services and SilentCipher integration as the web application

## Research Framework Requirements

### Requirement 12

**User Story:** As a researcher, I want to integrate multiple state-of-the-art watermarking methods, so that I can perform comparative analysis and ensemble learning

#### Acceptance Criteria

1. THE Research Framework SHALL integrate WavMark (ByteDance) with full API access for encoding and decoding
2. THE Research Framework SHALL integrate IDEAW/DeAR methods using available research code implementations
3. THE Research Framework SHALL implement classical DSP baselines including Echo Hiding and Spread Spectrum methods
4. THE Research Framework SHALL provide a unified interface for all watermarking methods with standardized input/output formats
5. THE Research Framework SHALL support different message payload capacities across methods (40-bit for SilentCipher, method-specific for others)
6. THE Research Framework SHALL maintain method-specific configuration parameters and optimization settings
7. THE Research Framework SHALL provide method selection and combination interfaces for ensemble approaches
8. THE Research Framework SHALL log all method-specific performance metrics and execution times
9. THE Research Framework SHALL handle method-specific preprocessing and postprocessing requirements
10. THE Research Framework SHALL provide fallback mechanisms when specific methods fail or are unavailable

### Requirement 13

**User Story:** As a researcher, I want to implement ensemble learning strategies, so that I can improve watermarking robustness through method combination

#### Acceptance Criteria

1. THE Ensemble Engine SHALL implement majority voting fusion for multiple watermarking methods
2. THE Ensemble Engine SHALL implement confidence-weighted fusion using method-specific confidence scores
3. THE Ensemble Engine SHALL implement adaptive method selection based on audio characteristics
4. THE Ensemble Engine SHALL support parallel encoding with multiple methods on the same audio
5. THE Ensemble Engine SHALL support sequential encoding where one method's output feeds into another
6. THE Ensemble Engine SHALL implement consensus decoding that requires agreement across multiple methods
7. THE Ensemble Engine SHALL provide ensemble confidence scoring that combines individual method confidences
8. THE Ensemble Engine SHALL support dynamic method weighting based on historical performance
9. THE Ensemble Engine SHALL log ensemble decision processes and individual method contributions
10. THE Ensemble Engine SHALL provide ensemble performance metrics compared to individual methods

### Requirement 14

**User Story:** As a researcher, I want to adapt and extend the IDEAW INN-based watermarking method, so that I can contribute original research to the field

#### Acceptance Criteria

1. THE Research Framework SHALL integrate the IDEAW repository as a base INN implementation
2. THE IDEAW Integration SHALL use the existing dual-embedding architecture (message + location code)
3. THE Research Framework SHALL support modifying IDEAW's INN blocks using FrEIA framework for experimentation
4. THE IDEAW Integration SHALL maintain the original MIHNET architecture with configurable INN block counts
5. THE Research Framework SHALL support training custom IDEAW variants on new datasets
6. THE IDEAW Integration SHALL provide both pre-trained model usage and custom training capabilities
7. THE Research Framework SHALL enable architecture modifications (coupling layers, dense blocks, attack layers)
8. THE IDEAW Integration SHALL support the dual-embedding workflow (embed_msg, embed_lcode, extract_lcode, extract_msg)
9. THE Research Framework SHALL provide detailed logging of INN architecture parameters and training metrics
10. THE IDEAW Integration SHALL be testable in Google Colab environment with GPU support

### Requirement 15

**User Story:** As a researcher, I want a comprehensive attack suite, so that I can systematically evaluate watermarking robustness

#### Acceptance Criteria

1. THE Attack Suite SHALL implement MP3 compression attacks at multiple bitrates (64, 128, 192, 320 kbps)
2. THE Attack Suite SHALL implement additive noise attacks (Gaussian noise at various SNR levels)
3. THE Attack Suite SHALL implement environmental noise attacks using realistic noise samples
4. THE Attack Suite SHALL implement low-pass filtering attacks with configurable cutoff frequencies
5. THE Attack Suite SHALL implement time-scale modification attacks (speed changes from 0.8x to 1.2x)
6. THE Attack Suite SHALL implement sample rate conversion attacks (8kHz, 16kHz, 22kHz, 44.1kHz, 48kHz)
7. THE Attack Suite SHALL implement re-recording simulation with room impulse responses and microphone characteristics
8. THE Attack Suite SHALL implement adversarial removal attacks using gradient-based optimization
9. THE Attack Suite SHALL implement overwriting attacks that attempt to embed conflicting watermarks
10. THE Attack Suite SHALL provide configurable attack intensity parameters for systematic evaluation
11. THE Attack Suite SHALL support batch processing of multiple attacks on the same audio
12. THE Attack Suite SHALL log detailed attack parameters and resulting audio characteristics

### Requirement 16

**User Story:** As a researcher, I want comprehensive evaluation metrics, so that I can quantify watermarking performance scientifically

#### Acceptance Criteria

1. THE Evaluation System SHALL calculate Bit Error Rate (BER) for all recovered payload bits
2. THE Evaluation System SHALL measure imperceptibility using SNR, PESQ, and STOI metrics
3. THE Evaluation System SHALL calculate detection rates and false positive rates for watermark presence
4. THE Evaluation System SHALL measure encoding and decoding latency for all methods
5. THE Evaluation System SHALL report model sizes and computational requirements
6. THE Evaluation System SHALL perform statistical significance testing (t-tests, ANOVA) on results
7. THE Evaluation System SHALL generate confidence intervals for all reported metrics
8. THE Evaluation System SHALL create comparative performance tables across all methods
9. THE Evaluation System SHALL generate robustness curves showing performance vs attack intensity
10. THE Evaluation System SHALL export results in academic paper-ready formats (LaTeX tables, publication-quality plots)
11. THE Evaluation System SHALL maintain detailed experimental logs for reproducibility
12. THE Evaluation System SHALL support cross-validation and multiple random seed evaluation

### Requirement 17

**User Story:** As a researcher, I want automated experimental workflows, so that I can efficiently conduct large-scale evaluations

#### Acceptance Criteria

1. THE Research Framework SHALL provide automated batch processing for multiple audio files
2. THE Research Framework SHALL support systematic parameter sweeps for all methods
3. THE Research Framework SHALL implement automated cross-validation with configurable fold numbers
4. THE Research Framework SHALL provide progress tracking and estimated completion times for long experiments
5. THE Research Framework SHALL implement checkpointing for resuming interrupted experiments
6. THE Research Framework SHALL generate automated reports with statistical analysis
7. THE Research Framework SHALL support distributed processing across multiple GPUs/machines
8. THE Research Framework SHALL provide experiment configuration files for reproducible research
9. THE Research Framework SHALL implement automated hyperparameter optimization for custom methods
10. THE Research Framework SHALL generate publication-ready figures and tables automatically

### Requirement 18

**User Story:** As a researcher, I want integration with academic tools, so that I can streamline the research publication process

#### Acceptance Criteria

1. THE Research Framework SHALL export experimental data in formats compatible with academic analysis tools (R, MATLAB, Python)
2. THE Research Framework SHALL generate LaTeX-formatted tables for direct inclusion in papers
3. THE Research Framework SHALL create publication-quality plots using matplotlib with academic styling
4. THE Research Framework SHALL provide BibTeX citations for all integrated methods and datasets
5. THE Research Framework SHALL generate reproducibility documentation including environment specifications
6. THE Research Framework SHALL support integration with version control for experiment tracking
7. THE Research Framework SHALL provide templates for academic paper sections (methodology, results)
8. THE Research Framework SHALL generate supplementary material packages for paper submissions
9. THE Research Framework SHALL support integration with academic collaboration platforms
10. THE Research Framework SHALL provide code documentation suitable for academic code sharing
