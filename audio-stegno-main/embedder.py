import numpy as np

def apply_bit_interleaving(bits, block_size=8):
    """Interleave bits: reads column-by-column across blocks"""
    n = len(bits)
    padded_length = ((n + block_size - 1) // block_size) * block_size
    padded_bits = bits + [0] * (padded_length - n)

    num_blocks = padded_length // block_size
    # output[i * num_blocks + b] = input[b * block_size + i]
    interleaved = [0] * padded_length
    for i in range(block_size):
        for b in range(num_blocks):
            interleaved[i * num_blocks + b] = padded_bits[b * block_size + i]

    return interleaved[:n]

def calculate_checksum(bits):
    """Calculate a simple 8-bit checksum for error detection"""
    checksum = sum(bits) % 256
    checksum_bits = [int(b) for b in format(checksum, '08b')]
    return checksum_bits

def apply_arnold_transform(bits, iterations=2):
    """Apply Arnold's Cat Map on full n*n square, returns full padded list"""
    n = int(np.sqrt(len(bits)))
    if n * n < len(bits):
        n += 1
    padded = bits + [0] * (n * n - len(bits))
    matrix = np.array(padded).reshape(n, n)

    for _ in range(iterations):
        new_matrix = np.zeros_like(matrix)
        for i in range(n):
            for j in range(n):
                new_i = (i + j) % n
                new_j = (i + 2 * j) % n
                new_matrix[new_i, new_j] = matrix[i, j]
        matrix = new_matrix

    # Return full n*n so decoder can invert cleanly, caller trims to original length
    return matrix.flatten().tolist()

def embed_with_header(audio_samples, encrypted_bits):
    stego_audio = audio_samples.copy()
    
    print(f"    -> Starting multi-layer embedding process...")
    
    # 1. Apply bit interleaving
    interleaved_bits = apply_bit_interleaving(encrypted_bits, block_size=8)
    print(f"    -> Applied bit interleaving (block size: 8)")
    
    # 2. Apply Arnold transform (returns full n*n padded list)
    arnold_bits = apply_arnold_transform(interleaved_bits, iterations=2)
    print(f"    -> Applied Arnold Cat Map transformation (2 iterations)")

    # 3. Calculate checksum on the arnold output (full padded)
    checksum_bits = calculate_checksum(arnold_bits)
    print(f"    -> Checksum calculated: {int(''.join(map(str, checksum_bits)), 2)}")

    # 4. Store original (pre-pad) length in header so decoder knows how many bits to recover
    msg_length = len(interleaved_bits)  # original length before arnold padding
    header_bits = [int(b) for b in bin(msg_length)[2:].zfill(16)]
    
    # 5. Create sync pattern (8 bits: 10101010) for detection
    sync_pattern = [1, 0, 1, 0, 1, 0, 1, 0]
    
    # 6. Combine: Sync + Length Header + Checksum + Arnold Data
    total_payload = sync_pattern + header_bits + checksum_bits + arnold_bits
    print(f"    -> Total payload: {len(total_payload)} bits (sync:8 + length:16 + checksum:8 + data:{len(arnold_bits)})")
    
    if len(total_payload) > len(stego_audio):
        raise ValueError(f"Audio too short! Need {len(total_payload)} samples, have {len(stego_audio)}")
    
    # 7. Multi-bit embedding with position hopping
    hop_distance = 7  # Prime number for better distribution
    current_pos = 100  # Start offset
    
    for bit in total_payload:
        if current_pos >= len(stego_audio):
            current_pos = current_pos % len(stego_audio)
        
        # Standard LSB replacement
        stego_audio[current_pos] = (stego_audio[current_pos] & ~1) | bit
        current_pos += hop_distance
    
    print(f"    -> Embedded using position hopping (distance: {hop_distance})")
    
    return stego_audio