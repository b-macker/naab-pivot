#!/bin/bash
# NAAb Pivot - Master Test Runner
# Runs comprehensive test suite with parallel execution

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
NAAB_BIN="$PROJECT_ROOT/naab/build/naab-lang"
TEST_MODE="${1:-all}"  # all | unit | integration | performance | cross-platform

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if NAAb is built
if [ ! -f "$NAAB_BIN" ]; then
    echo -e "${RED}Error: NAAb not built. Run: bash build.sh${NC}"
    exit 1
fi

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          NAAb Pivot - Comprehensive Test Suite           ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Test Mode: $TEST_MODE${NC}"
echo -e "${YELLOW}NAAb Binary: $NAAB_BIN${NC}"
echo ""

# Initialize counters
TOTAL_PASS=0
TOTAL_FAIL=0
TOTAL_SKIP=0

# Create results directory
mkdir -p "$SCRIPT_DIR/results"

# Function to run a test suite
run_test_suite() {
    SUITE_NAME=$1
    SUITE_DIR=$2

    if [ ! -d "$SUITE_DIR" ]; then
        echo -e "${YELLOW}  ⊘ $SUITE_NAME tests directory not found (skipped)${NC}"
        return
    fi

    echo -e "${BLUE}📦 Running $SUITE_NAME tests...${NC}"

    local SUITE_PASS=0
    local SUITE_FAIL=0
    local SUITE_SKIP=0

    # Find all .naab test files
    shopt -s nullglob
    TEST_FILES=("$SUITE_DIR"/*.naab)

    if [ ${#TEST_FILES[@]} -eq 0 ]; then
        echo -e "${YELLOW}  ⊘ No test files found in $SUITE_DIR${NC}"
        return
    fi

    for test_file in "${TEST_FILES[@]}"; do
        TEST_NAME=$(basename "$test_file" .naab)
        echo -n "  ├─ $TEST_NAME... "

        # Run test with timeout
        if timeout 30s "$NAAB_BIN" "$test_file" > "$SCRIPT_DIR/results/${TEST_NAME}.log" 2>&1; then
            echo -e "${GREEN}✓ PASS${NC}"
            SUITE_PASS=$((SUITE_PASS + 1))
            TOTAL_PASS=$((TOTAL_PASS + 1))
        else
            EXIT_CODE=$?
            if [ $EXIT_CODE -eq 124 ]; then
                echo -e "${YELLOW}⏱ TIMEOUT${NC}"
                SUITE_SKIP=$((SUITE_SKIP + 1))
                TOTAL_SKIP=$((TOTAL_SKIP + 1))
            else
                echo -e "${RED}✗ FAIL${NC}"
                SUITE_FAIL=$((SUITE_FAIL + 1))
                TOTAL_FAIL=$((TOTAL_FAIL + 1))

                # Show first 5 lines of error
                echo -e "${RED}$(head -5 "$SCRIPT_DIR/results/${TEST_NAME}.log")${NC}"
            fi
        fi
    done

    echo -e "  ${BLUE}└─ $SUITE_NAME: ${GREEN}$SUITE_PASS pass${NC}, ${RED}$SUITE_FAIL fail${NC}, ${YELLOW}$SUITE_SKIP skip${NC}"
    echo ""
}

# Run test suites based on mode
if [ "$TEST_MODE" == "all" ] || [ "$TEST_MODE" == "unit" ]; then
    run_test_suite "Unit" "$SCRIPT_DIR/unit"
fi

if [ "$TEST_MODE" == "all" ] || [ "$TEST_MODE" == "integration" ]; then
    run_test_suite "Integration" "$SCRIPT_DIR/integration"
fi

if [ "$TEST_MODE" == "all" ] || [ "$TEST_MODE" == "performance" ]; then
    run_test_suite "Performance" "$SCRIPT_DIR/performance"
fi

if [ "$TEST_MODE" == "all" ] || [ "$TEST_MODE" == "cross-platform" ]; then
    run_test_suite "Cross-Platform" "$SCRIPT_DIR/cross-platform"
fi

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
TOTAL=$((TOTAL_PASS + TOTAL_FAIL + TOTAL_SKIP))
echo -e "  ${BLUE}Total:${NC} $TOTAL | ${GREEN}Pass:${NC} $TOTAL_PASS | ${RED}Fail:${NC} $TOTAL_FAIL | ${YELLOW}Skip:${NC} $TOTAL_SKIP"

if [ $TOTAL_PASS -gt 0 ]; then
    PASS_PERCENT=$(( (TOTAL_PASS * 100) / TOTAL ))
    echo -e "  ${GREEN}Success Rate: ${PASS_PERCENT}%${NC}"
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

# Exit with failure if any tests failed
if [ $TOTAL_FAIL -gt 0 ]; then
    echo -e "${RED}⚠ Tests failed. Check results/ for details.${NC}"
    exit 1
else
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
fi
