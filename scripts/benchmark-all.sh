#!/bin/bash
# benchmark-all.sh - Run all NAAb Pivot benchmark suites
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
NAAB_BIN="$ROOT_DIR/naab/build/naab-lang"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        NAAb Pivot - Nightly Benchmark Suite               ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Verify naab-lang binary exists
if [ ! -x "$NAAB_BIN" ]; then
    echo "Error: naab-lang not found at $NAAB_BIN"
    echo "Run build.sh first"
    exit 1
fi

echo "Using: $NAAB_BIN"
echo "Date:  $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

PASS=0
FAIL=0

# Run each benchmark suite
for bench in "$ROOT_DIR/tests/performance"/bench-*.naab; do
    if [ -f "$bench" ]; then
        name=$(basename "$bench")
        echo "━━━ Running: $name ━━━"
        if "$NAAB_BIN" "$bench" 2>&1; then
            echo "✓ $name passed"
            PASS=$((PASS + 1))
        else
            echo "✗ $name failed"
            FAIL=$((FAIL + 1))
        fi
        echo ""
    fi
done

# Run the main benchmark module
echo "━━━ Running: benchmark.naab (full suite) ━━━"
if "$NAAB_BIN" "$ROOT_DIR/benchmark.naab" 2>&1; then
    echo "✓ benchmark.naab passed"
    PASS=$((PASS + 1))
else
    echo "✗ benchmark.naab failed"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "════════════════════════════════════════"
echo "Results: $PASS passed, $FAIL failed"
echo "════════════════════════════════════════"

# Store results as JSON for the workflow
mkdir -p "$ROOT_DIR/benchmark-history"
DATE=$(date +%Y-%m-%d)
cat > "$ROOT_DIR/benchmark-history/${DATE}.json" <<EOF
{
  "date": "$DATE",
  "passed": $PASS,
  "failed": $FAIL,
  "total": $((PASS + FAIL))
}
EOF

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
