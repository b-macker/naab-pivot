# Plugins Guide

**Extending NAAb Pivot with Custom Plugins**

---

## Plugin Types

1. **Analyzers:** Detect specific workload types (ML, crypto, I/O-bound)
2. **Synthesizers:** Generate code for custom targets or optimizations
3. **Validators:** Custom testing strategies (fuzz, property-based, formal)

---

## Plugin Structure

### Directory Layout

```
plugins/
├── analyzers/
│   ├── ml_detector.naab
│   ├── ml_detector.json
│   ├── crypto_detector.naab
│   └── crypto_detector.json
├── synthesizers/
│   ├── simd_optimizer.naab
│   ├── simd_optimizer.json
│   ├── gpu_optimizer.naab
│   └── gpu_optimizer.json
└── validators/
    ├── fuzzer.naab
    ├── fuzzer.json
    ├── property_checker.naab
    └── property_checker.json
```

### Plugin Metadata

**File:** `ml_detector.json`

```json
{
  "id": "ml-detector",
  "version": "1.0.0",
  "type": "analyzer",
  "name": "ML Workload Detector",
  "description": "Detects machine learning workloads",
  "author": "Your Name",
  "supported_languages": ["python", "julia"],
  "entry_point": "execute"
}
```

### Plugin Implementation

**File:** `ml_detector.naab`

```naab
export fn execute(input_data) {
    let source = input_data["source"]
    let language = input_data["language"]

    // Detection logic
    let ml_keywords = ["numpy", "tensorflow", "torch", "sklearn", "keras"]
    let ml_detected = false
    let confidence = 0.0

    for keyword in ml_keywords {
        if string.index_of(source, keyword) != -1 {
            ml_detected = true
            confidence = confidence + 0.2
        }
    }

    return {
        "status": if ml_detected { "ML_DETECTED" } else { "NOT_DETECTED" },
        "confidence": confidence,
        "recommended_optimizations": if ml_detected {
            ["gpu_acceleration", "vectorization", "parallel_inference"]
        } else {
            []
        }
    }
}
```

---

## Using Plugins

### Load Plugin

```naab
use plugin_loader

main {
    let plugin_id = plugin_loader.register_plugin(
        "plugins/analyzers/ml_detector.naab",
        "analyzer"
    )

    io.write("Plugin loaded: ", plugin_id, "\n")
}
```

### Execute Plugin

```naab
use plugin_loader

main {
    let plugin_id = plugin_loader.register_plugin(
        "plugins/analyzers/ml_detector.naab",
        "analyzer"
    )

    let result = plugin_loader.execute_plugin(plugin_id, {
        "source": file.read("model_training.py"),
        "language": "python"
    })

    if result["status"] == "ML_DETECTED" {
        io.write("ML workload detected!\n")
        io.write("Confidence: ", result["confidence"], "\n")
        io.write("Optimizations: ", array.join(result["recommended_optimizations"], ", "), "\n")
    }
}
```

---

## Example Plugins

### 1. SIMD Optimizer

**Purpose:** Automatically vectorize loops

**File:** `plugins/synthesizers/simd_optimizer.naab`

```naab
export fn execute(input_data) {
    let func_spec = input_data["function"]
    let target = input_data["target"]

    if func_spec["has_loops"] == false {
        return {"status": "NOT_APPLICABLE"}
    }

    // Generate SIMD-optimized code
    let simd_code = generate_simd_code(func_spec, target)

    return {
        "status": "OPTIMIZED",
        "code": simd_code,
        "expected_speedup": 4.0
    }
}

fn generate_simd_code(func_spec, target) {
    if target == "CPP" {
        return "
#include <immintrin.h>

double ${FUNCTION_NAME}(int n) {
    __m256d sum_vec = _mm256_setzero_pd();
    for (int i = 0; i < n - 3; i += 4) {
        __m256d v = _mm256_set_pd(i+3, i+2, i+1, i);
        sum_vec = _mm256_add_pd(sum_vec, v);
    }
    return _mm256_reduce_add_pd(sum_vec);
}
"
    }
    return ""
}
```

### 2. Fuzz Tester

**Purpose:** Property-based testing for validation

**File:** `plugins/validators/fuzzer.naab`

```naab
export fn execute(input_data) {
    let legacy_path = input_data["legacy"]
    let vessel_path = input_data["vessel"]
    let iterations = input_data["iterations"] || 10000

    let passed = 0
    let failed = 0

    for i in 0..iterations {
        let random_input = generate_random_input()

        let legacy_output = run_command(legacy_path, random_input)
        let vessel_output = run_command(vessel_path, random_input)

        if abs(legacy_output - vessel_output) < 0.001 {
            passed = passed + 1
        } else {
            failed = failed + 1
            io.write("  Failed on input: ", random_input, "\n")
        }
    }

    return {
        "status": if failed == 0 { "PASSED" } else { "FAILED" },
        "passed": passed,
        "failed": failed,
        "confidence": (1.0 * passed) / (1.0 * iterations)
    }
}

fn generate_random_input() {
    // Random number generation
    let random_val = <<python
import random
random.randint(1, 1000000)
    >>
    return json.parse(random_val)
}
```

---

## Plugin API

### Analyzer Plugin Interface

```naab
export fn execute(input_data: object) -> object {
    // input_data contains:
    // - source: string (source code)
    // - language: string (source language)
    // - file_path: string (file path)

    // Return object with:
    return {
        "status": "DETECTED" | "NOT_DETECTED",
        "confidence": 0.0-1.0,
        "metadata": {...}
    }
}
```

### Synthesizer Plugin Interface

```naab
export fn execute(input_data: object) -> object {
    // input_data contains:
    // - function: object (function spec from analyzer)
    // - target: string (target language)
    // - profile: object (optimization profile)

    // Return object with:
    return {
        "status": "OPTIMIZED" | "NOT_APPLICABLE" | "ERROR",
        "code": "...",  // Generated code
        "expected_speedup": 5.0
    }
}
```

### Validator Plugin Interface

```naab
export fn execute(input_data: object) -> object {
    // input_data contains:
    // - legacy: string (legacy implementation path)
    // - vessel: string (vessel implementation path)
    // - test_count: number (number of tests)

    // Return object with:
    return {
        "status": "PASSED" | "FAILED",
        "passed": number,
        "failed": number,
        "confidence": 0.0-1.0
    }
}
```

---

## Plugin Best Practices

### 1. Error Handling

Always catch and return errors:

```naab
export fn execute(input_data) {
    try {
        // Plugin logic
        return {"status": "SUCCESS"}
    } catch (e) {
        return {
            "status": "ERROR",
            "error": e
        }
    }
}
```

### 2. Timeouts

Include timeout handling for long-running operations:

```naab
let start_time = time.now()
let timeout_ms = 30000

while condition {
    if time.now() - start_time > timeout_ms {
        return {"status": "TIMEOUT"}
    }
    // Plugin logic
}
```

### 3. Validation

Validate input data:

```naab
export fn execute(input_data) {
    if input_data["source"] == null {
        return {"status": "ERROR", "error": "Missing source field"}
    }

    // Plugin logic
}
```

---

## Plugin Development Workflow

1. **Create plugin directory:**

```bash
mkdir -p plugins/analyzers/my_plugin
cd plugins/analyzers/my_plugin
```

2. **Create metadata file:**

```bash
cat > my_plugin.json <<EOF
{
  "id": "my-plugin",
  "version": "1.0.0",
  "type": "analyzer",
  "entry_point": "execute"
}
EOF
```

3. **Implement plugin:**

```bash
cat > my_plugin.naab <<EOF
export fn execute(input_data) {
    return {"status": "SUCCESS"}
}
EOF
```

4. **Test plugin:**

```naab
use plugin_loader

main {
    let plugin_id = plugin_loader.register_plugin(
        "plugins/analyzers/my_plugin/my_plugin.naab",
        "analyzer"
    )

    let result = plugin_loader.execute_plugin(plugin_id, {
        "source": "test code"
    })

    io.write(json.stringify(result, true), "\n")
}
```

5. **Publish plugin:**

```bash
git add plugins/analyzers/my_plugin/
git commit -m "Add my_plugin analyzer"
git push
```

---

**Next:** [Troubleshooting](troubleshooting.md) | [Contributing](contributing.md)
