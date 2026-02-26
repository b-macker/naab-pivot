# Test fixture: Math-heavy Python code
import math

def calculate_pi(iterations):
    """Monte Carlo Pi estimation"""
    inside = 0
    for i in range(iterations):
        x = (i * 1234567) % 10000 / 10000.0
        y = (i * 7654321) % 10000 / 10000.0
        if x*x + y*y <= 1.0:
            inside += 1
    return 4.0 * inside / iterations

def matrix_multiply(n):
    """Simple matrix multiplication"""
    a = [[i+j for j in range(n)] for i in range(n)]
    b = [[i*j for j in range(n)] for i in range(n)]
    c = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c[i][j] += a[i][k] * b[k][j]
    
    return c[0][0]

if __name__ == "__main__":
    print(calculate_pi(10000))
    print(matrix_multiply(50))
