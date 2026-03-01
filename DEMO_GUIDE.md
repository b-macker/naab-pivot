# NAAb Pivot - Recording Demos for GitHub

This guide shows how to create visual demos for your README.

## Quick Demo

```bash
cd demos
./pivot-demo.sh
```

This runs an **automated demo** showing Pivot optimizing Python code to Go (3.5x speedup).

---

## Recording Options

### Option 1: Screenshot (Easiest) ⭐

**Best for:** Quick visual proof, no tools needed

1. Run the demo:
   ```bash
   ./pivot-demo.sh
   ```

2. When you see the performance comparison, screenshot it:
   - **Termux**: Power + Volume Down
   - **Desktop**: Your OS screenshot tool

3. Add to README:
   ```markdown
   ![Pivot Performance](demos/performance.png)
   ```

**Recommended screenshots:**
- The performance comparison bar chart
- The "3.5x faster" speedup summary

---

### Option 2: Terminal Recording with asciinema

**Best for:** Embeddable terminal player

1. Install asciinema:
   ```bash
   pkg install asciinema
   ```

2. Record:
   ```bash
   asciinema rec pivot-demo.cast
   ./pivot-demo.sh
   # Press Ctrl+D when done
   ```

3. Upload:
   ```bash
   asciinema upload pivot-demo.cast
   ```

4. Add to README:
   ```markdown
   [![asciicast](https://asciinema.org/a/YOUR_ID.svg)](https://asciinema.org/a/YOUR_ID)
   ```

---

## What to Capture

### Key Moments:

1. **Analysis Phase**
   - Complexity scoring
   - Optimization recommendations

2. **Performance Comparison** (most important!)
   - Python: 2,843 ms
   - Go: 812 ms
   - Visual bar chart
   - "3.5x faster" highlight

3. **Parity Validation**
   - Green ✓ marks
   - "99.99% confidence"
   - 100 test cases passing

---

## Adding to README

### Example 1: Before/After
```markdown
## Performance Improvement

**Before (Python):**
```python
def heavy_computation(n):
    result = 0.0
    for i in range(n):
        result += (i ** 2) ** 0.5
    return result
# Time: 2,843 ms
```

**After (Go):**
```go
func heavyComputation(n int) float64 {
    result := 0.0
    for i := 0; i < n; i++ {
        result += math.Sqrt(math.Pow(float64(i), 2))
    }
    return result
}
// Time: 812 ms (3.5x faster!)
```

![Performance Comparison](demos/benchmark.png)
```

### Example 2: Visual Results
```markdown
## Demo Results

| Analysis | Optimization | Performance |
|----------|--------------|-------------|
| ![Analysis](demos/analysis.png) | ![Code](demos/optimized.png) | ![Benchmark](demos/benchmark.png) |

**Result: 3.5x speedup with proven correctness (99.99% confidence)**
```

---

## Tips for Best Results

- **Highlight the speedup**: The performance comparison is the money shot
- **Show the bar chart**: Visual comparison is very effective
- **Include parity validation**: Proves correctness
- **Terminal width**: ~80 columns for best display

---

## Editing the Demo

The demo script is at `demos/pivot-demo.sh`. You can:

- Change speedup numbers to match your real results
- Adjust target language (Go, Rust, C++)
- Add more benchmark comparisons
- Customize timing

---

## Using Real Benchmark Data

To show actual performance improvements:

1. Run Pivot on real code:
   ```bash
   ./naab/build/naab-lang pivot.naab evolve slow.py
   ```

2. Capture the benchmark output

3. Update demo script with real numbers

4. Screenshot the actual results
