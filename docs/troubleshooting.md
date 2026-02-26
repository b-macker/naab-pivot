# Troubleshooting Guide

**Common Issues and Solutions**

---

## Installation Issues

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

### Permission Denied

**Problem:** `bash: ./naab/build/naab-lang: Permission denied`

**Solution:**

```bash
chmod +x naab/build/naab-lang
```

---

## Compilation Issues

### Go Compiler Not Found

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

### Rust Compiler Not Found

**Problem:** "rustc: command not found"

**Solution:**

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Verify
rustc --version
```

---

### C++ Compilation Fails

**Problem:** "g++: error: unrecognized command line option '-march=native'"

**Solution:**

```bash
# Use generic optimization instead
./naab/build/naab-lang pivot.naab evolve slow.py --profile conservative
```

---

## Validation Issues

### Parity Validation Fails

**Problem:** "Parity NOT CERTIFIED - deviation too high"

**Reasons:**

1. **Floating-point precision differences**

**Solution:** Increase tolerance

```bash
export PIVOT_TOLERANCE=0.01  # 1% tolerance
./naab/build/naab-lang pivot.naab validate slow.py vessel
```

2. **Non-deterministic behavior** (random, time-based)

**Solution:** Seed random generators, use fixed timestamps

3. **Integer overflow handling**

**Solution:** Use `--profile ultra-safe` for overflow checking

---

### Test Cases Fail

**Problem:** All test cases fail with "Execution error"

**Solution:** Check vessel binary directly

```bash
# Run vessel manually
./vessels/compute_vessel 10000

# Check exit code
echo $?  # Should be 0
```

---

## Performance Issues

### Slow Analysis

**Problem:** Analysis takes >5 minutes

**Solutions:**

1. **Check NAAb build mode:**

```bash
cd naab/build
cmake .. -DCMAKE_BUILD_TYPE=Release
make clean && make naab-lang -j4
```

2. **Split large files:**

If file >1000 LOC, split into smaller modules

3. **Use hotspot-only mode:**

```bash
./naab/build/naab-lang pivot.naab evolve --hotspot-only slow.py
```

---

### Slow Compilation

**Problem:** Vessel compilation takes too long

**Solutions:**

1. **Enable parallel compilation:**

```bash
./naab/build/naab-lang pivot.naab synthesize blueprint.json --parallel 8
```

2. **Use cache:**

```bash
# Avoid --no-cache flag
# Cache is enabled by default
```

3. **Use ccache:**

```bash
# Install ccache
sudo apt-get install ccache

# Use with C++
export CXX="ccache g++"
```

---

### Lower Speedup Than Expected

**Problem:** Speedup is only 1.5x, expected 5x

**Possible Causes:**

1. **I/O-bound workload** (file reads, network calls)
   - Speedup limited by I/O, not CPU

2. **Wrong profile** (ultra-safe instead of aggressive)

**Solution:**

```bash
./naab/build/naab-lang pivot.naab evolve slow.py --profile aggressive
```

3. **Not enough iterations** in benchmark

**Solution:**

```bash
./naab/build/naab-lang benchmark.naab vessels/ --iterations 1000
```

---

## Governance Issues

### Governance Violation

**Problem:** "Governance check failed: Network access not allowed"

**Solution:** Modify `govern.json`

```json
{
  "capabilities": {
    "network": {"enabled": true}
  }
}
```

Or use override (caution):

```bash
./naab/build/naab-lang pivot.naab --governance-override evolve slow.py
```

---

### Blocked Language

**Problem:** "Language 'python' not allowed by governance"

**Solution:** Add to allowed languages in `govern.json`

```json
{
  "languages": {
    "allowed": ["python", "cpp", "rust", "go"]
  }
}
```

---

## Dashboard Issues

### Dashboard Won't Start

**Problem:** "Address already in use"

**Solution:** Change port

```bash
export PIVOT_DASHBOARD_PORT=3000
./naab/build/naab-lang dashboard.naab
```

---

### Dashboard Shows No Data

**Problem:** Dashboard is empty

**Solution:** Verify workspace path

```bash
export PIVOT_WORKSPACE=/path/to/projects
./naab/build/naab-lang dashboard.naab
```

---

## Docker Issues

### Docker Build Fails

**Problem:** "Docker build failed: Out of disk space"

**Solution:** Clean Docker

```bash
docker system prune -a
docker build -t naab-pivot .
```

---

### Container Can't Access Files

**Problem:** "Permission denied" in Docker container

**Solution:** Fix volume permissions

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  --user $(id -u):$(id -g) \
  naab-pivot
```

---

## Plugin Issues

### Plugin Not Found

**Problem:** "Plugin not found: ml_detector"

**Solution:** Check plugin path

```bash
ls -la plugins/analyzers/ml_detector.naab
# Ensure file exists

# Register with full path
plugin_loader.register_plugin(
    "/absolute/path/to/plugins/analyzers/ml_detector.naab",
    "analyzer"
)
```

---

### Plugin Execution Fails

**Problem:** "Plugin execution failed: ..."

**Solution:** Test plugin directly

```naab
use ml_detector

main {
    let result = ml_detector.execute({
        "source": "test code",
        "language": "python"
    })

    io.write(json.stringify(result, true), "\n")
}
```

---

## Error Messages

### "UNSUPPORTED_LANGUAGE"

**Cause:** File extension not recognized

**Solution:** Use `--language` flag

```bash
./naab/build/naab-lang pivot.naab analyze script.txt --language python
```

---

### "COMPILATION_ERROR"

**Cause:** Generated code doesn't compile

**Solution:** Inspect generated code

```bash
cat vessels/compute_GO.go

# Try compiling manually
go build vessels/compute_GO.go
```

---

### "PARITY_FAILED"

**Cause:** Implementations produce different results

**Solution:** Increase test count and tolerance

```bash
./naab/build/naab-lang pivot.naab validate slow.py vessel \
  --test-count 10000 \
  --tolerance 0.01
```

---

### "TIMEOUT"

**Cause:** Operation exceeded time limit

**Solution:** Increase timeout

```bash
export PIVOT_TIMEOUT=600  # 10 minutes
./naab/build/naab-lang pivot.naab evolve slow.py
```

---

## Debugging Tips

### Enable Verbose Logging

```bash
./naab/build/naab-lang pivot.naab --verbose evolve slow.py
```

### Check Environment Variables

```bash
env | grep PIVOT
```

### Inspect Generated Files

```bash
ls -lah vessels/
cat vessels/compute_GO.go
file vessels/compute_vessel
```

### Manual Testing

```bash
# Test vessel manually
./vessels/compute_vessel 10000

# Time execution
time ./vessels/compute_vessel 10000000
```

### Use Debugger

```bash
# GDB for C++
gdb vessels/compute_vessel

# Delve for Go
dlv exec vessels/compute_vessel
```

---

## Getting Help

1. **Check FAQ:** [docs/faq.md](faq.md)
2. **Search Issues:** https://github.com/b-macker/naab-pivot/issues
3. **Discord:** https://discord.gg/naab-pivot
4. **Email:** support@naab-pivot.dev

When reporting issues, include:
- NAAb Pivot version
- Operating system
- Error message (full output)
- Minimal reproduction case
- Expected vs actual behavior

---

**Next:** [FAQ](faq.md) | [Contributing](contributing.md)
