import numpy as np
import wave

def text_to_bits(text):
    bits = []
    for char in text:
        bits.extend([int(b) for b in format(ord(char), '08b')])
    return bits

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte_chunk = bits[i:i+8]
        if len(byte_chunk) == 8:
            byte_str = "".join(map(str, byte_chunk))
            try:
                # Manual conversion to handle potential stray bits
                char_code = int(byte_str, 2)
                chars.append(chr(char_code))
            except:
                chars.append("?") # Placeholder for failed bits
    return "".join(chars)

def read_wav(file_path):
    """Reads a wav file and returns the parameters and audio samples as a numpy array."""
    with wave.open(file_path, 'rb') as wav:
        params = wav.getparams()
        n_frames = wav.getnframes()
        frames = wav.readframes(n_frames)
        
        # Determine bit depth
        if params.sampwidth == 1: # 8-bit
            dtype = np.uint8
        else: # 16-bit is most common
            dtype = np.int16
            
        samples = np.frombuffer(frames, dtype=dtype)
    return params, samples

def write_wav(file_path, params, samples):
    """Writes a numpy array of samples back into a playable wav file."""
    with wave.open(file_path, 'wb') as wav:
        wav.setparams(params)
        wav.writeframes(samples.tobytes())

def calculate_metrics(original, stego):
    # Convert to float to avoid overflow during squaring
    orig = original.astype(np.float64)
    steg = stego.astype(np.float64)
    
    mse = np.mean((orig - steg)**2)
    if mse == 0:
        psnr = 100
    else:
        # Standard PSNR formula for 16-bit audio
        max_pixel = 65535.0
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return mse, psnr