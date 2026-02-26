#!/bin/bash
# install.sh - System-wide installation for naab-pivot
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PREFIX="${1:-/usr/local}"

# Check if user has write permission to PREFIX
if [ ! -w "$PREFIX" ]; then
    echo "⚠ No write permission to $PREFIX"
    echo "Run with sudo: sudo bash install.sh"
    echo "Or specify a different prefix: bash install.sh ~/.local"
    exit 1
fi

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        NAAb Pivot - System Installation                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Installation prefix: $PREFIX"
echo ""

# Build if not already built
if [ ! -f "$SCRIPT_DIR/naab/build/naab-lang" ]; then
    echo "Building NAAb first..."
    bash "$SCRIPT_DIR/build.sh"
fi

# Create installation directories
mkdir -p "$PREFIX/bin"
mkdir -p "$PREFIX/share/naab-pivot"
mkdir -p "$PREFIX/share/naab-pivot/templates"
mkdir -p "$PREFIX/share/naab-pivot/profiles"
mkdir -p "$PREFIX/share/naab-pivot/examples"

# Install naab-lang binary
echo "Installing naab-lang binary..."
cp "$SCRIPT_DIR/naab/build/naab-lang" "$PREFIX/bin/"

# Install naab-pivot scripts
echo "Installing naab-pivot scripts..."
cp "$SCRIPT_DIR"/pivot.naab "$PREFIX/share/naab-pivot/"
cp "$SCRIPT_DIR"/analyze.naab "$PREFIX/share/naab-pivot/"
cp "$SCRIPT_DIR"/synthesize.naab "$PREFIX/share/naab-pivot/"
cp "$SCRIPT_DIR"/validate.naab "$PREFIX/share/naab-pivot/"
cp "$SCRIPT_DIR"/benchmark.naab "$PREFIX/share/naab-pivot/"
cp "$SCRIPT_DIR"/migrate.naab "$PREFIX/share/naab-pivot/"

# Install modules
echo "Installing modules..."
cp -r "$SCRIPT_DIR"/modules "$PREFIX/share/naab-pivot/"

# Install templates
echo "Installing templates..."
cp -r "$SCRIPT_DIR"/templates/* "$PREFIX/share/naab-pivot/templates/"

# Install profiles
echo "Installing profiles..."
cp -r "$SCRIPT_DIR"/profiles/* "$PREFIX/share/naab-pivot/profiles/"

# Install examples
echo "Installing examples..."
cp -r "$SCRIPT_DIR"/examples/* "$PREFIX/share/naab-pivot/examples/"

# Create naab-pivot wrapper script
echo "Creating naab-pivot command..."
cat > "$PREFIX/bin/naab-pivot" <<'WRAPPER'
#!/bin/bash
PIVOT_DIR="/usr/local/share/naab-pivot"
if [ -d "$HOME/.local/share/naab-pivot" ]; then
    PIVOT_DIR="$HOME/.local/share/naab-pivot"
fi

exec naab-lang "$PIVOT_DIR/pivot.naab" "$@"
WRAPPER

chmod +x "$PREFIX/bin/naab-pivot"

echo ""
echo "✓ Installation complete!"
echo ""
echo "Installed binaries:"
echo "  $PREFIX/bin/naab-lang"
echo "  $PREFIX/bin/naab-pivot"
echo ""
echo "Installation directory:"
echo "  $PREFIX/share/naab-pivot/"
echo ""
echo "Usage:"
echo "  naab-pivot --help"
echo "  naab-pivot analyze file.py"
echo "  naab-pivot evolve file.py --profile balanced"
echo ""

# Check if PREFIX/bin is in PATH
if [[ ":$PATH:" != *":$PREFIX/bin:"* ]]; then
    echo "⚠ Warning: $PREFIX/bin is not in your PATH"
    echo "Add to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"$PREFIX/bin:\$PATH\""
    echo ""
fi
