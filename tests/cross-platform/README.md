# Cross-Platform Tests

These tests verify NAAb Pivot functionality across different operating systems.

## Test Coverage

### test-linux.naab
- Linux path handling (`/tmp/`, `/home/`)
- Compiler availability (gcc, g++, rustc, go)
- Shared library loading (.so files)
- POSIX-specific features

### test-macos.naab
- macOS path handling (`/Users/`, `/Applications/`)
- Homebrew compiler paths
- Dynamic library loading (.dylib files)
- macOS-specific features

### test-windows.naab
- Windows path handling (`C:\`, backslashes)
- MSVC/MinGW compiler detection
- DLL loading
- Windows-specific features

### test-android.naab
- Android/Termux path handling
- Cross-compilation support
- Limited compiler availability handling
- Resource constraints

## Running Tests

```bash
# Run all cross-platform tests
bash tests/run-all-tests.sh cross-platform

# Run specific platform test
./naab/build/naab-lang tests/cross-platform/test-linux.naab
```

## Platform-Specific Notes

**Linux:**
- Full compiler suite expected (gcc, g++, rustc, go)
- POSIX path conventions
- Shared library (.so) support

**macOS:**
- Compilers typically via Homebrew
- Different path conventions
- Dynamic library (.dylib) support

**Windows:**
- MSVC or MinGW required
- Backslash path separators
- DLL support
- May require WSL for full functionality

**Android/Termux:**
- Limited compiler availability
- Reduced resource limits
- Cross-compilation may be needed
- Storage permissions
