#!/bin/bash
# build.sh - Build NAAb from submodule for naab-pivot
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NAAB_DIR="$SCRIPT_DIR/naab"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        NAAb Pivot - Building NAAb Language...            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if submodule is initialized
if [ ! -f "$NAAB_DIR/CMakeLists.txt" ]; then
    echo "⚠ NAAb submodule not initialized"
    echo "Initializing submodule..."
    cd "$SCRIPT_DIR"
    git submodule update --init --recursive
fi

# Detect number of CPU cores
if command -v nproc &> /dev/null; then
    NPROC=$(nproc)
elif command -v sysctl &> /dev/null; then
    NPROC=$(sysctl -n hw.ncpu)
else
    NPROC=4
fi

echo "Building NAAb with $NPROC parallel jobs..."
mkdir -p "$NAAB_DIR/build"
cd "$NAAB_DIR/build"

# Configure with CMake
cmake .. -DCMAKE_BUILD_TYPE=Release

# Build naab-lang
make naab-lang -j"$NPROC"

echo ""
echo "✓ NAAb built successfully!"
echo "Binary: $NAAB_DIR/build/naab-lang"
echo ""
echo "Usage:"
echo "  ./naab/build/naab-lang pivot.naab --help"
echo "  ./naab/build/naab-lang pivot.naab evolve examples/01-basic-evolution/slow.py"
echo ""
