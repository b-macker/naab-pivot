# Contributing to NAAb Pivot

**Thank you for your interest in contributing!**

---

## Ways to Contribute

1. **Report Bugs:** https://github.com/b-macker/naab-pivot/issues
2. **Suggest Features:** Open feature request issue
3. **Write Code:** Submit pull requests
4. **Improve Docs:** Fix typos, add examples
5. **Create Plugins:** Share custom analyzers/synthesizers
6. **Write Templates:** Add new target languages
7. **Share Examples:** Real-world use cases

---

## Getting Started

### 1. Fork Repository

```bash
# Fork on GitHub
# https://github.com/b-macker/naab-pivot/fork

# Clone your fork
git clone --recursive https://github.com/YOUR_USERNAME/naab-pivot.git
cd naab-pivot
```

### 2. Create Branch

```bash
git checkout -b feature/my-feature
```

### 3. Make Changes

```bash
# Build and test
bash build.sh
cd tests && bash run-all-tests.sh
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: Add my feature

Detailed description of changes.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

### 5. Push and Create PR

```bash
git push origin feature/my-feature

# Create PR on GitHub
```

---

## Development Setup

### Dependencies

```bash
# Ubuntu/Debian
sudo apt-get install cmake build-essential golang rustc g++ clang python3 ruby nodejs npm php zig julia

# macOS
brew install cmake go rust llvm python ruby node php zig julia
```

### Build NAAb

```bash
bash build.sh

# Verify
./naab/build/naab-lang --version
```

### Run Tests

```bash
cd tests
bash run-all-tests.sh

# Run specific test
bash run-all-tests.sh unit
bash run-all-tests.sh integration
```

---

## Code Guidelines

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
test: Add tests
refactor: Refactor code
perf: Improve performance
chore: Maintenance tasks
```

### Code Style

- **NAAb:** Follow existing style (snake_case functions, clear names)
- **Go:** `gofmt`
- **Rust:** `rustfmt`
- **C++:** Clang-format

### Documentation

- Add docstrings to functions
- Update README.md if adding features
- Add examples in `examples/` for new functionality
- Update relevant docs in `docs/`

---

## Adding Features

### Adding New Template

1. Create template file:

```bash
cp templates/go_template.naab templates/v_template.naab
```

2. Update template engine:

```naab
// In modules/template_engine.naab
fn get_extension(target) {
    if target == "V" { return "v" }
    // ...
}
```

3. Add tests:

```bash
# Create test case
cat > tests/unit/test-v-template.naab <<'EOF'
// Test V template
use template_engine
main {
    let code = template_engine.generate({...}, "V")
    // Assert expectations
}
EOF
```

4. Update documentation:

```bash
# Add to docs/templates.md
```

### Adding New Profile

1. Create profile file:

```bash
cat > profiles/my-profile.json <<'EOF'
{
  "name": "my-profile",
  "optimization_level": 2,
  ...
}
EOF
```

2. Document in `docs/profiles.md`

### Adding New Plugin

1. Create plugin directory:

```bash
mkdir -p plugins/analyzers/my-plugin
```

2. Create metadata:

```bash
cat > plugins/analyzers/my-plugin/my-plugin.json <<'EOF'
{
  "id": "my-plugin",
  "version": "1.0.0",
  "type": "analyzer"
}
EOF
```

3. Implement plugin:

```bash
cat > plugins/analyzers/my-plugin/my-plugin.naab <<'EOF'
export fn execute(input_data) {
    return {"status": "SUCCESS"}
}
EOF
```

4. Add tests

5. Document in `docs/plugins.md`

---

## Testing Guidelines

### Unit Tests

Test individual modules:

```naab
// tests/unit/test-analyze.naab
use analyzer

main {
    let result = analyzer.analyze_file("fixture.py")
    assert(result["status"] == "ANALYZED")
}
```

### Integration Tests

Test full pipeline:

```naab
// tests/integration/test-full-pipeline.naab
use analyzer
use synthesizer
use validator

main {
    // Test analyze → synthesize → validate
}
```

### Performance Tests

Track performance regressions:

```naab
// tests/performance/bench-analyzer.naab
use benchmark

main {
    let result = benchmark.run_single_benchmark("analyzer.bench.json")
    assert(result["mean"] < 1000)  // < 1 second
}
```

---

## Pull Request Checklist

Before submitting PR:

- [ ] Tests pass: `bash tests/run-all-tests.sh`
- [ ] Code formatted
- [ ] Documentation updated
- [ ] Examples added (if new feature)
- [ ] CHANGELOG.md updated
- [ ] Commits follow conventional commits
- [ ] No merge conflicts
- [ ] PR description explains changes

---

## Review Process

1. **Automated Checks:** CI runs tests, linters, security scans
2. **Code Review:** Maintainer reviews code
3. **Feedback:** Address reviewer comments
4. **Approval:** PR approved and merged
5. **Release:** Included in next release

---

## Code of Conduct

Be respectful, inclusive, and constructive. See [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md).

---

## Questions?

- **Discord:** https://discord.gg/naab-pivot
- **GitHub Discussions:** https://github.com/b-macker/naab-pivot/discussions
- **Email:** dev@naab-pivot.dev

---

**Thank you for contributing!** 🚀
