"""
Unit tests for AudioProcessor class
"""

import pytest
import numpy as np
import os
import tempfile
from services.audio_processor import AudioProcessor


@pytest.fixture
def audio_processor():
    """Create AudioProcessor instance for testing"""
    return AudioProcessor()


@pytest.fixture
def sample_audio_mono():
    """Create sample mono audio data"""
    sample_rate = 16000
    duration = 1.0  # 1 second
    frequency = 440  # A4 note
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)
    return audio, sample_rate


@pytest.fixture
def sample_audio_stereo():
    """Create sample stereo audio data"""
    sample_rate = 44100
    duration = 1.0
    frequency = 440
    t = np.linspace(0, duration, int(sample_rate * duration))
    left = 0.5 * np.sin(2 * np.pi * frequency * t)
    right = 0.5 * np.sin(2 * np.pi * frequency * 1.5 * t)
    audio = np.array([left, right])
    return audio, sample_rate


@pytest.fixture
def temp_wav_file(sample_audio_mono):
    """Create a temporary WAV file for testing"""
    import soundfile as sf
    audio, sample_rate = sample_audio_mono
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        temp_path = f.name
    
    sf.write(temp_path, audio, sample_rate)
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


class TestLoadAudio:
    """Tests for load_audio method"""
    
    def test_load_valid_audio(self, audio_processor, temp_wav_file):
        """Test loading a valid audio file"""
        audio_data, sample_rate = audio_processor.load_audio(temp_wav_file)
        
        assert audio_data is not None
        assert len(audio_data) > 0
        assert sample_rate == 16000
        assert audio_data.ndim == 2  # Should be 2D (channels, samples)
    
    def test_load_nonexistent_file(self, audio_processor):
        """Test loading a file that doesn't exist"""
        with pytest.raises(FileNotFoundError):
            audio_processor.load_audio('nonexistent_file.wav')
    
    def test_load_with_target_sample_rate(self, audio_processor, temp_wav_file):
        """Test loading with resampling"""
        audio_data, sample_rate = audio_processor.load_audio(temp_wav_file, sr=44100)
        
        assert sample_rate == 44100
        assert audio_data is not None


class TestSaveAudio:
    """Tests for save_audio method"""
    
    def test_save_mono_audio(self, audio_processor, sample_audio_mono):
        """Test saving mono audio"""
        audio, sample_rate = sample_audio_mono
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name
        
        try:
            audio_processor.save_audio(audio, sample_rate, temp_path)
            assert os.path.exists(temp_path)
            
            # Verify by loading back
            loaded_audio, loaded_sr = audio_processor.load_audio(temp_path)
            assert loaded_sr == sample_rate
            assert len(loaded_audio[0]) > 0
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_save_stereo_audio(self, audio_processor, sample_audio_stereo):
        """Test saving stereo audio"""
        audio, sample_rate = sample_audio_stereo
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name
        
        try:
            audio_processor.save_audio(audio, sample_rate, temp_path)
            assert os.path.exists(temp_path)
            
            # Verify by loading back
            loaded_audio, loaded_sr = audio_processor.load_audio(temp_path)
            assert loaded_sr == sample_rate
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_save_empty_audio(self, audio_processor):
        """Test saving empty audio raises error"""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Audio data is empty"):
                audio_processor.save_audio(np.array([]), 16000, temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_save_invalid_sample_rate(self, audio_processor, sample_audio_mono):
        """Test saving with invalid sample rate"""
        audio, _ = sample_audio_mono
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Invalid sample rate"):
                audio_processor.save_audio(audio, -1, temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestValidateFormat:
    """Tests for validate_format method"""
    
    def test_validate_valid_file(self, audio_processor, temp_wav_file):
        """Test validation of valid audio file"""
        result = audio_processor.validate_format(temp_wav_file)
        
        assert result['valid'] is True
        assert result['format'] == '.wav'
        assert result['sample_rate'] == 16000
        assert len(result['errors']) == 0
    
    def test_validate_nonexistent_file(self, audio_processor):
        """Test validation of nonexistent file"""
        result = audio_processor.validate_format('nonexistent.wav')
        
        assert result['valid'] is False
        assert 'File does not exist' in result['errors']
    
    def test_validate_unsupported_sample_rate(self, audio_processor, sample_audio_mono):
        """Test validation with unsupported sample rate"""
        import soundfile as sf
        audio, _ = sample_audio_mono
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name
        
        try:
            # Save with unsupported sample rate
            sf.write(temp_path, audio, 22050)
            
            result = audio_processor.validate_format(temp_path)
            
            assert result['valid'] is False
            assert any('Unsupported sample rate' in err for err in result['errors'])
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestGetMetadata:
    """Tests for get_metadata method"""
    
    def test_metadata_mono_audio(self, audio_processor, sample_audio_mono):
        """Test metadata extraction from mono audio"""
        audio, sample_rate = sample_audio_mono
        
        metadata = audio_processor.get_metadata(audio, sample_rate)
        
        assert metadata['sample_rate'] == sample_rate
        assert metadata['channels'] == 1
        assert metadata['samples'] == len(audio)
        assert abs(metadata['duration'] - 1.0) < 0.01  # Should be ~1 second
    
    def test_metadata_stereo_audio(self, audio_processor, sample_audio_stereo):
        """Test metadata extraction from stereo audio"""
        audio, sample_rate = sample_audio_stereo
        
        metadata = audio_processor.get_metadata(audio, sample_rate)
        
        assert metadata['sample_rate'] == sample_rate
        assert metadata['channels'] == 2
        assert metadata['samples'] == audio.shape[1]
        assert abs(metadata['duration'] - 1.0) < 0.01


class TestApplyNoise:
    """Tests for apply_noise method"""
    
    def test_apply_noise_default(self, audio_processor, sample_audio_mono):
        """Test applying noise with default parameters"""
        audio, _ = sample_audio_mono
        
        noisy_audio = audio_processor.apply_noise(audio)
        
        assert noisy_audio.shape == audio.shape
        assert not np.array_equal(noisy_audio, audio)  # Should be different
        assert np.max(np.abs(noisy_audio)) <= 1.0  # Should be normalized
    
    def test_apply_noise_different_levels(self, audio_processor, sample_audio_mono):
        """Test applying different noise levels"""
        audio, _ = sample_audio_mono
        
        noisy_low = audio_processor.apply_noise(audio, noise_level_db=-30)
        noisy_high = audio_processor.apply_noise(audio, noise_level_db=-10)
        
        # Higher noise level should create more difference
        diff_low = np.mean(np.abs(audio - noisy_low))
        diff_high = np.mean(np.abs(audio - noisy_high))
        
        assert diff_high > diff_low


class TestApplyCompression:
    """Tests for apply_compression method"""
    
    def test_apply_compression_default(self, audio_processor, sample_audio_mono):
        """Test applying compression with default parameters"""
        audio, sample_rate = sample_audio_mono
        
        compressed = audio_processor.apply_compression(audio, sample_rate)
        
        assert compressed.shape == audio.shape
        assert np.max(np.abs(compressed)) <= 1.0
    
    def test_apply_compression_different_bitrates(self, audio_processor, sample_audio_mono):
        """Test applying different compression bitrates"""
        audio, sample_rate = sample_audio_mono
        
        compressed_low = audio_processor.apply_compression(audio, sample_rate, bitrate=64)
        compressed_high = audio_processor.apply_compression(audio, sample_rate, bitrate=256)
        
        # Both should be valid
        assert compressed_low.shape == audio.shape
        assert compressed_high.shape == audio.shape


class TestResampleAudio:
    """Tests for resample_audio method"""
    
    def test_resample_upsample(self, audio_processor, sample_audio_mono):
        """Test upsampling audio"""
        audio, sample_rate = sample_audio_mono
        target_rate = 44100
        
        resampled = audio_processor.resample_audio(audio, sample_rate, target_rate)
        
        expected_length = int(len(audio) * target_rate / sample_rate)
        assert abs(len(resampled) - expected_length) <= 1  # Allow 1 sample difference
    
    def test_resample_downsample(self, audio_processor):
        """Test downsampling audio"""
        sample_rate = 44100
        target_rate = 16000
        duration = 1.0
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)
        
        resampled = audio_processor.resample_audio(audio, sample_rate, target_rate)
        
        expected_length = int(len(audio) * target_rate / sample_rate)
        assert abs(len(resampled) - expected_length) <= 1
    
    def test_resample_same_rate(self, audio_processor, sample_audio_mono):
        """Test resampling to same rate returns unchanged"""
        audio, sample_rate = sample_audio_mono
        
        resampled = audio_processor.resample_audio(audio, sample_rate, sample_rate)
        
        assert np.array_equal(resampled, audio)
