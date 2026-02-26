#!/usr/bin/env python3
"""
Example 3: ML Model Inference Optimization (Python → C++)
Original NumPy-based neural network inference
"""

import sys
import time
import math

def sigmoid(x):
    """Sigmoid activation function"""
    return 1.0 / (1.0 + math.exp(-x))

def relu(x):
    """ReLU activation function"""
    return max(0.0, x)

def matrix_multiply(A, B):
    """Simple matrix multiplication (m×n) × (n×p) = (m×p)"""
    m, n = len(A), len(A[0])
    n2, p = len(B), len(B[0])

    if n != n2:
        raise ValueError("Matrix dimensions don't match")

    result = [[0.0 for _ in range(p)] for _ in range(m)]

    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]

    return result

def vector_add(a, b):
    """Element-wise vector addition"""
    return [a[i] + b[i] for i in range(len(a))]

def apply_activation(vec, activation='relu'):
    """Apply activation function to vector"""
    if activation == 'relu':
        return [relu(x) for x in vec]
    elif activation == 'sigmoid':
        return [sigmoid(x) for x in vec]
    else:
        return vec

def forward_pass(input_vec, weights, biases):
    """
    Neural network forward pass:
    - Input layer: 784 features (28×28 image)
    - Hidden layer 1: 256 neurons (ReLU)
    - Hidden layer 2: 128 neurons (ReLU)
    - Output layer: 10 classes (Sigmoid)
    """
    # Layer 1: 784 → 256
    h1 = matrix_multiply([input_vec], weights[0])[0]
    h1 = vector_add(h1, biases[0])
    h1 = apply_activation(h1, 'relu')

    # Layer 2: 256 → 128
    h2 = matrix_multiply([h1], weights[1])[0]
    h2 = vector_add(h2, biases[1])
    h2 = apply_activation(h2, 'relu')

    # Layer 3: 128 → 10
    output = matrix_multiply([h2], weights[2])[0]
    output = vector_add(output, biases[2])
    output = apply_activation(output, 'sigmoid')

    return output

def batch_inference(inputs, weights, biases):
    """Run inference on batch of inputs"""
    results = []
    for input_vec in inputs:
        output = forward_pass(input_vec, weights, biases)
        prediction = output.index(max(output))
        results.append(prediction)
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("READY")
        print("Usage: python3 slow_inference.py <batch_size>")
        sys.exit(0)

    batch_size = int(sys.argv[1])

    # Initialize dummy weights and biases
    # Layer 1: 784 → 256
    weights = [
        [[0.01 * (i + j) for j in range(256)] for i in range(784)],
        [[0.01 * (i + j) for j in range(128)] for i in range(256)],
        [[0.01 * (i + j) for j in range(10)] for i in range(128)]
    ]

    biases = [
        [0.1] * 256,
        [0.1] * 128,
        [0.1] * 10
    ]

    # Generate dummy input batch (28×28 flattened images)
    inputs = [[0.5 * (i % 255) / 255.0 for i in range(784)] for _ in range(batch_size)]

    # Benchmark
    start = time.time()
    results = batch_inference(inputs, weights, biases)
    end = time.time()

    elapsed_ms = (end - start) * 1000
    throughput = batch_size / (elapsed_ms / 1000.0)

    # Output
    print(f"Batch size: {batch_size}")
    print(f"Predictions: {results[:10]}...")  # First 10 predictions
    print(f"Time: {elapsed_ms:.2f}ms", file=sys.stderr)
    print(f"Throughput: {throughput:.2f} inferences/sec", file=sys.stderr)
