#!/usr/bin/env python3
"""
Standalone Audio Watermarking Demo Interface

A CLI tool for quickly testing SilentCipher audio watermarking functionality
without running the full web application. This interface directly uses the
backend services for encoding and decoding watermarks.

Usage:
    # Encode with text message
    python standalone_demo.py encode --input audio.wav --output watermarked.wav --message "Hello" --format text

    # Encode with numeric array
    python standalone_demo.py encode --input audio.wav --output watermarked.wav --message "100,150,200,50,75" --format numeric

    # Encode with binary string
    python standalone_demo.py encode --input audio.wav --output watermarked.wav --message "0101010101010101010101010101010101010101" --format binary

    # Decode watermark
    python standalone_demo.py decode --input watermarked.wav

    # Encode and play (optional feature)
    python standalone_demo.py encode --input audio.wav --output watermarked.wav --message "Test" --format text --play
"""

import argparse
import sys
import os
from typing import List, Optional

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.audio_processor import AudioProcessor
from services.silentcipher_service import SilentCipherService
from utils.message_converter import MessageConverter


def parse_arguments():
    """
    Parse command-line arguments for the standalone demo interface.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='Standalone Audio Watermarking Demo - Test SilentCipher functionality',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Encode with text message
  %(prog)s encode --input audio.wav --output watermarked.wav --message "Hello" --format text

  # Encode with numeric array
  %(prog)s encode --input audio.wav --output watermarked.wav --message "100,150,200,50,75" --format numeric

  # Decode watermark
  %(prog)s decode --input watermarked.wav
        """
    )
    
    # Create subparsers for encode and decode commands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute', required=True)
    
    # Encode subcommand
    encode_parser = subparsers.add_parser('encode', help='Encode a watermark into an audio file')
    encode_parser.add_argument(
        '--input',
        required=True,
        help='Path to input audio file (WAV format, 16kHz or 44.1kHz)'
    )
    encode_parser.add_argument(
        '--output',
        required=True,
        help='Path to output watermarked audio file'
    )
    encode_parser.add_argument(
        '--message',
        required=True,
        help='Message to embed (format depends on --format option)'
    )
    encode_parser.add_argument(
        '--format',
        choices=['numeric', 'text', 'binary'],
        default='text',
        help='Message format: numeric (5 comma-separated integers 0-255), text (string), or binary (40-bit string)'
    )
    encode_parser.add_argument(
        '--model',
        choices=['16k', '44.1k'],
        default='44.1k',
        help='Model type to use (default: 44.1k)'
    )
    encode_parser.add_argument(
        '--play',
        action='store_true',
        help='Play the encoded audio after encoding (requires pygame)'
    )
    
    # Decode subcommand
    decode_parser = subparsers.add_parser('decode', help='Decode a watermark from an audio file')
    decode_parser.add_argument(
        '--input',
        required=True,
        help='Path to watermarked audio file'
    )
    decode_parser.add_argument(
        '--model',
        choices=['16k', '44.1k'],
        default='44.1k',
        help='Model type to use (default: 44.1k)'
    )
    decode_parser.add_argument(
        '--phase-shift',
        action='store_true',
        help='Use phase shift decoding for robustness (slower but more robust to audio crops)'
    )
    
    return parser.parse_args()


def validate_arguments(args):
    """
    Validate parsed command-line arguments.
    
    Args:
        args: Parsed arguments namespace
        
    Raises:
        ValueError: If arguments are invalid
    """
    # Validate input file exists
    if not os.path.exists(args.input):
        raise ValueError(f"Input file does not exist: {args.input}")
    
    # Validate input file extension
    if not args.input.lower().endswith('.wav'):
        raise ValueError(f"Input file must be a WAV file: {args.input}")
    
    # Validate encode-specific arguments
    if args.command == 'encode':
        # Validate output path
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            raise ValueError(f"Output directory does not exist: {output_dir}")
        
        # Validate message format
        if args.format == 'numeric':
            # Parse and validate numeric message
            try:
                parts = args.message.split(',')
                if len(parts) != 5:
                    raise ValueError(f"Numeric message must have exactly 5 integers, got {len(parts)}")
                
                values = [int(p.strip()) for p in parts]
                for i, val in enumerate(values):
                    if not 0 <= val <= 255:
                        raise ValueError(f"Numeric value at position {i} must be between 0 and 255, got {val}")
            except ValueError as e:
                if "invalid literal" in str(e):
                    raise ValueError(f"Numeric message must contain only integers: {args.message}")
                raise
        
        elif args.format == 'binary':
            # Validate binary message
            clean_binary = args.message.replace(' ', '').replace('_', '')
            if len(clean_binary) != 40:
                raise ValueError(f"Binary message must be exactly 40 bits, got {len(clean_binary)}")
            if not all(c in '01' for c in clean_binary):
                raise ValueError("Binary message must contain only '0' and '1' characters")
        
        elif args.format == 'text':
            # Validate text message
            if not args.message:
                raise ValueError("Text message cannot be empty")


def main():
    """Main entry point for the standalone demo interface."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Validate arguments
        validate_arguments(args)
        
        # Execute command
        if args.command == 'encode':
            run_encode(args)
        elif args.command == 'decode':
            run_decode(args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


def run_encode(args):
    """
    Execute the encoding workflow.
    
    Args:
        args: Parsed command-line arguments
    """
    print("=" * 60)
    print("Audio Watermarking - Encode")
    print("=" * 60)
    
    # Initialize services
    audio_processor = AudioProcessor()
    silentcipher_service = SilentCipherService()
    message_converter = MessageConverter()
    
    # Check if SilentCipher is available
    if not silentcipher_service.is_available():
        raise RuntimeError(
            "SilentCipher library is not installed. "
            "Install with: pip install silentcipher"
        )
    
    # Step 1: Load input audio
    print(f"\n[1/5] Loading input audio: {args.input}")
    try:
        audio_data, sample_rate = audio_processor.load_audio(args.input)
        metadata = audio_processor.get_metadata(audio_data, sample_rate)
        print(f"  ✓ Loaded successfully")
        print(f"    - Duration: {metadata['duration']:.2f} seconds")
        print(f"    - Sample rate: {metadata['sample_rate']} Hz")
        print(f"    - Channels: {metadata['channels']}")
        
        # Validate audio
        if metadata['duration'] < 3.0:
            raise RuntimeError(
                f"Audio too short ({metadata['duration']:.2f}s). "
                f"SilentCipher requires at least 3 seconds of audio for reliable watermarking."
            )
        
        if sample_rate not in [16000, 44100]:
            print(f"  ⚠ Warning: Sample rate is {sample_rate}Hz.")
            print(f"    SilentCipher works best with 16kHz or 44.1kHz.")
            print(f"    Audio will be resampled automatically.")
    except Exception as e:
        raise RuntimeError(f"Failed to load audio: {e}")
    
    # Step 2: Convert message to numeric format
    print(f"\n[2/5] Converting message to numeric format")
    print(f"  Format: {args.format}")
    print(f"  Input: {args.message}")
    
    try:
        if args.format == 'numeric':
            # Parse comma-separated integers
            message_values = [int(p.strip()) for p in args.message.split(',')]
        elif args.format == 'text':
            # Convert text to numeric
            message_values = message_converter.text_to_numeric(args.message)
        elif args.format == 'binary':
            # Convert binary to numeric
            message_values = message_converter.binary_to_numeric(args.message)
        else:
            raise ValueError(f"Unknown format: {args.format}")
        
        print(f"  ✓ Converted to numeric: {message_values}")
    except Exception as e:
        raise RuntimeError(f"Failed to convert message: {e}")
    
    # Step 3: Encode watermark
    print(f"\n[3/5] Encoding watermark using SilentCipher ({args.model} model)")
    print(f"  This may take a moment...")
    
    try:
        watermarked_audio, sdr = silentcipher_service.encode_audio(
            audio_data,
            sample_rate,
            message_values
        )
        print(f"  ✓ Encoding successful")
        print(f"    - SDR: {sdr:.2f} dB")
    except Exception as e:
        raise RuntimeError(f"Failed to encode watermark: {e}")
    
    # Step 4: Save watermarked audio
    print(f"\n[4/5] Saving watermarked audio: {args.output}")
    try:
        audio_processor.save_audio(watermarked_audio, sample_rate, args.output)
        print(f"  ✓ Saved successfully")
    except Exception as e:
        raise RuntimeError(f"Failed to save audio: {e}")
    
    # Step 5: Optional playback
    if args.play:
        print(f"\n[5/5] Playing encoded audio...")
        try:
            play_audio(args.output)
        except Exception as e:
            print(f"  ⚠ Playback failed: {e}")
            print(f"    (Playback is optional - file was saved successfully)")
    else:
        print(f"\n[5/5] Playback skipped (use --play to enable)")
    
    # Display summary
    print("\n" + "=" * 60)
    print("Encoding Complete!")
    print("=" * 60)
    print(f"Output file: {args.output}")
    print(f"SDR value: {sdr:.2f} dB")
    print(f"Message (numeric): {message_values}")
    if args.format == 'text':
        print(f"Message (text): {args.message}")
    elif args.format == 'binary':
        print(f"Message (binary): {args.message}")
    print("=" * 60)


def run_decode(args):
    """
    Execute the decoding workflow.
    
    Args:
        args: Parsed command-line arguments
    """
    print("=" * 60)
    print("Audio Watermarking - Decode")
    print("=" * 60)
    
    # Initialize services
    audio_processor = AudioProcessor()
    silentcipher_service = SilentCipherService()
    message_converter = MessageConverter()
    
    # Check if SilentCipher is available
    if not silentcipher_service.is_available():
        raise RuntimeError(
            "SilentCipher library is not installed. "
            "Install with: pip install silentcipher"
        )
    
    # Step 1: Load input audio
    print(f"\n[1/3] Loading input audio: {args.input}")
    try:
        audio_data, sample_rate = audio_processor.load_audio(args.input)
        metadata = audio_processor.get_metadata(audio_data, sample_rate)
        print(f"  ✓ Loaded successfully")
        print(f"    - Duration: {metadata['duration']:.2f} seconds")
        print(f"    - Sample rate: {metadata['sample_rate']} Hz")
        print(f"    - Channels: {metadata['channels']}")
    except Exception as e:
        raise RuntimeError(f"Failed to load audio: {e}")
    
    # Step 2: Decode watermark
    print(f"\n[2/3] Decoding watermark using SilentCipher ({args.model} model)")
    if args.phase_shift:
        print(f"  Phase shift decoding enabled (this will take longer)")
    print(f"  This may take a moment...")
    
    try:
        result = silentcipher_service.decode_audio(
            audio_data,
            sample_rate,
            phase_shift_decoding=args.phase_shift
        )
        
        if not result['detected']:
            print(f"  ✗ No watermark detected")
            print("\n" + "=" * 60)
            print("Decoding Result: NO WATERMARK FOUND")
            print("=" * 60)
            print("The audio file does not contain a detectable watermark.")
            print("This could mean:")
            print("  - The audio was not watermarked")
            print("  - The watermark was destroyed by processing")
            print("  - The audio quality is too low")
            print("=" * 60)
            return
        
        message_values = result['message']
        confidence = result['confidence']
        
        print(f"  ✓ Watermark detected successfully")
        
    except Exception as e:
        raise RuntimeError(f"Failed to decode watermark: {e}")
    
    # Step 3: Format and display results
    print(f"\n[3/3] Formatting decoded message")
    
    # Convert to other formats
    try:
        text_message = message_converter.numeric_to_text(message_values)
        binary_message = message_converter.numeric_to_binary(message_values)
    except Exception as e:
        print(f"  ⚠ Warning: Could not convert to all formats: {e}")
        text_message = "(conversion failed)"
        binary_message = "(conversion failed)"
    
    # Display results
    print("\n" + "=" * 60)
    print("Decoding Complete - Watermark Detected!")
    print("=" * 60)
    print("\nDecoded Message:")
    print(f"  Numeric:  {message_values}")
    print(f"  Text:     '{text_message}'")
    print(f"  Binary:   {binary_message}")
    
    if confidence is not None:
        print(f"\nConfidence Score: {confidence:.4f}")
        
        # Provide interpretation
        if confidence >= 0.9:
            confidence_level = "Very High"
        elif confidence >= 0.7:
            confidence_level = "High"
        elif confidence >= 0.5:
            confidence_level = "Medium"
        else:
            confidence_level = "Low"
        
        print(f"Confidence Level: {confidence_level}")
    
    print("=" * 60)


def play_audio(file_path: str):
    """
    Play audio file using pygame (optional feature).
    
    Args:
        file_path: Path to audio file to play
        
    Raises:
        ImportError: If pygame is not installed
        RuntimeError: If playback fails
    """
    try:
        import pygame
    except ImportError:
        raise ImportError(
            "pygame is required for audio playback. "
            "Install with: pip install pygame"
        )
    
    try:
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load and play the audio file
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        print(f"  ♪ Playing audio...")
        print(f"    Press Ctrl+C to stop playback")
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        print(f"  ✓ Playback finished")
        
        # Clean up
        pygame.mixer.quit()
        
    except KeyboardInterrupt:
        # User interrupted playback
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        print(f"\n  ⏹ Playback stopped by user")
    except Exception as e:
        pygame.mixer.quit()
        raise RuntimeError(f"Playback failed: {e}")


if __name__ == '__main__':
    main()
