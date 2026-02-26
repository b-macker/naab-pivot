# Optimization Profiles

**Deep Dive into Profile System**

NAAb Pivot provides 8 optimization profiles, each balancing safety, performance, and binary size differently. This guide explains each profile and when to use them.

---

## Table of Contents

- [Profile Overview](#profile-overview)
- [Profile Comparison](#profile-comparison)
- [Built-in Profiles](#built-in-profiles)
  - [ultra-safe](#ultra-safe)
  - [conservative](#conservative)
  - [balanced](#balanced)
  - [aggressive](#aggressive)
  - [experimental](#experimental)
  - [minimal](#minimal)
  - [embedded](#embedded)
  - [wasm](#wasm)
- [Custom Profiles](#custom-profiles)
- [Profile Selection Guide](#profile-selection-guide)

---

## Profile Overview

Profiles control:
- **Optimization Level:** -O0 (none) to -O3 (aggressive)
- **Safety Features:** Bounds checking, overflow detection
- **Code Generation:** SIMD, inline assembly, unsafe code
- **Binary Size:** Debug symbols, static linking
- **Target Environment:** Desktop, embedded, web

---

## Profile Comparison

| Profile | Safety | Speed | Size | Use Case |
|---------|--------|-------|------|----------|
| ultra-safe | ⭐⭐⭐⭐⭐ | ⭐⭐ | Large | Safety-critical, medical |
| conservative | ⭐⭐⭐⭐ | ⭐⭐⭐ | Medium | Production, default |
| balanced | ⭐⭐⭐ | ⭐⭐⭐⭐ | Medium | General purpose (default) |
| aggressive | ⭐⭐ | ⭐⭐⭐⭐⭐ | Small | High-performance computing |
| experimental | ⭐ | ⭐⭐⭐⭐⭐ | Small | Research, benchmarking |
| minimal | ⭐⭐⭐ | ⭐⭐⭐ | Tiny | Resource-constrained |
| embedded | ⭐⭐⭐ | ⭐⭐⭐⭐ | Tiny | Embedded systems, IoT |
| wasm | ⭐⭐⭐⭐ | ⭐⭐⭐ | Small | WebAssembly, browsers |

---

## Built-in Profiles

### ultra-safe

**Maximum safety, no unsafe optimizations**

**Configuration:**

```json
{
  "name": "ultra-safe",
  "description": "Maximum safety for critical systems",

  "optimization_level": 1,
  "enable_simd": false,
  "enable_lto": false,
  "enable_unsafe": false,

  "bounds_checking": true,
  "overflow_checking": true,
  "null_checking": true,

  "go": {
    "flags": "-race -gcflags=all=-d=checkptr",
    "env": {"GOEXPERIMENT": "fieldtrack"}
  },

  "rust": {
    "opt_level": 1,
    "flags": "-C overflow-checks=on -C debug-assertions=on",
    "features": []
  },

  "cpp": {
    "optimization": "-O1",
    "flags": "-fno-unsafe-math-optimizations -fstack-protector-strong",
    "defines": []
  }
}
```

**Use Cases:**
- Medical devices
- Aviation software
- Financial systems
- Safety-critical infrastructure

**Trade-offs:**
- ✅ Maximum safety guarantees
- ✅ All runtime checks enabled
- ✅ Easy debugging
- ❌ ~2x slower than aggressive
- ❌ Larger binaries

**Example:**

```bash
./naab/build/naab-lang pivot.naab evolve critical.py --profile ultra-safe
```

---

### conservative

**Safety-first, minimal aggressive optimizations**

**Configuration:**

```json
{
  "name": "conservative",
  "description": "Safety-first production profile",

  "optimization_level": 2,
  "enable_simd": false,
  "enable_lto": false,
  "enable_unsafe": false,

  "bounds_checking": true,
  "overflow_checking": true,
  "null_checking": true,

  "go": {
    "flags": "-trimpath",
    "env": {}
  },

  "rust": {
    "opt_level": 2,
    "flags": "-C overflow-checks=on",
    "features": []
  },

  "cpp": {
    "optimization": "-O2",
    "flags": "-fno-fast-math -fstack-protector",
    "defines": []
  }
}
```

**Use Cases:**
- Production web services
- Enterprise applications
- User-facing software
- Long-running processes

**Trade-offs:**
- ✅ Good balance of safety & speed
- ✅ Suitable for production
- ✅ Predictable performance
- ❌ ~30% slower than aggressive

**Example:**

```bash
./naab/build/naab-lang pivot.naab evolve service.py --profile conservative
```

---

### balanced

**Default profile - balanced safety and performance**

**Configuration:**

```json
{
  "name": "balanced",
  "description": "Balanced safety and performance (default)",

  "optimization_level": 2,
  "enable_simd": true,
  "enable_lto": false,
  "enable_unsafe": false,

  "bounds_checking": true,
  "overflow_checking": false,
  "null_checking": true,

  "go": {
    "flags": "-trimpath",
    "env": {}
  },

  "rust": {
    "opt_level": 2,
    "flags": "",
    "features": []
  },

  "cpp": {
    "optimization": "-O2",
    "flags": "-march=native",
    "defines": []
  }
}
```

**Use Cases:**
- General-purpose optimization
- Development & testing
- Most production workloads
- Default choice when unsure

**Trade-offs:**
- ✅ Good safety guarantees
- ✅ Good performance (3-5x typical speedup)
- ✅ SIMD optimizations enabled
- ✅ Reasonable binary size
- ❌ Not maximum performance

**Example:**

```bash
./naab/build/naab-lang pivot.naab evolve compute.py
# Uses balanced profile by default
```

---

### aggressive

**Maximum performance, some safety trade-offs**

**Configuration:**

```json
{
  "name": "aggressive",
  "description": "Maximum performance optimizations",

  "optimization_level": 3,
  "enable_simd": true,
  "enable_lto": true,
  "enable_unsafe": true,

  "bounds_checking": false,
  "overflow_checking": false,
  "null_checking": false,

  "go": {
    "flags": "-ldflags=-s -w -trimpath",
    "env": {"GOGC": "off"}
  },

  "rust": {
    "opt_level": 3,
    "flags": "-C target-cpu=native -C lto=fat",
    "features": []
  },

  "cpp": {
    "optimization": "-O3",
    "flags": "-march=native -ffast-math -flto",
    "defines": ["NDEBUG"]
  }
}
```

**Use Cases:**
- High-performance computing
- Batch processing
- Data pipelines
- Scientific computing
- When profiling shows hotspots

**Trade-offs:**
- ✅ Maximum performance (5-15x typical speedup)
- ✅ LTO enabled (cross-function optimization)
- ✅ SIMD + fast-math
- ❌ May use unsafe code
- ❌ Harder to debug
- ❌ Longer compile times

**Example:**

```bash
./naab/build/naab-lang pivot.naab evolve batch_process.py --profile aggressive
```

**Warning:** Only use aggressive profile after parity validation passes. Not recommended for safety-critical systems.

---

### experimental

**Bleeding-edge optimizations (use at own risk)**

**Configuration:**

```json
{
  "name": "experimental",
  "description": "Bleeding-edge experimental optimizations",

  "optimization_level": 3,
  "enable_simd": true,
  "enable_lto": true,
  "enable_unsafe": true,

  "bounds_checking": false,
  "overflow_checking": false,
  "null_checking": false,

  "go": {
    "flags": "-ldflags=-s -w -trimpath",
    "env": {"GOEXPERIMENT": "newinliner,rangefunc"}
  },

  "rust": {
    "opt_level": 3,
    "flags": "-C target-cpu=native -C lto=fat -Z inline-mir",
    "features": []
  },

  "cpp": {
    "optimization": "-Ofast",
    "flags": "-march=native -mavx512f -flto -fipa-pta",
    "defines": ["NDEBUG"]
  }
}
```

**Use Cases:**
- Research & benchmarking
- Proof-of-concept
- Competitive programming
- When absolute maximum speed needed

**Trade-offs:**
- ✅ Absolute maximum performance
- ✅ AVX-512 SIMD (if supported)
- ✅ Experimental compiler features
- ❌ May be unstable
- ❌ Not portable across CPUs
- ❌ May violate standards (fast-math)

**Example:**

```bash
./naab/build/naab-lang pivot.naab evolve benchmark.py --profile experimental
```

**Warning:** Experimental profile may produce incorrect results due to fast-math and other aggressive assumptions. Always validate thoroughly.

---

### minimal

**Smallest binary size**

**Configuration:**

```json
{
  "name": "minimal",
  "description": "Minimize binary size",

  "optimization_level": "z",
  "enable_simd": false,
  "enable_lto": false,
  "enable_unsafe": false,

  "bounds_checking": true,
  "overflow_checking": false,
  "null_checking": true,

  "go": {
    "flags": "-ldflags=-s -w -trimpath",
    "env": {}
  },

  "rust": {
    "opt_level": "z",
    "flags": "-C strip=symbols -C panic=abort",
    "features": []
  },

  "cpp": {
    "optimization": "-Os",
    "flags": "-ffunction-sections -fdata-sections -Wl,--gc-sections",
    "defines": ["NDEBUG"]
  }
}
```

**Use Cases:**
- Constrained storage
- Containerized deployments
- Edge devices
- Serverless functions (cold start optimization)

**Trade-offs:**
- ✅ Smallest binary size (10-50% smaller)
- ✅ Faster cold starts
- ✅ Reduced memory footprint
- ❌ ~10-20% slower than balanced
- ❌ Longer compile times (LTO)

**Example:**

```bash
./naab/build/naab-lang pivot.naab evolve lambda_function.py --profile minimal
```

---

### embedded

**Embedded systems & IoT devices**

**Configuration:**

```json
{
  "name": "embedded",
  "description": "Embedded systems (no_std, static)",

  "optimization_level": 2,
  "enable_simd": false,
  "enable_lto": true,
  "enable_unsafe": false,

  "bounds_checking": true,
  "overflow_checking": false,
  "null_checking": true,

  "go": {
    "flags": "-ldflags=-s -w",
    "env": {"CGO_ENABLED": "0"}
  },

  "rust": {
    "opt_level": 2,
    "flags": "-C panic=abort -C opt-level=z",
    "features": [],
    "target": "thumbv7em-none-eabihf"
  },

  "cpp": {
    "optimization": "-O2",
    "flags": "-nostdlib -fno-exceptions -fno-rtti",
    "defines": ["EMBEDDED"]
  },

  "zig": {
    "optimization": "ReleaseSafe",
    "flags": "-target arm-freestanding-none",
    "features": []
  }
}
```

**Use Cases:**
- IoT sensors
- Microcontrollers
- Real-time systems
- Bare-metal environments

**Trade-offs:**
- ✅ no_std compatible (Rust)
- ✅ Static linking only
- ✅ Small memory footprint
- ✅ Deterministic timing
- ❌ No dynamic allocation
- ❌ No OS dependencies

**Example:**

```bash
./naab/build/naab-lang pivot.naab evolve sensor_logic.py --profile embedded --target zig
```

---

### wasm

**WebAssembly / browser deployment**

**Configuration:**

```json
{
  "name": "wasm",
  "description": "WebAssembly target",

  "optimization_level": 2,
  "enable_simd": true,
  "enable_lto": true,
  "enable_unsafe": false,

  "bounds_checking": true,
  "overflow_checking": false,
  "null_checking": true,

  "go": {
    "flags": "",
    "env": {"GOOS": "js", "GOARCH": "wasm"}
  },

  "rust": {
    "opt_level": 2,
    "flags": "-C target-feature=+simd128",
    "target": "wasm32-unknown-unknown",
    "features": []
  },

  "cpp": {
    "optimization": "-O2",
    "flags": "-fwasm-exceptions",
    "target": "wasm32",
    "compiler": "emcc"
  }
}
```

**Use Cases:**
- Browser-based applications
- Web workers
- Server-side WASM (Wasmtime, Wasmer)
- Edge computing (Cloudflare Workers)

**Trade-offs:**
- ✅ Runs in browser
- ✅ Portable across platforms
- ✅ Sandboxed execution
- ❌ Limited system access
- ❌ Async/await constraints

**Example:**

```bash
./naab/build/naab-lang pivot.naab evolve web_compute.py --profile wasm --target rust
```

---

## Custom Profiles

### Creating Custom Profiles

Create a new profile file in `profiles/` directory:

```bash
cd ~/naab-pivot
cp profiles/custom.json.example profiles/my-profile.json
```

**File: `profiles/my-profile.json`**

```json
{
  "name": "my-profile",
  "description": "Custom profile for my use case",

  "optimization_level": 2,
  "enable_simd": true,
  "enable_lto": false,
  "enable_unsafe": false,

  "bounds_checking": true,
  "overflow_checking": false,
  "null_checking": true,

  "go": {
    "flags": "-ldflags=-s -w",
    "env": {}
  },

  "rust": {
    "opt_level": 2,
    "flags": "-C target-cpu=native",
    "features": ["serde", "tokio"]
  },

  "cpp": {
    "optimization": "-O2",
    "flags": "-march=native -fopenmp",
    "defines": ["MY_CUSTOM_FLAG"],
    "includes": ["/usr/local/include/mylib"]
  }
}
```

### Using Custom Profiles

```bash
./naab/build/naab-lang pivot.naab evolve code.py --profile my-profile
```

### Profile Inheritance

Profiles can inherit from base profiles:

```json
{
  "name": "my-aggressive",
  "inherits": "aggressive",
  "description": "Aggressive with custom tweaks",

  "rust": {
    "features": ["rayon", "simd"]
  }
}
```

---

## Profile Selection Guide

### Decision Tree

```
Do you need maximum safety?
├─ YES → ultra-safe
└─ NO
   ├─ Is this production code?
   │  ├─ YES → conservative or balanced
   │  └─ NO
   │     ├─ Do you need maximum speed?
   │     │  ├─ YES → aggressive or experimental
   │     │  └─ NO → balanced
   │     └─ Target environment?
   │        ├─ Embedded → embedded
   │        ├─ Browser → wasm
   │        ├─ Serverless → minimal
   │        └─ General → balanced
```

### By Use Case

| Use Case | Recommended Profile | Rationale |
|----------|---------------------|-----------|
| Web API | conservative | Stability + performance |
| Batch processing | aggressive | Maximum throughput |
| IoT sensor | embedded | Resource constraints |
| Browser app | wasm | Platform requirement |
| Data pipeline | aggressive | Speed critical |
| Medical device | ultra-safe | Safety critical |
| Development | balanced | Good default |
| Benchmarking | experimental | Maximum speed |
| AWS Lambda | minimal | Cold start optimization |
| Real-time trading | aggressive | Latency critical |

### Performance Expectations

Based on typical Python → compiled evolution:

| Profile | Typical Speedup | Binary Size |
|---------|----------------|-------------|
| ultra-safe | 2-3x | 3-5 MB |
| conservative | 3-5x | 2-3 MB |
| balanced | 3-6x | 2 MB |
| aggressive | 5-15x | 1-2 MB |
| experimental | 8-20x | 1-2 MB |
| minimal | 3-5x | 0.5-1 MB |
| embedded | 4-8x | 100-500 KB |
| wasm | 2-4x | 500 KB-2 MB |

**Note:** Actual speedups vary by workload. CPU-bound tasks see larger improvements than I/O-bound tasks.

---

## Profile Configuration Reference

### Top-Level Fields

- `name` (string): Profile identifier
- `description` (string): Human-readable description
- `optimization_level` (number|string): 0-3, "s", "z"
- `enable_simd` (boolean): Enable SIMD instructions
- `enable_lto` (boolean): Enable link-time optimization
- `enable_unsafe` (boolean): Allow unsafe code optimizations
- `bounds_checking` (boolean): Runtime bounds checking
- `overflow_checking` (boolean): Integer overflow checking
- `null_checking` (boolean): Null pointer checking

### Language-Specific Sections

#### Go

```json
"go": {
  "flags": "-trimpath",                    // Compiler flags
  "env": {"GOEXPERIMENT": "newinliner"}   // Environment variables
}
```

#### Rust

```json
"rust": {
  "opt_level": 2,                         // 0-3, "s", "z"
  "flags": "-C target-cpu=native",        // rustc flags
  "features": ["serde", "rayon"],         // Cargo features
  "target": "x86_64-unknown-linux-gnu"    // Target triple
}
```

#### C++

```json
"cpp": {
  "optimization": "-O2",                  // -O0, -O1, -O2, -O3, -Os, -Ofast
  "flags": "-march=native -fopenmp",      // Compiler flags
  "defines": ["NDEBUG"],                  // Preprocessor defines
  "includes": ["/usr/local/include"]      // Include paths
}
```

---

**Next:** [Templates Guide](templates.md) | [Benchmarking Guide](benchmarking.md)
