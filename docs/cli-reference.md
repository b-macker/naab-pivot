# CLI Reference

**Complete Command-Line Interface Documentation**

NAAb Pivot provides a comprehensive CLI for analyzing, synthesizing, validating, and benchmarking code evolution.

---

## Table of Contents

- [Global Options](#global-options)
- [Commands](#commands)
  - [analyze](#analyze)
  - [synthesize](#synthesize)
  - [validate](#validate)
  - [benchmark](#benchmark)
  - [evolve](#evolve)
  - [migrate](#migrate)
  - [dashboard](#dashboard)
- [Environment Variables](#environment-variables)
- [Configuration Files](#configuration-files)
- [Exit Codes](#exit-codes)
- [Examples](#examples)

---

## Global Options

These options apply to all commands:

```bash
./naab/build/naab-lang pivot.naab [GLOBAL OPTIONS] <command> [COMMAND OPTIONS]
```

### `--help, -h`

Display help information

```bash
./naab/build/naab-lang pivot.naab --help
./naab/build/naab-lang pivot.naab analyze --help
```

### `--version, -v`

Display version information

```bash
./naab/build/naab-lang pivot.naab --version
# Output: NAAb Pivot v1.0.0
```

### `--verbose`

Enable verbose logging

```bash
./naab/build/naab-lang pivot.naab --verbose analyze slow.py
```

### `--quiet, -q`

Suppress all output except errors

```bash
./naab/build/naab-lang pivot.naab --quiet evolve slow.py
```

### `--profile <name>`

Select optimization profile

**Options:** `ultra-safe`, `conservative`, `balanced` (default), `aggressive`, `experimental`, `minimal`, `embedded`, `wasm`

```bash
./naab/build/naab-lang pivot.naab --profile aggressive evolve slow.py
```

### `--output <path>`

Set output directory for vessels

```bash
./naab/build/naab-lang pivot.naab --output ./build/vessels evolve slow.py
```

### `--format <format>`

Set report output format

**Options:** `json` (default), `html`, `csv`, `sarif`, `markdown`

```bash
./naab/build/naab-lang pivot.naab --format html benchmark ./vessels
```

### `--governance-override`

Override governance checks (use with caution)

```bash
./naab/build/naab-lang pivot.naab --governance-override evolve slow.py
```

### `--governance-report <path>`

Generate governance compliance report

```bash
./naab/build/naab-lang pivot.naab --governance-report report.json evolve slow.py
```

---

## Commands

### analyze

**Analyze source code for optimization opportunities**

#### Synopsis

```bash
./naab/build/naab-lang pivot.naab analyze <file> [OPTIONS]
```

#### Options

##### `--language <lang>`

Force language detection (auto-detected by default)

**Options:** `python`, `ruby`, `javascript`, `naab`, `php`, `java`, `go`, `csharp`

```bash
./naab/build/naab-lang pivot.naab analyze script.txt --language python
```

##### `--min-complexity <n>`

Only report functions with complexity >= n (default: 5)

```bash
./naab/build/naab-lang pivot.naab analyze slow.py --min-complexity 10
```

##### `--target <lang>`

Force target language recommendation

**Options:** `go`, `cpp`, `rust`, `ruby`, `js`, `php`, `zig`, `julia`

```bash
./naab/build/naab-lang pivot.naab analyze slow.py --target rust
```

##### `--hotspot-only`

Only analyze functions detected as hotspots (requires profiling data)

```bash
./naab/build/naab-lang pivot.naab analyze slow.py --hotspot-only --profile-data profile.json
```

##### `--profile-data <path>`

Use profiling data for hotspot detection

```bash
./naab/build/naab-lang pivot.naab analyze slow.py --profile-data cProfile.prof
```

##### `--json-output <path>`

Write analysis blueprint to JSON file

```bash
./naab/build/naab-lang pivot.naab analyze slow.py --json-output analysis.json
```

#### Examples

**Basic analysis:**

```bash
./naab/build/naab-lang pivot.naab analyze slow_compute.py
```

**Output:**
```json
{
  "status": "ANALYZED",
  "source": "PYTHON",
  "functions": [
    {
      "name": "heavy_computation",
      "complexity": 8,
      "target": "GO"
    }
  ]
}
```

**Force Rust target:**

```bash
./naab/build/naab-lang pivot.naab analyze slow.py --target rust > blueprint.json
```

**Profile-guided analysis:**

```bash
# Generate profile data
python -m cProfile -o slow.prof slow.py

# Analyze with profiling
./naab/build/naab-lang pivot.naab analyze slow.py \
  --profile-data slow.prof \
  --hotspot-only
```

---

### synthesize

**Generate optimized vessel code from analysis blueprint**

#### Synopsis

```bash
./naab/build/naab-lang pivot.naab synthesize <blueprint.json> [OPTIONS]
```

#### Options

##### `--profile <name>`

Optimization profile (overrides global)

```bash
./naab/build/naab-lang pivot.naab synthesize blueprint.json --profile aggressive
```

##### `--parallel <n>`

Compile N vessels in parallel (default: CPU count)

```bash
./naab/build/naab-lang pivot.naab synthesize blueprint.json --parallel 8
```

##### `--no-cache`

Disable vessel cache (force recompilation)

```bash
./naab/build/naab-lang pivot.naab synthesize blueprint.json --no-cache
```

##### `--enable-simd`

Enable SIMD optimizations (AVX2, AVX-512)

```bash
./naab/build/naab-lang pivot.naab synthesize blueprint.json --enable-simd
```

##### `--enable-lto`

Enable Link-Time Optimization

```bash
./naab/build/naab-lang pivot.naab synthesize blueprint.json --enable-lto
```

##### `--strip-debug`

Strip debug symbols from binaries

```bash
./naab/build/naab-lang pivot.naab synthesize blueprint.json --strip-debug
```

##### `--template-dir <path>`

Use custom template directory

```bash
./naab/build/naab-lang pivot.naab synthesize blueprint.json --template-dir ./custom-templates
```

#### Examples

**Basic synthesis:**

```bash
./naab/build/naab-lang pivot.naab synthesize analysis.json
```

**Output:**
```
  [SYNTHESIZER] Loading blueprint: analysis.json
  [SYNTHESIZER] Generating heavy_computation (GO)...
    ✓ Code generated: vessels/heavy_computation_GO.go
    ✓ Compiling...
    ✓ Compilation successful: vessels/heavy_computation_vessel
```

**Aggressive optimization:**

```bash
./naab/build/naab-lang pivot.naab synthesize blueprint.json \
  --profile aggressive \
  --enable-simd \
  --enable-lto \
  --strip-debug
```

**Parallel compilation:**

```bash
./naab/build/naab-lang pivot.naab synthesize blueprint.json --parallel 16
```

---

### validate

**Validate parity between legacy and vessel implementations**

#### Synopsis

```bash
./naab/build/naab-lang pivot.naab validate <legacy> <vessel> [OPTIONS]
```

#### Options

##### `--test-count <n>`

Number of test cases to run (default: 100)

```bash
./naab/build/naab-lang pivot.naab validate slow.py vessel --test-count 1000
```

##### `--tolerance <float>`

Maximum allowed relative error (default: 0.001 = 0.1%)

```bash
./naab/build/naab-lang pivot.naab validate slow.py vessel --tolerance 0.01
```

##### `--confidence <float>`

Required confidence level (default: 0.9999 = 99.99%)

```bash
./naab/build/naab-lang pivot.naab validate slow.py vessel --confidence 0.999
```

##### `--test-cases <file>`

Use custom test cases from JSON file

```bash
./naab/build/naab-lang pivot.naab validate slow.py vessel --test-cases cases.json
```

**Format (`cases.json`):**
```json
{
  "test_cases": [
    {"input": [1, 2, 3], "expected": 6},
    {"input": [10, 20], "expected": 30}
  ]
}
```

##### `--fuzz-test`

Enable fuzz testing (random inputs)

```bash
./naab/build/naab-lang pivot.naab validate slow.py vessel --fuzz-test --test-count 10000
```

##### `--property-based`

Enable property-based testing (QuickCheck-style)

```bash
./naab/build/naab-lang pivot.naab validate slow.py vessel --property-based
```

##### `--report <path>`

Save validation report to file

```bash
./naab/build/naab-lang pivot.naab validate slow.py vessel --report validation.json
```

#### Examples

**Basic validation:**

```bash
./naab/build/naab-lang pivot.naab validate slow_compute.py vessels/heavy_computation_vessel
```

**Output:**
```
  [VALIDATOR] Comparing implementations...
    Legacy: slow_compute.py
    Vessel: vessels/heavy_computation_vessel

  Running 100 test cases...
  ✓ Test 0: ✓ (error: 0.00001%)
  ...
  ✓ Test 99: ✓ (error: 0.00001%)

  ═══════════════════════════════════════════════
  ✅ PARITY CERTIFIED
  ═══════════════════════════════════════════════

  Performance:
    Legacy: 2843ms
    Vessel: 812ms
    Speedup: 3.5x ⚡
```

**Strict validation:**

```bash
./naab/build/naab-lang pivot.naab validate slow.py vessel \
  --test-count 10000 \
  --tolerance 0.0001 \
  --confidence 0.99999
```

**Fuzz testing:**

```bash
./naab/build/naab-lang pivot.naab validate slow.py vessel \
  --fuzz-test \
  --test-count 100000 \
  --report fuzz-results.json
```

---

### benchmark

**Run performance benchmarks on vessels**

#### Synopsis

```bash
./naab/build/naab-lang pivot.naab benchmark <vessel-dir> [OPTIONS]
```

#### Options

##### `--iterations <n>`

Number of benchmark iterations (default: 100)

```bash
./naab/build/naab-lang pivot.naab benchmark vessels/ --iterations 1000
```

##### `--warmup <n>`

Number of warmup iterations (default: 10)

```bash
./naab/build/naab-lang pivot.naab benchmark vessels/ --warmup 50
```

##### `--baseline <file>`

Compare against baseline results

```bash
./naab/build/naab-lang pivot.naab benchmark vessels/ --baseline baseline.json
```

##### `--regression-threshold <percent>`

Fail if performance degrades by more than N% (default: 10)

```bash
./naab/build/naab-lang pivot.naab benchmark vessels/ \
  --baseline baseline.json \
  --regression-threshold 5
```

##### `--save-baseline <file>`

Save current results as new baseline

```bash
./naab/build/naab-lang pivot.naab benchmark vessels/ --save-baseline baseline.json
```

##### `--format <format>`

Output format (json, html, csv, sarif)

```bash
./naab/build/naab-lang pivot.naab benchmark vessels/ --format html > report.html
```

##### `--compare`

Compare multiple vessels

```bash
./naab/build/naab-lang pivot.naab benchmark vessels/ --compare
```

#### Examples

**Basic benchmark:**

```bash
./naab/build/naab-lang pivot.naab benchmark vessels/
```

**Output:**
```
  [BENCHMARK] Running benchmark suite: vessels/

  Benchmark: heavy_computation_vessel
    Iterations: 100
    Mean: 812.34ms
    Median: 812.00ms
    P95: 814.50ms
    P99: 815.00ms

  ✓ Benchmark complete: vessels/benchmark-report.json
```

**Regression detection:**

```bash
./naab/build/naab-lang pivot.naab benchmark vessels/ \
  --baseline previous-run.json \
  --regression-threshold 5
```

**HTML report:**

```bash
./naab/build/naab-lang pivot.naab benchmark vessels/ \
  --format html \
  --output benchmark-report.html
```

---

### evolve

**Run full evolution pipeline (analyze → synthesize → validate → benchmark)**

#### Synopsis

```bash
./naab/build/naab-lang pivot.naab evolve <file> [OPTIONS]
```

#### Options

Accepts all options from `analyze`, `synthesize`, `validate`, and `benchmark` commands.

##### Common Options

```bash
--profile <name>           # Optimization profile
--target <lang>            # Force target language
--min-complexity <n>       # Minimum complexity threshold
--test-count <n>           # Validation test count
--tolerance <float>        # Validation tolerance
--format <format>          # Report format
--output <path>            # Output directory
```

#### Examples

**Basic evolution:**

```bash
./naab/build/naab-lang pivot.naab evolve slow_compute.py
```

**Output:**
```
╔══════════════════════════════════════════════╗
║        NAAb Pivot - Code Evolution           ║
╚══════════════════════════════════════════════╝

[1/4] Analyzing...
  ✓ Detected: Python
  ✓ Found 1 function: heavy_computation
  ✓ Recommended target: GO

[2/4] Synthesizing...
  ✓ Generated: vessels/heavy_computation_GO.go
  ✓ Compiled: vessels/heavy_computation_vessel

[3/4] Validating...
  ✓ Running 100 test cases...
  ✓ PARITY CERTIFIED (99.99% confidence)

[4/4] Benchmarking...
  ✓ Legacy: 2843ms
  ✓ Vessel: 812ms
  ✓ Speedup: 3.5x ⚡

═══════════════════════════════════════════════
✅ EVOLUTION COMPLETE
═══════════════════════════════════════════════

Vessels: ./vessels/
Reports: ./vessels/evolution-report.json
```

**Aggressive optimization:**

```bash
./naab/build/naab-lang pivot.naab evolve slow.py \
  --profile aggressive \
  --target rust \
  --enable-simd \
  --enable-lto \
  --test-count 1000
```

**Generate HTML report:**

```bash
./naab/build/naab-lang pivot.naab evolve slow.py --format html > report.html
```

---

### migrate

**Create incremental migration plan for large codebases**

#### Synopsis

```bash
./naab/build/naab-lang migrate.naab create_migration_plan <project-dir> [OPTIONS]
```

#### Options

##### `--min-score <n>`

Minimum optimization score to include (default: 50)

```bash
./naab/build/naab-lang migrate.naab create_migration_plan ./project --min-score 80
```

##### `--phases <n>`

Number of migration phases (default: 4)

```bash
./naab/build/naab-lang migrate.naab create_migration_plan ./project --phases 6
```

##### `--output <path>`

Save migration plan to file

```bash
./naab/build/naab-lang migrate.naab create_migration_plan ./project --output plan.json
```

##### `--estimate-effort`

Include time/resource estimates

```bash
./naab/build/naab-lang migrate.naab create_migration_plan ./project --estimate-effort
```

#### Examples

**Create migration plan:**

```bash
./naab/build/naab-lang migrate.naab create_migration_plan /path/to/large/project
```

**Output:**
```json
{
  "status": "PLAN_CREATED",
  "total_files": 156,
  "candidates": [
    {
      "file": "core/sales_aggregator.py",
      "score": 92.3,
      "estimated_speedup": 12.5,
      "functions": [...]
    }
  ],
  "phases": [
    {
      "phase": 1,
      "name": "Low-hanging fruit",
      "files": 12,
      "estimated_effort_weeks": 6
    }
  ]
}
```

---

### dashboard

**Launch web dashboard for visualization**

#### Synopsis

```bash
./naab/build/naab-lang dashboard.naab [OPTIONS]
```

#### Options

##### `--port <n>`

Dashboard port (default: 8080)

```bash
./naab/build/naab-lang dashboard.naab --port 3000
```

##### `--host <addr>`

Bind address (default: 0.0.0.0)

```bash
./naab/build/naab-lang dashboard.naab --host localhost
```

##### `--workspace <path>`

Workspace directory to monitor (default: ./workspace)

```bash
./naab/build/naab-lang dashboard.naab --workspace /path/to/projects
```

#### Examples

```bash
./naab/build/naab-lang dashboard.naab

# Output:
# 📊 Dashboard URL: http://localhost:8080
# 🚀 Press Ctrl+C to stop
```

---

## Environment Variables

### `PIVOT_OUTPUT`

Default output directory for vessels

```bash
export PIVOT_OUTPUT=/opt/vessels
./naab/build/naab-lang pivot.naab evolve slow.py
```

### `PIVOT_PROFILE`

Default optimization profile

```bash
export PIVOT_PROFILE=aggressive
./naab/build/naab-lang pivot.naab evolve slow.py
```

### `PIVOT_TOLERANCE`

Default validation tolerance

```bash
export PIVOT_TOLERANCE=0.01  # 1%
./naab/build/naab-lang pivot.naab validate slow.py vessel
```

### `PIVOT_WORKSPACE`

Workspace directory for dashboard

```bash
export PIVOT_WORKSPACE=/path/to/projects
./naab/build/naab-lang dashboard.naab
```

### `PIVOT_DASHBOARD_PORT`

Dashboard port

```bash
export PIVOT_DASHBOARD_PORT=3000
./naab/build/naab-lang dashboard.naab
```

---

## Configuration Files

### Global Config: `~/.pivotrc`

```json
{
  "profile": "balanced",
  "output": "~/vessels",
  "format": "json",
  "test_count": 100,
  "tolerance": 0.001,
  "parallel": 8,
  "enable_simd": false,
  "enable_lto": false
}
```

### Project Config: `./.pivotrc`

Overrides global config for current project:

```json
{
  "project_name": "MyProject",
  "profile": "aggressive",
  "output": "./build/vessels",
  "enable_simd": true,
  "enable_lto": true,
  "governance": {
    "enforce": true,
    "config": "./govern.json"
  }
}
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Analysis failed |
| 4 | Synthesis failed (compilation error) |
| 5 | Validation failed (parity NOT certified) |
| 6 | Benchmark failed (regression detected) |
| 7 | Governance violation |
| 8 | File not found |
| 9 | Permission denied |
| 10 | Timeout |

---

## Examples

### Example 1: Quick Evolution

```bash
./naab/build/naab-lang pivot.naab evolve slow.py
```

### Example 2: Custom Profile & Target

```bash
./naab/build/naab-lang pivot.naab evolve slow.py \
  --profile aggressive \
  --target rust
```

### Example 3: Strict Validation

```bash
./naab/build/naab-lang pivot.naab evolve slow.py \
  --test-count 10000 \
  --tolerance 0.0001 \
  --confidence 0.99999
```

### Example 4: Pipeline with HTML Report

```bash
./naab/build/naab-lang pivot.naab evolve slow.py \
  --format html \
  --output ./reports/evolution.html
```

### Example 5: Incremental Migration

```bash
# Analyze project
./naab/build/naab-lang migrate.naab create_migration_plan ./my-project > plan.json

# Evolve Phase 1 files
for file in $(jq -r '.phases[0].files[]' plan.json); do
  ./naab/build/naab-lang pivot.naab evolve "$file"
done
```

### Example 6: CI/CD Integration

```bash
# Run in CI pipeline
./naab/build/naab-lang pivot.naab benchmark vessels/ \
  --baseline baseline.json \
  --regression-threshold 5 \
  --format sarif > benchmark.sarif

# Upload to GitHub Code Scanning
gh api repos/:owner/:repo/code-scanning/sarifs \
  --method POST \
  --field sarif=@benchmark.sarif
```

---

**Next:** [API Reference](api-reference.md) | [Profiles Guide](profiles.md)
