# Security Best Practices

**Secure Code Evolution with NAAb Pivot**

---

## Governance Enforcement

### Enable Strict Governance

**File:** `govern.json`

```json
{
  "version": "3.0",
  "mode": "enforce",

  "languages": {
    "allowed": ["python", "cpp", "rust", "go"],
    "blocked": ["shell"]
  },

  "capabilities": {
    "network": {"enabled": false},
    "filesystem": {"mode": "read"},
    "shell": {"enabled": false}
  },

  "code_quality": {
    "no_secrets": {"level": "hard"},
    "no_placeholders": {"level": "hard"},
    "no_hardcoded_results": {"level": "hard"}
  }
}
```

---

## Input Validation

### Sanitize Inputs

```rust
fn process_input(input: &str) -> Result<f64, String> {
    // Validate input
    if input.is_empty() {
        return Err("Empty input".to_string());
    }

    // Parse with error handling
    match input.parse::<f64>() {
        Ok(value) => Ok(value),
        Err(_) => Err("Invalid number".to_string())
    }
}
```

### Bound Checking

```rust
fn safe_access(arr: &[f64], index: usize) -> Option<f64> {
    arr.get(index).copied()
}
```

---

## Secrets Management

### Never Hardcode Secrets

```rust
// ✗ Bad
const API_KEY: &str = "sk_live_abc123";

// ✓ Good
use std::env;
let api_key = env::var("API_KEY").expect("API_KEY not set");
```

### Use Environment Variables

```bash
export API_KEY="sk_live_abc123"
./vessels/app_vessel
```

---

## Memory Safety

### Use Safe Profiles

```bash
# Ultra-safe profile: No unsafe code
./naab/build/naab-lang pivot.naab evolve app.py --profile ultra-safe
```

### Rust Safety Features

```rust
// Borrow checker prevents use-after-free
fn safe_code() {
    let data = vec![1, 2, 3];
    let slice = &data[..];
    // data dropped, slice still valid - compile error
}
```

---

## Vulnerability Scanning

### CodeQL Scanning

**File:** `.github/workflows/codeql.yml`

```yaml
name: CodeQL

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v3
      - uses: github/codeql-action/init@v2
        with:
          languages: cpp, rust, go
      - run: bash build.sh
      - uses: github/codeql-action/analyze@v2
```

### Dependency Scanning

```bash
# Rust
cargo audit

# Go
go list -json -m all | nancy sleuth

# C++
cppcheck --enable=all src/
```

---

## Sandboxing

### Docker Isolation

```bash
docker run --rm \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --read-only \
  -v $(pwd):/workspace:ro \
  bmacker/naab-pivot:latest \
  naab-lang /opt/naab-pivot/pivot.naab analyze /workspace/app.py
```

### Seccomp Profiles

```bash
docker run --rm \
  --security-opt seccomp=seccomp-profile.json \
  bmacker/naab-pivot:latest
```

---

## Safe Compilation Flags

### Rust

```toml
# Cargo.toml
[profile.release]
overflow-checks = true
```

### C++

```bash
g++ -O2 \
  -fstack-protector-strong \
  -D_FORTIFY_SOURCE=2 \
  -Wformat -Wformat-security \
  app.cpp
```

### Go

```bash
go build -race -gcflags=all=-d=checkptr app.go
```

---

## Supply Chain Security

### Verify Submodules

```bash
cd naab-pivot
git submodule status
# Verify commit hash matches official repository
```

### Pin Dependencies

**Rust:**

```toml
# Cargo.lock committed
```

**Go:**

```
# go.sum committed
```

---

## Security Checklist

- [ ] Governance enabled (`govern.json`)
- [ ] No hardcoded secrets
- [ ] Input validation implemented
- [ ] Bounds checking enabled
- [ ] Safe profile used (`ultra-safe` or `conservative`)
- [ ] CodeQL scanning enabled
- [ ] Dependency scanning configured
- [ ] Docker sandboxing applied
- [ ] Supply chain verified
- [ ] Security audit completed

---

## Reporting Vulnerabilities

**Email:** security@naab-pivot.dev

**PGP Key:** [naab-pivot-security.asc](https://naab-pivot.dev/security.asc)

**Responsible Disclosure:**
1. Email security team with details
2. Allow 90 days for patch
3. Coordinated disclosure

---

**Next:** [FAQ](faq.md) | [Governance](governance.md)
