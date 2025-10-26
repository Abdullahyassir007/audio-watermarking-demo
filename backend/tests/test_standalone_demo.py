"""
Tests for standalone_demo.py CLI interface
"""

import pytest
import sys
import os
import tempfile
import numpy as np
import soundfile as sf
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import standalone_demo
from services.silentcipher_service import SILENTCIPHER_AVAILABLE


# Skip tests if SilentCipher is not available
pytestmark = pytest.mark.skipif(
    not SILENTCIPHER_AVAILABLE,
    reason="SilentCipher library not installed"
)


@pytest.fixture
def sample_audio_file():
    """Create a temporary sample audio file for testing"""
    sample_rate = 44100
    duration = 5.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = (0.3 * np.sin(2 * np.pi * 440 * t) +
             0.2 * np.sin(2 * np.pi * 880 * t) +
             0.1 * np.random.randn(len(t)))
    audio = audio / np.max(np.abs(audio)) * 0.5
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        temp_path = f.name
    
    sf.write(temp_path, audio, sample_rate)
    
    yield temp_path
    
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def output_audio_file():
    """Create a temporary output file path"""
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        temp_path = f.name
    
    # Remove the file so it can be created by the test
    os.remove(temp_path)
    
    yield temp_path
    
    if os.path.exists(temp_path):
        os.remove(temp_path)


class TestArgumentParsing:
    """Tests for command-line argument parsing"""
    
    def test_parse_encode_command_text(self):
        """Test parsing encode command with text message"""
        test_args = [
            'standalone_demo.py',
            'encode',
            '--input', 'input.wav',
            '--output', 'output.wav',
            '--message', 'Hello',
            '--format', 'text'
        ]
        
        with patch.object(sys, 'argv', test_args):
            args = standalone_demo.parse_arguments()
            
            assert args.command == 'encode'
            assert args.input == 'input.wav'
            assert args.output == 'output.wav'
            assert args.message == 'Hello'
            assert args.format == 'text'
            assert args.model == '44.1k'  # default
            assert args.play is False  # default
    
    def test_parse_encode_command_numeric(self):
        """Test parsing encode command with numeric message"""
        test_args = [
            'standalone_demo.py',
            'encode',
            '--input', 'input.wav',
            '--output', 'output.wav',
            '--message', '100,150,200,50,75',
            '--format', 'numeric'
        ]
        
        with patch.object(sys, 'argv', test_args):
            args = standalone_demo.parse_arguments()
            
            assert args.command == 'encode'
            assert args.message == '100,150,200,50,75'
            assert args.format == 'numeric'
    
    def test_parse_encode_command_binary(self):
        """Test parsing encode command with binary message"""
        test_args = [
            'standalone_demo.py',
            'encode',
            '--input', 'input.wav',
            '--output', 'output.wav',
            '--message', '0101010101010101010101010101010101010101',
            '--format', 'binary'
        ]
        
        with patch.object(sys, 'argv', test_args):
            args = standalone_demo.parse_arguments()
            
            assert args.command == 'encode'
            assert args.message == '0101010101010101010101010101010101010101'
            assert args.format == 'binary'
    
    def test_parse_encode_with_play_flag(self):
        """Test parsing encode command with play flag"""
        test_args = [
            'standalone_demo.py',
            'encode',
            '--input', 'input.wav',
            '--output', 'output.wav',
            '--message', 'Test',
            '--play'
        ]
        
        with patch.object(sys, 'argv', test_args):
            args = standalone_demo.parse_arguments()
            
            assert args.play is True
    
    def test_parse_decode_command(self):
        """Test parsing decode command"""
        test_args = [
            'standalone_demo.py',
            'decode',
            '--input', 'watermarked.wav'
        ]
        
        with patch.object(sys, 'argv', test_args):
            args = standalone_demo.parse_arguments()
            
            assert args.command == 'decode'
            assert args.input == 'watermarked.wav'
            assert args.model == '44.1k'  # default
    
    def test_parse_decode_with_phase_shift(self):
        """Test parsing decode command with phase shift flag"""
        test_args = [
            'standalone_demo.py',
            'decode',
            '--input', 'watermarked.wav',
            '--phase-shift'
        ]
        
        with patch.object(sys, 'argv', test_args):
            args = standalone_demo.parse_arguments()
            
            assert args.phase_shift is True
    
    def test_parse_with_16k_model(self):
        """Test parsing with 16k model option"""
        test_args = [
            'standalone_demo.py',
            'encode',
            '--input', 'input.wav',
            '--output', 'output.wav',
            '--message', 'Test',
            '--model', '16k'
        ]
        
        with patch.object(sys, 'argv', test_args):
            args = standalone_demo.parse_arguments()
            
            assert args.model == '16k'


class TestArgumentValidation:
    """Tests for argument validation"""
    
    def test_validate_nonexistent_input_file(self):
        """Test validation fails for nonexistent input file"""
        args = MagicMock()
        args.command = 'encode'
        args.input = 'nonexistent.wav'
        args.output = 'output.wav'
        args.message = 'Test'
        args.format = 'text'
        
        with pytest.raises(ValueError, match="Input file does not exist"):
            standalone_demo.validate_arguments(args)
    
    def test_validate_non_wav_input(self, sample_audio_file):
        """Test validation fails for non-WAV file"""
        # Create a temporary non-WAV file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            non_wav_file = f.name
            f.write(b'fake mp3 data')
        
        try:
            args = MagicMock()
            args.command = 'encode'
            args.input = non_wav_file
            args.output = 'output.wav'
            args.message = 'Test'
            args.format = 'text'
            
            with pytest.raises(ValueError, match="must be a WAV file"):
                standalone_demo.validate_arguments(args)
        finally:
            if os.path.exists(non_wav_file):
                os.remove(non_wav_file)
    
    def test_validate_numeric_message_wrong_count(self, sample_audio_file):
        """Test validation fails for numeric message with wrong count"""
        args = MagicMock()
        args.command = 'encode'
        args.input = sample_audio_file
        args.output = 'output.wav'
        args.message = '100,150,200'  # Only 3 values
        args.format = 'numeric'
        
        with pytest.raises(ValueError, match="exactly 5 integers"):
            standalone_demo.validate_arguments(args)
    
    def test_validate_numeric_message_out_of_range(self, sample_audio_file):
        """Test validation fails for numeric message with out-of-range values"""
        args = MagicMock()
        args.command = 'encode'
        args.input = sample_audio_file
        args.output = 'output.wav'
        args.message = '100,150,300,50,75'  # 300 is out of range
        args.format = 'numeric'
        
        with pytest.raises(ValueError, match="between 0 and 255"):
            standalone_demo.validate_arguments(args)
    
    def test_validate_binary_message_wrong_length(self, sample_audio_file):
        """Test validation fails for binary message with wrong length"""
        args = MagicMock()
        args.command = 'encode'
        args.input = sample_audio_file
        args.output = 'output.wav'
        args.message = '01010101'  # Only 8 bits
        args.format = 'binary'
        
        with pytest.raises(ValueError, match="exactly 40 bits"):
            standalone_demo.validate_arguments(args)
    
    def test_validate_binary_message_invalid_characters(self, sample_audio_file):
        """Test validation fails for binary message with invalid characters"""
        args = MagicMock()
        args.command = 'encode'
        args.input = sample_audio_file
        args.output = 'output.wav'
        args.message = '0101010101010101010101010101010101012345'  # Contains 2,3,4,5
        args.format = 'binary'
        
        with pytest.raises(ValueError, match="only '0' and '1'"):
            standalone_demo.validate_arguments(args)
    
    def test_validate_empty_text_message(self, sample_audio_file):
        """Test validation fails for empty text message"""
        args = MagicMock()
        args.command = 'encode'
        args.input = sample_audio_file
        args.output = 'output.wav'
        args.message = ''
        args.format = 'text'
        
        with pytest.raises(ValueError, match="cannot be empty"):
            standalone_demo.validate_arguments(args)
    
    def test_validate_valid_encode_args(self, sample_audio_file):
        """Test validation passes for valid encode arguments"""
        args = MagicMock()
        args.command = 'encode'
        args.input = sample_audio_file
        args.output = 'output.wav'
        args.message = 'Test'
        args.format = 'text'
        
        # Should not raise any exception
        standalone_demo.validate_arguments(args)
    
    def test_validate_valid_decode_args(self, sample_audio_file):
        """Test validation passes for valid decode arguments"""
        args = MagicMock()
        args.command = 'decode'
        args.input = sample_audio_file
        
        # Should not raise any exception
        standalone_demo.validate_arguments(args)


class TestEncodeWorkflow:
    """Tests for the encode workflow"""
    
    def test_encode_with_text_message(self, sample_audio_file, output_audio_file):
        """Test encoding with text message"""
        args = MagicMock()
        args.input = sample_audio_file
        args.output = output_audio_file
        args.message = 'Hello'
        args.format = 'text'
        args.model = '44.1k'
        args.play = False
        
        # Run encode
        standalone_demo.run_encode(args)
        
        # Verify output file was created
        assert os.path.exists(output_audio_file)
        
        # Verify output file is valid audio
        audio, sample_rate = sf.read(output_audio_file)
        assert len(audio) > 0
        assert sample_rate == 44100
    
    def test_encode_with_numeric_message(self, sample_audio_file, output_audio_file):
        """Test encoding with numeric message"""
        args = MagicMock()
        args.input = sample_audio_file
        args.output = output_audio_file
        args.message = '100,150,200,50,75'
        args.format = 'numeric'
        args.model = '44.1k'
        args.play = False
        
        # Run encode
        standalone_demo.run_encode(args)
        
        # Verify output file was created
        assert os.path.exists(output_audio_file)
    
    def test_encode_with_binary_message(self, sample_audio_file, output_audio_file):
        """Test encoding with binary message"""
        args = MagicMock()
        args.input = sample_audio_file
        args.output = output_audio_file
        args.message = '0101010101010101010101010101010101010101'
        args.format = 'binary'
        args.model = '44.1k'
        args.play = False
        
        # Run encode
        standalone_demo.run_encode(args)
        
        # Verify output file was created
        assert os.path.exists(output_audio_file)


class TestDecodeWorkflow:
    """Tests for the decode workflow"""
    
    def test_decode_watermarked_audio(self, sample_audio_file, output_audio_file):
        """Test decoding watermarked audio"""
        # First encode a watermark
        encode_args = MagicMock()
        encode_args.input = sample_audio_file
        encode_args.output = output_audio_file
        encode_args.message = 'Test'
        encode_args.format = 'text'
        encode_args.model = '44.1k'
        encode_args.play = False
        
        standalone_demo.run_encode(encode_args)
        
        # Now decode it
        decode_args = MagicMock()
        decode_args.input = output_audio_file
        decode_args.model = '44.1k'
        decode_args.phase_shift = False
        
        # Should not raise any exception
        standalone_demo.run_decode(decode_args)
    
    def test_decode_non_watermarked_audio(self, sample_audio_file):
        """Test decoding non-watermarked audio"""
        args = MagicMock()
        args.input = sample_audio_file
        args.model = '44.1k'
        args.phase_shift = False
        
        # Should not raise exception, but should report no watermark
        standalone_demo.run_decode(args)


class TestEndToEndWorkflows:
    """End-to-end integration tests"""
    
    def test_complete_encode_decode_cycle_text(self, sample_audio_file, output_audio_file):
        """Test complete encode-decode cycle with text message"""
        message = 'Hello'
        
        # Encode
        encode_args = MagicMock()
        encode_args.input = sample_audio_file
        encode_args.output = output_audio_file
        encode_args.message = message
        encode_args.format = 'text'
        encode_args.model = '44.1k'
        encode_args.play = False
        
        standalone_demo.run_encode(encode_args)
        assert os.path.exists(output_audio_file)
        
        # Decode
        decode_args = MagicMock()
        decode_args.input = output_audio_file
        decode_args.model = '44.1k'
        decode_args.phase_shift = False
        
        standalone_demo.run_decode(decode_args)
    
    def test_complete_encode_decode_cycle_numeric(self, sample_audio_file, output_audio_file):
        """Test complete encode-decode cycle with numeric message"""
        message = '123,234,111,222,11'
        
        # Encode
        encode_args = MagicMock()
        encode_args.input = sample_audio_file
        encode_args.output = output_audio_file
        encode_args.message = message
        encode_args.format = 'numeric'
        encode_args.model = '44.1k'
        encode_args.play = False
        
        standalone_demo.run_encode(encode_args)
        assert os.path.exists(output_audio_file)
        
        # Decode
        decode_args = MagicMock()
        decode_args.input = output_audio_file
        decode_args.model = '44.1k'
        decode_args.phase_shift = False
        
        standalone_demo.run_decode(decode_args)
    
    def test_complete_encode_decode_cycle_binary(self, sample_audio_file, output_audio_file):
        """Test complete encode-decode cycle with binary message"""
        message = '1010101010101010101010101010101010101010'
        
        # Encode
        encode_args = MagicMock()
        encode_args.input = sample_audio_file
        encode_args.output = output_audio_file
        encode_args.message = message
        encode_args.format = 'binary'
        encode_args.model = '44.1k'
        encode_args.play = False
        
        standalone_demo.run_encode(encode_args)
        assert os.path.exists(output_audio_file)
        
        # Decode
        decode_args = MagicMock()
        decode_args.input = output_audio_file
        decode_args.model = '44.1k'
        decode_args.phase_shift = False
        
        standalone_demo.run_decode(decode_args)


class TestPlaybackFeature:
    """Tests for optional playback feature"""
    
    def test_play_audio_success(self):
        """Test successful audio playback with mocked pygame"""
        # Mock pygame module
        mock_pygame = MagicMock()
        mock_pygame.mixer.music.get_busy.return_value = False
        
        with patch.dict('sys.modules', {'pygame': mock_pygame}):
            # Import play_audio function after mocking
            import importlib
            importlib.reload(standalone_demo)
            
            standalone_demo.play_audio('test.wav')
            
            mock_pygame.mixer.init.assert_called_once()
            mock_pygame.mixer.music.load.assert_called_once_with('test.wav')
            mock_pygame.mixer.music.play.assert_called_once()
            mock_pygame.mixer.quit.assert_called_once()
    
    def test_play_audio_without_pygame(self):
        """Test playback fails gracefully without pygame"""
        with patch.dict('sys.modules', {'pygame': None}):
            with pytest.raises(ImportError, match="pygame is required"):
                standalone_demo.play_audio('test.wav')


class TestErrorHandling:
    """Tests for error handling"""
    
    def test_encode_with_invalid_audio_file(self, output_audio_file):
        """Test encoding with invalid audio file"""
        # Create an invalid audio file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            invalid_file = f.name
            f.write(b'invalid audio data')
        
        try:
            args = MagicMock()
            args.input = invalid_file
            args.output = output_audio_file
            args.message = 'Test'
            args.format = 'text'
            args.model = '44.1k'
            args.play = False
            
            with pytest.raises(RuntimeError):
                standalone_demo.run_encode(args)
        finally:
            if os.path.exists(invalid_file):
                os.remove(invalid_file)
    
    def test_decode_with_invalid_audio_file(self):
        """Test decoding with invalid audio file"""
        # Create an invalid audio file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            invalid_file = f.name
            f.write(b'invalid audio data')
        
        try:
            args = MagicMock()
            args.input = invalid_file
            args.model = '44.1k'
            args.phase_shift = False
            
            with pytest.raises(RuntimeError):
                standalone_demo.run_decode(args)
        finally:
            if os.path.exists(invalid_file):
                os.remove(invalid_file)
