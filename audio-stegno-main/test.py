from utilities import read_wav, write_wav, text_to_bits, bits_to_text, calculate_metrics
from logistic_mapper import generate_quantum_chaotic_sequence, scramble_bits
from embedder import embed_with_header
from decoder import extract_blindly
import time
import numpy as np


# --- INITIALIZATION ---
start_total = time.time()
print(f"[{time.strftime('%H:%M:%S')}] Initializing Quantum-Chaotic Steganography Pipeline...")

INPUT_WAV = "sample.wav"
OUTPUT_WAV = "stego_audio.wav"
SECRET_TEXT = "SSN College Of Engineering"
SEED, MU = 0.618, 3.9

# --- STEP 1: SENDER SIDE (ENCRYPTION & EMBEDDING) ---
print(f"\n[{time.strftime('%H:%M:%S')}] --- SENDER PHASE ---")
print(f"[{time.strftime('%H:%M:%S')}] 1. Converting text message to bitstream...")
bits = text_to_bits(SECRET_TEXT)
print(f"    -> Message: '{SECRET_TEXT}' ({len(bits)} bits)")

print(f"[{time.strftime('%H:%M:%S')}] 2. Generating Quantum Chaotic Key (Seed: {SEED})...")
t_key = time.time()
key = generate_quantum_chaotic_sequence(len(bits), seed_theta=SEED, mu=MU)
print(f"    -> Key generated in {time.time() - t_key:.2f}s")

print(f"[{time.strftime('%H:%M:%S')}] 3. Scrambling message bits with Quantum Key (XOR)...")
encrypted_bits = scramble_bits(bits, key)

print(f"[{time.strftime('%H:%M:%S')}] 4. Loading carrier audio and embedding data...")
params, samples = read_wav(INPUT_WAV)
stego_samples = embed_with_header(samples, encrypted_bits)
write_wav(OUTPUT_WAV, params, stego_samples)
print(f"    -> Stego-audio saved as '{OUTPUT_WAV}'")

# --- STEP 2: RECEIVER SIDE (EXTRACTION & DECRYPTION) ---
print(f"\n[{time.strftime('%H:%M:%S')}] --- RECEIVER PHASE ---")
print(f"[{time.strftime('%H:%M:%S')}] 1. Reading stego-audio file...")
_, received_samples = read_wav(OUTPUT_WAV)

print(f"[{time.strftime('%H:%M:%S')}] 2. Performing Blind Extraction (Detecting Header)...")
extracted_payload = extract_blindly(received_samples)

print(f"[{time.strftime('%H:%M:%S')}] 3. Regenerating matching Quantum Key...")
dec_key = generate_quantum_chaotic_sequence(len(extracted_payload), seed_theta=SEED, mu=MU)

print(f"[{time.strftime('%H:%M:%S')}] 4. Descrambling and reconstructing text...")
decrypted_bits = scramble_bits(extracted_payload, dec_key)
final_message = bits_to_text(decrypted_bits)

# --- FINAL RESULTS ---
print("\n" + "="*40)
print(f"DECODED MESSAGE: {final_message}")
print(f"TOTAL EXECUTION TIME: {time.time() - start_total:.2f}s")
print("="*40)

# --- QUALITY ANALYSIS ---
mse, psnr = calculate_metrics(samples, stego_samples)
print(f"\n--- QUALITY METRICS (Original vs Stego) ---")
print(f"  > Mean Squared Error (MSE): {mse:.8f}")
print(f"  > Peak Signal-to-Noise Ratio (PSNR): {psnr:.2f} dB")
print("  > Result: " + ("Indistinguishable/Excellent" if psnr > 80 else "Good/Visible"))
print("-" * 40)