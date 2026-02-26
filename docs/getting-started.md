# Getting Started with NAAb Pivot

**Transform slow interpreted code into blazing-fast compiled code with mathematical parity proof.**

NAAb Pivot automatically analyzes performance bottlenecks, generates optimized code in compiled languages (Go, C++, Rust), validates correctness, and proves speedups.

---

## Table of Contents

- [Quick Start (5 Minutes)](#quick-start-5-minutes)
- [Installation](#installation)
  - [Linux / macOS](#linux--macos)
  - [Windows](#windows)
  - [Docker](#docker)
- [Your First Evolution](#your-first-evolution)
- [Understanding the Output](#understanding-the-output)
- [Next Steps](#next-steps)
- [Troubleshooting](#troubleshooting)

---

## Quick Start (5 Minutes)

```bash
# 1. Clone with submodules
git clone --recursive https://github.com/b-macker/naab-pivot.git
cd naab-pivot

# 2. Build NAAb language
bash build.sh

# 3. Analyze slow code
./naab/build/naab-lang pivot.naab analyze examples/01-basic-evolution/slow.py

# 4. Run full evolution pipeline
./naab/build/naab-lang pivot.naab evolve examples/01-basic-evolution/slow.py --profile balanced

# 5. View results
cat vessels/benchmark-report.json
```

**Expected Output:**
```json
{
  "status": "EVOLUTION_COMPLETE",
  "speedup": 3.5,
  "parity_certified": true,
  "confidence": 99.99
}
```

---

## Installation

### Prerequisites

**Required:**
- Git with submodule support
- CMake 3.15+
- C++ compiler (GCC 9+, Clang 10+, MSVC 2019+)
- Make or Ninja

**Optional (for target languages):**
- Go 1.21+ (for Go vessel generation)
- Rust 1.70+ (for Rust vessel generation)
- GCC/Clang (for C++ vessel generation)
- Ruby 3.0+ (for Ruby vessel generation)
- Node.js 18+ (for JavaScript vessel generation)
- PHP 8.0+ (for PHP vessel generation)
- Zig 0.11+ (for Zig vessel generation)
- Julia 1.9+ (for Julia vessel generation)

### Linux / macOS

#### Option 1: Quick Install (Recommended)

```bash
# Clone repository with submodules
git clone --recursive https://github.com/b-macker/naab-pivot.git
cd naab-pivot

# Build NAAb language (takes 2-5 minutes)
bash build.sh

# Optionally install system-wide
sudo bash install.sh
```

#### Option 2: Manual Build

```bash
# Clone repository
git clone https://github.com/b-macker/naab-pivot.git
cd naab-pivot

# Initialize submodules
git submodule update --init --recursive

# Build NAAb
cd naab
mkdir -p build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make naab-lang -j$(nproc)

# Test installation
./naab-lang --version
```

#### Verify Installation

```bash
# Check NAAb binary
./naab/build/naab-lang --version
# Expected: NAAb Language Interpreter v1.0.0

# Check Pivot CLI
./naab/build/naab-lang pivot.naab --help
# Expected: Shows Pivot command help

# Run test suite
cd tests
bash run-all-tests.sh
# Expected: All tests pass
```

### Windows

#### Option 1: Using WSL2 (Recommended)

```powershell
# Install WSL2 (Windows Subsystem for Linux)
wsl --install

# Launch WSL2
wsl

# Follow Linux installation steps above
```

#### Option 2: Native Windows Build

```powershell
# Install dependencies
# - Visual Studio 2019+ with C++ tools
# - CMake 3.15+
# - Git for Windows

# Clone repository
git clone --recursive https://github.com/b-macker/naab-pivot.git
cd naab-pivot

# Build with CMake
cd naab
mkdir build
cd build
cmake .. -G "Visual Studio 16 2019"
cmake --build . --config Release

# Test
.\Release\naab-lang.exe --version
```

### Docker

**Pull from Docker Hub:**

```bash
docker pull bmacker/naab-pivot:latest

# Run analysis
docker run --rm -v $(pwd):/workspace bmacker/naab-pivot:latest \
  naab-lang /opt/naab-pivot/pivot.naab analyze /workspace/slow.py

# Run full evolution
docker run --rm -v $(pwd):/workspace bmacker/naab-pivot:latest \
  naab-lang /opt/naab-pivot/pivot.naab evolve /workspace/slow.py
```

**Build locally:**

```bash
git clone --recursive https://github.com/b-macker/naab-pivot.git
cd naab-pivot

# Build image
docker build -t naab-pivot .

# Run container
docker run -it --rm -v $(pwd)/workspace:/workspace naab-pivot
```

**Docker Compose (with dashboard):**

```bash
# Start all services
docker-compose up -d

# Access dashboard
open http://localhost:8080

# Stop services
docker-compose down
```

---

## Your First Evolution

Let's optimize a slow Python function step-by-step.

### Step 1: Create Source File

```bash
cd ~/naab-pivot
mkdir -p workspace
```

**Create `workspace/slow_compute.py`:**

```python
import time

def heavy_computation(n):
    """Compute-intensive calculation"""
    result = 0.0
    for i in range(n):
        result += (i ** 2) ** 0.5
    return result

if __name__ == "__main__":
    start = time.time()
    result = heavy_computation(10_000_000)
    elapsed = time.time() - start
    print(f"Result: {result}")
    print(f"Time: {elapsed * 1000:.2f}ms")
```

**Test the original:**

```bash
python3 workspace/slow_compute.py
# Expected: ~2500-3000ms
```

### Step 2: Analyze for Optimization

```bash
./naab/build/naab-lang pivot.naab analyze workspace/slow_compute.py > workspace/analysis.json
```

**Output (`analysis.json`):**

```json
{
  "status": "ANALYZED",
  "source": "PYTHON",
  "functions": [
    {
      "name": "heavy_computation",
      "line_start": 3,
      "line_count": 6,
      "complexity": 8,
      "has_loops": true,
      "target": "GO",
      "reason": "High complexity with loops detected"
    }
  ]
}
```

**What this means:**
- ✅ Detected 1 function: `heavy_computation`
- ✅ Complexity score: 8 (medium-high)
- ✅ Recommended target: **Go** (good for loops + concurrency)
- 💡 Estimated speedup: 3-5x

### Step 3: Generate Optimized Vessel

```bash
./naab/build/naab-lang pivot.naab synthesize workspace/analysis.json
```

**Output:**

```
  [SYNTHESIZER] Loading blueprint: workspace/analysis.json
  [SYNTHESIZER] Generating heavy_computation (GO)...
    ✓ Code generated: vessels/heavy_computation_GO.go
    ✓ Compiling...
    ✓ Compilation successful: vessels/heavy_computation_vessel
```

**Generated Go code (`vessels/heavy_computation_GO.go`):**

```go
package main
import ("fmt"; "math"; "os"; "strconv"; "time")

func heavyComputation(n int) float64 {
    result := 0.0
    for i := 0; i < n; i++ {
        result += math.Sqrt(math.Pow(float64(i), 2))
    }
    return result
}

func main() {
    start := time.Now()
    result := heavyComputation(10_000_000)
    elapsed := time.Since(start)
    fmt.Printf("Result: %f\n", result)
    fmt.Printf("Time: %.2fms\n", float64(elapsed.Microseconds())/1000.0)
}
```

### Step 4: Validate Parity

```bash
./naab/build/naab-lang pivot.naab validate workspace/slow_compute.py vessels/heavy_computation_vessel
```

**Output:**

```
  [VALIDATOR] Comparing implementations...
    Legacy: workspace/slow_compute.py
    Vessel: vessels/heavy_computation_vessel

  Running 100 test cases...
  ✓ Test 0: ✓ (error: 0.00001%)
  ✓ Test 1: ✓ (error: 0.00002%)
  ...
  ✓ Test 99: ✓ (error: 0.00001%)

  ═══════════════════════════════════════════════
  ✅ PARITY CERTIFIED
  ═══════════════════════════════════════════════

  Test cases: 100
  Passed: 100
  Failed: 0
  Confidence: 99.99%

  Performance:
    Legacy: 2843ms
    Vessel: 812ms
    Speedup: 3.5x ⚡
```

**What this means:**
- ✅ Mathematical proof: Both implementations produce identical results
- ✅ Statistical confidence: 99.99%
- ✅ Performance gain: **3.5x faster**
- ✅ Safe to deploy in production

### Step 5: Full Pipeline (All-in-One)

```bash
./naab/build/naab-lang pivot.naab evolve workspace/slow_compute.py --profile balanced
```

This runs all steps automatically: analyze → synthesize → validate → benchmark

---

## Understanding the Output

### Analysis Report

```json
{
  "status": "ANALYZED",
  "source": "PYTHON",
  "functions": [
    {
      "name": "heavy_computation",
      "line_start": 3,
      "line_count": 6,
      "complexity": 8,
      "has_loops": true,
      "target": "GO",
      "reason": "High complexity with loops detected"
    }
  ]
}
```

**Fields:**
- `status`: "ANALYZED" (success) or error
- `source`: Source language detected (PYTHON, RUBY, JAVASCRIPT, NAAB)
- `functions`: Array of detected functions
- `complexity`: Cyclomatic complexity score (1-20+)
- `target`: Recommended target language (GO, CPP, RUST)
- `reason`: Why this target was chosen

### Synthesis Report

```json
{
  "status": "SYNTHESIZED",
  "vessels": [
    {
      "name": "heavy_computation",
      "target": "GO",
      "src": "vessels/heavy_computation_GO.go",
      "bin": "vessels/heavy_computation_vessel",
      "status": "COMPILED"
    }
  ]
}
```

**Statuses:**
- `COMPILED`: Successfully compiled, ready to use
- `CACHED`: Using previously compiled version (no changes)
- `INTERPRETED`: Compilation failed, fallback mode
- `ERROR`: Fatal error, check logs

### Validation Report

```json
{
  "certified": true,
  "test_count": 100,
  "performance": {
    "legacy_ms": 2843,
    "vessel_ms": 812,
    "speedup": 3.5
  },
  "statistics": {
    "mean_error": 0.000012,
    "median_error": 0.000008,
    "stddev": 0.000005,
    "max_error": 0.000045
  }
}
```

**Key Fields:**
- `certified`: `true` = parity proven, safe to deploy
- `speedup`: Performance multiplier (3.5 = 3.5x faster)
- `mean_error`: Average deviation (typically < 0.01%)
- `max_error`: Worst-case deviation

---

## Next Steps

### 1. Explore Example Projects

```bash
cd examples/

# Basic tutorial
cd 01-basic-evolution/
cat README.md

# Advanced examples
cd ../05-crypto-mining/
cat README.md

# Real-world microservices
cd ../10-polyglot-microservices/
cat README.md
```

### 2. Try Different Profiles

```bash
# Maximum safety (no unsafe optimizations)
./naab/build/naab-lang pivot.naab evolve slow.py --profile ultra-safe

# Balanced (default)
./naab/build/naab-lang pivot.naab evolve slow.py --profile balanced

# Maximum speed (may use unsafe code)
./naab/build/naab-lang pivot.naab evolve slow.py --profile aggressive
```

### 3. Target Specific Languages

```bash
# Force Rust compilation
./naab/build/naab-lang pivot.naab evolve slow.py --target rust

# Force C++ with SIMD
./naab/build/naab-lang pivot.naab evolve slow.py --target cpp --enable-simd
```

### 4. Generate Reports

```bash
# HTML report with charts
./naab/build/naab-lang pivot.naab evolve slow.py --format html

# CSV for spreadsheets
./naab/build/naab-lang pivot.naab evolve slow.py --format csv

# SARIF for GitHub Code Scanning
./naab/build/naab-lang pivot.naab evolve slow.py --format sarif
```

### 5. Incremental Migration

```bash
# Analyze entire project
./naab/build/naab-lang migrate.naab create_migration_plan /path/to/project

# View migration phases
cat migration-plan.json
```

---

## Troubleshooting

### NAAb Build Fails

**Problem:** `cmake: command not found`

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install cmake build-essential

# macOS
brew install cmake

# Fedora
sudo dnf install cmake gcc-c++
```

---

### Submodule Empty

**Problem:** `naab/` directory exists but is empty

**Solution:**
```bash
cd naab-pivot
git submodule update --init --recursive
bash build.sh
```

---

### Compilation Fails

**Problem:** "Go compiler not found"

**Solution:**
```bash
# Install Go
# Ubuntu/Debian
sudo apt-get install golang-go

# macOS
brew install go

# Or download from https://go.dev/dl/

# Verify
go version
```

---

### Parity Validation Fails

**Problem:** "Parity NOT CERTIFIED - deviation too high"

**Solution:**
1. Check if function uses floating-point arithmetic (precision differences)
2. Try adjusting tolerance:
   ```bash
   export PIVOT_TOLERANCE=0.01  # 1% tolerance
   ```
3. Review function logic for non-deterministic behavior (random, time-based)

---

### Slow Analysis

**Problem:** Analysis takes >5 minutes

**Solution:**
1. Ensure NAAb built in Release mode (not Debug)
2. Check for large files (>1000 LOC) - split into smaller modules
3. Use profile-guided optimization:
   ```bash
   ./naab/build/naab-lang pivot.naab evolve --hotspot-only slow.py
   ```

---

### Permission Denied

**Problem:** `bash: ./naab/build/naab-lang: Permission denied`

**Solution:**
```bash
chmod +x naab/build/naab-lang
```

---

## Getting Help

- **Documentation:** [docs/](../docs/)
- **Examples:** [examples/](../examples/)
- **FAQ:** [docs/faq.md](faq.md)
- **GitHub Issues:** https://github.com/b-macker/naab-pivot/issues
- **Discord:** https://discord.gg/naab-pivot
- **Email:** support@naab-pivot.dev

---

## What's Next?

1. **Read Architecture Guide:** [docs/architecture.md](architecture.md)
2. **Learn CLI Commands:** [docs/cli-reference.md](cli-reference.md)
3. **Explore Profiles:** [docs/profiles.md](profiles.md)
4. **Write Plugins:** [docs/plugins.md](plugins.md)
5. **Contribute:** [docs/contributing.md](contributing.md)

---

**Ready to optimize your code? Let's go! 🚀**
