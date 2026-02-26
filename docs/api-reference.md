# API Reference

**Complete Module API Documentation**

This document describes the programmatic API for all NAAb Pivot modules, allowing you to integrate Pivot into your own tools and workflows.

---

## Table of Contents

- [Core Modules](#core-modules)
  - [Analyzer](#analyzer)
  - [Synthesizer](#synthesizer)
  - [Validator](#validator)
  - [Benchmarker](#benchmarker)
  - [Migrator](#migrator)
- [Support Modules](#support-modules)
  - [Template Engine](#template-engine)
  - [Config Manager](#config-manager)
  - [Plugin Loader](#plugin-loader)
  - [Dependency Analyzer](#dependency-analyzer)
  - [Hotspot Detector](#hotspot-detector)
  - [Report Generator](#report-generator)
  - [Vessel Cache](#vessel-cache)
- [Data Types](#data-types)
- [Error Handling](#error-handling)
- [Usage Examples](#usage-examples)

---

## Core Modules

### Analyzer

**Module:** `analyze.naab`

**Purpose:** Analyze source code to detect optimization opportunities

#### Functions

##### `analyze_file(file_path: string) -> AnalysisResult`

Analyze a single source file for optimization opportunities.

**Parameters:**
- `file_path` (string): Absolute or relative path to source file

**Returns:** `AnalysisResult` object (see [Data Types](#analysisresult))

**Throws:**
- `FileNotFoundError`: If file doesn't exist
- `UnsupportedLanguageError`: If language not supported
- `ParseError`: If source code cannot be parsed

**Example:**

```naab
use analyzer

main {
    let result = analyzer.analyze_file("slow_compute.py")

    io.write("Status: ", result["status"], "\n")
    io.write("Functions found: ", array.length(result["functions"]), "\n")

    for func in result["functions"] {
        io.write("  - ", func["name"], " (complexity: ", func["complexity"], ")\n")
    }
}
```

##### `analyze_python(source: string, path: string) -> AnalysisResult`

Analyze Python source code directly (without file I/O).

**Parameters:**
- `source` (string): Python source code
- `path` (string): Virtual file path (for error reporting)

**Returns:** `AnalysisResult` object

**Example:**

```naab
use analyzer

main {
    let python_code = "def compute(n):\n    return sum(range(n))"
    let result = analyzer.analyze_python(python_code, "virtual.py")
}
```

##### `analyze_ruby(source: string, path: string) -> AnalysisResult`

Analyze Ruby source code directly.

##### `analyze_javascript(source: string, path: string) -> AnalysisResult`

Analyze JavaScript source code directly.

##### `analyze_naab(source: string, path: string) -> AnalysisResult`

Analyze NAAb source code directly.

##### `detect_extension(file_path: string) -> string`

Detect language from file extension.

**Parameters:**
- `file_path` (string): File path

**Returns:** Extension string ("py", "rb", "js", "naab", etc.)

**Example:**

```naab
use analyzer

main {
    let ext = analyzer.detect_extension("script.py")
    io.write("Extension: ", ext, "\n")  // "py"
}
```

---

### Synthesizer

**Module:** `synthesize.naab`

**Purpose:** Generate optimized vessel code from analysis blueprint

#### Functions

##### `generate_vessels(blueprint_path: string) -> SynthesisResult`

Generate optimized vessels from analysis blueprint.

**Parameters:**
- `blueprint_path` (string): Path to analysis blueprint JSON file

**Returns:** `SynthesisResult` object (see [Data Types](#synthesisresult))

**Throws:**
- `BlueprintNotFoundError`: If blueprint file doesn't exist
- `BlueprintInvalidError`: If blueprint JSON is malformed
- `CompilationError`: If vessel compilation fails

**Example:**

```naab
use synthesizer
use env

main {
    env.set_var("PIVOT_OUTPUT", "./vessels/")

    let result = synthesizer.generate_vessels("analysis.json")

    io.write("Vessels generated: ", array.length(result["vessels"]), "\n")

    for vessel in result["vessels"] {
        if vessel["status"] == "COMPILED" {
            io.write("  ✓ ", vessel["name"], " → ", vessel["bin"], "\n")
        } else if vessel["status"] == "CACHED" {
            io.write("  ↻ ", vessel["name"], " (cached)\n")
        } else {
            io.write("  ✗ ", vessel["name"], " (failed)\n")
        }
    }
}
```

##### `should_rebuild(src_path: string, bin_path: string, new_code: string) -> boolean`

Check if vessel needs recompilation.

**Parameters:**
- `src_path` (string): Generated source file path
- `bin_path` (string): Compiled binary path
- `new_code` (string): New generated code

**Returns:** `true` if recompilation needed, `false` if cached version can be used

**Example:**

```naab
use synthesizer

main {
    let rebuild = synthesizer.should_rebuild(
        "vessels/func_GO.go",
        "vessels/func_vessel",
        "package main\n..."
    )

    if rebuild {
        io.write("Recompilation needed\n")
    } else {
        io.write("Using cached vessel\n")
    }
}
```

##### `compile_vessel(src: string, bin: string, target: string) -> void`

Compile vessel source code to binary.

**Parameters:**
- `src` (string): Source file path
- `bin` (string): Output binary path
- `target` (string): Target language ("GO", "CPP", "RUST")

**Throws:**
- `CompilationError`: If compilation fails
- `CompilerNotFoundError`: If compiler not installed

**Example:**

```naab
use synthesizer

main {
    try {
        synthesizer.compile_vessel(
            "vessels/compute_GO.go",
            "vessels/compute_vessel",
            "GO"
        )
        io.write("Compilation successful\n")
    } catch (e) {
        io.write("Compilation failed: ", e, "\n")
    }
}
```

---

### Validator

**Module:** `validate.naab`

**Purpose:** Validate parity between legacy and vessel implementations

#### Functions

##### `validate_parity(legacy_path: string, vessel_path: string) -> ValidationResult`

Validate parity between two implementations.

**Parameters:**
- `legacy_path` (string): Path to legacy implementation
- `vessel_path` (string): Path to vessel binary

**Returns:** `ValidationResult` object (see [Data Types](#validationresult))

**Throws:**
- `FileNotFoundError`: If either file doesn't exist
- `ExecutionError`: If execution fails
- `ParityFailedError`: If parity validation fails

**Example:**

```naab
use validator

main {
    let result = validator.validate_parity(
        "slow_compute.py",
        "vessels/compute_vessel"
    )

    if result["certified"] {
        io.write("✅ PARITY CERTIFIED\n")
        io.write("Speedup: ", result["performance"]["speedup"], "x\n")
    } else {
        io.write("❌ PARITY FAILED\n")
        io.write("Failed tests: ", result["failed"], "/", result["test_count"], "\n")
    }
}
```

##### `load_test_cases() -> array`

Load or generate test cases for validation.

**Returns:** Array of test case objects

**Example:**

```naab
use validator

main {
    let test_cases = validator.load_test_cases()
    io.write("Test cases: ", array.length(test_cases), "\n")
}
```

##### `run_legacy(legacy_path: string, test: object) -> any`

Execute legacy implementation with test input.

**Parameters:**
- `legacy_path` (string): Path to legacy implementation
- `test` (object): Test case object

**Returns:** Output value (any type)

##### `run_vessel(vessel_path: string, test: object) -> any`

Execute vessel implementation with test input.

**Parameters:**
- `vessel_path` (string): Path to vessel binary
- `test` (object): Test case object

**Returns:** Output value (any type)

##### `compute_stats(differences: array) -> object`

Compute statistical analysis of validation results.

**Parameters:**
- `differences` (array): Array of difference objects

**Returns:** Statistics object with mean, median, stddev, max_error

**Example:**

```naab
use validator

main {
    let differences = [
        {"absolute": 0.00001, "relative": 0.000001},
        {"absolute": 0.00002, "relative": 0.000002}
    ]

    let stats = validator.compute_stats(differences)
    io.write("Mean error: ", stats["mean"], "\n")
    io.write("Max error: ", stats["max_error"], "\n")
}
```

---

### Benchmarker

**Module:** `benchmark.naab`

**Purpose:** Track performance over time and detect regressions

#### Functions

##### `run_suite(bench_dir: string) -> BenchmarkReport`

Run benchmark suite on vessels.

**Parameters:**
- `bench_dir` (string): Directory containing vessels to benchmark

**Returns:** `BenchmarkReport` object (see [Data Types](#benchmarkreport))

**Example:**

```naab
use benchmark

main {
    let report = benchmark.run_suite("./vessels/")

    io.write("Benchmarks run: ", array.length(report["results"]), "\n")

    for result in report["results"] {
        io.write("  ", result["benchmark"], ": ", result["mean"], "ms\n")
    }
}
```

##### `run_single_benchmark(bench_path: string) -> BenchmarkResult`

Run a single benchmark.

**Parameters:**
- `bench_path` (string): Path to benchmark specification JSON

**Returns:** `BenchmarkResult` object

**Example:**

```naab
use benchmark

main {
    let result = benchmark.run_single_benchmark("compute.bench.json")
    io.write("Mean: ", result["mean"], "ms\n")
    io.write("P95: ", result["p95"], "ms\n")
}
```

##### `generate_benchmark_report(results: array) -> object`

Generate comprehensive benchmark report.

**Parameters:**
- `results` (array): Array of benchmark results

**Returns:** Report object with summary statistics

---

### Migrator

**Module:** `migrate.naab`

**Purpose:** Create incremental migration plans for large codebases

#### Functions

##### `create_migration_plan(project_dir: string) -> MigrationPlan`

Analyze project and create migration plan.

**Parameters:**
- `project_dir` (string): Root directory of project

**Returns:** `MigrationPlan` object (see [Data Types](#migrationplan))

**Example:**

```naab
use migrate

main {
    let plan = migrate.create_migration_plan("/path/to/project")

    io.write("Total files: ", plan["total_files"], "\n")
    io.write("Candidates: ", array.length(plan["candidates"]), "\n")
    io.write("Phases: ", array.length(plan["phases"]), "\n")

    for phase in plan["phases"] {
        io.write("  Phase ", phase["phase"], ": ", phase["name"], "\n")
        io.write("    Files: ", phase["files"], "\n")
        io.write("    Effort: ", phase["estimated_effort_weeks"], " weeks\n")
    }
}
```

##### `calculate_priority_score(analysis: AnalysisResult) -> number`

Calculate optimization priority score.

**Parameters:**
- `analysis` (AnalysisResult): Analysis result object

**Returns:** Priority score (0-100)

##### `create_migration_phases(candidates: array) -> array`

Create migration phases from candidates.

**Parameters:**
- `candidates` (array): Array of candidate files

**Returns:** Array of phase objects

---

## Support Modules

### Template Engine

**Module:** `modules/template_engine.naab`

#### Functions

##### `generate(func_spec: object, target: string) -> string`

Generate code from template.

**Parameters:**
- `func_spec` (object): Function specification
- `target` (string): Target language ("GO", "CPP", "RUST")

**Returns:** Generated source code string

**Example:**

```naab
use template_engine

main {
    let func_spec = {
        "name": "compute",
        "complexity": 10,
        "arguments": ["n: int"],
        "return_type": "float"
    }

    let code = template_engine.generate(func_spec, "GO")
    io.write(code, "\n")
}
```

##### `load_template(target: string) -> string`

Load template for target language.

**Parameters:**
- `target` (string): Target language

**Returns:** Template string

---

### Config Manager

**Module:** `modules/config_manager.naab`

#### Functions

##### `load_config() -> object`

Load configuration from .pivotrc files.

**Returns:** Merged configuration object

**Example:**

```naab
use config_manager

main {
    let config = config_manager.load_config()

    io.write("Profile: ", config["profile"], "\n")
    io.write("Output: ", config["output"], "\n")
    io.write("Parallel: ", config["parallel"], "\n")
}
```

##### `load_profile(profile_name: string) -> object`

Load optimization profile.

**Parameters:**
- `profile_name` (string): Profile name ("balanced", "aggressive", etc.)

**Returns:** Profile configuration object

**Example:**

```naab
use config_manager

main {
    let profile = config_manager.load_profile("aggressive")

    io.write("Optimization level: ", profile["optimization_level"], "\n")
    io.write("SIMD enabled: ", profile["enable_simd"], "\n")
}
```

---

### Plugin Loader

**Module:** `modules/plugin_loader.naab`

#### Functions

##### `register_plugin(plugin_path: string, plugin_type: string) -> string`

Register and load a plugin.

**Parameters:**
- `plugin_path` (string): Path to plugin .naab file
- `plugin_type` (string): Plugin type ("analyzer", "synthesizer", "validator")

**Returns:** Plugin ID string

**Throws:**
- `PluginNotFoundError`: If plugin file doesn't exist
- `PluginInvalidError`: If plugin doesn't meet interface requirements

**Example:**

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

##### `execute_plugin(plugin_id: string, input_data: object) -> object`

Execute registered plugin.

**Parameters:**
- `plugin_id` (string): Plugin ID from registration
- `input_data` (object): Input data for plugin

**Returns:** Plugin execution result

**Example:**

```naab
use plugin_loader

main {
    let plugin_id = plugin_loader.register_plugin("ml_detector.naab", "analyzer")

    let result = plugin_loader.execute_plugin(plugin_id, {
        "source": source_code,
        "language": "python"
    })

    io.write("Detection result: ", result["status"], "\n")
}
```

##### `list_plugins() -> array`

List all registered plugins.

**Returns:** Array of plugin metadata objects

---

### Dependency Analyzer

**Module:** `modules/dependency_analyzer.naab`

#### Functions

##### `analyze_dependencies(file_path: string) -> object`

Analyze function dependencies in source file.

**Parameters:**
- `file_path` (string): Source file path

**Returns:** Dependency graph object

**Example:**

```naab
use dependency_analyzer

main {
    let deps = dependency_analyzer.analyze_dependencies("complex.py")

    io.write("Functions: ", array.length(deps["functions"]), "\n")
    io.write("Dependencies:\n")

    for func_name in object.keys(deps["dependencies"]) {
        let func_deps = deps["dependencies"][func_name]
        io.write("  ", func_name, " depends on: ", array.join(func_deps, ", "), "\n")
    }
}
```

##### `build_call_graph(file_path: string) -> object`

Build function call graph.

**Parameters:**
- `file_path` (string): Source file path

**Returns:** Call graph object

---

### Hotspot Detector

**Module:** `modules/hotspot_detector.naab`

#### Functions

##### `detect_hotspots(profile_data_path: string) -> object`

Detect performance hotspots from profiling data.

**Parameters:**
- `profile_data_path` (string): Path to profiling data file

**Returns:** Hotspots object (see [Data Types](#hotspots))

**Example:**

```naab
use hotspot_detector

main {
    let hotspots = hotspot_detector.detect_hotspots("profile.prof")

    io.write("Total functions: ", hotspots["total_functions"], "\n")
    io.write("Hotspots found: ", array.length(hotspots["hotspots"]), "\n")

    for hotspot in hotspots["hotspots"] {
        io.write("  ", hotspot["function"], ": ", hotspot["percentage"], "%\n")
        io.write("    Recommended: ", hotspot["recommended_target"], "\n")
    }
}
```

##### `parse_profile_data(path: string) -> object`

Parse profiling data from various formats.

**Parameters:**
- `path` (string): Profile data file path

**Returns:** Parsed profile data object

##### `recommend_target_language(func_data: object) -> string`

Recommend target language based on function characteristics.

**Parameters:**
- `func_data` (object): Function data from profiling

**Returns:** Recommended target language string

---

### Report Generator

**Module:** `modules/report_generator.naab`

#### Functions

##### `generate_report(results: object, format: string, output_path: string) -> void`

Generate evolution report in specified format.

**Parameters:**
- `results` (object): Evolution results data
- `format` (string): Output format ("json", "html", "csv", "sarif", "markdown")
- `output_path` (string): Output file path

**Example:**

```naab
use report_generator

main {
    let results = {
        "speedup": 3.5,
        "certified": true,
        "vessels": [...]
    }

    report_generator.generate_report(results, "html", "report.html")
    io.write("Report generated: report.html\n")
}
```

##### `generate_json_report(results: object, output_path: string) -> void`

Generate JSON report.

##### `generate_html_report(results: object, output_path: string) -> void`

Generate interactive HTML report with charts.

##### `generate_csv_report(results: object, output_path: string) -> void`

Generate CSV report for spreadsheets.

##### `generate_sarif_report(results: object, output_path: string) -> void`

Generate SARIF report for GitHub Code Scanning.

##### `generate_markdown_report(results: object, output_path: string) -> void`

Generate Markdown report.

---

### Vessel Cache

**Module:** `modules/vessel_cache.naab`

#### Functions

##### `get_cached_vessel(hash: string) -> string | null`

Retrieve cached vessel by hash.

**Parameters:**
- `hash` (string): SHA-256 hash of vessel specification

**Returns:** Path to cached vessel binary, or `null` if not found

**Example:**

```naab
use vessel_cache

main {
    let hash = compute_hash(code + profile + compiler_version)
    let cached = vessel_cache.get_cached_vessel(hash)

    if cached != null {
        io.write("Using cached vessel: ", cached, "\n")
    } else {
        io.write("Cache miss, recompiling\n")
    }
}
```

##### `store_vessel(hash: string, src_path: string, bin_path: string) -> void`

Store vessel in cache.

**Parameters:**
- `hash` (string): SHA-256 hash
- `src_path` (string): Generated source file path
- `bin_path` (string): Compiled binary path

##### `clear_cache() -> void`

Clear all cached vessels.

---

## Data Types

### AnalysisResult

```naab
{
  "status": "ANALYZED",          // Status string
  "source": "PYTHON",             // Source language
  "file_path": "/path/to/file.py", // Source file path
  "timestamp": 1234567890,        // Unix timestamp
  "functions": [                  // Array of function objects
    {
      "name": "compute",          // Function name
      "line_start": 10,           // Starting line number
      "line_count": 25,           // Number of lines
      "complexity": 12,           // Cyclomatic complexity
      "has_loops": true,          // Has for/while loops
      "has_recursion": false,     // Has recursive calls
      "target": "GO",             // Recommended target
      "reason": "High loop complexity", // Recommendation reason
      "dependencies": ["math"],   // Required imports
      "hotspot_score": 85.3       // Optimization priority (0-100)
    }
  ]
}
```

### SynthesisResult

```naab
{
  "status": "SYNTHESIZED",        // Status string
  "profile": "balanced",          // Profile used
  "vessels": [                    // Array of vessel objects
    {
      "name": "compute",          // Vessel name
      "target": "GO",             // Target language
      "src": "vessels/compute_GO.go", // Source file path
      "bin": "vessels/compute_vessel", // Binary file path
      "status": "COMPILED",       // COMPILED | CACHED | INTERPRETED | ERROR
      "compile_time_ms": 1234,    // Compilation time
      "binary_size_bytes": 1847296, // Binary size
      "checksum": "sha256:..."    // SHA-256 checksum
    }
  ],
  "cache_hits": 2,                // Number of cache hits
  "cache_misses": 1               // Number of cache misses
}
```

### ValidationResult

```naab
{
  "certified": true,              // Parity certified (boolean)
  "confidence": 99.99,            // Confidence percentage
  "test_count": 1000,             // Number of tests run
  "passed": 1000,                 // Number passed
  "failed": 0,                    // Number failed
  "performance": {
    "legacy_ms": 2843.52,         // Legacy execution time
    "vessel_ms": 812.34,          // Vessel execution time
    "speedup": 3.50,              // Speedup factor
    "latency_reduction": 71.43    // Latency reduction %
  },
  "statistics": {
    "mean_error": 0.000012,       // Mean absolute error
    "median_error": 0.000008,     // Median absolute error
    "stddev": 0.000005,           // Standard deviation
    "max_error": 0.000045,        // Maximum error
    "ks_statistic": 0.032,        // Kolmogorov-Smirnov statistic
    "ks_p_value": 0.876           // KS p-value
  }
}
```

### BenchmarkReport

```naab
{
  "benchmark_id": "bench_123",    // Unique benchmark ID
  "timestamp": 1234567890,        // Unix timestamp
  "results": [                    // Array of benchmark results
    {
      "benchmark": "compute",     // Benchmark name
      "iterations": 100,          // Number of iterations
      "timings_ms": [812, 815, ...], // All timing data
      "mean": 812.34,             // Mean time (ms)
      "median": 812.00,           // Median time (ms)
      "min": 810.00,              // Minimum time (ms)
      "max": 815.00,              // Maximum time (ms)
      "stddev": 1.42,             // Standard deviation
      "p95": 814.50,              // 95th percentile
      "p99": 815.00               // 99th percentile
    }
  ],
  "baseline": {
    "mean": 2843.52,              // Baseline mean
    "regression_threshold": 10.0,  // Threshold %
    "regression_detected": false   // Regression detected
  }
}
```

### MigrationPlan

```naab
{
  "status": "PLAN_CREATED",       // Status string
  "total_files": 156,             // Total files analyzed
  "candidates": [                 // Array of candidate files
    {
      "file": "core/sales.py",    // File path
      "score": 92.3,              // Priority score (0-100)
      "estimated_speedup": 12.5,  // Estimated speedup
      "functions": [...]          // Function details
    }
  ],
  "phases": [                     // Array of migration phases
    {
      "phase": 1,                 // Phase number
      "name": "Low-hanging fruit", // Phase name
      "files": 12,                // Number of files
      "estimated_effort_weeks": 6 // Estimated effort
    }
  ]
}
```

### Hotspots

```naab
{
  "total_functions": 145,         // Total functions profiled
  "hotspots": [                   // Array of hotspot objects
    {
      "function": "process_batch", // Function name
      "file": "core.py",          // Source file
      "line": 234,                // Line number
      "time_ms": 1234.5,          // Cumulative time (ms)
      "percentage": 23.4,         // % of total time
      "call_count": 10000,        // Number of calls
      "recommended_target": "GO"  // Recommended language
    }
  ],
  "optimization_potential": 18.5  // Total potential speedup
}
```

---

## Error Handling

All functions may throw errors. Use `try/catch` blocks for error handling:

```naab
use analyzer

main {
    try {
        let result = analyzer.analyze_file("slow.py")
        io.write("Success: ", result["status"], "\n")
    } catch (e) {
        io.write("Error: ", e, "\n")
    }
}
```

### Common Errors

- `FileNotFoundError`: File doesn't exist
- `UnsupportedLanguageError`: Language not supported
- `ParseError`: Source code cannot be parsed
- `CompilationError`: Vessel compilation failed
- `CompilerNotFoundError`: Required compiler not installed
- `ParityFailedError`: Parity validation failed
- `PluginNotFoundError`: Plugin file not found
- `PluginInvalidError`: Plugin doesn't meet interface requirements

---

## Usage Examples

### Example 1: Full Pipeline

```naab
use analyzer
use synthesizer
use validator
use benchmark
use env

main {
    // Step 1: Analyze
    io.write("[1/4] Analyzing...\n")
    let analysis = analyzer.analyze_file("slow.py")

    // Step 2: Synthesize
    io.write("[2/4] Synthesizing...\n")
    env.set_var("PIVOT_OUTPUT", "./vessels/")
    file.write("blueprint.json", json.stringify(analysis, true))
    let synthesis = synthesizer.generate_vessels("blueprint.json")

    // Step 3: Validate
    io.write("[3/4] Validating...\n")
    let vessel_bin = synthesis["vessels"][0]["bin"]
    let validation = validator.validate_parity("slow.py", vessel_bin)

    // Step 4: Benchmark
    io.write("[4/4] Benchmarking...\n")
    let bench = benchmark.run_suite("./vessels/")

    // Report
    if validation["certified"] {
        io.write("✅ PARITY CERTIFIED\n")
        io.write("Speedup: ", validation["performance"]["speedup"], "x\n")
    }
}
```

### Example 2: Custom Plugin

```naab
use plugin_loader

main {
    // Register custom analyzer plugin
    let plugin_id = plugin_loader.register_plugin(
        "plugins/analyzers/ml_detector.naab",
        "analyzer"
    )

    // Execute plugin
    let result = plugin_loader.execute_plugin(plugin_id, {
        "source": file.read("model_training.py"),
        "language": "python"
    })

    if result["status"] == "ML_DETECTED" {
        io.write("ML workload detected!\n")
        io.write("Confidence: ", result["confidence"], "\n")
        io.write("Recommended: GPU acceleration\n")
    }
}
```

### Example 3: Hotspot-Driven Evolution

```naab
use hotspot_detector
use analyzer
use synthesizer

main {
    // Detect hotspots from profiling
    let hotspots = hotspot_detector.detect_hotspots("profile.prof")

    // Evolve only hotspot functions
    for hotspot in hotspots["hotspots"] {
        io.write("Optimizing: ", hotspot["function"], "\n")

        // Analyze specific file
        let analysis = analyzer.analyze_file(hotspot["file"])

        // Generate vessels for this function only
        let synthesis = synthesizer.generate_vessels(analysis)

        io.write("  ✓ Speedup: ", hotspot["estimated_speedup"], "x\n")
    }
}
```

---

**Next:** [Profiles Guide](profiles.md) | [Templates Guide](templates.md)
