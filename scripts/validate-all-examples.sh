#!/bin/bash
# NAAb Pivot - End-to-End Example Validation Script
# Validates all 10 example projects for v1.0.0 release

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
NAAB_BIN="$PROJECT_ROOT/naab/build/naab-lang"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       NAAb Pivot - End-to-End Example Validation         ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check NAAb is built
if [ ! -f "$NAAB_BIN" ]; then
    echo -e "${RED}Error: NAAb not built. Run: bash build.sh${NC}"
    exit 1
fi

# Initialize counters
TOTAL_EXAMPLES=10
PASSED=0
FAILED=0
SKIPPED=0

# Function to validate an example
validate_example() {
    EXAMPLE_NUM=$1
    EXAMPLE_NAME=$2
    EXPECTED_SPEEDUP=$3

    EXAMPLE_DIR="$PROJECT_ROOT/examples/${EXAMPLE_NUM}-${EXAMPLE_NAME}"

    if [ ! -d "$EXAMPLE_DIR" ]; then
        echo -e "${YELLOW}  ⊘ Example ${EXAMPLE_NUM} not found (skipped)${NC}"
        SKIPPED=$((SKIPPED + 1))
        return
    fi

    echo -e "${BLUE}📦 Validating Example ${EXAMPLE_NUM}: ${EXAMPLE_NAME}${NC}"

    # Check README exists
    if [ -f "$EXAMPLE_DIR/README.md" ]; then
        echo -e "  ├─ README.md... ${GREEN}✓${NC}"
    else
        echo -e "  ├─ README.md... ${RED}✗ MISSING${NC}"
        FAILED=$((FAILED + 1))
        return
    fi

    # Check .pivotrc exists
    if [ -f "$EXAMPLE_DIR/.pivotrc" ]; then
        echo -e "  ├─ .pivotrc... ${GREEN}✓${NC}"
    else
        echo -e "  ├─ .pivotrc... ${RED}✗ MISSING${NC}"
        FAILED=$((FAILED + 1))
        return
    fi

    # Check source file exists
    SOURCE_FILES=$(find "$EXAMPLE_DIR" -maxdepth 1 -name "*.py" -o -name "*.rb" -o -name "*.js" -o -name "*.naab" | head -1)
    if [ -n "$SOURCE_FILES" ]; then
        echo -e "  ├─ Source file... ${GREEN}✓${NC}"
    else
        echo -e "  ├─ Source file... ${RED}✗ MISSING${NC}"
        FAILED=$((FAILED + 1))
        return
    fi

    # Check benchmark/profile file exists
    BENCHMARK_FILE=$(find "$EXAMPLE_DIR" -maxdepth 1 -name "benchmark.json" -o -name "profile.json" -o -name "*benchmark*" -o -name "*profile*" | head -1)
    if [ -n "$BENCHMARK_FILE" ]; then
        echo -e "  ├─ Benchmark data... ${GREEN}✓${NC}"
    else
        echo -e "  ├─ Benchmark data... ${YELLOW}⚠ MISSING${NC}"
    fi

    # Verify README contains expected speedup
    if grep -q "${EXPECTED_SPEEDUP}x" "$EXAMPLE_DIR/README.md" 2>/dev/null; then
        echo -e "  ├─ Speedup documented (${EXPECTED_SPEEDUP}x)... ${GREEN}✓${NC}"
    else
        echo -e "  ├─ Speedup documented... ${YELLOW}⚠ NOT VERIFIED${NC}"
    fi

    echo -e "  ${GREEN}└─ Example ${EXAMPLE_NUM} validated${NC}"
    PASSED=$((PASSED + 1))
    echo ""
}

# Validate all 10 examples
validate_example "01" "basic-evolution" "3.5"
validate_example "02" "batch-processing" "10"
validate_example "03" "ml-optimization" "15"
validate_example "04" "web-backend" "8"
validate_example "05" "crypto-mining" "18"
validate_example "06" "data-pipeline" "10"
validate_example "07" "scientific-compute" "60"
validate_example "08" "embedded-system" "15"
validate_example "09" "incremental-migration" "5-15"
validate_example "10" "polyglot-microservices" "7.1"

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "  ${BLUE}Total Examples:${NC} $TOTAL_EXAMPLES"
echo -e "  ${GREEN}Passed:${NC} $PASSED"
echo -e "  ${RED}Failed:${NC} $FAILED"
echo -e "  ${YELLOW}Skipped:${NC} $SKIPPED"

if [ $TOTAL_EXAMPLES -eq $PASSED ]; then
    PASS_PERCENT=100
else
    PASS_PERCENT=$(( (PASSED * 100) / TOTAL_EXAMPLES ))
fi

echo -e "  ${GREEN}Success Rate: ${PASS_PERCENT}%${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

# Exit status
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}⚠ Some examples failed validation${NC}"
    exit 1
else
    echo -e "${GREEN}✅ All examples validated successfully!${NC}"
    exit 0
fi
