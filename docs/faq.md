# Frequently Asked Questions (FAQ)

---

## General Questions

### What is NAAb Pivot?

NAAb Pivot is a polyglot code evolution tool that automatically analyzes slow interpreted code (Python, Ruby, JavaScript, NAAb) and generates optimized compiled versions (Go, C++, Rust) while mathematically proving correctness.

### How does it work?

1. **Analyze:** Parse source code, detect functions, calculate complexity
2. **Synthesize:** Generate optimized code using templates
3. **Validate:** Run statistical tests to prove parity (99.99% confidence)
4. **Benchmark:** Measure performance improvements

### Is it safe to use in production?

Yes, if parity validation passes. NAAb Pivot includes mathematical proof that legacy and vessel implementations produce identical results. Use `conservative` or `balanced` profiles for production.

### What speedups can I expect?

Typical speedups by workload:
- CPU-bound loops: 3-15x
- Math-heavy: 5-20x
- I/O-bound: 1.5-3x (limited by I/O)
- Cryptographic: 10-25x (with SIMD)

### Does it replace manual rewriting?

NAAb Pivot automates initial optimization, but manual tuning may achieve higher performance. It's best for:
- Rapid prototyping
- Hotspot optimization
- Incremental migration
- Proof-of-concept

---

## Technical Questions

### Which languages are supported?

**Source (analyzed):** Python, Ruby, JavaScript, NAAb, PHP, Java, Go, C#

**Target (generated):** Go, C++, Rust, Ruby, JavaScript, PHP, Zig, Julia

### Can I add custom languages?

Yes! Create custom templates in `templates/` directory and register in template engine.

### How accurate is parity validation?

99.99% confidence with 100-10,000 test cases. Uses:
- Mean Absolute Error (MAE)
- Kolmogorov-Smirnov test
- Statistical confidence intervals

### What if parity fails?

1. Check for floating-point precision issues → increase tolerance
2. Look for non-deterministic behavior (random, time-based)
3. Verify function has no side effects
4. Use `--test-count 10000` for more thorough testing

### How does caching work?

Vessels are cached by SHA-256 hash of:
- Generated source code
- Optimization profile
- Compiler version
- Target architecture

Recompilation only occurs if any of these change.

---

## Performance Questions

### Why is speedup lower than expected?

Common causes:
1. **I/O-bound workload:** File reads/writes limit speedup
2. **Wrong profile:** Try `--profile aggressive`
3. **Not CPU-intensive:** Simple logic doesn't benefit from compilation
4. **Overhead:** Very short functions (<1ms) may have profiling overhead

### Can I use GPUs?

Not yet built-in. Use custom plugins for GPU code generation (CUDA, OpenCL).

### Does it support SIMD?

Yes! Enable with `--enable-simd` or use `aggressive` profile. Supports AVX2, AVX-512.

### What about parallelism?

- **Go:** Automatic goroutines
- **Rust:** Rayon parallel iterators
- **C++:** OpenMP pragmas

Enable with `--enable-parallel` or custom templates.

---

## Usage Questions

### How do I optimize a single function?

```bash
./naab/build/naab-lang pivot.naab analyze my_module.py --min-complexity 10
./naab/build/naab-lang pivot.naab evolve my_module.py
```

### Can I migrate an entire project?

Yes! Use migration planner:

```bash
./naab/build/naab-lang migrate.naab create_migration_plan /path/to/project
```

### How do I integrate with CI/CD?

Use GitHub Action:

```yaml
- uses: b-macker/naab-pivot@v1
  with:
    file: slow_code.py
    profile: balanced
    validate: true
```

### Can I deploy vessels as containers?

Yes! Use Docker:

```bash
docker build -t my-vessel .
docker run my-vessel
```

---

## Troubleshooting Questions

### Why does build fail?

Most common: Missing dependencies. Install:

```bash
# Ubuntu/Debian
sudo apt-get install cmake build-essential golang rustc g++

# macOS
brew install cmake go rust
```

### Compilation takes forever

Enable parallel compilation:

```bash
./naab/build/naab-lang pivot.naab synthesize blueprint.json --parallel 8
```

### "Governance violation" error

Check `govern.json` or use override:

```bash
./naab/build/naab-lang pivot.naab --governance-override evolve slow.py
```

---

## Comparison Questions

### vs Manual Rewriting?

| Aspect | NAAb Pivot | Manual Rewriting |
|--------|-----------|------------------|
| Speed | Minutes | Days/Weeks |
| Correctness | Mathematically proven | Manual testing |
| Flexibility | Template-based | Unlimited |
| Performance | Good (3-15x) | Excellent (10-100x) |
| Maintenance | Automated | Manual |

**Use NAAb Pivot for:** Rapid optimization, hotspot fixes, POCs

**Use Manual Rewriting for:** Maximum performance, custom algorithms

### vs JIT Compilers (PyPy, V8)?

JIT compilers optimize at runtime; NAAb Pivot generates ahead-of-time compiled code. NAAb Pivot typically achieves higher speedups for CPU-bound workloads.

### vs Cython/Numba?

Similar goals, different approaches:
- **Cython/Numba:** Annotate Python code
- **NAAb Pivot:** Generate new code in different languages

NAAb Pivot is better for complete rewrites; Cython/Numba better for incremental optimization.

---

## Licensing Questions

### What license does NAAb Pivot use?

MIT License - free for commercial and personal use.

### Can I sell vessels generated by NAAb Pivot?

Yes! Generated code is yours to use, modify, and sell.

### Can I contribute?

Yes! See [docs/contributing.md](contributing.md) for guidelines.

---

## Future Questions

### Roadmap?

See [docs/roadmap.md](roadmap.md) for planned features:
- More target languages (V, Odin, Nim)
- GPU code generation
- ML-based optimization prediction
- Cloud integration (AWS Lambda, Google Cloud Functions)

### How can I help?

- Report bugs: https://github.com/b-macker/naab-pivot/issues
- Write plugins
- Add language templates
- Improve documentation
- Spread the word!

---

**Next:** [Contributing](contributing.md) | [Roadmap](roadmap.md)
