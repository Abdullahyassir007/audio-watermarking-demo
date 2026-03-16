"""
DECODER — Run this on the receiver's device.
Extracts and decrypts the hidden message from a stego WAV file.
Requires the same SEED and MU used during encoding.
"""
from utilities import read_wav, bits_to_text
from logistic_mapper import generate_quantum_chaotic_sequence, scramble_bits
from decoder import extract_blindly
import time

# ── CONFIG (must match encode.py on sender side) ──────────────────────────────
STEGO_WAV  = "stego_audio.wav"
SEED, MU   = 0.618, 3.9
# ─────────────────────────────────────────────────────────────────────────────

print(f"[{time.strftime('%H:%M:%S')}] Starting Quantum-Chaotic Decoder...")
print(f"  Stego file : {STEGO_WAV}")
print(f"  Seed       : {SEED}  |  Mu: {MU}\n")

t = time.time()

_, stego_audio = read_wav(STEGO_WAV)
print(f"[1] Loaded stego audio ({len(stego_audio)} samples)")

print(f"[2] Extracting hidden bits...")
extracted = extract_blindly(stego_audio)

print(f"\n[3] Regenerating quantum chaotic key ({len(extracted)} bits)...")
key = generate_quantum_chaotic_sequence(len(extracted), seed_theta=SEED, mu=MU)

decrypted = scramble_bits(extracted, key)
message   = bits_to_text(decrypted)

print(f"\n{'='*45}")
print(f"  DECODED MESSAGE: {message}")
print(f"  Time taken     : {time.time()-t:.2f}s")
print(f"{'='*45}")
