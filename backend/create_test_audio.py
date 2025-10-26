#!/usr/bin/env python3
"""
Create a proper test audio file for watermarking demos.

This script generates a 5-second audio file at 44.1kHz with a pleasant tone.
"""

import numpy as np
import soundfile as sf
import os

def create_test_audio(output_path="test_audio_demo.wav", duration=5.0, sample_rate=44100):
    """
    Create a test audio file with multiple frequency components.
    
    Args:
        output_path: Path to save the audio file
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
    """
    print(f"Creating test audio file...")
    print(f"  Duration: {duration} seconds")
    print(f"  Sample rate: {sample_rate} Hz")
    
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create a pleasant multi-tone audio signal
    # Mix of musical notes (A4=440Hz, E5=659Hz, C5=523Hz)
    audio = (
        0.3 * np.sin(2 * np.pi * 440 * t) +  # A4
        0.2 * np.sin(2 * np.pi * 659 * t) +  # E5
        0.15 * np.sin(2 * np.pi * 523 * t) + # C5
        0.1 * np.sin(2 * np.pi * 880 * t) +  # A5
        0.05 * np.random.randn(len(t))       # Add slight noise for realism
    )
    
    # Normalize to prevent clipping
    audio = audio / np.max(np.abs(audio)) * 0.7
    
    # Apply fade in/out to avoid clicks
    fade_samples = int(0.01 * sample_rate)  # 10ms fade
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    audio[:fade_samples] *= fade_in
    audio[-fade_samples:] *= fade_out
    
    # Save the audio file
    sf.write(output_path, audio, sample_rate)
    
    print(f"✓ Created: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    
    return output_path


def check_audio_files(directory="test_audio"):
    """Check all audio files in a directory and report their properties."""
    import glob
    
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return
    
    audio_files = glob.glob(os.path.join(directory, "*.wav"))
    
    if not audio_files:
        print(f"No WAV files found in {directory}")
        return
    
    print(f"\nChecking {len(audio_files)} audio files in {directory}:")
    print("=" * 80)
    
    suitable_files = []
    unsuitable_files = []
    
    for file in sorted(audio_files):
        try:
            info = sf.info(file)
            duration = info.duration
            sample_rate = info.samplerate
            
            # Check if suitable for watermarking
            is_suitable = (
                duration >= 3.0 and
                sample_rate in [16000, 44100]
            )
            
            status = "✓" if is_suitable else "✗"
            
            print(f"{status} {os.path.basename(file)}")
            print(f"   Duration: {duration:.2f}s, Sample rate: {sample_rate}Hz, Channels: {info.channels}")
            
            if is_suitable:
                suitable_files.append(file)
            else:
                unsuitable_files.append(file)
                if duration < 3.0:
                    print(f"   ⚠ Too short (need ≥3s)")
                if sample_rate not in [16000, 44100]:
                    print(f"   ⚠ Unsupported sample rate (need 16kHz or 44.1kHz)")
        
        except Exception as e:
            print(f"✗ {os.path.basename(file)}")
            print(f"   Error: {e}")
            unsuitable_files.append(file)
    
    print("=" * 80)
    print(f"\nSummary:")
    print(f"  Suitable for watermarking: {len(suitable_files)}")
    print(f"  Unsuitable: {len(unsuitable_files)}")
    
    if suitable_files:
        print(f"\n✓ You can use these files for testing:")
        for file in suitable_files[:5]:  # Show first 5
            print(f"  - {file}")
    
    if unsuitable_files and not suitable_files:
        print(f"\n✗ None of the files are suitable for watermarking.")
        print(f"  Creating a proper test file...")
        create_test_audio()


if __name__ == "__main__":
    import sys
    
    print("=" * 80)
    print("Audio Watermarking Test File Creator")
    print("=" * 80)
    
    # Check existing test_audio directory
    if os.path.exists("test_audio"):
        check_audio_files("test_audio")
    else:
        print("\nNo test_audio directory found.")
    
    # Always create a demo file
    print("\n" + "=" * 80)
    print("Creating demo audio file...")
    print("=" * 80)
    create_test_audio("test_audio_demo.wav", duration=5.0, sample_rate=44100)
    
    print("\n" + "=" * 80)
    print("Done!")
    print("=" * 80)
    print("\nYou can now test watermarking with:")
    print("  python standalone_demo.py encode --input test_audio_demo.wav --output watermarked.wav --message 'Hello'")
    print("  python standalone_demo.py decode --input watermarked.wav")
    print("\nOr use the GUI:")
    print("  python standalone_demo_gui.py")
    print("=" * 80)
