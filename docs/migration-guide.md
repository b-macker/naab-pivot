# Incremental Migration Guide

**Migrating Large Codebases with NAAb Pivot**

---

## Strategy Overview

### Phase 1: Analysis (Week 1-2)
- Profile application
- Identify hotspots
- Prioritize candidates

### Phase 2: Prototype (Week 3-4)
- Optimize top 3 hotspots
- Validate parity
- Measure impact

### Phase 3: Incremental Rollout (Week 5-12)
- Deploy Phase 1 functions
- Monitor production
- Iterate on remaining functions

### Phase 4: Stabilization (Week 13-16)
- Performance tuning
- Documentation
- Training

---

## Creating Migration Plan

```bash
./naab/build/naab-lang migrate.naab create_migration_plan /path/to/project
```

**Output:** `migration-plan.json`

```json
{
  "total_files": 156,
  "candidates": [
    {
      "file": "core/sales_aggregator.py",
      "score": 92.3,
      "estimated_speedup": 12.5,
      "functions": [...]
    }
  ],
  "phases": [
    {
      "phase": 1,
      "name": "Low-hanging fruit",
      "files": 12,
      "estimated_effort_weeks": 6
    }
  ]
}
```

---

## Hotspot Detection

### Profile Application

**Python:**

```bash
python -m cProfile -o app.prof app.py
```

**Ruby:**

```bash
gem install ruby-prof
ruby-prof app.rb > profile.txt
```

### Analyze Profile

```bash
./naab/build/naab-lang pivot.naab analyze app.py --profile-data app.prof --hotspot-only
```

---

## Migration Patterns

### Pattern 1: Function-Level Evolution

**Before:**

```python
# core/sales.py
def calculate_commission(sales_data):
    total = 0
    for sale in sales_data:
        total += sale['amount'] * 0.05
    return total
```

**After:**

```python
# core/sales.py
import vessel_calculate_commission

def calculate_commission(sales_data):
    # Delegate to optimized vessel
    return vessel_calculate_commission.run(sales_data)
```

### Pattern 2: Module-Level Evolution

Replace entire Python module with Go package:

**Before:**

```python
from core import sales_aggregator
result = sales_aggregator.aggregate(data)
```

**After:**

```python
import ctypes
sales_lib = ctypes.CDLL('./vessels/sales_aggregator.so')
result = sales_lib.aggregate(data)
```

### Pattern 3: Service-Level Evolution

Extract hotspot as microservice:

**Before:** Python monolith

**After:** Python API Gateway + Rust compute service

---

## FFI Integration

### Python ↔ Go (PyO3)

**Go vessel:**

```go
//export CalculateCommission
func CalculateCommission(data *C.char) C.double {
    // Implementation
}
```

**Python wrapper:**

```python
import ctypes

lib = ctypes.CDLL('./vessels/sales.so')
lib.CalculateCommission.argtypes = [ctypes.c_char_p]
lib.CalculateCommission.restype = ctypes.c_double

def calculate_commission(sales_data):
    json_data = json.dumps(sales_data).encode('utf-8')
    return lib.CalculateCommission(json_data)
```

### Python ↔ Rust (PyO3)

**Rust vessel:**

```rust
use pyo3::prelude::*;

#[pyfunction]
fn calculate_commission(sales_data: Vec<f64>) -> f64 {
    sales_data.iter().sum::<f64>() * 0.05
}

#[pymodule]
fn vessel_sales(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_commission, m)?)?;
    Ok(())
}
```

**Python usage:**

```python
import vessel_sales

result = vessel_sales.calculate_commission(sales_data)
```

---

## Deployment Strategies

### Strategy 1: Canary Deployment

```python
import random

def calculate_commission(sales_data):
    if random.random() < 0.1:  # 10% traffic
        return vessel_calculate_commission.run(sales_data)
    else:
        return legacy_calculate_commission(sales_data)
```

### Strategy 2: Feature Flag

```python
from feature_flags import is_enabled

def calculate_commission(sales_data):
    if is_enabled('use_optimized_commission'):
        return vessel_calculate_commission.run(sales_data)
    else:
        return legacy_calculate_commission(sales_data)
```

### Strategy 3: A/B Testing

```python
def calculate_commission(sales_data, user_id):
    if user_id % 2 == 0:  # Group A
        return vessel_calculate_commission.run(sales_data)
    else:  # Group B
        return legacy_calculate_commission(sales_data)
```

---

## Monitoring

### Metrics to Track

1. **Performance:** Response time, throughput
2. **Correctness:** Error rate, output validation
3. **Resource Usage:** CPU, memory, network
4. **Business Impact:** Revenue, user engagement

### Example Dashboard

```python
import prometheus_client

latency_histogram = prometheus_client.Histogram('commission_latency', 'Commission calculation latency')

@latency_histogram.time()
def calculate_commission(sales_data):
    return vessel_calculate_commission.run(sales_data)
```

---

## Rollback Plan

### Immediate Rollback

```python
# Emergency rollback flag
USE_VESSEL = os.getenv('USE_OPTIMIZED_COMMISSION', 'true') == 'true'

def calculate_commission(sales_data):
    if USE_VESSEL:
        try:
            return vessel_calculate_commission.run(sales_data)
        except Exception as e:
            logger.error(f"Vessel failed: {e}, falling back to legacy")
            return legacy_calculate_commission(sales_data)
    else:
        return legacy_calculate_commission(sales_data)
```

**Rollback:**

```bash
export USE_OPTIMIZED_COMMISSION=false
systemctl restart app
```

---

## Best Practices

1. **Start Small:** Optimize 1-3 functions first
2. **Validate Thoroughly:** 10,000+ test cases
3. **Monitor Closely:** Track metrics for 1-2 weeks
4. **Keep Fallback:** Legacy code for emergency rollback
5. **Document Changes:** Update architecture diagrams
6. **Train Team:** Knowledge transfer sessions

---

## Case Study: E-Commerce Platform

**Problem:** Sales aggregation slow (23.4% CPU time)

**Solution:**

1. **Week 1-2:** Profiling identified `calculate_commission` hotspot
2. **Week 3-4:** Evolved to Rust, 12.5x speedup
3. **Week 5:** Canary deployment (10% traffic)
4. **Week 6:** Increased to 50% traffic
5. **Week 7:** Full rollout (100% traffic)

**Result:**
- Response time: 245ms → 19ms
- CPU usage: -78%
- Revenue: +12% (faster checkout)
- ROI: 2 months

---

**Next:** [Performance Tuning](performance-tuning.md) | [Security](security.md)
