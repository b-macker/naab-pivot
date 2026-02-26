#!/usr/bin/env python3
"""
Example 2: Batch File Processing (Python → Rust)
Original Python implementation with file I/O and data transformation
"""

import sys
import time
import json
import hashlib
from pathlib import Path

def process_batch(data_items):
    """
    Process a batch of data items:
    - Parse JSON
    - Transform data
    - Compute hash
    - Aggregate results
    """
    results = []

    for item in data_items:
        # Parse if string
        if isinstance(item, str):
            try:
                item = json.loads(item)
            except:
                item = {"value": item}

        # Transform
        value = item.get("value", 0)
        transformed = value * 2 + 100

        # Compute hash
        hash_input = f"{value}:{transformed}".encode()
        hash_result = hashlib.sha256(hash_input).hexdigest()[:16]

        # Store result
        results.append({
            "original": value,
            "transformed": transformed,
            "hash": hash_result
        })

    return results

def aggregate_results(results):
    """Aggregate batch results"""
    total = sum(r["transformed"] for r in results)
    count = len(results)
    average = total / count if count > 0 else 0

    return {
        "total": total,
        "count": count,
        "average": average
    }

def process_file_batch(file_paths):
    """
    Process multiple files in batch:
    - Read each file
    - Parse content
    - Process data
    - Aggregate
    """
    all_results = []

    for path in file_paths:
        if Path(path).exists():
            with open(path, 'r') as f:
                content = f.read()
                # Simulate processing
                data = [{"value": i} for i in range(1000)]
                results = process_batch(data)
                all_results.extend(results)

    return aggregate_results(all_results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("READY")
        print("Usage: python3 process_files.py <count>")
        sys.exit(0)

    # Generate test data
    count = int(sys.argv[1])
    test_data = [{"value": i} for i in range(count)]

    # Benchmark
    start = time.time()
    results = process_batch(test_data)
    aggregated = aggregate_results(results)
    end = time.time()

    elapsed_ms = (end - start) * 1000

    # Output
    print(f"Total: {aggregated['total']}")
    print(f"Count: {aggregated['count']}")
    print(f"Average: {aggregated['average']:.2f}")
    print(f"Time: {elapsed_ms:.2f}ms", file=sys.stderr)
