# Example: Slow Python code that needs optimization

def heavy_computation(n):
    """CPU-intensive calculation (slow in Python)"""
    result = 0.0
    for i in range(n):
        result += (i ** 2) ** 0.5
    return result

def fibonacci(n):
    """Inefficient recursive Fibonacci"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def process_data(data):
    """Data processing loop"""
    results = []
    for item in data:
        # Simulated heavy processing
        value = sum([x**2 for x in range(item)])
        results.append(value)
    return results

if __name__ == "__main__":
    import time

    start = time.time()
    result = heavy_computation(10_000_000)
    elapsed = time.time() - start

    print(f"Result: {result:.2f}")
    print(f"Time: {elapsed*1000:.0f}ms")
