# Test fixture: Python file with loops (for analyzer testing)

def heavy_computation(n):
    """Compute-intensive function with nested loops"""
    result = 0.0
    for i in range(n):
        for j in range(100):
            result += (i * j) ** 0.5
    return result

def simple_function(x):
    """Simple function without loops"""
    return x * 2 + 1

def crypto_hash(data):
    """Cryptographic hashing (should recommend Rust)"""
    import hashlib
    return hashlib.sha256(data.encode()).hexdigest()

if __name__ == "__main__":
    result = heavy_computation(1000)
    print(f"Result: {result}")
