# Audio Watermarking Backend

Backend service for the Audio Watermarking Demo application, providing REST API endpoints and standalone CLI/GUI tools for audio watermarking using Sony's SilentCipher technology.

## Features

- 🎵 **Audio Watermarking API**: REST endpoints for encoding and decoding watermarks
- 🖥️ **Standalone CLI Tool**: Command-line interface for quick testing without the web app
- 🖼️ **Optional GUI Tool**: Tkinter-based graphical interface for desktop use
- 🔧 **Audio Processing**: Support for WAV files at 16kHz and 44.1kHz sample rates
- 📝 **Multiple Message Formats**: Numeric arrays, text strings, and binary strings
- 🎚️ **Distortion Testing**: Apply noise, compression, and resampling to test robustness

## Installation

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install SilentCipher

```bash
pip install silentcipher
```

## Standalone Demo Interface

The standalone demo interface provides a quick way to test audio watermarking functionality directly from the command line or through a simple GUI, without running the full web application.

### CLI Usage

#### Basic Commands

**Encode a watermark:**
```bash
python standalone_demo.py encode --input audio.wav --output watermarked.wav --message "Hello" --format text
```

**Decode a watermark:**
```bash
python standalone_demo.py decode --input watermarked.wav
```

#### Message Formats

**1. Text Format (default)**
```bash
python standalone_demo.py encode \
  --input audio.wav \
  --output watermarked.wav \
  --message "Hello" \
  --format text
```

**2. Numeric Format (5 integers, 0-255)**
```bash
python standalone_demo.py encode \
  --input audio.wav \
  --output watermarked.wav \
  --message "100,150,200,50,75" \
  --format numeric
```

**3. Binary Format (40-bit string)**
```bash
python standalone_demo.py encode \
  --input audio.wav \
  --output watermarked.wav \
  --message "0101010101010101010101010101010101010101" \
  --format binary
```

#### Advanced Options

**Specify model type:**
```bash
python standalone_demo.py encode \
  --input audio.wav \
  --output watermarked.wav \
  --message "Test" \
  --model 44.1k
```

**Play audio after encoding (requires pygame):**
```bash
python standalone_demo.py encode \
  --input audio.wav \
  --output watermarked.wav \
  --message "Test" \
  --play
```

**Use phase shift decoding for robustness:**
```bash
python standalone_demo.py decode \
  --input watermarked.wav \
  --phase-shift
```

#### Complete Examples

**Example 1: Encode and decode a text message**
```bash
# Encode
python standalone_demo.py encode \
  --input original.wav \
  --output watermarked.wav \
  --message "SecretMessage" \
  --format text

# Decode
python standalone_demo.py decode \
  --input watermarked.wav
```

**Example 2: Encode with numeric array**
```bash
python standalone_demo.py encode \
  --input audio.wav \
  --output watermarked.wav \
  --message "123,234,111,222,11" \
  --format numeric
```

**Example 3: Encode with binary string**
```bash
python standalone_demo.py encode \
  --input audio.wav \
  --output watermarked.wav \
  --message "1010101010101010101010101010101010101010" \
  --format binary
```

### GUI Usage

For users who prefer a graphical interface, a Tkinter-based GUI is available:

```bash
python standalone_demo_gui.py
```

The GUI provides:
- File selection dialogs for input/output audio
- Tabbed interface for encoding and decoding
- Message format selection (text, numeric, binary)
- Real-time progress updates
- Results display with all message formats

### Command-Line Arguments Reference

#### Encode Command

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` | Yes | - | Path to input audio file (WAV format) |
| `--output` | Yes | - | Path to output watermarked audio file |
| `--message` | Yes | - | Message to embed (format depends on --format) |
| `--format` | No | `text` | Message format: `numeric`, `text`, or `binary` |
| `--model` | No | `44.1k` | Model type: `16k` or `44.1k` |
| `--play` | No | `False` | Play encoded audio after encoding |

#### Decode Command

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` | Yes | - | Path to watermarked audio file |
| `--model` | No | `44.1k` | Model type: `16k` or `44.1k` |
| `--phase-shift` | No | `False` | Use phase shift decoding (slower but more robust) |

### Message Format Specifications

#### Numeric Format
- Exactly 5 integers
- Each integer must be between 0 and 255
- Comma-separated values
- Example: `100,150,200,50,75`

#### Text Format
- Any UTF-8 text string
- Will be converted to 5 bytes (truncated or padded)
- Example: `Hello`, `Test123`, `Secret`

#### Binary Format
- Exactly 40 bits (characters '0' and '1')
- Can include spaces or underscores for readability (will be ignored)
- Example: `0101010101010101010101010101010101010101`
- Example with formatting: `01010101 01010101 01010101 01010101 01010101`

### Audio File Requirements

- **Format**: WAV files only
- **Sample Rates**: 16kHz or 44.1kHz (44.1kHz recommended)
- **Duration**: Minimum 3-5 seconds for reliable watermarking
- **Channels**: Mono or stereo (will use first channel for watermarking)
- **File Size**: Maximum 50MB

### Output Information

#### Encoding Output
```
============================================================
Audio Watermarking - Encode
============================================================

[1/5] Loading input audio: audio.wav
  ✓ Loaded successfully
    - Duration: 5.23 seconds
    - Sample rate: 44100 Hz
    - Channels: 1

[2/5] Converting message to numeric format
  Format: text
  Input: Hello
  ✓ Converted to numeric: [72, 101, 108, 108, 111]

[3/5] Encoding watermark using SilentCipher (44.1k model)
  This may take a moment...
  ✓ Encoding successful
    - SDR: 28.45 dB

[4/5] Saving watermarked audio: watermarked.wav
  ✓ Saved successfully

[5/5] Playback skipped (use --play to enable)

============================================================
Encoding Complete!
============================================================
Output file: watermarked.wav
SDR value: 28.45 dB
Message (numeric): [72, 101, 108, 108, 111]
Message (text): Hello
============================================================
```

#### Decoding Output
```
============================================================
Audio Watermarking - Decode
============================================================

[1/3] Loading input audio: watermarked.wav
  ✓ Loaded successfully
    - Duration: 5.23 seconds
    - Sample rate: 44100 Hz
    - Channels: 1

[2/3] Decoding watermark using SilentCipher (44.1k model)
  This may take a moment...
  ✓ Watermark detected successfully

[3/3] Formatting decoded message

============================================================
Decoding Complete - Watermark Detected!
============================================================

Decoded Message:
  Numeric:  [72, 101, 108, 108, 111]
  Text:     'Hello'
  Binary:   0100100001100101011011000110110001101111

Confidence Score: 0.9876
Confidence Level: Very High
============================================================
```

## REST API Usage

### Start the Flask Server

```bash
python app.py
```

The server will start on `http://localhost:5000` by default.

### API Endpoints

#### POST /api/encode
Encode a watermark into an audio file.

**Request:**
- `audio_file`: Audio file (multipart/form-data)
- `message`: JSON object with message payload

**Response:**
```json
{
  "success": true,
  "encoded_audio": "<base64_encoded_audio>",
  "sdr": 28.45,
  "message": [72, 101, 108, 108, 111]
}
```

#### POST /api/decode
Decode a watermark from an audio file.

**Request:**
- `audio_file`: Watermarked audio file (multipart/form-data)

**Response:**
```json
{
  "success": true,
  "status": "detected",
  "message": [72, 101, 108, 108, 111],
  "confidence": 0.9876
}
```

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run tests for standalone interface:

```bash
pytest tests/test_standalone_demo.py -v
```

Run specific test:

```bash
pytest tests/test_standalone_demo.py::TestEncodeWorkflow::test_encode_with_text_message -v
```

## Troubleshooting

### SilentCipher Not Found

If you get an error about SilentCipher not being installed:

```bash
pip install silentcipher
```

### Pygame Not Found (for --play option)

If you want to use the `--play` option:

```bash
pip install pygame
```

### Audio File Format Errors

Ensure your audio files are:
- WAV format (not MP3, FLAC, etc.)
- 16kHz or 44.1kHz sample rate
- Not corrupted or truncated

### Low SDR Values

If SDR values are low (< 15 dB):
- Check audio quality and duration
- Ensure audio is not too short (minimum 3-5 seconds)
- Try using 44.1kHz sample rate instead of 16kHz

### Watermark Not Detected

If decoding fails to detect a watermark:
- Verify the audio was actually watermarked
- Check if the audio was heavily processed or compressed
- Try using `--phase-shift` flag for more robust decoding
- Ensure the same model type is used for encoding and decoding

## Project Structure

```
backend/
├── services/
│   ├── audio_processor.py       # Audio loading, saving, and processing
│   ├── silentcipher_service.py  # SilentCipher integration
│   └── __init__.py
├── utils/
│   ├── message_converter.py     # Message format conversion
│   └── __init__.py
├── tests/
│   ├── test_audio_processor.py
│   ├── test_message_converter.py
│   ├── test_silentcipher_service.py
│   ├── test_standalone_demo.py
│   └── __init__.py
├── standalone_demo.py           # CLI interface
├── standalone_demo_gui.py       # GUI interface
├── app.py                       # Flask API server
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Dependencies

Core dependencies:
- `flask` - Web framework
- `flask-cors` - CORS support
- `silentcipher` - Audio watermarking
- `librosa` - Audio processing
- `soundfile` - Audio I/O
- `numpy` - Numerical operations

Optional dependencies:
- `pygame` - Audio playback (for --play option)
- `pytest` - Testing framework

See `requirements.txt` for complete list.

## Contributing

This project follows a spec-driven development approach. See the main project README and `.kiro/specs/` directory for specifications and implementation tasks.

## License

MIT

## Acknowledgments

- [Sony SilentCipher](https://github.com/sony/silentcipher) - Deep audio watermarking technology
- [Librosa](https://librosa.org/) - Audio analysis library
