# Audio Watermarking Demo

A full-stack web application showcasing Sony's SilentCipher audio watermarking technology. This demo allows users to embed imperceptible watermarks in audio files, decode them, test robustness through distortions, and share watermarked audio across devices.

## Features

- 🎵 **Audio Watermarking**: Embed custom messages (numeric, text, or binary) into audio files
- 🔍 **Watermark Detection**: Decode and verify embedded watermarks with confidence scores
- 🎚️ **Distortion Testing**: Test watermark robustness against noise, compression, and resampling
- 📱 **Cross-Device Sharing**: Share watermarked audio between devices in real-time
- 🔌 **Backend Abstraction**: Support for multiple watermarking providers (extensible architecture)
- 🎨 **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- 🖥️ **Standalone Tools**: CLI and GUI interfaces for quick testing without the web app

## Tech Stack

### Frontend
- React 18+ with TypeScript
- Tailwind CSS
- Axios for API communication
- Socket.IO Client for real-time features
- Wavesurfer.js for audio visualization

### Backend
- Flask (Python 3.8+)
- SilentCipher for audio watermarking
- Flask-SocketIO for WebSocket support
- Librosa for audio processing

## Project Structure

```
audio-watermarking-demo/
├── frontend/          # React TypeScript application
├── backend/           # Flask API server
├── .kiro/            # Kiro spec files
│   └── specs/
│       └── audio-watermarking-demo/
│           ├── requirements.md
│           ├── design.md
│           └── tasks.md
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Git

### Quick Start with Standalone CLI

For quick testing without setting up the full web application:

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt
pip install silentcipher

# Encode a watermark
python standalone_demo.py encode --input audio.wav --output watermarked.wav --message "Hello" --format text

# Decode a watermark
python standalone_demo.py decode --input watermarked.wav
```

See [backend/README.md](backend/README.md) for complete standalone interface documentation.

### Full Web Application Setup

Detailed setup instructions will be added as the project is implemented. See `.kiro/specs/audio-watermarking-demo/` for the complete specification.

## Development Status

This project is currently in development following a spec-driven approach. Check the [tasks.md](.kiro/specs/audio-watermarking-demo/tasks.md) file for implementation progress.

## Documentation

### User Documentation
- [Backend & Standalone Tools](backend/README.md) - CLI/GUI usage and API reference

### Developer Documentation
- [Requirements](.kiro/specs/audio-watermarking-demo/requirements.md)
- [Design](.kiro/specs/audio-watermarking-demo/design.md)
- [Implementation Tasks](.kiro/specs/audio-watermarking-demo/tasks.md)

## License

MIT

## Acknowledgments

- [Sony SilentCipher](https://github.com/sony/silentcipher) - Deep audio watermarking technology
