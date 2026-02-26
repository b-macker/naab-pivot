# NAAb Pivot Architecture

**System Design & Data Flow Documentation**

This document explains the internal architecture of NAAb Pivot, how components interact, and the data flow through the evolution pipeline.

---

## Table of Contents

- [High-Level Overview](#high-level-overview)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Module Descriptions](#module-descriptions)
- [Template System](#template-system)
- [Plugin Architecture](#plugin-architecture)
- [Caching & Incremental Builds](#caching--incremental-builds)
- [Governance Integration](#governance-integration)
- [Performance Considerations](#performance-considerations)

---

## High-Level Overview

NAAb Pivot follows a **pipeline architecture** with four main stages:

```
┌──────────┐      ┌─────────────┐      ┌───────────┐      ┌────────────┐
│ Analyze  │  →   │ Synthesize  │  →   │ Validate  │  →   │ Benchmark  │
└──────────┘      └─────────────┘      └───────────┘      └────────────┘
     ↓                   ↓                    ↓                  ↓
  AST Parse        Code Generation      Parity Check      Performance
  Complexity       Template Render       Statistical       Metrics
  Detection        Compilation           Validation        Tracking
```

### Design Principles

1. **Composability:** Each stage can run independently
2. **Idempotency:** Running twice produces same result
3. **Incremental:** Only recompile when source changes
4. **Extensibility:** Plugin system for custom analyzers/synthesizers
5. **Safety:** Governance system enforces security policies

---

## Component Architecture

```
naab-pivot/
├── Core CLI (pivot.naab)
│   └── Orchestrates pipeline stages
│
├── Analysis Engine (analyze.naab)
│   ├── Language Detection
│   ├── AST Parsing
│   ├── Complexity Analysis
│   └── Target Recommendation
│
├── Synthesis Engine (synthesize.naab)
│   ├── Template Engine
│   ├── Code Generation
│   ├── Compilation Manager
│   └── Vessel Cache
│
├── Validation Engine (validate.naab)
│   ├── Test Case Generator
│   ├── Execution Harness
│   ├── Statistical Analysis
│   └── Parity Engine
│
├── Benchmark Engine (benchmark.naab)
│   ├── Performance Profiling
│   ├── Metrics Collection
│   ├── Regression Detection
│   └── Report Generation
│
└── Support Modules
    ├── Config Manager
    ├── Plugin Loader
    ├── Dependency Analyzer
    ├── Hotspot Detector
    └── Report Generator
```

### Core Dependencies

- **NAAb Language:** Polyglot interpreter (C++)
- **AST Parsers:** Python (ast), Ruby (Ripper), JS (acorn)
- **Compilers:** Go, Rust (rustc), C++ (g++/clang)
- **Template Engine:** String interpolation with profiles
- **Governance Engine:** govern.json enforcement

---

## Data Flow

### Full Evolution Pipeline

```
Input: slow_code.py
    ↓
┌─────────────────────────────────────────────────┐
│ 1. ANALYZE STAGE                                │
│                                                 │
│  ┌──────────────┐      ┌────────────────┐     │
│  │ Detect Lang  │  →   │ Parse AST      │     │
│  └──────────────┘      └────────────────┘     │
│         ↓                      ↓               │
│  ┌──────────────┐      ┌────────────────┐     │
│  │ Extract Func │  →   │ Calc Complexity│     │
│  └──────────────┘      └────────────────┘     │
│         ↓                                      │
│  ┌──────────────┐                             │
│  │ Recommend    │                             │
│  │ Target Lang  │                             │
│  └──────────────┘                             │
│         ↓                                      │
│  Output: blueprint.json                        │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ 2. SYNTHESIZE STAGE                             │
│                                                 │
│  Input: blueprint.json                          │
│         ↓                                      │
│  ┌──────────────┐      ┌────────────────┐     │
│  │ Load Profile │  →   │ Select Template│     │
│  └──────────────┘      └────────────────┘     │
│         ↓                      ↓               │
│  ┌──────────────┐      ┌────────────────┐     │
│  │ Render Code  │  →   │ Check Cache    │     │
│  └──────────────┘      └────────────────┘     │
│         ↓                      ↓               │
│  ┌──────────────┐      ┌────────────────┐     │
│  │ Compile (if  │  →   │ Generate Binary│     │
│  │   needed)    │      │   (vessel)     │     │
│  └──────────────┘      └────────────────┘     │
│         ↓                                      │
│  Output: vessel binary + metadata              │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ 3. VALIDATE STAGE                               │
│                                                 │
│  Input: legacy code + vessel binary             │
│         ↓                                      │
│  ┌──────────────┐      ┌────────────────┐     │
│  │ Generate     │  →   │ Run Legacy     │     │
│  │ Test Cases   │      │ Implementation │     │
│  └──────────────┘      └────────────────┘     │
│         ↓                      ↓               │
│  ┌──────────────┐      ┌────────────────┐     │
│  │ Run Vessel   │  →   │ Compare Results│     │
│  │ Implementation│      │                │     │
│  └──────────────┘      └────────────────┘     │
│         ↓                      ↓               │
│  ┌──────────────┐      ┌────────────────┐     │
│  │ Statistical  │  →   │ Certify Parity │     │
│  │ Analysis     │      │ (99.99% conf)  │     │
│  └──────────────┘      └────────────────┘     │
│         ↓                                      │
│  Output: certification + statistics            │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ 4. BENCHMARK STAGE                              │
│                                                 │
│  Input: certified vessels                       │
│         ↓                                      │
│  ┌──────────────┐      ┌────────────────┐     │
│  │ Run          │  →   │ Collect        │     │
│  │ Iterations   │      │ Timings        │     │
│  └──────────────┘      └────────────────┘     │
│         ↓                      ↓               │
│  ┌──────────────┐      ┌────────────────┐     │
│  │ Calculate    │  →   │ Detect         │     │
│  │ Statistics   │      │ Regressions    │     │
│  └──────────────┘      └────────────────┘     │
│         ↓                      ↓               │
│  ┌──────────────┐      ┌────────────────┐     │
│  │ Generate     │  →   │ Export         │     │
│  │ Reports      │      │ (JSON/HTML/CSV)│     │
│  └──────────────┘      └────────────────┘     │
│         ↓                                      │
│  Output: benchmark report + historical data    │
└─────────────────────────────────────────────────┘
    ↓
Final Output: Optimized vessel + certification + benchmarks
```

### Data Formats

#### 1. Analysis Blueprint (JSON)

```json
{
  "status": "ANALYZED",
  "source": "PYTHON",
  "file_path": "/path/to/slow_code.py",
  "timestamp": 1234567890,
  "functions": [
    {
      "name": "heavy_computation",
      "line_start": 10,
      "line_count": 25,
      "complexity": 12,
      "has_loops": true,
      "has_recursion": false,
      "target": "GO",
      "reason": "High loop complexity, good for goroutines",
      "dependencies": ["math", "time"],
      "hotspot_score": 85.3
    }
  ]
}
```

#### 2. Synthesis Manifest (JSON)

```json
{
  "status": "SYNTHESIZED",
  "profile": "balanced",
  "vessels": [
    {
      "name": "heavy_computation",
      "target": "GO",
      "src": "vessels/heavy_computation_GO.go",
      "bin": "vessels/heavy_computation_vessel",
      "status": "COMPILED",
      "compile_time_ms": 1234,
      "binary_size_bytes": 1847296,
      "checksum": "sha256:abc123..."
    }
  ],
  "cache_hits": 0,
  "cache_misses": 1
}
```

#### 3. Validation Certificate (JSON)

```json
{
  "certified": true,
  "confidence": 99.99,
  "test_count": 1000,
  "passed": 1000,
  "failed": 0,
  "performance": {
    "legacy_ms": 2843.52,
    "vessel_ms": 812.34,
    "speedup": 3.50,
    "latency_reduction": 71.43
  },
  "statistics": {
    "mean_error": 0.000012,
    "median_error": 0.000008,
    "stddev": 0.000005,
    "max_error": 0.000045,
    "ks_statistic": 0.032,
    "ks_p_value": 0.876
  },
  "timestamp": 1234567890
}
```

#### 4. Benchmark Report (JSON)

```json
{
  "benchmark_id": "bench_1234567890",
  "vessel": "heavy_computation_vessel",
  "iterations": 100,
  "timings_ms": [812, 815, 810, ...],
  "statistics": {
    "mean": 812.34,
    "median": 812.00,
    "min": 810.00,
    "max": 815.00,
    "stddev": 1.42,
    "p95": 814.50,
    "p99": 815.00
  },
  "baseline": {
    "mean": 2843.52,
    "regression_threshold": 10.0,
    "regression_detected": false
  },
  "environment": {
    "os": "linux",
    "arch": "x86_64",
    "cpu": "Intel i7-9700K",
    "cores": 8,
    "ram_gb": 32
  }
}
```

---

## Module Descriptions

### 1. Analyzer (analyze.naab)

**Purpose:** Detect optimization opportunities

**Workflow:**
1. Detect source language via file extension
2. Parse source code into AST (language-specific)
3. Extract function definitions
4. Calculate cyclomatic complexity
5. Recommend target language based on heuristics

**Language-Specific Parsing:**

```python
# Python AST
<<python[source]
import ast
tree = ast.parse(source)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        # Extract function metadata
>>
```

```ruby
# Ruby Ripper
<<ruby[source]
require 'ripper'
sexp = Ripper.sexp(source)
# Parse S-expressions
>>
```

```javascript
# JavaScript Acorn
<<javascript[source]
const acorn = require('acorn');
const ast = acorn.parse(source);
// Walk AST
>>
```

**Complexity Metrics:**
- Loop count (for/while)
- Conditional branches (if/else)
- Recursion depth
- Line count
- Function call density

**Target Language Heuristics:**
- **Go:** High loop count, concurrency opportunities
- **C++:** Math-heavy, SIMD potential, template metaprogramming
- **Rust:** Safety-critical, crypto, ownership complexity

### 2. Synthesizer (synthesize.naab)

**Purpose:** Generate optimized vessel code

**Workflow:**
1. Load optimization profile (ultra-safe → aggressive)
2. Select appropriate template for target language
3. Render code with variable substitution
4. Check vessel cache (SHA-256 hash)
5. Compile if needed (incremental)
6. Store vessel binary + metadata

**Template Rendering:**

```naab
let template = file.read("templates/go_template.naab")
let code = template
code = string.replace(code, "${FUNCTION_NAME}", func_spec["name"])
code = string.replace(code, "${ITERATIONS}", "" + func_spec["complexity"])
code = string.replace(code, "${OPTIMIZATION_FLAGS}", profile["flags"])
```

**Compilation:**

```naab
if target == "GO" {
    <<bash[src, bin, flags]
    go build -o "$bin" -ldflags="$flags" "$src" 2>&1
    >>
} else if target == "RUST" {
    <<bash[src, bin, profile]
    rustc -C opt-level=$profile -o "$bin" "$src" 2>&1
    >>
} else if target == "CPP" {
    <<bash[src, bin, flags]
    g++ -O3 -march=native $flags -o "$bin" "$src" 2>&1
    >>
}
```

### 3. Validator (validate.naab)

**Purpose:** Mathematically prove parity

**Workflow:**
1. Generate test cases (random, edge cases, regression)
2. Execute legacy implementation N times
3. Execute vessel implementation N times
4. Compare results statistically
5. Calculate confidence interval
6. Issue certification or reject

**Statistical Tests:**
1. **Mean Absolute Error (MAE):** Average deviation
2. **Relative Error:** Percentage difference
3. **Kolmogorov-Smirnov Test:** Distribution similarity
4. **Confidence Interval:** 99.99% threshold

**Test Case Generation:**

```naab
fn generate_test_cases(func_spec) {
    let cases = []

    // Random cases
    for i in 0..100 {
        cases.push(random_input(func_spec["signature"]))
    }

    // Edge cases
    cases.push(0)
    cases.push(1)
    cases.push(-1)
    cases.push(max_int)
    cases.push(min_int)

    // Regression cases (from previous runs)
    let regression = load_regression_cases(func_spec["name"])
    cases = array.concat(cases, regression)

    return cases
}
```

### 4. Benchmarker (benchmark.naab)

**Purpose:** Track performance over time

**Workflow:**
1. Load benchmark specifications
2. Run N iterations (configurable)
3. Collect timing data
4. Calculate statistics (mean, median, p95, p99)
5. Compare to baseline (regression detection)
6. Generate reports (JSON, HTML, CSV, SARIF)

**Benchmark Execution:**

```naab
fn run_single_benchmark(bench_spec) {
    let iterations = bench_spec["iterations"] || 100
    let timings = []

    for i in 0..iterations {
        // Warmup
        if i < 10 {
            run_task(bench_spec["task"])
            continue
        }

        // Timed execution
        let start = time.now()
        run_task(bench_spec["task"])
        let duration = time.now() - start
        timings.push(duration)
    }

    return compute_statistics(timings)
}
```

---

## Template System

### Template Structure

```
templates/
├── go_template.naab        # Go codegen
├── cpp_template.naab       # C++ codegen
├── rust_template.naab      # Rust codegen
└── [other languages]
```

### Template Variables

```naab
// Available variables in templates:
${FUNCTION_NAME}        // Original function name
${FUNCTION_ARGS}        // Argument list
${FUNCTION_BODY}        // Translated function body
${ITERATIONS}           // Complexity-based iteration count
${OPTIMIZATION_FLAGS}   // Profile-specific flags
${IMPORTS}              // Required imports/includes
${NAMESPACE}            // Package/namespace
${TYPE_ANNOTATIONS}     // Type hints
```

### Example Template (Go)

```go
package main

import (
    "fmt"
    "math"
    "os"
    "strconv"
    "time"
)

func ${FUNCTION_NAME}(${FUNCTION_ARGS}) ${RETURN_TYPE} {
    ${FUNCTION_BODY}
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("READY")
        return
    }

    // Parse arguments
    ${ARG_PARSING}

    // Execute function
    start := time.Now()
    result := ${FUNCTION_NAME}(${CALL_ARGS})
    elapsed := time.Since(start)

    // Output results
    fmt.Printf("Result: %v\n", result)
    fmt.Printf("Time: %.2fms\n", float64(elapsed.Microseconds())/1000.0)
}
```

---

## Plugin Architecture

### Plugin Types

1. **Analyzers:** Custom language support, specialized detection
2. **Synthesizers:** Custom target languages, specialized code generation
3. **Validators:** Custom testing strategies (fuzz, property-based)

### Plugin Interface

```naab
// Plugin metadata (plugin_name.json)
{
    "id": "ml-detector",
    "type": "analyzer",
    "version": "1.0.0",
    "entry_point": "execute",
    "supported_languages": ["python", "julia"]
}

// Plugin implementation (plugin_name.naab)
export fn execute(input_data) {
    // Plugin logic here
    return {
        "status": "DETECTED",
        "confidence": 0.95,
        "metadata": {...}
    }
}
```

### Plugin Loading

```naab
// Load plugin
use plugin_loader
let plugin_id = plugin_loader.register_plugin("plugins/analyzers/ml_detector.naab", "analyzer")

// Execute plugin
let result = plugin_loader.execute_plugin(plugin_id, {
    "source": source_code,
    "language": "python"
})
```

---

## Caching & Incremental Builds

### Vessel Cache

**Purpose:** Avoid recompilation when source hasn't changed

**Cache Key:** SHA-256 hash of:
- Generated source code
- Optimization profile
- Compiler version
- Target architecture

**Cache Structure:**

```
.cache/
├── vessels/
│   ├── abc123def456.go         # Generated source
│   ├── abc123def456.bin        # Compiled binary
│   └── abc123def456.meta       # Metadata
└── index.json                  # Cache index
```

**Cache Lookup:**

```naab
fn should_rebuild(src_path, bin_path, new_code) {
    // Check if source exists and matches
    if file.exists(src_path) == false { return true }
    if file.exists(bin_path) == false { return true }

    let old_code = file.read(src_path)
    if old_code != new_code { return true }

    // Check cache index
    let hash = compute_hash(new_code + profile + compiler_version)
    if cache_has(hash) {
        io.write("    ✓ Using cached vessel\n")
        return false
    }

    return true
}
```

---

## Governance Integration

### Security Policies

NAAb Pivot enforces `govern.json` policies:

```json
{
  "languages": {
    "allowed": ["python", "cpp", "rust", "go", "bash"]
  },
  "capabilities": {
    "network": {"enabled": false},
    "filesystem": {"mode": "read"}
  },
  "code_quality": {
    "no_secrets": {"level": "hard"},
    "no_placeholders": {"level": "soft"}
  }
}
```

### Enforcement Points

1. **Analyzer:** Checks if source language is allowed
2. **Synthesizer:** Validates generated code against policies
3. **Validator:** Ensures test execution within limits
4. **Benchmarker:** Restricts resource usage

---

## Performance Considerations

### Optimization Strategies

1. **Parallel Compilation:** Compile multiple vessels concurrently
2. **Incremental Builds:** Cache unchanged vessels
3. **Lazy Evaluation:** Only compute when needed
4. **Memory Pooling:** Reuse allocated memory
5. **Profile-Guided Optimization:** Use profiling data to guide optimization

### Bottlenecks & Solutions

| Bottleneck | Solution |
|------------|----------|
| AST parsing | Cache parsed AST, use faster parsers (tree-sitter) |
| Compilation | Parallel compilation, ccache/sccache |
| Validation | Reduce test iterations, parallel execution |
| Benchmarking | Statistical sampling instead of exhaustive |

---

## Future Architecture Enhancements

1. **Distributed Compilation:** Compile vessels on remote servers
2. **ML-Based Optimization:** Train models to predict best target language
3. **GPU Code Generation:** CUDA/OpenCL backend
4. **WebAssembly Support:** Generate WASM modules
5. **Cloud Integration:** AWS Lambda, Google Cloud Functions

---

**Next:** [CLI Reference](cli-reference.md) | [Profiles Guide](profiles.md)
