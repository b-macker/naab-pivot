# Performance Tuning Guide

**Advanced Optimization Techniques**

---

## Profile-Guided Optimization (PGO)

### 1. Generate Profile Data

**Python:**

```bash
python -m cProfile -o app.prof app.py
```

**Go:**

```bash
go build -o app
./app -cpuprofile=cpu.prof
```

**Rust:**

```bash
cargo build --release
perf record ./target/release/app
perf report > profile.txt
```

### 2. Analyze Hotspots

```bash
./naab/build/naab-lang pivot.naab analyze app.py \
  --profile-data app.prof \
  --hotspot-only
```

### 3. Optimize Hotspots

```bash
./naab/build/naab-lang pivot.naab evolve app.py \
  --profile aggressive \
  --enable-simd \
  --enable-lto
```

---

## SIMD Optimization

### Enable SIMD

```bash
./naab/build/naab-lang pivot.naab evolve slow.py --enable-simd
```

### Custom SIMD Template

**C++ with AVX2:**

```cpp
#include <immintrin.h>

double compute(int n) {
    __m256d sum_vec = _mm256_setzero_pd();
    for (int i = 0; i < n - 3; i += 4) {
        __m256d v = _mm256_set_pd(i+3, i+2, i+1, i);
        __m256d squared = _mm256_mul_pd(v, v);
        __m256d sqrt_v = _mm256_sqrt_pd(squared);
        sum_vec = _mm256_add_pd(sum_vec, sqrt_v);
    }
    return _mm256_reduce_add_pd(sum_vec);
}
```

**Compile:**

```bash
g++ -O3 -march=native -mavx2 compute.cpp -o compute
```

---

## Parallelization

### Go Goroutines

```go
func computeParallel(n int) float64 {
    numCPU := runtime.NumCPU()
    chunkSize := n / numCPU
    results := make([]float64, numCPU)
    var wg sync.WaitGroup

    for i := 0; i < numCPU; i++ {
        wg.Add(1)
        go func(idx int) {
            defer wg.Done()
            start := idx * chunkSize
            end := start + chunkSize
            results[idx] = computeChunk(start, end)
        }(i)
    }

    wg.Wait()
    return sum(results)
}
```

### Rust Rayon

```rust
use rayon::prelude::*;

fn compute_parallel(n: i32) -> f64 {
    (0..n)
        .into_par_iter()
        .map(|i| (i as f64).powi(2).sqrt())
        .sum()
}
```

---

## Memory Optimization

### Stack Allocation

```rust
// ✓ Good: Stack allocation
fn compute(n: usize) -> [f64; 1000] {
    let mut arr = [0.0; 1000];
    for i in 0..n {
        arr[i] = (i as f64).sqrt();
    }
    arr
}

// ✗ Bad: Heap allocation
fn compute_heap(n: usize) -> Vec<f64> {
    let mut vec = Vec::with_capacity(1000);
    for i in 0..n {
        vec.push((i as f64).sqrt());
    }
    vec
}
```

### Memory Pooling

```cpp
class MemoryPool {
    std::vector<double*> pool;
public:
    double* allocate(size_t size) {
        if (!pool.empty()) {
            double* ptr = pool.back();
            pool.pop_back();
            return ptr;
        }
        return new double[size];
    }

    void deallocate(double* ptr) {
        pool.push_back(ptr);
    }
};
```

---

## Cache Optimization

### Data Layout

```cpp
// ✓ Good: Array of Structs (AoS) for cache locality
struct Point {
    double x, y, z;
};
std::vector<Point> points(1000);

// Process sequentially
for (auto& p : points) {
    process(p.x, p.y, p.z);
}
```

### Loop Tiling

```cpp
// ✓ Good: Tiled loop for cache efficiency
for (int ii = 0; ii < n; ii += 64) {
    for (int jj = 0; jj < n; jj += 64) {
        for (int i = ii; i < min(ii+64, n); i++) {
            for (int j = jj; j < min(jj+64, n); j++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}
```

---

## Compiler Optimizations

### Link-Time Optimization (LTO)

```bash
# Go
go build -ldflags="-s -w" -trimpath

# Rust
cargo build --release
# Add to Cargo.toml:
# [profile.release]
# lto = true

# C++
g++ -O3 -flto -fuse-linker-plugin compute.cpp
```

### Inlining

```rust
#[inline(always)]
fn fast_function(x: f64) -> f64 {
    x * x
}
```

---

## Benchmarking Best Practices

### 1. Warmup Iterations

```naab
for i in 0..10 {
    run_function()  // Warmup
}

let start = time.now()
for i in 0..100 {
    run_function()  // Measure
}
let elapsed = time.now() - start
```

### 2. Statistical Significance

Run at least 100 iterations for reliable statistics.

### 3. Control Environment

```bash
# Disable CPU frequency scaling
sudo cpupower frequency-set --governor performance

# Run benchmarks
./naab/build/naab-lang benchmark.naab vessels/

# Re-enable scaling
sudo cpupower frequency-set --governor powersave
```

---

## Profiling Tools

### CPU Profiling

**Linux perf:**

```bash
perf record -g ./vessel
perf report
```

**macOS Instruments:**

```bash
instruments -t "Time Profiler" ./vessel
```

### Memory Profiling

**Valgrind:**

```bash
valgrind --tool=massif ./vessel
ms_print massif.out
```

**Heaptrack:**

```bash
heaptrack ./vessel
heaptrack_gui heaptrack.vessel.*.gz
```

---

## Performance Checklist

- [ ] Profiled application to identify hotspots
- [ ] Used aggressive optimization profile
- [ ] Enabled SIMD instructions
- [ ] Enabled link-time optimization
- [ ] Parallelized independent operations
- [ ] Optimized memory allocation
- [ ] Improved cache locality
- [ ] Benchmarked with sufficient iterations
- [ ] Controlled environment (CPU scaling off)
- [ ] Validated parity after optimizations

---

**Next:** [Security Guide](security.md) | [Troubleshooting](troubleshooting.md)
