#!/bin/bash
# NAAb Pivot - Dashboard Functionality Test
# Tests the web dashboard components

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
NAAB_BIN="$PROJECT_ROOT/naab/build/naab-lang"
DASHBOARD_DIR="$PROJECT_ROOT/dashboard"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         NAAb Pivot - Dashboard Functionality Test        ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

PASSED=0
FAILED=0

# Test 1: Dashboard files exist
echo -e "${BLUE}Test 1: Dashboard files existence...${NC}"

DASHBOARD_FILES=(
    "serve.naab"
    "static/index.html"
    "static/style.css"
    "static/app.js"
    "static/charts.js"
)

for file in "${DASHBOARD_FILES[@]}"; do
    if [ -f "$DASHBOARD_DIR/$file" ]; then
        echo -e "  ├─ $file... ${GREEN}✓${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ├─ $file... ${RED}✗ MISSING${NC}"
        FAILED=$((FAILED + 1))
    fi
done

echo ""

# Test 2: HTML structure validation
echo -e "${BLUE}Test 2: HTML structure validation...${NC}"

if grep -q "<div id=\"projects-list\">" "$DASHBOARD_DIR/static/index.html"; then
    echo -e "  ├─ Projects section... ${GREEN}✓${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "  ├─ Projects section... ${RED}✗ MISSING${NC}"
    FAILED=$((FAILED + 1))
fi

if grep -q "<canvas id=\"performanceChart\">" "$DASHBOARD_DIR/static/index.html"; then
    echo -e "  ├─ Performance chart... ${GREEN}✓${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "  ├─ Performance chart... ${RED}✗ MISSING${NC}"
    FAILED=$((FAILED + 1))
fi

if grep -q "<div id=\"vessels-catalog\">" "$DASHBOARD_DIR/static/index.html"; then
    echo -e "  ├─ Vessels catalog... ${GREEN}✓${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "  ├─ Vessels catalog... ${RED}✗ MISSING${NC}"
    FAILED=$((FAILED + 1))
fi

echo ""

# Test 3: JavaScript dependencies
echo -e "${BLUE}Test 3: JavaScript dependencies...${NC}"

if grep -q "Chart.js" "$DASHBOARD_DIR/static/index.html"; then
    echo -e "  ├─ Chart.js CDN... ${GREEN}✓${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "  ├─ Chart.js CDN... ${RED}✗ MISSING${NC}"
    FAILED=$((FAILED + 1))
fi

if grep -q "axios" "$DASHBOARD_DIR/static/index.html"; then
    echo -e "  ├─ Axios CDN... ${GREEN}✓${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "  ├─ Axios CDN... ${RED}✗ MISSING${NC}"
    FAILED=$((FAILED + 1))
fi

echo ""

# Test 4: CSS styling
echo -e "${BLUE}Test 4: CSS styling validation...${NC}"

if grep -q ".card" "$DASHBOARD_DIR/static/style.css"; then
    echo -e "  ├─ Card styles... ${GREEN}✓${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "  ├─ Card styles... ${RED}✗ MISSING${NC}"
    FAILED=$((FAILED + 1))
fi

if grep -q "gradient" "$DASHBOARD_DIR/static/style.css"; then
    echo -e "  ├─ Gradient theme... ${GREEN}✓${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "  ├─ Gradient theme... ${RED}✗ MISSING${NC}"
    FAILED=$((FAILED + 1))
fi

echo ""

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
TOTAL=$((PASSED + FAILED))
echo -e "  ${BLUE}Total Tests:${NC} $TOTAL"
echo -e "  ${GREEN}Passed:${NC} $PASSED"
echo -e "  ${RED}Failed:${NC} $FAILED"

if [ $TOTAL -gt 0 ]; then
    PASS_PERCENT=$(( (PASSED * 100) / TOTAL ))
    echo -e "  ${GREEN}Success Rate: ${PASS_PERCENT}%${NC}"
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

# Exit status
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}⚠ Dashboard validation failed${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Dashboard validated successfully!${NC}"
    echo ""
    echo -e "${YELLOW}To test dashboard functionality:${NC}"
    echo -e "  1. Start server: ./naab/build/naab-lang dashboard/serve.naab"
    echo -e "  2. Open browser: http://localhost:8080"
    echo -e "  3. Verify all sections load correctly"
    exit 0
fi
