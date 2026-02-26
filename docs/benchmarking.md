# Benchmarking Guide

**Performance Tracking and Regression Detection**

---

## Quick Start

```bash
# Run benchmark suite
./naab/build/naab-lang benchmark.naab vessels/

# Generate HTML report
./naab/build/naab-lang benchmark.naab vessels/ --format html > report.html

# Regression detection
./naab/build/naab-lang benchmark.naab vessels/ \
  --baseline baseline.json \
  --regression-threshold 5
```

---

## Benchmark Specifications

**File:** `compute.bench.json`

```json
{
  "name": "compute_benchmark",
  "vessel": "vessels/compute_vessel",
  "iterations": 100,
  "warmup": 10,
  "timeout_ms": 10000,
  "inputs": [
    {"n": 1000000},
    {"n": 10000000},
    {"n": 100000000}
  ]
}
```

---

## Running Benchmarks

### Single Benchmark

```naab
use benchmark

main {
    let result = benchmark.run_single_benchmark("compute.bench.json")

    io.write("Mean: ", result["mean"], "ms\n")
    io.write("Median: ", result["median"], "ms\n")
    io.write("P95: ", result["p95"], "ms\n")
    io.write("P99: ", result["p99"], "ms\n")
}
```

### Benchmark Suite

```naab
use benchmark

main {
    let report = benchmark.run_suite("./vessels/")

    for result in report["results"] {
        io.write(result["benchmark"], ": ", result["mean"], "ms\n")
    }
}
```

---

## Statistical Analysis

### Metrics Collected

- **Mean:** Average execution time
- **Median:** Middle value (50th percentile)
- **Min/Max:** Fastest/slowest execution
- **Standard Deviation:** Variability measure
- **P95/P99:** 95th/99th percentile (tail latency)

### Example Output

```json
{
  "benchmark": "heavy_computation",
  "iterations": 100,
  "statistics": {
    "mean": 812.34,
    "median": 812.00,
    "min": 810.00,
    "max": 815.00,
    "stddev": 1.42,
    "p95": 814.50,
    "p99": 815.00
  }
}
```

---

## Regression Detection

### Setup Baseline

```bash
# First run - establish baseline
./naab/build/naab-lang benchmark.naab vessels/ --save-baseline baseline.json
```

### Compare Against Baseline

```bash
# Subsequent runs - detect regressions
./naab/build/naab-lang benchmark.naab vessels/ \
  --baseline baseline.json \
  --regression-threshold 10
```

**Output:**

```
  [BENCHMARK] Comparing against baseline...
    compute_vessel: 812ms (baseline: 800ms) → +1.5% ✓
    process_vessel: 1234ms (baseline: 1100ms) → +12.2% ⚠ REGRESSION
```

**Exit code 6 if regression detected**

---

## Report Formats

### JSON Report

```bash
./naab/build/naab-lang benchmark.naab vessels/ --format json > report.json
```

**Output:**

```json
{
  "timestamp": 1234567890,
  "results": [...],
  "baseline": {...},
  "regressions": []
}
```

### HTML Report

```bash
./naab/build/naab-lang benchmark.naab vessels/ --format html > report.html
```

Includes:
- Interactive charts (Chart.js)
- Performance trends
- Regression highlights
- Comparison tables

### CSV Report

```bash
./naab/build/naab-lang benchmark.naab vessels/ --format csv > report.csv
```

**Format:**

```csv
benchmark,mean,median,min,max,stddev,p95,p99
compute,812.34,812.00,810.00,815.00,1.42,814.50,815.00
```

### SARIF Report

```bash
./naab/build/naab-lang benchmark.naab vessels/ --format sarif > report.sarif
```

Upload to GitHub Code Scanning for regression tracking.

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Performance Benchmarks

on: [push, pull_request]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive

      - name: Build NAAb
        run: bash build.sh

      - name: Run Benchmarks
        run: |
          ./naab/build/naab-lang benchmark.naab vessels/ \
            --baseline baseline.json \
            --regression-threshold 5 \
            --format sarif > benchmark.sarif

      - name: Upload Results
        if: always()
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: benchmark.sarif
```

---

## Best Practices

### 1. Sufficient Iterations

Use at least 100 iterations for statistical significance:

```json
{
  "iterations": 100,
  "warmup": 10
}
```

### 2. Control Environment

Run benchmarks on consistent hardware:

```bash
# Disable CPU frequency scaling
sudo cpupower frequency-set --governor performance

# Run benchmarks
./naab/build/naab-lang benchmark.naab vessels/

# Re-enable scaling
sudo cpupower frequency-set --governor powersave
```

### 3. Isolate Workloads

Close other applications during benchmarking:

```bash
# Check CPU usage
top -b -n 1 | head -20

# Run benchmarks when system is idle
./naab/build/naab-lang benchmark.naab vessels/
```

### 4. Track Historical Data

Store benchmark results over time:

```bash
# Timestamp results
DATE=$(date +%Y-%m-%d)
./naab/build/naab-lang benchmark.naab vessels/ \
  --format json > "benchmark-history/$DATE.json"
```

### 5. Set Realistic Thresholds

Allow some variance (5-10%):

```bash
# Too strict (may have false positives)
--regression-threshold 1

# Recommended
--regression-threshold 10
```

---

## Advanced Features

### Custom Test Inputs

```json
{
  "name": "matrix_multiply",
  "inputs": [
    {"size": 100, "density": 0.1},
    {"size": 500, "density": 0.5},
    {"size": 1000, "density": 1.0}
  ]
}
```

### Memory Profiling

```bash
# Track memory usage
/usr/bin/time -v ./vessels/compute_vessel 10000000 2>&1 | grep "Maximum resident"
```

### Parallel Benchmarking

```naab
// Run multiple benchmarks in parallel
use benchmark

main {
    let bench_files = ["compute.bench.json", "process.bench.json", "transform.bench.json"]

    // Run in parallel (if supported)
    let results = []
    for bench_file in bench_files {
        let result = benchmark.run_single_benchmark(bench_file)
        results.push(result)
    }
}
```

---

**Next:** [Plugins Guide](plugins.md) | [Troubleshooting](troubleshooting.md)
