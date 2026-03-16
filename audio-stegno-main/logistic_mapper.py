import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def generate_quantum_chaotic_sequence(length, seed_theta=0.618, mu=3.9):
    backend = AerSimulator()
    key = []
    
    # 1. Pre-calculate angles with FIXED PRECISION
    angles = []
    curr = seed_theta
    for _ in range(length):
        # We round to 10 decimal places to prevent float-point drift
        angles.append(round(curr, 10))
        
        x_n = curr / np.pi
        x_next = mu * x_n * (1 - x_n)
        curr = x_next * np.pi

    # 2. Batch Processing (24 bits at a time)
    batch_size = 24 
    for i in range(0, length, batch_size):
        current_batch_len = min(batch_size, length - i)
        qc = QuantumCircuit(current_batch_len, current_batch_len)
        
        for j in range(current_batch_len):
            qc.ry(angles[i + j], j)
            qc.measure(j, j)
        
        t_qc = transpile(qc, backend)
        # We use a fixed seed for the simulator to ensure perfect reproducibility
        job = backend.run(t_qc, shots=1, memory=True, seed_simulator=42)
        result = job.result()
        
        bitstring = result.get_memory()[0] 
        # Reverse to fix Little-Endian ordering
        ordered_bits = [int(b) for b in bitstring[::-1]]
        key.extend(ordered_bits)

    return key[:length]

def scramble_bits(bits, key):
    # Ensure they are the same length
    return [b ^ k for b, k in zip(bits, key)]