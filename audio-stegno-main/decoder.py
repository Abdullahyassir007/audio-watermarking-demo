import numpy as np

def reverse_bit_interleaving(interleaved_bits, block_size=8):
    """Reverse the bit interleaving process"""
    n = len(interleaved_bits)
    padded_length = ((n + block_size - 1) // block_size) * block_size
    padded_bits = interleaved_bits + [0] * (padded_length - n)

    num_blocks = padded_length // block_size
    # Forward interleave: output[i * num_blocks + b] = input[b * block_size + i]
    # So reverse: original[b * block_size + i] = interleaved[i * num_blocks + b]
    original = [0] * padded_length
    for i in range(block_size):
        for b in range(num_blocks):
            original[b * block_size + i] = padded_bits[i * num_blocks + b]

    return original[:n]

def reverse_arnold_transform(bits, original_length, iterations=2):
    """Reverse Arnold's Cat Map — bits must be full n*n square"""
    n = int(np.sqrt(len(bits)))
    matrix = np.array(bits).reshape(n, n)

    for _ in range(iterations):
        new_matrix = np.zeros_like(matrix)
        for i in range(n):
            for j in range(n):
                orig_i = (2 * i - j) % n
                orig_j = (-i + j) % n
                new_matrix[orig_i, orig_j] = matrix[i, j]
        matrix = new_matrix

    return matrix.flatten().tolist()[:original_length]

def verify_checksum(bits, checksum_bits):
    """Verify the checksum matches the extracted bits"""
    calculated_checksum = sum(bits) % 256
    extracted_checksum = int("".join(map(str, checksum_bits)), 2)
    return calculated_checksum == extracted_checksum

def extract_blindly(stego_audio):
    print(f"    -> Starting multi-layer extraction process...")
    
    # 1. Extract with position hopping (matching embedder)
    hop_distance = 7
    current_pos = 100
    
    # First, extract sync pattern and headers to determine length
    header_size = 8 + 16 + 8  # sync + length + checksum
    header_bits = []
    
    for _ in range(header_size):
        if current_pos >= len(stego_audio):
            current_pos = current_pos % len(stego_audio)
        header_bits.append(stego_audio[current_pos] & 1)
        current_pos += hop_distance
    
    # 2. Verify sync pattern
    sync_pattern = header_bits[0:8]
    expected_sync = [1, 0, 1, 0, 1, 0, 1, 0]
    if sync_pattern == expected_sync:
        print(f"    -> ✓ Sync pattern detected")
    else:
        print(f"    -> ✗ WARNING: Sync pattern mismatch")
    
    # 3. Extract length header (original pre-arnold length)
    length_bits = header_bits[8:24]
    msg_length = int("".join(map(str, length_bits)), 2)
    print(f"    -> Message length detected: {msg_length} bits")

    # 4. Extract checksum
    checksum_bits = header_bits[24:32]
    print(f"    -> Checksum extracted: {int(''.join(map(str, checksum_bits)), 2)}")

    # 5. Compute full arnold square size to know how many bits to extract
    n = int(np.sqrt(msg_length))
    if n * n < msg_length:
        n += 1
    arnold_size = n * n

    # 6. Extract the arnold data bits (full square)
    data_bits = []
    for _ in range(arnold_size):
        if current_pos >= len(stego_audio):
            current_pos = current_pos % len(stego_audio)
        data_bits.append(stego_audio[current_pos] & 1)
        current_pos += hop_distance

    print(f"    -> Extracted {len(data_bits)} arnold bits (n={n}, square={arnold_size})")

    # 7. Verify checksum
    is_valid = verify_checksum(data_bits, checksum_bits)
    if is_valid:
        print(f"    -> ✓ Checksum verification PASSED")
    else:
        print(f"    -> ✗ WARNING: Checksum verification FAILED")

    # 8. Reverse Arnold transform (trim to msg_length inside)
    unscrambled_bits = reverse_arnold_transform(data_bits, msg_length, iterations=2)
    print(f"    -> Reversed Arnold Cat Map transformation")

    # 9. Reverse bit interleaving
    original_bits = reverse_bit_interleaving(unscrambled_bits, block_size=8)
    print(f"    -> Reversed bit interleaving")

    return original_bits