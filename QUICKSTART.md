# NAAb Pivot - Quick Start Guide

**Get started with NAAb Pivot in 5 minutes!**

---

## What is NAAb Pivot?

NAAb Pivot automatically **optimizes slow code** by generating fast compiled versions while **proving correctness** through parity validation.

**Real Results:**
- Python → Go: **3.5x faster**
- Python → Rust: **18x faster** (with SIMD)
- Python → Julia: **60x faster** (with GPU)

---

## Installation

### Option 1: Docker (Recommended)

```bash
docker pull bmacker/naab-pivot:latest
docker run -v $(pwd):/workspace bmacker/naab-pivot analyze slow_code.py
```

### Option 2: From Source

```bash
# Clone repository
git clone --recursive https://github.com/b-macker/naab-pivot.git
cd naab-pivot

# Build NAAb
bash build.sh

# Add to PATH (optional)
export PATH="$PWD/naab/build:$PATH"
```

### Option 3: GitHub Action

```yaml
# .github/workflows/optimize.yml
name: Optimize Code
on: [push]
jobs:
  optimize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: b-macker/naab-pivot@v1
        with:
          file: src/critical_path.py
          profile: balanced
```

---

## 5-Minute Tutorial

### Step 1: Create Slow Code

Create `slow.py`:

```python
# slow.py - Heavy computation
def compute(n):
    result = 0.0
    for i in range(n):
        result += (i ** 2) ** 0.5
    return result

if __name__ == "__main__":
    import time
    start = time.time()
    result = compute(10_000_000)
    print(f"Result: {result}")
    print(f"Time: {(time.time() - start) * 1000:.2f}ms")
```

**Baseline:** ~2,800ms

### Step 2: Analyze

```bash
./naab/build/naab-lang pivot.naab analyze slow.py
```

**Output:**
```json
{
  "status": "ANALYZED",
  "source": "PYTHON",
  "functions": [
    {
      "name": "compute",
      "complexity": 8,
      "target": "GO",
      "reason": "High complexity loop detected"
    }
  ]
}
```

### Step 3: Evolve (Full Pipeline)

```bash
./naab/build/naab-lang pivot.naab evolve slow.py --profile balanced
```

**What Happens:**
1. ✅ Analyzes code (detects hotspots)
2. ✅ Generates optimized Go version
3. ✅ Compiles to binary
4. ✅ Validates parity (proves correctness)
5. ✅ Benchmarks performance

**Output:**
```
╔══════════════════════════════════════════════════════════════╗
║              NAAb Pivot - Evolution Complete                 ║
╚══════════════════════════════════════════════════════════════╝

  [ANALYZER] Detected: compute (Python)
  [SYNTHESIZER] Generated: compute_GO.go
  [COMPILER] Built: vessels/compute_vessel
  [VALIDATOR] Parity: ✅ CERTIFIED (99.99% confidence)
  [BENCHMARK] Performance: 3.5x faster (2843ms → 812ms)

✅ Evolution successful!
  - Original: 2843ms
  - Optimized: 812ms
  - Speedup: 3.5x
  - Memory: 73% reduction
  - Parity: CERTIFIED
```

### Step 4: Use Optimized Version

```bash
./vessels/compute_vessel 10000000
```

**Result:** 812ms (3.5x faster) ✅

---

## Common Use Cases

### Use Case 1: Optimize Single Function

```bash
# Analyze
naab-lang pivot.naab analyze mycode.py > analysis.json

# Review recommendations
cat analysis.json

# Synthesize specific function
naab-lang pivot.naab synthesize analysis.json \
  --function compute \
  --target rust \
  --profile aggressive

# Validate
naab-lang pivot.naab validate mycode.py vessels/compute_vessel

# Benchmark
naab-lang pivot.naab benchmark vessels/
```

### Use Case 2: Batch Optimization

```bash
# Analyze entire project
for file in src/*.py; do
  naab-lang pivot.naab analyze "$file" >> project_analysis.json
done

# Synthesize all hotspots
naab-lang pivot.naab synthesize project_analysis.json \
  --profile balanced \
  --output vessels/

# Validate all
naab-lang pivot.naab validate src/ vessels/

# Generate report
naab-lang pivot.naab benchmark vessels/ \
  --format html \
  --output performance_report.html
```

### Use Case 3: Incremental Migration

```bash
# Create migration plan
naab-lang migrate.naab create-plan ./legacy_project

# Output: migration_plan.json with prioritized functions

# Migrate phase 1 (low-hanging fruit)
naab-lang migrate.naab execute-phase migration_plan.json --phase 1

# Validate phase 1
naab-lang migrate.naab validate-phase migration_plan.json --phase 1

# Continue to phase 2, 3, etc.
```

---

## Configuration

### Create `.pivotrc` in Your Project

```json
{
  "project_name": "my-project",
  "profile": "balanced",
  "targets": ["go", "rust", "cpp"],
  "output_dir": "./vessels",
  "governance": {
    "enabled": true,
    "config": "govern.json"
  }
}
```

### Available Profiles

| Profile | Safety | Speed | Use Case |
|---------|--------|-------|----------|
| `ultra-safe` | Maximum | Moderate | Mission-critical systems |
| `conservative` | High | Good | Production (default) |
| `balanced` | Medium | Very Good | General purpose ✅ |
| `aggressive` | Low | Excellent | Performance-critical |
| `experimental` | Minimal | Maximum | Benchmarking, research |

**Set Profile:**
```bash
naab-lang pivot.naab evolve code.py --profile aggressive
```

---

## Understanding Results

### Parity Validation

**What is Parity?**
- Proves optimized code produces **identical results** to original
- Uses statistical analysis with 99.99% confidence
- Tests 100+ input combinations
- Validates both correctness AND performance

**Parity Report:**
```json
{
  "certified": true,
  "test_count": 100,
  "max_deviation": 0.00001,
  "confidence": 99.99,
  "performance": {
    "legacy_ms": 2843,
    "vessel_ms": 812,
    "speedup": 3.5
  }
}
```

### Performance Metrics

**Speedup Calculation:**
```
Speedup = Original Time / Optimized Time
Example: 2843ms / 812ms = 3.5x
```

**Memory Reduction:**
```
Reduction = (1 - Optimized Memory / Original Memory) × 100%
Example: (1 - 12MB / 45MB) × 100% = 73%
```

---

## Optimization Profiles Explained

### Balanced Profile (Recommended)

```json
{
  "name": "balanced",
  "compiler_flags": {
    "go": "-O2",
    "rust": "-C opt-level=2",
    "cpp": "-O2 -std=c++17"
  },
  "safety": {
    "bounds_checking": true,
    "overflow_checking": true,
    "null_checking": true
  },
  "optimizations": {
    "simd": false,
    "lto": false,
    "inline": "moderate"
  }
}
```

**When to Use:**
- General-purpose optimization
- Production code
- First-time users
- Balanced safety + performance

### Aggressive Profile

```json
{
  "name": "aggressive",
  "compiler_flags": {
    "go": "-O3",
    "rust": "-C opt-level=3",
    "cpp": "-O3 -march=native"
  },
  "safety": {
    "bounds_checking": false,  // Disabled for speed
    "overflow_checking": false,
    "null_checking": true
  },
  "optimizations": {
    "simd": true,  // Enable SIMD
    "lto": true,   // Link-time optimization
    "inline": "aggressive"
  }
}
```

**When to Use:**
- Performance-critical code
- Benchmarking
- After extensive testing
- Non-safety-critical paths

---

## Troubleshooting

### Issue 1: "NAAb binary not found"

**Solution:**
```bash
# Build NAAb
bash build.sh

# Or create symlink
mkdir -p naab/build
ln -s ~/.naab/language/build/naab-lang naab/build/naab-lang
```

### Issue 2: Compilation fails

**Solution:**
```bash
# Check compiler installed
which go   # Go compiler
which g++  # C++ compiler
which rustc  # Rust compiler

# Install missing compilers
# Ubuntu/Debian:
sudo apt install golang g++ rustc

# macOS:
brew install go gcc rust
```

### Issue 3: Parity validation fails

**Possible Causes:**
- Floating-point precision differences
- Non-deterministic algorithms (random, threading)
- External dependencies (files, network)

**Solution:**
```bash
# Increase tolerance
naab-lang pivot.naab validate code.py vessel \
  --tolerance 0.001  # Allow 0.1% deviation

# Or use custom test cases
naab-lang pivot.naab validate code.py vessel \
  --test-cases my_tests.json
```

### Issue 4: Low speedup (< 2x)

**Possible Causes:**
- I/O-bound code (not CPU-bound)
- Already optimized code
- Small input sizes (overhead dominates)

**Solution:**
```bash
# Use profile-guided optimization
naab-lang pivot.naab evolve code.py \
  --profile aggressive \
  --enable-pgo

# Or try different target language
naab-lang pivot.naab evolve code.py --target rust
```

---

## Next Steps

### Learn More

1. **Examples:** Explore `examples/` directory (10 real-world projects)
2. **Documentation:** Read `docs/` guides
3. **API Reference:** See `docs/api-reference.md`
4. **Benchmarking:** Read `docs/benchmarking.md`

### Advanced Features

1. **Plugin System:** Create custom analyzers/synthesizers
2. **Web Dashboard:** Visualize performance trends
3. **CI/CD Integration:** Automate optimization in pipelines
4. **Migration Guide:** Migrate large codebases incrementally

### Example Projects

| Example | Speedup | Description |
|---------|---------|-------------|
| 01-basic-evolution | 3.5x | Simple Python → Go |
| 02-batch-processing | 8x | File processing → Rust |
| 03-ml-optimization | 12x | ML inference → C++ |
| 05-crypto-mining | 18x | Crypto hashing → Rust+SIMD |
| 07-scientific-compute | 60x | Physics sim → Julia+GPU |

**Explore:**
```bash
cd examples/01-basic-evolution
cat README.md  # Read tutorial
```

---

## Getting Help

### Resources

- **Documentation:** `docs/` directory
- **Examples:** `examples/` directory
- **FAQ:** `docs/faq.md`
- **Troubleshooting:** `docs/troubleshooting.md`

### Community

- **GitHub Issues:** Report bugs, request features
- **GitHub Discussions:** Ask questions, share results
- **Contributing:** See `CONTRIBUTING.md`

### Common Questions

**Q: Which language should I target?**
A: Use the analyzer's recommendation, or:
- **Go:** Concurrent workloads, network services
- **Rust:** Safety-critical, high performance
- **C++:** Math-heavy, scientific computing
- **Julia:** Scientific computing, GPU acceleration

**Q: How much speedup can I expect?**
A: Typical: 3-15x, Exceptional: 15-60x (depends on workload)

**Q: Is the optimized code safe?**
A: Yes! Parity validation proves correctness with 99.99% confidence.

**Q: Can I customize the generated code?**
A: Yes! Edit templates in `templates/` directory.

---

## Quick Command Reference

```bash
# Analyze code
naab-lang pivot.naab analyze <file>

# Full evolution
naab-lang pivot.naab evolve <file> [--profile <name>]

# Validate parity
naab-lang pivot.naab validate <original> <optimized>

# Benchmark
naab-lang pivot.naab benchmark <vessels-dir>

# Create migration plan
naab-lang migrate.naab create-plan <project-dir>

# Launch dashboard
naab-lang dashboard.naab

# Run tests
cd tests && bash run-all-tests.sh
```

---

## Example Output

### Successful Evolution

```
╔══════════════════════════════════════════════════════════════╗
║              NAAb Pivot - Evolution Report                   ║
╚══════════════════════════════════════════════════════════════╝

Project: my-project
Profile: balanced
Target: GO

──────────────────────────────────────────────────────────────

Function: compute
  Source: Python (25 lines)
  Target: Go (optimized)
  Complexity: 8 (high)

──────────────────────────────────────────────────────────────

✅ Analysis:     COMPLETE (detected 1 hotspot)
✅ Synthesis:    COMPLETE (generated compute.go)
✅ Compilation:  COMPLETE (built compute_vessel)
✅ Validation:   CERTIFIED (99.99% confidence)
✅ Benchmark:    COMPLETE (3.5x speedup)

──────────────────────────────────────────────────────────────

Performance:
  Original:  2843ms (Python)
  Optimized:  812ms (Go)
  Speedup:   3.5x faster ⚡
  Memory:    45MB → 12MB (73% reduction)

──────────────────────────────────────────────────────────────

Files Created:
  vessels/compute.go       (generated source)
  vessels/compute_vessel   (compiled binary)
  vessels/benchmark.json   (performance data)
  vessels/parity_report.json

──────────────────────────────────────────────────────────────

Next Steps:
  1. Review: cat vessels/compute.go
  2. Test:   ./vessels/compute_vessel 10000000
  3. Integrate: See docs/integration.md

╚══════════════════════════════════════════════════════════════╝
```

---

## Pro Tips

### Tip 1: Start with Balanced Profile
Always begin with `--profile balanced`. Only use `aggressive` after validation.

### Tip 2: Validate Before Production
Run parity validation with production-like workloads:
```bash
naab-lang pivot.naab validate code.py vessel --test-cases prod_tests.json
```

### Tip 3: Use Dashboard for Tracking
Monitor performance trends over time:
```bash
naab-lang dashboard.naab
# Open: http://localhost:8080
```

### Tip 4: Incremental Optimization
Don't optimize everything at once. Focus on hotspots:
```bash
# Profile first
python -m cProfile -o profile.out code.py

# Then optimize top functions
naab-lang pivot.naab evolve code.py --functions "top_3_hotspots"
```

### Tip 5: Version Control Vessels
Track optimized versions in git:
```bash
git add vessels/*.go vessels/*.rs
git commit -m "Add optimized vessels (3.5x speedup)"
```

---

**That's it! You're ready to start optimizing with NAAb Pivot.** 🚀

For more examples, see the `examples/` directory.
For detailed documentation, see `docs/getting-started.md`.

**Happy optimizing!**
