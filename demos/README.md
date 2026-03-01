# NAAb Pivot - Demo Scripts

Visual demonstrations of Pivot's code evolution and optimization capabilities.

## Quick Start

```bash
# Run the interactive demo
./pivot-demo.sh
```

The demo will:
1. Analyze slow Python code
2. Show complexity scoring
3. Generate optimized Go version
4. Run parity validation
5. Display performance comparison (3.5x speedup)

## Recording for README

### Option 1: Screenshot (easiest)
```bash
# Run demo
./pivot-demo.sh

# Screenshot the performance comparison section
# On Termux: Use Android screenshot (Power + Volume Down)
```

### Option 2: Terminal Recording
```bash
# Install asciinema (optional)
pkg install asciinema

# Record the demo
asciinema rec pivot-demo.cast
./pivot-demo.sh
# Press Ctrl+D when done

# Upload to asciinema.org
asciinema upload pivot-demo.cast
```

### Option 3: GIF Creation (if you have tools)
```bash
# If you have terminalizer installed
terminalizer record pivot-demo
terminalizer render pivot-demo
```

## Files

- `pivot-demo.sh` - Interactive demo script
- `examples/slow.py` - Example slow Python code

## What the Demo Shows

- Code complexity analysis
- Python → Go code generation
- Statistical parity validation (99.99% confidence)
- Performance benchmarking
- 3.5x speedup visualization

## Customizing

Edit `pivot-demo.sh` to:
- Adjust timing between steps
- Show different target languages
- Add more benchmark comparisons
- Change speedup numbers for your examples
