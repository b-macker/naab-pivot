#!/usr/bin/env python3
"""
Example 1: Basic Python → Go Evolution
Original slow Python implementation
"""

import time
import sys

def heavy_computation(n):
    """Compute-intensive function with mathematical operations"""
    result = 0.0
    for i in range(n):
        result += (i ** 2) ** 0.5
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("READY")
        print("Usage: python3 slow.py <number>")
        sys.exit(0)

    n = int(sys.argv[1])

    start = time.time()
    result = heavy_computation(n)
    end = time.time()

    elapsed_ms = (end - start) * 1000

    print(f"Result: {result:.15f}")
    print(f"Time: {elapsed_ms:.2f}ms", file=sys.stderr)
