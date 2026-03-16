"""
ENCODER — Run this on the sender's device.
Embeds a secret message into a carrier WAV file.
Transfer the output stego_audio.wav to the receiver.
"""
from utilities import read_wav, write_wav, text_to_bits
from logistic_mapper import generate_quantum_chaotic_sequence, scramble_bits
from embedder import embed_with_header
import time

# ── CONFIG (must match decode.py on receiver side) ────────────────────────────
INPUT_WAV  = "sample.wav"
OUTPUT_WAV = "stego_audio.wav"
SEED, MU   = 0.618, 3.9
# ─────────────────────────────────────────────────────────────────────────────

SECRET_TEXT = input("Enter secret message to embed: ").strip()
if not SECRET_TEXT:
    print("No message entered. Exiting.")
    exit()

print(f"\n[{time.strftime('%H:%M:%S')}] Starting Quantum-Chaotic Encoder...")
print(f"  Message : '{SECRET_TEXT}'")
print(f"  Carrier : {INPUT_WAV}")
print(f"  Seed    : {SEED}  |  Mu: {MU}")

t = time.time()

bits          = text_to_bits(SECRET_TEXT)
print(f"\n[1] Converted to {len(bits)} bits")

print(f"[2] Generating quantum chaotic key...")
key           = generate_quantum_chaotic_sequence(len(bits), seed_theta=SEED, mu=MU)
print(f"    Key generated in {time.time()-t:.2f}s")

encrypted     = scramble_bits(bits, key)
print(f"[3] Message encrypted with quantum key (XOR)")

params, audio = read_wav(INPUT_WAV)
stego         = embed_with_header(audio, encrypted)
write_wav(OUTPUT_WAV, params, stego)

print(f"\n[✓] Done! Stego audio saved as '{OUTPUT_WAV}'")
print(f"    Transfer '{OUTPUT_WAV}' to the receiver.")
print(f"    They must use Seed={SEED}, Mu={MU} to decode.")
print(f"    Total time: {time.time()-t:.2f}s")
