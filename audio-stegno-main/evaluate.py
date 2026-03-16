import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import wave
import time
import os

from utilities import read_wav, write_wav, text_to_bits, bits_to_text, calculate_metrics
from logistic_mapper import generate_quantum_chaotic_sequence, scramble_bits
from embedder import embed_with_header
from decoder import extract_blindly

# ── Config ──────────────────────────────────────────────────────────────────
INPUT_WAV  = "sample.wav"
OUTPUT_WAV = "stego_audio.wav"
SECRET_TEXT = "Hello World"
SEED, MU   = 0.618, 3.9
PLOTS_DIR  = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
def bit_accuracy(original_text, decoded_text):
    orig_bits = text_to_bits(original_text)
    # Pad or trim decoded to same length
    dec_bits  = text_to_bits(decoded_text[:len(original_text)])
    dec_bits += [0] * (len(orig_bits) - len(dec_bits))
    correct = sum(o == d for o, d in zip(orig_bits, dec_bits))
    return correct / len(orig_bits) * 100

def snr(original, stego):
    orig = original.astype(np.float64)
    steg = stego.astype(np.float64)
    signal_power = np.mean(orig ** 2)
    noise_power  = np.mean((orig - steg) ** 2)
    if noise_power == 0:
        return float('inf')
    return 10 * np.log10(signal_power / noise_power)

def compute_ber(original_text, decoded_text):
    orig_bits = text_to_bits(original_text)
    dec_bits  = text_to_bits(decoded_text[:len(original_text)])
    dec_bits += [0] * (len(orig_bits) - len(dec_bits))
    errors = sum(o != d for o, d in zip(orig_bits, dec_bits))
    return errors / len(orig_bits)

# ── Run Pipeline ─────────────────────────────────────────────────────────────
print("=" * 55)
print("  QUANTUM-CHAOTIC STEGANOGRAPHY — EVALUATION SUITE")
print("=" * 55)

t_start = time.time()

# Sender
bits          = text_to_bits(SECRET_TEXT)
key           = generate_quantum_chaotic_sequence(len(bits), seed_theta=SEED, mu=MU)
encrypted     = scramble_bits(bits, key)
params, orig  = read_wav(INPUT_WAV)
stego         = embed_with_header(orig, encrypted)
write_wav(OUTPUT_WAV, params, stego)

# Receiver
_, recv       = read_wav(OUTPUT_WAV)
extracted     = extract_blindly(recv)
dec_key       = generate_quantum_chaotic_sequence(len(extracted), seed_theta=SEED, mu=MU)
dec_bits      = scramble_bits(extracted, dec_key)
decoded_text  = bits_to_text(dec_bits)

t_total = time.time() - t_start

# ── Metrics ──────────────────────────────────────────────────────────────────
mse, psnr_val = calculate_metrics(orig, stego)
snr_val       = snr(orig, stego)
ber           = compute_ber(SECRET_TEXT, decoded_text)
acc           = bit_accuracy(SECRET_TEXT, decoded_text)
diff          = np.abs(orig.astype(np.float64) - stego.astype(np.float64))
max_diff      = diff.max()
mean_diff     = diff.mean()

print(f"\n  Original  : '{SECRET_TEXT}'")
print(f"  Decoded   : '{decoded_text}'")
print(f"\n{'─'*55}")
print(f"  MSE                  : {mse:.6f}")
print(f"  PSNR                 : {psnr_val:.2f} dB")
print(f"  SNR                  : {snr_val:.2f} dB")
print(f"  BER                  : {ber:.4f}  ({ber*100:.2f}%)")
print(f"  Bit Accuracy         : {acc:.2f}%")
print(f"  Max Sample Diff      : {max_diff:.0f}")
print(f"  Mean Sample Diff     : {mean_diff:.4f}")
print(f"  Total Time           : {t_total:.2f}s")
print(f"{'─'*55}\n")

# ── Plot 1: Waveform Comparison ───────────────────────────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(14, 8))
fig.suptitle("Waveform Analysis: Original vs Stego Audio", fontsize=14, fontweight='bold')

t = np.arange(len(orig))
axes[0].plot(t, orig,  color='steelblue', linewidth=0.4, alpha=0.9)
axes[0].set_title("Original Audio")
axes[0].set_ylabel("Amplitude")
axes[0].set_xlim(0, len(orig))

axes[1].plot(t, stego, color='darkorange', linewidth=0.4, alpha=0.9)
axes[1].set_title("Stego Audio (after embedding)")
axes[1].set_ylabel("Amplitude")
axes[1].set_xlim(0, len(orig))

axes[2].plot(t, diff,  color='crimson', linewidth=0.4, alpha=0.9)
axes[2].set_title(f"Difference Signal  (max={max_diff:.0f}, mean={mean_diff:.4f})")
axes[2].set_ylabel("| Δ Amplitude |")
axes[2].set_xlabel("Sample Index")
axes[2].set_xlim(0, len(orig))

plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/01_waveform_comparison.png", dpi=150)
plt.close()
print(f"  [✓] Saved 01_waveform_comparison.png")

# ── Plot 2: Spectrogram Comparison ───────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Spectrogram Comparison", fontsize=14, fontweight='bold')

sample_rate = params.framerate
axes[0].specgram(orig,  Fs=sample_rate, cmap='viridis')
axes[0].set_title("Original Audio Spectrogram")
axes[0].set_xlabel("Time (s)")
axes[0].set_ylabel("Frequency (Hz)")

axes[1].specgram(stego, Fs=sample_rate, cmap='viridis')
axes[1].set_title("Stego Audio Spectrogram")
axes[1].set_xlabel("Time (s)")
axes[1].set_ylabel("Frequency (Hz)")

plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/02_spectrogram_comparison.png", dpi=150)
plt.close()
print(f"  [✓] Saved 02_spectrogram_comparison.png")

# ── Plot 3: LSB Distribution ──────────────────────────────────────────────────
orig_lsb  = orig  & 1
stego_lsb = stego & 1

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle("LSB Distribution: Original vs Stego", fontsize=14, fontweight='bold')

for ax, lsb, label, color in zip(
    axes,
    [orig_lsb, stego_lsb],
    ["Original", "Stego"],
    ["steelblue", "darkorange"]
):
    counts = [np.sum(lsb == 0), np.sum(lsb == 1)]
    ax.bar(["LSB=0", "LSB=1"], counts, color=color, edgecolor='black', alpha=0.85)
    ax.set_title(f"{label} LSB Distribution")
    ax.set_ylabel("Count")
    for i, c in enumerate(counts):
        ax.text(i, c + len(lsb)*0.005, f"{c/len(lsb)*100:.1f}%", ha='center', fontsize=10)

plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/03_lsb_distribution.png", dpi=150)
plt.close()
print(f"  [✓] Saved 03_lsb_distribution.png")

# ── Plot 4: Quantum Chaotic Key Visualisation ─────────────────────────────────
key_vis_len = 200
key_vis = generate_quantum_chaotic_sequence(key_vis_len, seed_theta=SEED, mu=MU)

# Also show the logistic map trajectory
logistic_vals = []
curr = SEED
for _ in range(key_vis_len):
    logistic_vals.append(curr)
    x_n = curr / np.pi
    curr = MU * x_n * (1 - x_n) * np.pi

fig, axes = plt.subplots(2, 2, figsize=(14, 8))
fig.suptitle("Quantum Chaotic Key Analysis", fontsize=14, fontweight='bold')

# Key bitstream
axes[0, 0].step(range(key_vis_len), key_vis, color='purple', linewidth=0.8)
axes[0, 0].set_title("Quantum Key Bitstream (first 200 bits)")
axes[0, 0].set_xlabel("Bit Index")
axes[0, 0].set_ylabel("Bit Value")
axes[0, 0].set_ylim(-0.2, 1.2)

# Key as heatmap (10x20 grid)
key_matrix = np.array(key_vis).reshape(10, 20)
im = axes[0, 1].imshow(key_matrix, cmap='RdYlGn', aspect='auto', interpolation='nearest')
axes[0, 1].set_title("Key Bit Heatmap (10×20)")
axes[0, 1].set_xlabel("Column")
axes[0, 1].set_ylabel("Row")
plt.colorbar(im, ax=axes[0, 1])

# Logistic map trajectory
axes[1, 0].plot(range(key_vis_len), logistic_vals, color='teal', linewidth=0.8)
axes[1, 0].set_title(f"Logistic Map Trajectory (μ={MU}, seed={SEED})")
axes[1, 0].set_xlabel("Iteration")
axes[1, 0].set_ylabel("Value")

# Key autocorrelation (randomness check)
key_centered = np.array(key_vis) - np.mean(key_vis)
autocorr = np.correlate(key_centered, key_centered, mode='full')
autocorr = autocorr[len(autocorr)//2:]
autocorr /= autocorr[0]
axes[1, 1].plot(autocorr[:80], color='darkred', linewidth=1)
axes[1, 1].axhline(0, color='black', linewidth=0.5, linestyle='--')
axes[1, 1].set_title("Key Autocorrelation (lower = more random)")
axes[1, 1].set_xlabel("Lag")
axes[1, 1].set_ylabel("Correlation")

plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/04_quantum_key_analysis.png", dpi=150)
plt.close()
print(f"  [✓] Saved 04_quantum_key_analysis.png")

# ── Plot 5: Metrics Summary Bar Chart ────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(13, 5))
fig.suptitle("Evaluation Metrics Summary", fontsize=14, fontweight='bold')

# PSNR / SNR
metrics_names = ["PSNR (dB)", "SNR (dB)"]
metrics_vals  = [psnr_val, snr_val]
bars = axes[0].bar(metrics_names, metrics_vals, color=['steelblue', 'seagreen'], edgecolor='black', alpha=0.85)
axes[0].set_title("Signal Quality")
axes[0].set_ylabel("dB")
for bar, val in zip(bars, metrics_vals):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f"{val:.2f}", ha='center', fontsize=11)

# BER
axes[1].bar(["BER"], [ber], color='crimson', edgecolor='black', alpha=0.85)
axes[1].set_title("Bit Error Rate")
axes[1].set_ylabel("BER")
axes[1].set_ylim(0, max(ber * 2, 0.1))
axes[1].text(0, ber + 0.002, f"{ber:.4f}", ha='center', fontsize=11)

# Bit Accuracy
axes[2].bar(["Bit Accuracy"], [acc], color='goldenrod', edgecolor='black', alpha=0.85)
axes[2].set_title("Bit Accuracy")
axes[2].set_ylabel("%")
axes[2].set_ylim(0, 110)
axes[2].text(0, acc + 1, f"{acc:.1f}%", ha='center', fontsize=11)

plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/05_metrics_summary.png", dpi=150)
plt.close()
print(f"  [✓] Saved 05_metrics_summary.png")

# ── Plot 6: Sample-level Difference Histogram ────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(diff[diff > 0], bins=10, color='darkorange', edgecolor='black', alpha=0.85)
ax.set_title("Distribution of Sample Differences (Original vs Stego)", fontsize=13)
ax.set_xlabel("Absolute Difference")
ax.set_ylabel("Number of Samples")
ax.set_yscale('log')
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}/06_difference_histogram.png", dpi=150)
plt.close()
print(f"  [✓] Saved 06_difference_histogram.png")

print(f"\n  All plots saved to '{PLOTS_DIR}/' folder.")
print("=" * 55)
