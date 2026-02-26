# Governance Integration

**Security Policy Enforcement with govern.json**

---

## Overview

NAAb Pivot enforces `govern.json` policies during code evolution to ensure:
- Only approved languages are used
- Network/filesystem access is controlled
- Code quality standards are met
- Execution limits are enforced

---

## Configuration

### Create govern.json

```bash
cd ~/naab-pivot
cat > govern.json <<'EOF'
{
  "version": "3.0",
  "mode": "enforce",

  "languages": {
    "allowed": ["python", "cpp", "rust", "go"]
  },

  "capabilities": {
    "network": {"enabled": false},
    "filesystem": {"mode": "read"}
  },

  "limits": {
    "timeout": {
      "global": 300,
      "per_block": 90
    }
  },

  "code_quality": {
    "no_secrets": {"level": "hard"},
    "no_placeholders": {"level": "soft"}
  }
}
EOF
```

---

## Enforcement Levels

- **hard:** Block execution, no override
- **soft:** Block execution, allow `--governance-override`
- **advisory:** Warn only

---

## Policy Sections

### 1. Languages

```json
{
  "languages": {
    "allowed": ["python", "cpp", "rust", "go", "bash"],
    "blocked": ["shell"]
  }
}
```

### 2. Capabilities

```json
{
  "capabilities": {
    "network": {"enabled": false},
    "filesystem": {"mode": "read"},  // read, write, none
    "shell": {"enabled": true}
  }
}
```

### 3. Limits

```json
{
  "limits": {
    "timeout": {
      "global": 300,
      "per_block": 90
    },
    "execution": {
      "call_depth": 50,
      "polyglot_blocks": 30
    },
    "code": {
      "max_lines_per_block": 300,
      "max_nesting_depth": 6
    }
  }
}
```

### 4. Code Quality

```json
{
  "code_quality": {
    "no_secrets": {"level": "hard"},
    "no_placeholders": {"level": "soft"},
    "no_hardcoded_results": {"level": "advisory"}
  }
}
```

---

## Usage

### Enforce Policies

```bash
# Policies automatically enforced
./naab/build/naab-lang pivot.naab evolve slow.py
```

### Override (Development)

```bash
# Use with caution
./naab/build/naab-lang pivot.naab --governance-override evolve slow.py
```

### Generate Report

```bash
./naab/build/naab-lang pivot.naab --governance-report report.json evolve slow.py
```

---

## CI/CD Integration

### GitHub Actions

```yaml
- name: Check Governance
  run: |
    ./naab/build/naab-lang pivot.naab \
      --governance-report governance.json \
      evolve slow.py

    # Fail if violations
    jq -e '.violations | length == 0' governance.json
```

---

**Next:** [CI/CD Guide](ci-cd.md) | [Security](security.md)
