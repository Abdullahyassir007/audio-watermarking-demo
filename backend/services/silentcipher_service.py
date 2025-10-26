"""
SilentCipher Integration Service

Provides interface to Sony's SilentCipher audio watermarking library.
Handles model loading, encoding, and decoding operations.
"""

import numpy as np
from typing import List, Tuple, Optional, Dict, Any
import logging

try:
    import silentcipher
    SILENTCIPHER_AVAILABLE = True
except ImportError:
    SILENTCIPHER_AVAILABLE = False
    silentcipher = None
    logging.warning("SilentCipher library not available. Install with: pip install silentcipher")


class SilentCipherService:
    """Service for encoding and decoding audio watermarks using SilentCipher."""
    
    def __init__(self, device: str = 'cpu'):
        """
        Initialize the SilentCipher service with model caching.
        
        Args:
            device: Device to run models on ('cpu' or 'cuda')
        """
        self._model_16k: Optional[Any] = None
        self._model_44k: Optional[Any] = None
        self._device = device
        self._logger = logging.getLogger(__name__)
        
        if not SILENTCIPHER_AVAILABLE:
            self._logger.error("SilentCipher library is not installed")
    
    def get_model(self, sample_rate: int) -> Any:
        """
        Load and cache SilentCipher model for the specified sample rate.
        
        Args:
            sample_rate: Sample rate in Hz (16000 or 44100)
            
        Returns:
            SilentCipher model instance
            
        Raises:
            ValueError: If sample rate is not supported
            RuntimeError: If SilentCipher is not available or model loading fails
        """
        if not SILENTCIPHER_AVAILABLE:
            raise RuntimeError(
                "SilentCipher library is not installed. "
                "Install with: pip install silentcipher"
            )
        
        # Determine which model to use
        if sample_rate == 16000:
            if self._model_16k is None:
                self._logger.info("Loading SilentCipher 16kHz model...")
                try:
                    self._model_16k = silentcipher.get_model(
                        model_type='16k',
                        device=self._device
                    )
                    self._logger.info("16kHz model loaded successfully")
                except Exception as e:
                    self._logger.error(f"Failed to load 16kHz model: {e}")
                    raise RuntimeError(f"Failed to load SilentCipher 16kHz model: {e}")
            return self._model_16k
        
        elif sample_rate == 44100:
            if self._model_44k is None:
                self._logger.info("Loading SilentCipher 44.1kHz model...")
                try:
                    self._model_44k = silentcipher.get_model(
                        model_type='44.1k',
                        device=self._device
                    )
                    self._logger.info("44.1kHz model loaded successfully")
                except Exception as e:
                    self._logger.error(f"Failed to load 44.1kHz model: {e}")
                    raise RuntimeError(f"Failed to load SilentCipher 44.1kHz model: {e}")
            return self._model_44k
        
        else:
            raise ValueError(
                f"Unsupported sample rate: {sample_rate}Hz. "
                f"Supported rates: 16000Hz, 44100Hz"
            )
    
    def encode_audio(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        message: List[int]
    ) -> Tuple[np.ndarray, float]:
        """
        Embed watermark into audio using SilentCipher.
        
        Args:
            audio_data: Audio data array (channels, samples) or (samples,)
            sample_rate: Sample rate in Hz (any rate - will be resampled to 44.1kHz internally)
            message: Message payload as list of 5 integers (0-255)
            
        Returns:
            Tuple of (watermarked_audio, sdr_value)
            - watermarked_audio: Audio with embedded watermark (at original sample rate)
            - sdr_value: Signal-to-Distortion Ratio in dB
            
        Note:
            Audio will be automatically resampled to 44.1kHz for watermarking,
            then resampled back to the original sample rate.
            
        Raises:
            ValueError: If inputs are invalid
            RuntimeError: If encoding fails
        """
        # Validate message
        if not isinstance(message, list) or len(message) != 5:
            raise ValueError("Message must be a list of 5 integers")
        
        if not all(isinstance(x, int) and 0 <= x <= 255 for x in message):
            raise ValueError("All message values must be integers between 0 and 255")
        
        # Validate audio data
        if audio_data is None or len(audio_data) == 0:
            raise ValueError("Audio data is empty")
        
        # Always use 44.1kHz model (it will handle resampling internally)
        model = self.get_model(44100)
        
        try:
            # Ensure audio is in the correct format for SilentCipher
            # SilentCipher expects (samples,) for mono
            if audio_data.ndim == 2:
                # Convert from (channels, samples) to (samples,) - use first channel
                if audio_data.shape[0] < audio_data.shape[1]:
                    audio_input = audio_data[0]
                else:
                    audio_input = audio_data[:, 0]
            else:
                audio_input = audio_data
            
            # Ensure minimum length for SilentCipher (pad if needed)
            # SilentCipher needs at least 3 seconds at the target sample rate
            min_samples = int(3.5 * sample_rate)  # 3.5 seconds to be safe
            original_length = len(audio_input)
            if len(audio_input) < min_samples:
                # Pad with silence to meet minimum length
                padding = min_samples - len(audio_input)
                audio_input = np.pad(audio_input, (0, padding), mode='constant', constant_values=0)
                self._logger.warning(
                    f"Audio padded from {original_length} to {len(audio_input)} samples "
                    f"({original_length/sample_rate:.2f}s to {len(audio_input)/sample_rate:.2f}s) "
                    f"to meet SilentCipher minimum length requirement"
                )
            
            # Encode the watermark using encode_wav
            self._logger.info(f"Encoding watermark with message: {message}")
            watermarked_audio, sdr = model.encode_wav(audio_input, sample_rate, message)
            
            # Trim back to original length if we padded
            if original_length < min_samples and len(watermarked_audio) > original_length:
                watermarked_audio = watermarked_audio[:original_length]
                self._logger.info(f"Trimmed watermarked audio back to original length: {original_length} samples")
            
            # Convert back to original format if needed
            if audio_data.ndim == 2 and audio_data.shape[0] < audio_data.shape[1]:
                # Expand back to stereo if original was stereo
                watermarked_audio = np.stack([watermarked_audio, watermarked_audio], axis=0)
            
            self._logger.info(f"Encoding successful. SDR: {sdr:.2f} dB")
            return watermarked_audio, float(sdr)
            
        except Exception as e:
            self._logger.error(f"Encoding failed: {e}")
            error_msg = str(e)
            if "broadcast" in error_msg or "shape" in error_msg:
                raise RuntimeError(
                    f"Failed to encode watermark due to audio length mismatch. "
                    f"This can happen with very short audio (<3s). "
                    f"Original error: {e}"
                )
            raise RuntimeError(f"Failed to encode watermark: {e}")
    
    def decode_audio(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        phase_shift_decoding: bool = False
    ) -> Dict[str, any]:
        """
        Extract watermark from audio using SilentCipher.
        
        Args:
            audio_data: Watermarked audio data array
            sample_rate: Sample rate in Hz (any rate - will be resampled to 44.1kHz internally)
            phase_shift_decoding: Whether to use phase shift decoding for robustness.
                                 WARNING: This drastically increases decode time.
                                 Only enable if you need robustness to audio crops.
            
        Returns:
            Dictionary with decoding results:
            {
                'detected': bool,
                'message': List[int] or None,
                'confidence': float or None
            }
            
        Note:
            Audio will be automatically resampled to 44.1kHz for decoding.
            
        Raises:
            ValueError: If inputs are invalid
            RuntimeError: If decoding fails
        """
        # Validate audio data
        if audio_data is None or len(audio_data) == 0:
            raise ValueError("Audio data is empty")
        
        # Always use 44.1kHz model (it will handle resampling internally)
        model = self.get_model(44100)
        
        try:
            # Ensure audio is in the correct format for SilentCipher
            # SilentCipher expects (samples,) for mono
            if audio_data.ndim == 2:
                # Convert from (channels, samples) to (samples,) - use first channel
                if audio_data.shape[0] < audio_data.shape[1]:
                    audio_input = audio_data[0]
                else:
                    audio_input = audio_data[:, 0]
            else:
                audio_input = audio_data
            
            # Decode the watermark using decode_wav
            self._logger.info("Decoding watermark from audio...")
            result = model.decode_wav(audio_input, sample_rate, phase_shift_decoding)
            
            # Parse the result - decode_wav returns a dict with 'status', 'messages', 'confidences'
            if not result.get('status', False):
                self._logger.info("No watermark detected")
                return {
                    'detected': False,
                    'message': None,
                    'confidence': None
                }
            
            # Get the first message (index 0) from the messages list
            messages = result.get('messages', [])
            confidences = result.get('confidences', [])
            
            if not messages or len(messages) == 0:
                self._logger.info("No watermark detected")
                return {
                    'detected': False,
                    'message': None,
                    'confidence': None
                }
            
            message = messages[0]
            confidence = confidences[0] if confidences else None
            
            self._logger.info(f"Watermark detected. Message: {message}")
            return {
                'detected': True,
                'message': message,
                'confidence': confidence
            }
            
        except Exception as e:
            self._logger.error(f"Decoding failed: {e}")
            raise RuntimeError(f"Failed to decode watermark: {e}")
    
    def _calculate_sdr(self, original: np.ndarray, watermarked: np.ndarray) -> float:
        """
        Calculate Signal-to-Distortion Ratio (SDR) in dB.
        
        SDR measures the quality of the watermarked audio compared to the original.
        Higher values indicate less distortion (more imperceptible watermark).
        
        Args:
            original: Original audio data
            watermarked: Watermarked audio data
            
        Returns:
            SDR value in decibels
        """
        # Ensure arrays have the same shape
        if original.shape != watermarked.shape:
            raise ValueError("Original and watermarked audio must have the same shape")
        
        # Calculate signal power
        signal_power = np.mean(original ** 2)
        
        # Calculate distortion (difference between original and watermarked)
        distortion = original - watermarked
        distortion_power = np.mean(distortion ** 2)
        
        # Avoid division by zero
        if distortion_power == 0:
            return float('inf')
        
        # Calculate SDR in dB
        sdr = 10 * np.log10(signal_power / distortion_power)
        
        return float(sdr)
    
    def is_available(self) -> bool:
        """
        Check if SilentCipher library is available.
        
        Returns:
            True if SilentCipher is installed and available
        """
        return SILENTCIPHER_AVAILABLE
    
    def get_supported_sample_rates(self) -> List[int]:
        """
        Get list of supported sample rates.
        
        Returns:
            List of supported sample rates in Hz
            
        Note:
            Currently only 44100Hz is fully supported.
            The 16kHz model has compatibility issues with the current library version.
        """
        return [44100]  # 16000 has model compatibility issues
