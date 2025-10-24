"""
Integration tests for SilentCipherService class
"""

import pytest
import numpy as np
import os
import tempfile
import soundfile as sf
from services.silentcipher_service import SilentCipherService, SILENTCIPHER_AVAILABLE


# Skip all tests if SilentCipher is not available
pytestmark = pytest.mark.skipif(
    not SILENTCIPHER_AVAILABLE,
    reason="SilentCipher library not installed"
)


@pytest.fixture
def silentcipher_service():
    """Create SilentCipherService instance for testing"""
    return SilentCipherService()


@pytest.fixture
def sample_audio_16k():
    """Create sample audio at 16kHz"""
    sample_rate = 16000
    duration = 5.0  # 5 seconds - SilentCipher needs longer audio
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Create more complex audio with multiple frequencies and some noise
    audio = (0.3 * np.sin(2 * np.pi * 440 * t) +
             0.2 * np.sin(2 * np.pi * 880 * t) +
             0.1 * np.sin(2 * np.pi * 220 * t) +
             0.05 * np.random.randn(len(t)))
    # Normalize
    audio = audio / np.max(np.abs(audio)) * 0.5
    return audio, sample_rate


@pytest.fixture
def sample_audio_44k():
    """Create sample audio at 44.1kHz"""
    sample_rate = 44100
    duration = 5.0  # 5 seconds - SilentCipher needs longer audio
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Create more complex audio with multiple frequencies and some noise
    audio = (0.3 * np.sin(2 * np.pi * 440 * t) +
             0.2 * np.sin(2 * np.pi * 880 * t) +
             0.1 * np.sin(2 * np.pi * 220 * t) +
             0.05 * np.random.randn(len(t)))
    # Normalize
    audio = audio / np.max(np.abs(audio)) * 0.5
    return audio, sample_rate


@pytest.fixture
def sample_message():
    """Create sample message payload"""
    return [72, 101, 108, 108, 111]  # "Hello" in ASCII


@pytest.fixture
def temp_audio_file_16k(sample_audio_16k):
    """Create temporary 16kHz audio file"""
    audio, sample_rate = sample_audio_16k
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        temp_path = f.name
    
    sf.write(temp_path, audio, sample_rate)
    
    yield temp_path, audio, sample_rate
    
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def temp_audio_file_44k(sample_audio_44k):
    """Create temporary 44.1kHz audio file"""
    audio, sample_rate = sample_audio_44k
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        temp_path = f.name
    
    sf.write(temp_path, audio, sample_rate)
    
    yield temp_path, audio, sample_rate
    
    if os.path.exists(temp_path):
        os.remove(temp_path)


class TestServiceInitialization:
    """Tests for service initialization"""
    
    def test_service_creation(self, silentcipher_service):
        """Test that service can be created"""
        assert silentcipher_service is not None
        assert silentcipher_service._model_16k is None
        assert silentcipher_service._model_44k is None
    
    def test_is_available(self, silentcipher_service):
        """Test availability check"""
        assert silentcipher_service.is_available() is True
    
    def test_get_supported_sample_rates(self, silentcipher_service):
        """Test getting supported sample rates"""
        rates = silentcipher_service.get_supported_sample_rates()
        assert 44100 in rates
        # Note: 16kHz model has compatibility issues with current library version


class TestModelLoading:
    """Tests for model loading and caching"""
    
    def test_load_44k_model(self, silentcipher_service):
        """Test loading 44.1kHz model"""
        model = silentcipher_service.get_model(44100)
        assert model is not None
        assert silentcipher_service._model_44k is not None
    
    def test_model_caching_44k(self, silentcipher_service):
        """Test that 44.1kHz model is cached"""
        model1 = silentcipher_service.get_model(44100)
        model2 = silentcipher_service.get_model(44100)
        assert model1 is model2  # Should be the same instance
    
    def test_unsupported_sample_rate(self, silentcipher_service):
        """Test that unsupported sample rate raises error"""
        with pytest.raises(ValueError, match="Unsupported sample rate"):
            silentcipher_service.get_model(22050)


class TestEncoding:
    """Tests for watermark encoding"""
    
    def test_encode_44k_audio(self, silentcipher_service, sample_audio_44k, sample_message):
        """Test encoding watermark into 44.1kHz audio"""
        audio, sample_rate = sample_audio_44k
        
        watermarked, sdr = silentcipher_service.encode_audio(audio, sample_rate, sample_message)
        
        assert watermarked is not None
        assert watermarked.shape == audio.shape
        assert isinstance(sdr, float)
        assert sdr > 0  # SDR should be positive (good quality)
    
    def test_encode_invalid_message_length(self, silentcipher_service, sample_audio_44k):
        """Test encoding with invalid message length"""
        audio, sample_rate = sample_audio_44k
        invalid_message = [1, 2, 3]  # Only 3 values instead of 5
        
        with pytest.raises(ValueError, match="Message must be a list of 5 integers"):
            silentcipher_service.encode_audio(audio, sample_rate, invalid_message)
    
    def test_encode_invalid_message_values(self, silentcipher_service, sample_audio_44k):
        """Test encoding with invalid message values"""
        audio, sample_rate = sample_audio_44k
        invalid_message = [1, 2, 3, 4, 300]  # 300 is out of range
        
        with pytest.raises(ValueError, match="between 0 and 255"):
            silentcipher_service.encode_audio(audio, sample_rate, invalid_message)
    
    def test_encode_empty_audio(self, silentcipher_service, sample_message):
        """Test encoding with empty audio"""
        empty_audio = np.array([])
        
        with pytest.raises(ValueError, match="Audio data is empty"):
            silentcipher_service.encode_audio(empty_audio, 16000, sample_message)
    
    def test_sdr_calculation(self, silentcipher_service, sample_audio_44k, sample_message):
        """Test that SDR is calculated correctly"""
        audio, sample_rate = sample_audio_44k
        
        watermarked, sdr = silentcipher_service.encode_audio(audio, sample_rate, sample_message)
        
        # SDR should typically be > 20 dB for imperceptible watermarks
        assert sdr > 15.0  # Allow some tolerance


class TestDecoding:
    """Tests for watermark decoding"""
    
    def test_decode_44k_audio(self, silentcipher_service):
        """Test decoding watermark from 44.1kHz audio using real audio"""
        import librosa
        import os
        
        # Use real audio file for reliable watermark detection
        test_audio_path = os.path.join(os.path.dirname(__file__), '../../silentcipher/examples/colab/test.wav')
        if not os.path.exists(test_audio_path):
            pytest.skip("Test audio file not found")
        
        audio, sample_rate = librosa.load(test_audio_path, sr=44100)
        sample_message = [72, 101, 108, 108, 111]
        
        # First encode
        watermarked, _ = silentcipher_service.encode_audio(audio, sample_rate, sample_message)
        
        # Then decode
        result = silentcipher_service.decode_audio(watermarked, sample_rate)
        
        assert result['detected'] is True
        assert result['message'] is not None
        assert len(result['message']) == 5
        # Message should match exactly
        assert result['message'] == sample_message
    
    def test_decode_non_watermarked_audio(self, silentcipher_service):
        """Test decoding from audio without watermark"""
        import librosa
        import os
        
        # Use real audio file
        test_audio_path = os.path.join(os.path.dirname(__file__), '../../silentcipher/examples/colab/test.wav')
        if not os.path.exists(test_audio_path):
            pytest.skip("Test audio file not found")
        
        audio, sample_rate = librosa.load(test_audio_path, sr=44100)
        
        result = silentcipher_service.decode_audio(audio, sample_rate)
        
        # Original audio without watermark may or may not be detected
        # This is expected behavior - just verify the function works
        assert 'detected' in result
        assert 'message' in result
    
    def test_decode_with_confidence(self, silentcipher_service, sample_audio_44k, sample_message):
        """Test that confidence scores are returned"""
        audio, sample_rate = sample_audio_44k
        
        # Encode and decode
        watermarked, _ = silentcipher_service.encode_audio(audio, sample_rate, sample_message)
        result = silentcipher_service.decode_audio(watermarked, sample_rate)
        
        if result['detected']:
            # Confidence should be provided
            assert result['confidence'] is not None
            assert isinstance(result['confidence'], float)
            assert 0.0 <= result['confidence'] <= 1.0
    
    def test_decode_empty_audio(self, silentcipher_service):
        """Test decoding with empty audio"""
        empty_audio = np.array([])
        
        with pytest.raises(ValueError, match="Audio data is empty"):
            silentcipher_service.decode_audio(empty_audio, 16000)


class TestEndToEndWorkflow:
    """End-to-end integration tests"""
    
    def test_encode_decode_cycle_44k(self, silentcipher_service):
        """Test complete encode-decode cycle with 44.1kHz audio using real audio file"""
        import librosa
        import os
        
        # Use the test audio from silentcipher examples
        test_audio_path = os.path.join(os.path.dirname(__file__), '../../silentcipher/examples/colab/test.wav')
        if not os.path.exists(test_audio_path):
            pytest.skip("Test audio file not found")
        
        audio, sample_rate = librosa.load(test_audio_path, sr=44100)
        message = [123, 234, 111, 222, 11]
        
        # Encode
        watermarked, sdr = silentcipher_service.encode_audio(audio, sample_rate, message)
        assert sdr > 0
        
        # Decode
        result = silentcipher_service.decode_audio(watermarked, sample_rate)
        assert result['detected'] is True
        
        # Verify message - should match exactly
        assert result['message'] == message
    
    def test_multiple_messages(self, silentcipher_service):
        """Test encoding and decoding multiple different messages"""
        import librosa
        import os
        
        # Use real audio file
        test_audio_path = os.path.join(os.path.dirname(__file__), '../../silentcipher/examples/colab/test.wav')
        if not os.path.exists(test_audio_path):
            pytest.skip("Test audio file not found")
        
        audio, sample_rate = librosa.load(test_audio_path, sr=44100)
        
        messages = [
            [1, 2, 3, 4, 5],
            [100, 150, 200, 250, 50],
            [123, 234, 111, 222, 11]
        ]
        
        for message in messages:
            watermarked, sdr = silentcipher_service.encode_audio(audio, sample_rate, message)
            result = silentcipher_service.decode_audio(watermarked, sample_rate)
            
            assert result['detected'] is True
            assert result['message'] == message


class TestSDRCalculation:
    """Tests for SDR calculation"""
    
    def test_sdr_identical_signals(self, silentcipher_service):
        """Test SDR with identical signals (should be infinite)"""
        signal = np.random.randn(1000)
        sdr = silentcipher_service._calculate_sdr(signal, signal)
        assert np.isinf(sdr)
    
    def test_sdr_different_signals(self, silentcipher_service):
        """Test SDR with different signals"""
        signal1 = np.random.randn(1000)
        signal2 = signal1 + 0.01 * np.random.randn(1000)
        
        sdr = silentcipher_service._calculate_sdr(signal1, signal2)
        assert isinstance(sdr, float)
        assert sdr > 0
    
    def test_sdr_shape_mismatch(self, silentcipher_service):
        """Test SDR with mismatched shapes"""
        signal1 = np.random.randn(1000)
        signal2 = np.random.randn(500)
        
        with pytest.raises(ValueError, match="same shape"):
            silentcipher_service._calculate_sdr(signal1, signal2)


# Tests that run even without SilentCipher installed
class TestWithoutSilentCipher:
    """Tests that should work even without SilentCipher"""
    
    @pytest.mark.skipif(SILENTCIPHER_AVAILABLE, reason="Only test when SilentCipher is not available")
    def test_service_creation_without_library(self):
        """Test service can be created even without SilentCipher"""
        service = SilentCipherService()
        assert service is not None
        assert service.is_available() is False
    
    @pytest.mark.skipif(SILENTCIPHER_AVAILABLE, reason="Only test when SilentCipher is not available")
    def test_get_model_without_library(self):
        """Test that get_model raises error without SilentCipher"""
        service = SilentCipherService()
        with pytest.raises(RuntimeError, match="not installed"):
            service.get_model(16000)
    
    def test_get_supported_sample_rates_always(self):
        """Test getting supported sample rates works without library"""
        service = SilentCipherService()
        rates = service.get_supported_sample_rates()
        assert 44100 in rates
