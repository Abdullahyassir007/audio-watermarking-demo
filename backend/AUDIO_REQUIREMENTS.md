# Audio Requirements for Watermarking

## Issue Summary

The error you encountered: `operands could not be broadcast together with shapes (2965,) (2966,)` occurs when using audio files that don't meet SilentCipher's requirements.

## Root Cause

Your `test_audio` folder contains audio files that are:
- **Too short**: 0.3-1.2 seconds (need ≥3 seconds)
- **Wrong sample rate**: 8000Hz (need 16kHz or 44.1kHz)

## Audio Requirements

### Minimum Requirements
| Requirement | Value | Your Files |
|-------------|-------|------------|
| **Duration** | ≥3 seconds | 0.3-1.2s ❌ |
| **Sample Rate** | 16kHz or 44.1kHz | 8kHz ❌ |
| **Format** | WAV | WAV ✅ |
| **Channels** | Mono or Stereo | Mono ✅ |

### Recommended Specifications
- **Duration**: 5-15 seconds (optimal)
- **Sample Rate**: 44.1kHz (best quality)
- **Bit Depth**: 16-bit or 24-bit
- **Content**: Real speech or music (synthetic tones work but with lower accuracy)

## Solutions

### Option 1: Use Provided Test Audio ✅
We've created a proper test file for you:

```bash
# Already created by create_test_audio.py
python standalone_demo.py encode --input test_audio_demo.wav --output watermarked.wav --message "Hello"
python standalone_demo.py decode --input watermarked.wav
```

### Option 2: Use SilentCipher Example Audio ✅
The best option is to use the example audio from SilentCipher:

```bash
# This file is 15 seconds at 32kHz (will be resampled automatically)
python standalone_demo.py encode --input ../silentcipher/examples/colab/test.wav --output watermarked.wav --message "Hello"
python standalone_demo.py decode --input watermarked.wav
```

### Option 3: Convert Your Audio Files
If you want to use your existing audio files, you need to:

1. **Concatenate multiple files** to reach 3+ seconds
2. **Resample to 16kHz or 44.1kHz**

Example using ffmpeg:
```bash
# Concatenate files
ffmpeg -i "concat:0_george_0.wav|0_george_1.wav|0_george_2.wav|0_george_3.wav|0_george_4.wav|0_george_5.wav" -acodec copy combined.wav

# Resample to 44.1kHz
ffmpeg -i combined.wav -ar 44100 combined_44k.wav
```

Or using Python:
```python
import soundfile as sf
import librosa
import numpy as np

# Load and concatenate multiple files
audio_files = ['0_george_0.wav', '0_george_1.wav', '0_george_2.wav', 
               '0_george_3.wav', '0_george_4.wav', '0_george_5.wav']

combined_audio = []
for file in audio_files:
    audio, sr = librosa.load(f'test_audio/{file}', sr=None)
    combined_audio.append(audio)

# Concatenate
combined = np.concatenate(combined_audio)

# Resample to 44.1kHz
combined_44k = librosa.resample(combined, orig_sr=8000, target_sr=44100)

# Save
sf.write('combined_44k.wav', combined_44k, 44100)
```

## Validation

### Check Your Audio Files
Run the validation script:
```bash
python create_test_audio.py
```

This will:
- Check all files in `test_audio/` directory
- Report which files are suitable
- Create a proper demo file if needed

### Manual Check
```bash
# Check duration and sample rate
python -c "import soundfile as sf; info = sf.info('your_file.wav'); print(f'Duration: {info.duration:.2f}s, Sample rate: {info.samplerate}Hz')"
```

## Error Messages Explained

### "Audio too short"
```
Error: Audio too short (0.30s). SilentCipher requires at least 3 seconds of audio for reliable watermarking.
```
**Solution**: Use longer audio or concatenate multiple files

### "Unsupported sample rate"
```
⚠ Warning: Sample rate is 8000Hz.
SilentCipher works best with 16kHz or 44.1kHz.
Audio will be resampled automatically.
```
**Solution**: Audio will be resampled, but quality may be affected. Better to use proper sample rate from the start.

### "operands could not be broadcast together"
```
Encoding failed: operands could not be broadcast together with shapes (2965,) (2966,)
```
**Solution**: This occurs with very short audio. Use audio ≥3 seconds.

## Best Practices

### For Testing
1. Use `test_audio_demo.wav` (created by our script)
2. Or use `../silentcipher/examples/colab/test.wav`
3. Duration: 5-15 seconds
4. Sample rate: 44.1kHz

### For Production
1. Use real speech or music recordings
2. Duration: 5-30 seconds (longer is better for robustness)
3. Sample rate: 44.1kHz
4. Avoid heavily compressed audio
5. Avoid audio with extreme processing

### For Research
1. Use standard datasets (LibriSpeech, VCTK, etc.)
2. Ensure consistent sample rates
3. Filter out very short utterances (<3s)
4. Document audio characteristics

## GUI Usage

The GUI now includes validation:
1. Select your audio file
2. If unsuitable, you'll see a clear error message
3. The error will explain what's wrong
4. Use one of the recommended test files instead

## CLI Usage

The CLI also validates audio:
```bash
# This will show a clear error
python standalone_demo.py encode --input test_audio/0_george_0.wav --output out.wav --message "Test"

# Output:
# Error: Audio too short (0.30s). SilentCipher requires at least 3 seconds of audio for reliable watermarking.
```

## Summary

**Your audio files are too short and have the wrong sample rate.**

**Quick fix:**
```bash
# Use the demo file we created
python standalone_demo.py encode --input test_audio_demo.wav --output watermarked.wav --message "Hello"
python standalone_demo.py decode --input watermarked.wav
```

**Or use SilentCipher's example:**
```bash
python standalone_demo.py encode --input ../silentcipher/examples/colab/test.wav --output watermarked.wav --message "Hello"
python standalone_demo.py decode --input watermarked.wav
```

Both of these will work perfectly!
