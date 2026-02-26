# NAAb Pivot - End-to-End Testing Guide

**Version:** 1.0.0
**Date:** 2026-02-26
**Purpose:** Comprehensive end-to-end testing and validation for v1.0.0 release

---

## Overview

This guide outlines the complete end-to-end testing process for NAAb Pivot v1.0.0, covering all 10 example projects, dashboard functionality, GitHub Action integration, and cross-platform compatibility.

---

## Prerequisites

### Required Software

```bash
# Core requirements
- NAAb language (built from submodule)
- Git (for repository operations)

# Optional compilers (for full testing)
- Go 1.21+ (for Go vessels)
- GCC/G++ (for C++ vessels)
- Rustc (for Rust vessels)
- Zig 0.11+ (for Zig vessels)
- Julia 1.9+ (for Julia vessels)
- Node.js 18+ (for JavaScript vessels)
- PHP 8+ (for PHP vessels)
- Ruby 3+ (for Ruby vessels)
```

### Build NAAb

```bash
cd ~/naab-pivot
bash build.sh
# Verify: ./naab/build/naab-lang --help
```

---

## Testing Phases

### Phase 1: Example Validation (Priority 1)

**Objective:** Verify all 10 example projects are complete and functional

**Script:** `scripts/validate-all-examples.sh`

```bash
# Run automated validation
bash scripts/validate-all-examples.sh

# Expected output:
# ✅ All examples validated successfully!
# Success Rate: 100%
```

**Manual Verification Checklist:**

For each example (01-10):
- [ ] README.md exists and is comprehensive
- [ ] Source file exists (Python/Ruby/JS)
- [ ] .pivotrc configuration file exists
- [ ] Benchmark/profile data exists
- [ ] Documented speedup matches claimed performance
- [ ] All files committed to git
- [ ] Example can be run successfully

**Example-Specific Tests:**

1. **Example 01 (Basic Evolution)**
   ```bash
   cd examples/01-basic-evolution
   # Verify Python source
   python slow.py
   # Expected: 2843ms execution time
   ```

2. **Example 02 (Batch Processing)**
   ```bash
   cd examples/02-batch-processing
   # Verify Python version works
   python process_files.py
   # Expected: 4231ms execution time
   ```

3. **Example 03 (ML Optimization)**
   ```bash
   cd examples/03-ml-optimization
   # Verify ML inference code
   python slow_inference.py
   # Expected: 1800ms execution time
   ```

4. **Example 04 (Web Backend)**
   ```bash
   cd examples/04-web-backend
   # Verify Flask API
   python api_server.py &
   curl http://localhost:5000/api/health
   # Expected: 200 OK response
   ```

5. **Example 05 (Crypto Mining)**
   ```bash
   cd examples/05-crypto-mining
   # Verify hash computation
   python hash_compute.py
   # Expected: 24.3s execution time
   ```

6. **Example 06 (Data Pipeline)**
   ```bash
   cd examples/06-data-pipeline
   # Verify ETL process
   python etl_process.py
   # Expected: 4500ms execution time
   ```

7. **Example 07 (Scientific Computing)**
   ```bash
   cd examples/07-scientific-compute
   # Verify simulation
   python simulation.py
   # Expected: 3600ms CPU execution
   ```

8. **Example 08 (Embedded System)**
   ```bash
   cd examples/08-embedded-system
   # Verify sensor logic
   python sensor_logic.py
   # Expected: 2200ms execution time
   ```

9. **Example 09 (Incremental Migration)**
   ```bash
   cd examples/09-incremental-migration
   # Verify migration plan
   cat migration_plan.json
   # Expected: 156K LOC migration plan
   ```

10. **Example 10 (Polyglot Microservices)**
    ```bash
    cd examples/10-polyglot-microservices
    # Verify Docker Compose
    docker-compose config
    # Expected: Valid compose file
    ```

---

### Phase 2: Dashboard Testing (Priority 1)

**Objective:** Verify web dashboard functionality

**Script:** `scripts/test-dashboard.sh`

```bash
# Run automated dashboard validation
bash scripts/test-dashboard.sh

# Expected output:
# ✅ Dashboard validated successfully!
# Success Rate: 100%
```

**Manual Dashboard Testing:**

1. **Start Dashboard Server**
   ```bash
   ./naab/build/naab-lang dashboard/serve.naab
   # Expected: Server starts on http://localhost:8080
   ```

2. **Browser Testing**
   - Open: http://localhost:8080
   - [ ] Page loads without errors
   - [ ] Header displays "NAAb Pivot"
   - [ ] Navigation links work
   - [ ] Overview section shows statistics
   - [ ] Projects section displays project list
   - [ ] Performance section shows charts
   - [ ] Vessels section shows catalog

3. **API Endpoint Testing**
   ```bash
   # Test projects API
   curl http://localhost:8080/api/projects
   # Expected: JSON with projects list

   # Test benchmarks API
   curl http://localhost:8080/api/benchmarks
   # Expected: JSON with benchmark data

   # Test vessels API
   curl http://localhost:8080/api/vessels
   # Expected: JSON with vessel metadata
   ```

4. **Chart.js Functionality**
   - [ ] Performance trend chart renders
   - [ ] Speedup distribution chart renders
   - [ ] Charts are interactive (hover tooltips)
   - [ ] No JavaScript console errors

5. **Responsive Design**
   - [ ] Desktop view (1920x1080) works
   - [ ] Tablet view (768x1024) works
   - [ ] Mobile view (375x667) works

---

### Phase 3: Unit Test Execution (Priority 2)

**Objective:** Run all unit tests and verify pass rate

**Script:** `tests/run-all-tests.sh unit`

```bash
# Run unit tests
cd tests
bash run-all-tests.sh unit

# Expected output:
# ✅ All tests passed!
# Pass: 34 | Fail: 0 | Skip: 0
```

**Unit Test Coverage:**
- [x] test-analyze.naab (8 tests)
- [x] test-synthesize.naab (6 tests)
- [x] test-validate.naab (5 tests)
- [x] test-benchmark.naab (4 tests)
- [x] test-template-engine.naab (3 tests)
- [x] test-config.naab (2 tests)
- [x] test-plugins.naab (3 tests)
- [x] test-cache.naab (3 tests)

**Pass Criteria:** ≥95% pass rate (≥32/34 tests)

---

### Phase 4: Integration Test Execution (Priority 2)

**Objective:** Run all integration tests

**Script:** `tests/run-all-tests.sh integration`

```bash
# Run integration tests
cd tests
bash run-all-tests.sh integration

# Expected output:
# ✅ All tests passed!
# Pass: 19 | Fail: 0 | Skip: 0
```

**Integration Test Coverage:**
- [x] test-full-pipeline.naab (4 tests)
- [x] test-error-recovery.naab (3 tests)
- [x] test-multi-file.naab (3 tests)
- [x] test-incremental.naab (3 tests)

**Pass Criteria:** ≥95% pass rate (≥18/19 tests)

---

### Phase 5: Performance Benchmarks (Priority 3)

**Objective:** Run performance benchmarks and verify no regressions

**Script:** `tests/run-all-tests.sh performance`

```bash
# Run performance benchmarks
cd tests
bash run-all-tests.sh performance

# Expected output:
# ✅ All tests passed!
# No performance regressions detected
```

**Performance Benchmarks:**
- [x] bench-analyzer.naab (analyzer speed test)
- [x] bench-synthesizer.naab (code generation speed)
- [x] bench-compilation.naab (compilation time tracking)
- [x] regression-suite.naab (regression detection)

**Performance Criteria:**
- Analyzer: <1000ms for 100 files
- Synthesizer: <500ms for 50 vessels
- Compilation: Reasonable average time
- Regression: <10% slowdown vs baseline

---

### Phase 6: Cross-Platform Testing (Priority 3)

**Objective:** Verify functionality across multiple operating systems

**Platforms:**
1. Linux (Ubuntu 20.04+)
2. macOS (10.15+)
3. Windows (10/11 or WSL2)
4. Android (Termux)

**Testing Procedure (Per Platform):**

```bash
# 1. Clone repository
git clone --recursive https://github.com/b-macker/naab-pivot.git
cd naab-pivot

# 2. Build NAAb
bash build.sh

# 3. Run test suite
cd tests
bash run-all-tests.sh

# 4. Validate examples
cd ..
bash scripts/validate-all-examples.sh

# 5. Test dashboard
bash scripts/test-dashboard.sh
```

**Platform-Specific Notes:**

**Linux:**
- Full compiler suite available
- Expected: 100% functionality

**macOS:**
- Compilers via Homebrew
- Path differences (/Users/ vs /home/)
- Expected: 100% functionality

**Windows (WSL2):**
- Use WSL2 for full compatibility
- Native Windows support limited
- Expected: 95% functionality

**Android (Termux):**
- Limited compiler availability
- Resource constraints
- Expected: Core functionality working

---

### Phase 7: GitHub Action Testing (Priority 2)

**Objective:** Verify GitHub Action works in CI/CD pipeline

**Setup Test Repository:**

1. Create test repository on GitHub
2. Add workflow file:

```yaml
# .github/workflows/test-naab-pivot.yml
name: Test NAAb Pivot Action

on: [push]

jobs:
  test-action:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Create test Python file
        run: |
          cat > slow.py << 'EOF'
          def compute(n):
              result = 0.0
              for i in range(n):
                  result += (i ** 2) ** 0.5
              return result
          EOF

      - name: Run NAAb Pivot
        uses: b-macker/naab-pivot@v1
        with:
          file: slow.py
          profile: balanced
          validate: true

      - name: Check Results
        run: |
          cat vessels/benchmark-report.json
          echo "Action completed successfully!"
```

3. Push and verify action runs
4. Check action outputs

**Expected Results:**
- [ ] Action runs without errors
- [ ] Speedup reported
- [ ] Parity certified
- [ ] Artifacts uploaded

---

### Phase 8: Documentation Review (Priority 3)

**Objective:** Verify all documentation is complete and accurate

**Documentation Checklist:**

Core Documentation:
- [ ] README.md (comprehensive, up-to-date)
- [ ] CHANGELOG.md (v1.0.0 documented)
- [ ] RELEASE_NOTES_v1.0.0.md (complete)
- [ ] CONTRIBUTING.md (clear guidelines)
- [ ] CODE_OF_CONDUCT.md (present)
- [ ] SECURITY.md (vulnerability reporting)
- [ ] LICENSE (MIT)

Docs Directory (17 files):
- [ ] getting-started.md
- [ ] architecture.md
- [ ] cli-reference.md
- [ ] api-reference.md
- [ ] profiles.md
- [ ] templates.md
- [ ] benchmarking.md
- [ ] plugins.md
- [ ] troubleshooting.md
- [ ] faq.md
- [ ] contributing.md
- [ ] governance.md
- [ ] ci-cd.md
- [ ] docker.md
- [ ] migration-guide.md
- [ ] performance-tuning.md
- [ ] security.md

Example READMEs (10 files):
- [ ] examples/01-basic-evolution/README.md
- [ ] examples/02-batch-processing/README.md
- [ ] examples/03-ml-optimization/README.md
- [ ] examples/04-web-backend/README.md
- [ ] examples/05-crypto-mining/README.md
- [ ] examples/06-data-pipeline/README.md
- [ ] examples/07-scientific-compute/README.md
- [ ] examples/08-embedded-system/README.md
- [ ] examples/09-incremental-migration/README.md
- [ ] examples/10-polyglot-microservices/README.md

---

### Phase 9: Docker Testing (Priority 3)

**Objective:** Verify Docker deployment works

**Docker Build Test:**

```bash
# Build Docker image
docker build -t naab-pivot:test .

# Expected: Image builds successfully
```

**Docker Run Test:**

```bash
# Run container
docker run -v $(pwd):/workspace naab-pivot:test --help

# Expected: Help text displayed
```

**Docker Compose Test:**

```bash
# Start services
docker-compose up -d

# Test dashboard
curl http://localhost:8080

# Stop services
docker-compose down

# Expected: Dashboard accessible
```

---

## Test Results Documentation

### Test Report Template

```markdown
# NAAb Pivot v1.0.0 - End-to-End Test Report

**Date:** YYYY-MM-DD
**Tester:** [Name]
**Platform:** [Linux/macOS/Windows/Android]

## Summary

- Total Tests: X
- Passed: X
- Failed: X
- Skipped: X
- Pass Rate: X%

## Phase Results

### Phase 1: Example Validation
- Status: [PASS/FAIL]
- Examples Validated: X/10
- Issues: [None or list]

### Phase 2: Dashboard Testing
- Status: [PASS/FAIL]
- Tests Passed: X/X
- Issues: [None or list]

### Phase 3: Unit Tests
- Status: [PASS/FAIL]
- Tests Passed: X/34
- Issues: [None or list]

### Phase 4: Integration Tests
- Status: [PASS/FAIL]
- Tests Passed: X/19
- Issues: [None or list]

### Phase 5: Performance Benchmarks
- Status: [PASS/FAIL]
- Benchmarks Passed: X/4
- Regressions: [None or list]

### Phase 6: Cross-Platform
- Status: [PASS/FAIL]
- Platforms Tested: X/4
- Issues: [None or list]

### Phase 7: GitHub Action
- Status: [PASS/FAIL]
- Action Runs: X/X successful
- Issues: [None or list]

### Phase 8: Documentation
- Status: [PASS/FAIL]
- Docs Verified: X/X
- Issues: [None or list]

### Phase 9: Docker
- Status: [PASS/FAIL]
- Tests Passed: X/3
- Issues: [None or list]

## Issues Found

[List any issues discovered during testing]

## Recommendations

[Any recommendations for improvements]

## Sign-Off

- [ ] All critical tests passed
- [ ] All documentation verified
- [ ] Ready for v1.0.0 release

**Approved By:** [Name]
**Date:** YYYY-MM-DD
```

---

## Success Criteria

**Minimum Requirements for v1.0.0 Release:**

- [ ] ≥95% example validation pass rate (≥9/10 examples)
- [ ] 100% dashboard functionality working
- [ ] ≥95% unit test pass rate (≥32/34 tests)
- [ ] ≥95% integration test pass rate (≥18/19 tests)
- [ ] No critical performance regressions
- [ ] ≥2 platforms tested successfully
- [ ] GitHub Action working in CI/CD
- [ ] All documentation complete and accurate
- [ ] Docker deployment functional

**Recommended for v1.0.0 Release:**

- [ ] 100% example validation (10/10 examples)
- [ ] 100% unit test pass rate (34/34 tests)
- [ ] 100% integration test pass rate (19/19 tests)
- [ ] All 4 platforms tested
- [ ] Zero performance regressions

---

## Troubleshooting

### Common Issues

**Issue: NAAb build fails**
- Solution: Ensure submodule initialized: `git submodule update --init --recursive`
- Solution: Install CMake: `sudo apt-get install cmake`

**Issue: Tests timeout**
- Solution: Increase timeout in run-all-tests.sh
- Solution: Run tests individually to isolate issue

**Issue: Dashboard won't start**
- Solution: Check port 8080 is available: `lsof -i :8080`
- Solution: Verify dashboard files exist: `ls dashboard/`

**Issue: Examples missing files**
- Solution: Check git status: `git status examples/`
- Solution: Re-clone repository: `git clone --recursive ...`

**Issue: Docker build fails**
- Solution: Check Docker version: `docker --version`
- Solution: Verify Dockerfile syntax: `docker build -t test --dry-run .`

---

## Next Steps After Testing

1. **Document Results**: Fill out test report template
2. **Fix Critical Issues**: Address any failures found
3. **Re-test**: Run tests again after fixes
4. **Update Documentation**: Reflect any changes
5. **Proceed to Release**: If all criteria met, proceed with v1.0.0 publication

---

**Generated:** 2026-02-26
**Version:** 1.0.0
**Status:** Ready for End-to-End Testing
