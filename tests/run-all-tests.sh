#!/bin/bash
# tests/run-all-tests.sh - Master test runner with parallel execution
# Usage: bash run-all-tests.sh [all|unit|integration|performance|cross-platform]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
NAAB_BIN="$PROJECT_ROOT/naab/build/naab-lang"
TEST_MODE="${1:-all}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        NAAb Pivot - Comprehensive Test Suite             ║"
echo "║        Polyglot Code Evolution Testing                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check NAAb binary exists
if [ ! -f "$NAAB_BIN" ]; then
    echo -e "${RED}Error: NAAb binary not found at $NAAB_BIN${NC}"
    echo "Run: bash build.sh"
    exit 1
fi

echo "📍 Project root: $PROJECT_ROOT"
echo "🔧 NAAb binary: $NAAB_BIN"
echo "🎯 Test mode: $TEST_MODE"
echo ""

# Test counters
TOTAL_PASS=0
TOTAL_FAIL=0
TOTAL_SKIP=0

# Create results directory
mkdir -p "$SCRIPT_DIR/results"

# Run a single test file
run_test() {
    local test_file="$1"
    local suite_name="$2"
    local test_name=$(basename "$test_file" .naab)

    echo -n "  ├─ $test_name... "

    # Run test with timeout
    if timeout 30s "$NAAB_BIN" "$test_file" > "$SCRIPT_DIR/results/${suite_name}_${test_name}.log" 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        TOTAL_PASS=$((TOTAL_PASS + 1))
        return 0
    else
        local exit_code=$?
        if [ $exit_code -eq 124 ]; then
            echo -e "${YELLOW}⏱ TIMEOUT${NC}"
        else
            echo -e "${RED}✗ FAIL${NC}"
            # Show first 10 lines of error
            head -n 10 "$SCRIPT_DIR/results/${suite_name}_${test_name}.log" | sed 's/^/      /'
        fi
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
        return 1
    fi
}

# Run a test suite
run_suite() {
    local suite_name="$1"
    local suite_dir="$2"

    if [ ! -d "$suite_dir" ]; then
        echo -e "${YELLOW}⚠ Suite directory not found: $suite_dir${NC}"
        return
    fi

    local test_count=$(find "$suite_dir" -name "*.naab" -type f | wc -l)
    if [ "$test_count" -eq 0 ]; then
        echo -e "${YELLOW}⚠ No tests found in $suite_name${NC}"
        return
    fi

    echo -e "${BLUE}📦 Running $suite_name tests ($test_count tests)...${NC}"

    # Run each test in suite
    for test_file in "$suite_dir"/*.naab; do
        if [ -f "$test_file" ]; then
            run_test "$test_file" "$suite_name"
        fi
    done

    echo ""
}

# Run test suites based on mode
if [ "$TEST_MODE" == "all" ] || [ "$TEST_MODE" == "unit" ]; then
    run_suite "Unit" "$SCRIPT_DIR/unit"
fi

if [ "$TEST_MODE" == "all" ] || [ "$TEST_MODE" == "integration" ]; then
    run_suite "Integration" "$SCRIPT_DIR/integration"
fi

if [ "$TEST_MODE" == "all" ] || [ "$TEST_MODE" == "performance" ]; then
    run_suite "Performance" "$SCRIPT_DIR/performance"
fi

if [ "$TEST_MODE" == "all" ] || [ "$TEST_MODE" == "cross-platform" ]; then
    run_suite "Cross-Platform" "$SCRIPT_DIR/cross-platform"
fi

# Final summary
echo "═══════════════════════════════════════════════════════════"
echo -e "  Total: $((TOTAL_PASS + TOTAL_FAIL + TOTAL_SKIP)) | ${GREEN}Pass: $TOTAL_PASS${NC} | ${RED}Fail: $TOTAL_FAIL${NC} | ${YELLOW}Skip: $TOTAL_SKIP${NC}"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Generate summary report
cat > "$SCRIPT_DIR/results/summary.txt" <<EOF
NAAb Pivot Test Summary
Generated: $(date)

Test Mode: $TEST_MODE
Total Tests: $((TOTAL_PASS + TOTAL_FAIL + TOTAL_SKIP))
Passed: $TOTAL_PASS
Failed: $TOTAL_FAIL
Skipped: $TOTAL_SKIP
Success Rate: $(awk "BEGIN {printf \"%.2f\", ($TOTAL_PASS / ($TOTAL_PASS + $TOTAL_FAIL)) * 100}")%
EOF

echo "📊 Test report: $SCRIPT_DIR/results/summary.txt"

# Exit with failure if any tests failed
if [ $TOTAL_FAIL -gt 0 ]; then
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
else
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
fi
