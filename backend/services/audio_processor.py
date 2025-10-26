"""
Audio processing service for loading, saving, validating, and manipulating audio files.
"""
import librosa
import soundfile as sf
import numpy as np
from typing import Tuple, Dict, Optional
import os


class AudioProcessor:
    """Handles audio file operations including loading, saving, validation, and distortion."""
    
    SUPPORTED_FORMATS = ['.wav', '.flac']
    SUPPORTED_SAMPLE_RATES = [16000, 44100]
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    def load_audio(self, file_path: str, sr: Optional[int] = None) -> Tuple[np.ndarray, int]:
        """
        Load audio file using librosa.
        
        Args:
            file_path: Path to the audio file
            sr: Target sample rate (None to preserve original)
            
        Returns:
            Tuple of (audio_data, sample_rate)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        try:
            # Load audio with librosa
            audio_data, sample_rate = librosa.load(file_path, sr=sr, mono=False)
            
            # Ensure audio is 2D (channels, samples)
            if audio_data.ndim == 1:
                audio_data = audio_data.reshape(1, -1)
            
            return audio_data, sample_rate
        except Exception as e:
            raise ValueError(f"Failed to load audio file: {str(e)}")
    
    def save_audio(self, audio_data: np.ndarray, sample_rate: int, file_path: str) -> None:
        """
        Save audio data to a WAV file.
        
        Args:
            audio_data: Audio data array (channels, samples) or (samples,)
            sample_rate: Sample rate in Hz
            file_path: Output file path
            
        Raises:
            ValueError: If audio data or sample rate is invalid
        """
        if audio_data is None or len(audio_data) == 0:
            raise ValueError("Audio data is empty")
        
        if sample_rate <= 0:
            raise ValueError(f"Invalid sample rate: {sample_rate}")
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Transpose if needed (soundfile expects samples, channels)
            if audio_data.ndim == 2 and audio_data.shape[0] < audio_data.shape[1]:
                audio_data = audio_data.T
            
            # Save using soundfile
            sf.write(file_path, audio_data, sample_rate)
        except Exception as e:
            raise ValueError(f"Failed to save audio file: {str(e)}")
    
    def validate_format(self, file_path: str) -> Dict[str, any]:
        """
        Validate audio file format and sample rate.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary with validation results:
            {
                'valid': bool,
                'format': str,
                'sample_rate': int,
                'errors': list
            }
        """
        errors = []
        
        # Check file exists
        if not os.path.exists(file_path):
            return {
                'valid': False,
                'format': None,
                'sample_rate': None,
                'errors': ['File does not exist']
            }
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > self.MAX_FILE_SIZE:
            errors.append(f'File size ({file_size} bytes) exceeds maximum ({self.MAX_FILE_SIZE} bytes)')
        
        # Check file extension
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in self.SUPPORTED_FORMATS:
            errors.append(f'Unsupported format: {ext}. Supported formats: {", ".join(self.SUPPORTED_FORMATS)}')
        
        # Try to load and check sample rate
        try:
            info = sf.info(file_path)
            sample_rate = info.samplerate
            
            if sample_rate not in self.SUPPORTED_SAMPLE_RATES:
                errors.append(
                    f'Unsupported sample rate: {sample_rate}Hz. '
                    f'Supported rates: {", ".join(map(str, self.SUPPORTED_SAMPLE_RATES))}Hz'
                )
            
            return {
                'valid': len(errors) == 0,
                'format': ext.lower(),
                'sample_rate': sample_rate,
                'errors': errors
            }
        except Exception as e:
            errors.append(f'Failed to read audio file: {str(e)}')
            return {
                'valid': False,
                'format': ext.lower() if ext else None,
                'sample_rate': None,
                'errors': errors
            }
    
    def get_metadata(self, audio_data: np.ndarray, sample_rate: int) -> Dict[str, any]:
        """
        Extract metadata from audio data.
        
        Args:
            audio_data: Audio data array
            sample_rate: Sample rate in Hz
            
        Returns:
            Dictionary with metadata:
            {
                'duration': float (seconds),
                'sample_rate': int,
                'channels': int,
                'samples': int
            }
        """
        if audio_data.ndim == 1:
            channels = 1
            samples = len(audio_data)
        else:
            channels = audio_data.shape[0]
            samples = audio_data.shape[1]
        
        duration = samples / sample_rate
        
        return {
            'duration': duration,
            'sample_rate': sample_rate,
            'channels': channels,
            'samples': samples
        }
    
    def apply_noise(self, audio_data: np.ndarray, noise_level_db: float = -20.0) -> np.ndarray:
        """
        Add Gaussian noise to audio data.
        
        Args:
            audio_data: Audio data array
            noise_level_db: Noise level in dB relative to signal (negative value)
            
        Returns:
            Audio data with added noise
        """
        # Calculate signal power
        signal_power = np.mean(audio_data ** 2)
        
        # Convert dB to linear scale
        noise_power = signal_power * (10 ** (noise_level_db / 10))
        
        # Generate Gaussian noise
        noise = np.random.normal(0, np.sqrt(noise_power), audio_data.shape)
        
        # Add noise to signal
        noisy_audio = audio_data + noise
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(noisy_audio))
        if max_val > 1.0:
            noisy_audio = noisy_audio / max_val
        
        return noisy_audio
    
    def apply_compression(self, audio_data: np.ndarray, sample_rate: int, bitrate: int = 128) -> np.ndarray:
        """
        Simulate MP3 compression by applying lossy transformations.
        
        This simulates compression artifacts without actually encoding to MP3.
        Uses frequency domain filtering to approximate compression effects.
        
        Args:
            audio_data: Audio data array
            sample_rate: Sample rate in Hz
            bitrate: Target bitrate in kbps (lower = more compression)
            
        Returns:
            Compressed audio data
        """
        # Apply frequency-based compression simulation
        # Lower bitrates remove more high-frequency content
        
        # Determine cutoff frequency based on bitrate
        # Lower bitrate = lower cutoff frequency
        if bitrate <= 64:
            cutoff_freq = 8000
        elif bitrate <= 128:
            cutoff_freq = 12000
        else:
            cutoff_freq = 16000
        
        # Apply low-pass filter to simulate compression
        from scipy import signal
        
        # Design butterworth low-pass filter
        nyquist = sample_rate / 2
        normalized_cutoff = cutoff_freq / nyquist
        
        # Ensure cutoff is valid
        if normalized_cutoff >= 1.0:
            return audio_data
        
        b, a = signal.butter(4, normalized_cutoff, btype='low')
        
        # Apply filter to each channel
        if audio_data.ndim == 1:
            compressed = signal.filtfilt(b, a, audio_data)
        else:
            compressed = np.zeros_like(audio_data)
            for i in range(audio_data.shape[0]):
                compressed[i] = signal.filtfilt(b, a, audio_data[i])
        
        # Add slight quantization noise to simulate lossy encoding
        quantization_noise = np.random.normal(0, 0.001, audio_data.shape)
        compressed = compressed + quantization_noise
        
        # Normalize
        max_val = np.max(np.abs(compressed))
        if max_val > 1.0:
            compressed = compressed / max_val
        
        return compressed
    
    def resample_audio(self, audio_data: np.ndarray, source_rate: int, target_rate: int) -> np.ndarray:
        """
        Resample audio to a different sample rate.
        
        Args:
            audio_data: Audio data array
            source_rate: Original sample rate in Hz
            target_rate: Target sample rate in Hz
            
        Returns:
            Resampled audio data
        """
        if source_rate == target_rate:
            return audio_data
        
        # Use librosa for resampling
        if audio_data.ndim == 1:
            resampled = librosa.resample(audio_data, orig_sr=source_rate, target_sr=target_rate)
        else:
            resampled = np.zeros((audio_data.shape[0], 
                                 int(audio_data.shape[1] * target_rate / source_rate)))
            for i in range(audio_data.shape[0]):
                resampled[i] = librosa.resample(audio_data[i], orig_sr=source_rate, target_sr=target_rate)
        
        return resampled
