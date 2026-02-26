# Template System Guide

**Code Generation Template Customization**

This guide explains how NAAb Pivot's template system works and how to create custom templates for code generation.

---

## Table of Contents

- [Template Overview](#template-overview)
- [Built-in Templates](#built-in-templates)
- [Template Variables](#template-variables)
- [Creating Custom Templates](#creating-custom-templates)
- [Template Best Practices](#template-best-practices)
- [Advanced Features](#advanced-features)

---

## Template Overview

Templates are code generation blueprints that transform function specifications into target language code. Each template includes:

- **Language boilerplate:** Imports, main function, entry point
- **Variable placeholders:** Substituted with analysis data
- **Optimization hooks:** Profile-specific compilation flags
- **I/O handling:** Command-line arguments, output formatting

### Template Flow

```
Analysis Blueprint (JSON)
    ↓
Template Selection (by target language)
    ↓
Variable Substitution (${FUNCTION_NAME}, etc.)
    ↓
Code Generation (source file)
    ↓
Compilation (binary vessel)
```

---

## Built-in Templates

NAAb Pivot includes 8 language templates:

| Template | Language | File |
|----------|----------|------|
| Go | Go 1.21+ | `templates/go_template.naab` |
| C++ | C++17 | `templates/cpp_template.naab` |
| Rust | Rust 1.70+ | `templates/rust_template.naab` |
| Ruby | Ruby 3.0+ | `templates/ruby_template.naab` |
| JavaScript | Node.js 18+ | `templates/js_template.naab` |
| PHP | PHP 8.0+ | `templates/php_template.naab` |
| Zig | Zig 0.11+ | `templates/zig_template.naab` |
| Julia | Julia 1.9+ | `templates/julia_template.naab` |

### Example: Go Template

**File:** `templates/go_template.naab`

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

    ${ARG_PARSING}

    start := time.Now()
    result := ${FUNCTION_NAME}(${CALL_ARGS})
    elapsed := time.Since(start)

    fmt.Printf("Result: %v\n", result)
    fmt.Printf("Time: %.2fms\n", float64(elapsed.Microseconds())/1000.0)
}
```

### Example: Rust Template

**File:** `templates/rust_template.naab`

```rust
use std::time::Instant;
use std::env;

fn ${FUNCTION_NAME}(${FUNCTION_ARGS}) -> ${RETURN_TYPE} {
    ${FUNCTION_BODY}
}

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        println!("READY");
        return;
    }

    ${ARG_PARSING}

    let start = Instant::now();
    let result = ${FUNCTION_NAME}(${CALL_ARGS});
    let elapsed = start.elapsed();

    println!("Result: {}", result);
    println!("Time: {:.2}ms", elapsed.as_micros() as f64 / 1000.0);
}
```

---

## Template Variables

Templates use `${VARIABLE}` syntax for placeholders.

### Available Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `${FUNCTION_NAME}` | Function name | `heavyComputation` |
| `${FUNCTION_ARGS}` | Function arguments | `n: i32, x: f64` |
| `${RETURN_TYPE}` | Return type | `f64` |
| `${FUNCTION_BODY}` | Function implementation | `let mut sum = 0.0; ...` |
| `${ARG_PARSING}` | Command-line arg parsing | `let n = args[1].parse::<i32>().unwrap();` |
| `${CALL_ARGS}` | Function call arguments | `n, x` |
| `${IMPORTS}` | Required imports/includes | `use rayon::prelude::*;` |
| `${NAMESPACE}` | Package/namespace | `com.example.compute` |
| `${OPTIMIZATION_FLAGS}` | Profile-specific flags | `-march=native` |
| `${TYPE_ANNOTATIONS}` | Type hints | `: f64` |

### Variable Context

Variables are populated from:

1. **Analysis Blueprint:** Function name, complexity, arguments
2. **Profile Configuration:** Optimization flags, features
3. **Template Logic:** Generated boilerplate, I/O handling

---

## Creating Custom Templates

### Step 1: Create Template File

```bash
cd ~/naab-pivot
cp templates/go_template.naab templates/custom_go.naab
```

### Step 2: Modify Template

**Example: Go template with OpenMP-style parallelism**

```go
package main

import (
    "fmt"
    "math"
    "os"
    "runtime"
    "strconv"
    "sync"
    "time"
)

func ${FUNCTION_NAME}(${FUNCTION_ARGS}) ${RETURN_TYPE} {
    // Original function body
    ${FUNCTION_BODY}
}

func ${FUNCTION_NAME}Parallel(${FUNCTION_ARGS}) ${RETURN_TYPE} {
    numCPU := runtime.NumCPU()
    runtime.GOMAXPROCS(numCPU)

    chunkSize := n / numCPU
    results := make([]float64, numCPU)
    var wg sync.WaitGroup

    for i := 0; i < numCPU; i++ {
        wg.Add(1)
        go func(idx int) {
            defer wg.Done()
            start := idx * chunkSize
            end := start + chunkSize
            if idx == numCPU-1 {
                end = n
            }
            // Process chunk
            sum := 0.0
            for j := start; j < end; j++ {
                sum += math.Sqrt(math.Pow(float64(j), 2))
            }
            results[idx] = sum
        }(i)
    }

    wg.Wait()

    // Combine results
    total := 0.0
    for _, r := range results {
        total += r
    }
    return total
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("READY")
        return
    }

    ${ARG_PARSING}

    start := time.Now()
    result := ${FUNCTION_NAME}Parallel(${CALL_ARGS})
    elapsed := time.Since(start)

    fmt.Printf("Result: %v\n", result)
    fmt.Printf("Time: %.2fms\n", float64(elapsed.Microseconds())/1000.0)
}
```

### Step 3: Register Template

Update `modules/template_engine.naab`:

```naab
export fn generate(func_spec, target) {
    let template_path = "templates/" + string.lower(target) + "_template.naab"

    // Check for custom template first
    let custom_path = env.get_var("PIVOT_CUSTOM_TEMPLATE")
    if custom_path != null && file.exists(custom_path) {
        template_path = custom_path
    }

    let template = file.read(template_path)
    // ... rest of code
}
```

### Step 4: Use Custom Template

```bash
export PIVOT_CUSTOM_TEMPLATE=templates/custom_go.naab
./naab/build/naab-lang pivot.naab evolve slow.py --target go
```

---

## Template Best Practices

### 1. Type Safety

Always include type annotations:

```rust
// ✓ Good
fn compute(n: i32) -> f64 {
    // ...
}

// ✗ Bad
fn compute(n) {
    // ...
}
```

### 2. Error Handling

Include proper error handling:

```go
// ✓ Good
n, err := strconv.Atoi(os.Args[1])
if err != nil {
    fmt.Fprintf(os.Stderr, "Invalid argument: %v\n", err)
    os.Exit(1)
}

// ✗ Bad
n, _ := strconv.Atoi(os.Args[1])
```

### 3. Consistent Formatting

Follow language conventions:

```rust
// ✓ Good (Rust style)
fn heavy_computation(n: i32) -> f64 {
    let mut sum = 0.0;
    for i in 0..n {
        sum += (i as f64).sqrt();
    }
    sum
}

// ✗ Bad (C style in Rust)
fn heavyComputation(n: i32) -> f64 {
    let mut sum = 0.0;
    for (let i = 0; i < n; i++) {
        sum += Math.sqrt(i);
    }
    return sum;
}
```

### 4. Performance Annotations

Include hints for optimizer:

```cpp
// ✓ Good
__attribute__((hot))
inline double compute(int n) {
    double sum = 0.0;
    #pragma omp parallel for reduction(+:sum)
    for (int i = 0; i < n; i++) {
        sum += std::sqrt(i * i);
    }
    return sum;
}
```

### 5. Portable Code

Avoid platform-specific code unless necessary:

```go
// ✓ Good (portable)
import "runtime"
numCPU := runtime.NumCPU()

// ✗ Bad (Linux-only)
numCPU := 8  // hardcoded
```

---

## Advanced Features

### Conditional Generation

Templates can include conditional logic:

```naab
// In template_engine.naab
let code = template

if profile["enable_simd"] {
    code = string.replace(code, "${SIMD_PRAGMA}", "#pragma omp simd")
} else {
    code = string.replace(code, "${SIMD_PRAGMA}", "")
}

if func_spec["has_loops"] {
    code = string.replace(code, "${PARALLEL_HINT}", "#pragma omp parallel for")
} else {
    code = string.replace(code, "${PARALLEL_HINT}", "")
}
```

### Profile-Specific Templates

Different templates for different profiles:

```bash
templates/
├── go_template.naab          # Default
├── go_template_safe.naab     # ultra-safe profile
├── go_template_aggressive.naab # aggressive profile
└── go_template_embedded.naab  # embedded profile
```

**Select based on profile:**

```naab
let template_path = "templates/" + target + "_template"

if profile["name"] == "ultra-safe" {
    template_path = template_path + "_safe"
} else if profile["name"] == "aggressive" {
    template_path = template_path + "_aggressive"
} else if profile["name"] == "embedded" {
    template_path = template_path + "_embedded"
}

template_path = template_path + ".naab"
```

### Multi-File Templates

Generate multiple files from one template:

```naab
// Generate main.go
let main_code = render_template("templates/go_main_template.naab", func_spec)
file.write("vessels/main.go", main_code)

// Generate compute.go
let compute_code = render_template("templates/go_compute_template.naab", func_spec)
file.write("vessels/compute.go", compute_code)

// Compile both files
<<bash
go build -o vessel vessels/*.go
>>
```

### Template Macros

Define reusable template fragments:

```naab
// Define macro
let timer_macro = "
let start = time.now()
${COMPUTATION}
let elapsed = time.now() - start
io.write(\"Time: \", elapsed, \"ms\\n\")
"

// Use macro
let code = string.replace(template, "${TIMER}", timer_macro)
code = string.replace(code, "${COMPUTATION}", func_body)
```

### Code Formatters

Apply language-specific formatters:

```naab
fn post_process_code(code, target) {
    if target == "GO" {
        // Run gofmt
        file.write("/tmp/temp.go", code)
        let formatted = <<bash
        gofmt /tmp/temp.go
        >>
        return formatted
    } else if target == "RUST" {
        // Run rustfmt
        file.write("/tmp/temp.rs", code)
        let formatted = <<bash
        rustfmt /tmp/temp.rs && cat /tmp/temp.rs
        >>
        return formatted
    }
    return code
}
```

---

## Template Examples

### Example 1: SIMD-Enabled C++ Template

```cpp
#include <iostream>
#include <cmath>
#include <chrono>
#include <immintrin.h>

${SIMD_PRAGMA}
double ${FUNCTION_NAME}(int n) {
    double sum = 0.0;

    #ifdef __AVX2__
    // AVX2 vectorized loop
    __m256d sum_vec = _mm256_setzero_pd();
    int i = 0;
    for (; i < n - 3; i += 4) {
        __m256d v = _mm256_set_pd(i+3, i+2, i+1, i);
        __m256d squared = _mm256_mul_pd(v, v);
        __m256d sqrt_v = _mm256_sqrt_pd(squared);
        sum_vec = _mm256_add_pd(sum_vec, sqrt_v);
    }

    // Horizontal sum
    double temp[4];
    _mm256_storeu_pd(temp, sum_vec);
    sum = temp[0] + temp[1] + temp[2] + temp[3];

    // Handle remaining elements
    for (; i < n; i++) {
        sum += std::sqrt(i * i);
    }
    #else
    // Scalar fallback
    for (int i = 0; i < n; i++) {
        sum += std::sqrt(i * i);
    }
    #endif

    return sum;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "READY" << std::endl;
        return 0;
    }

    int n = std::stoi(argv[1]);

    auto start = std::chrono::high_resolution_clock::now();
    double result = ${FUNCTION_NAME}(n);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> elapsed = end - start;

    std::cout << "Result: " << result << std::endl;
    std::cout << "Time: " << elapsed.count() << "ms" << std::endl;

    return 0;
}
```

### Example 2: Rust Rayon Parallel Template

```rust
use rayon::prelude::*;
use std::time::Instant;
use std::env;

fn ${FUNCTION_NAME}(n: i32) -> f64 {
    (0..n)
        .into_par_iter()
        .map(|i| (i as f64).powi(2).sqrt())
        .sum()
}

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        println!("READY");
        return;
    }

    let n: i32 = args[1].parse().expect("Invalid argument");

    let start = Instant::now();
    let result = ${FUNCTION_NAME}(n);
    let elapsed = start.elapsed();

    println!("Result: {}", result);
    println!("Time: {:.2}ms", elapsed.as_micros() as f64 / 1000.0);
}
```

---

## Troubleshooting

### Template Variable Not Substituted

**Problem:** `${VARIABLE}` appears in generated code

**Solution:** Ensure variable is defined in template engine:

```naab
code = string.replace(code, "${FUNCTION_NAME}", func_spec["name"])
```

### Compilation Fails After Template Change

**Problem:** Generated code doesn't compile

**Solution:** Test template manually:

```bash
# Generate code
./naab/build/naab-lang pivot.naab synthesize blueprint.json

# Inspect generated code
cat vessels/compute_GO.go

# Test compilation manually
go build vessels/compute_GO.go
```

### Profile Not Applied

**Problem:** Optimization flags not appearing in generated code

**Solution:** Check profile loading:

```naab
let profile = config_manager.load_profile("aggressive")
io.write("Profile flags: ", profile["go"]["flags"], "\n")
```

---

**Next:** [Benchmarking Guide](benchmarking.md) | [Plugins Guide](plugins.md)
