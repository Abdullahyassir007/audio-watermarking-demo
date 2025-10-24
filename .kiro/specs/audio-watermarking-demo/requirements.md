# Requirements Document

## Introduction

This document specifies the requirements for a front-end demo application that showcases audio watermarking capabilities using Sony's SilentCipher library. The application will allow users to upload audio files, embed watermarks with custom messages, apply distortions to test robustness, and decode watermarks from audio files. The demo aims to provide an intuitive interface for demonstrating the imperceptible nature and robustness of deep learning-based audio watermarking.

## Glossary

- **Demo Application**: The web-based front-end application that provides the user interface for audio watermarking operations
- **SilentCipher**: Sony's deep learning-based audio watermarking library that embeds imperceptible messages in audio
- **Watermark Encoder**: The component that embeds a message into an audio file using SilentCipher
- **Watermark Decoder**: The component that extracts embedded messages from watermarked audio files
- **Message Payload**: A 40-bit message represented as five 8-bit integers (0-255) or text string embedded in the audio
- **Audio Player**: The UI component that allows playback of original and watermarked audio
- **Distortion Module**: The optional component that applies audio transformations to test watermark robustness
- **Backend API**: The server-side service that interfaces with watermarking libraries (initially SilentCipher)
- **Backend Provider**: A specific watermarking service implementation (e.g., SilentCipher, future alternatives)
- **Audio Transfer**: The mechanism for sending watermarked audio between devices running the Demo Application
- **Device Session**: A unique identifier for a device instance running the Demo Application
- **User**: Any person interacting with the demo application

## Requirements

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

**User Story:** As a user, I want an intuitive and responsive interface, so that I can easily navigate and use the demo application

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
