# Test fixture: Python code with loops for optimization
import time

def heavy_computation(n):
    """Compute-intensive function with loops"""
    result = 0.0
    for i in range(n):
        result += (i ** 2) ** 0.5
    return result

def nested_loops(n):
    """Nested loop test"""
    total = 0
    for i in range(n):
        for j in range(n):
            total += i * j
    return total

def factorial(n):
    """Recursive function"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

if __name__ == "__main__":
    print(heavy_computation(1000))
    print(nested_loops(100))
    print(factorial(10))
