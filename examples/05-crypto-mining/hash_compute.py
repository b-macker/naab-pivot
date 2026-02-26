#!/usr/bin/env python3
"""
Example 5: Cryptographic Hash Mining (Python → Rust + SIMD)
Original Python implementation with SHA-256 brute-force search
"""

import hashlib
import time
import sys

def mine_hash(prefix, target_difficulty):
    """
    Find a nonce that produces a hash with N leading zeros

    This simulates proof-of-work mining like Bitcoin/Ethereum:
    - Compute SHA-256 hash of prefix + nonce
    - Check if hash starts with N zeros
    - If not, increment nonce and try again

    Args:
        prefix: String to prepend to nonce
        target_difficulty: Number of leading zeros required

    Returns:
        (nonce, hash) tuple when solution found
    """
    nonce = 0
    target = '0' * target_difficulty

    print(f"Mining hash with {target_difficulty} leading zeros...")
    print(f"Target pattern: {target}...")

    start_time = time.time()
    last_report = start_time

    while True:
        # Construct data to hash
        data = f"{prefix}{nonce}".encode('utf-8')

        # Compute SHA-256 hash
        hash_result = hashlib.sha256(data).hexdigest()

        # Check if we found a solution
        if hash_result.startswith(target):
            elapsed = time.time() - start_time
            print(f"\n✓ Solution found!")
            print(f"  Nonce: {nonce}")
            print(f"  Hash: {hash_result}")
            print(f"  Time: {elapsed:.2f}s")
            print(f"  Hashes/sec: {nonce / elapsed:.2f}")
            return nonce, hash_result

        # Progress reporting (every 5 seconds)
        now = time.time()
        if now - last_report >= 5.0:
            elapsed = now - start_time
            rate = nonce / elapsed if elapsed > 0 else 0
            print(f"  Tried {nonce:,} nonces in {elapsed:.1f}s ({rate:.2f} hashes/sec)")
            last_report = now

        nonce += 1

def mine_batch(prefix, difficulties):
    """Mine multiple targets for benchmarking"""
    results = []

    for difficulty in difficulties:
        print(f"\n{'='*60}")
        print(f"Target difficulty: {difficulty} leading zeros")
        print('='*60)

        start = time.time()
        nonce, hash_val = mine_hash(prefix, difficulty)
        elapsed = time.time() - start

        results.append({
            'difficulty': difficulty,
            'nonce': nonce,
            'hash': hash_val,
            'time_seconds': elapsed,
            'hashes_per_second': nonce / elapsed
        })

    return results

def calculate_energy_consumption(time_seconds, cpu_cores=1, tdp_watts=65):
    """
    Estimate energy consumption based on execution time

    Args:
        time_seconds: Execution time in seconds
        cpu_cores: Number of CPU cores used
        tdp_watts: CPU thermal design power (typical: 65W for desktop)

    Returns:
        Energy in joules
    """
    # Assume CPU runs at 80% TDP under full load
    power_watts = tdp_watts * 0.8 * (cpu_cores / 4.0)  # Normalize to 4 cores
    energy_joules = power_watts * time_seconds
    return energy_joules

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Single difficulty mode
        difficulty = int(sys.argv[1])
        prefix = sys.argv[2] if len(sys.argv) > 2 else "block_data_"

        start = time.time()
        nonce, hash_val = mine_hash(prefix, difficulty)
        elapsed = time.time() - start

        energy = calculate_energy_consumption(elapsed, cpu_cores=1)

        print(f"\nPerformance Summary:")
        print(f"  Time: {elapsed:.2f}s")
        print(f"  Hashes: {nonce:,}")
        print(f"  Rate: {nonce / elapsed:.2f} hashes/sec")
        print(f"  Energy: {energy:.2f} joules")
    else:
        # Benchmark mode - test multiple difficulties
        print("╔══════════════════════════════════════════════╗")
        print("║  Cryptographic Hash Mining Benchmark        ║")
        print("║  Python SHA-256 Proof-of-Work                ║")
        print("╚══════════════════════════════════════════════╝\n")

        difficulties = [4, 5]  # 4 zeros = ~65K attempts, 5 zeros = ~1M attempts
        results = mine_batch("block_data_", difficulties)

        print("\n" + "="*60)
        print("BENCHMARK RESULTS")
        print("="*60)

        total_time = 0
        total_hashes = 0

        for r in results:
            print(f"\nDifficulty {r['difficulty']}:")
            print(f"  Nonce: {r['nonce']:,}")
            print(f"  Time: {r['time_seconds']:.2f}s")
            print(f"  Rate: {r['hashes_per_second']:.2f} hashes/sec")

            energy = calculate_energy_consumption(r['time_seconds'])
            print(f"  Energy: {energy:.2f} joules")

            total_time += r['time_seconds']
            total_hashes += r['nonce']

        print(f"\nTotal:")
        print(f"  Time: {total_time:.2f}s")
        print(f"  Hashes: {total_hashes:,}")
        print(f"  Average rate: {total_hashes / total_time:.2f} hashes/sec")
        print(f"  Total energy: {calculate_energy_consumption(total_time):.2f} joules")
