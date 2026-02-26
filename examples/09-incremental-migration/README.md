# Example 9: Incremental Migration Strategy

A comprehensive guide to gradually migrating large Python/Ruby codebases to compiled languages while maintaining system stability.

## Overview

**Challenge:** You have a large production codebase (100K+ lines) and want to optimize performance without a risky "big bang" rewrite.

**Solution:** Incremental migration using NAAb Pivot's hotspot-first strategy.

**Key Principles:**
1. **Profile First** - Identify actual bottlenecks, not assumed ones
2. **Prioritize Impact** - Optimize code that matters most
3. **Validate Continuously** - Prove parity at every step
4. **Deploy Gradually** - Canary releases minimize risk
5. **Maintain Velocity** - Keep shipping features during migration

---

## Case Study: Enterprise ERP System

### System Overview

**Application:** Multi-tenant ERP system (order management, inventory, pricing)
- **Codebase:** 156,234 lines (91% Python, 8% JavaScript, 1% SQL)
- **Files:** 487 total
- **Team:** 5 engineers
- **Users:** 50,000+ daily active users
- **Traffic:** 8M requests/day

**Pain Points:**
- **Slow batch jobs:** Nightly reports take 9.5 hours (block other jobs)
- **API latency:** P95 latency 850ms (SLA: 500ms)
- **High cloud costs:** $18,500/month (want to reduce)
- **Scaling issues:** Need 12 servers to handle peak traffic

**Goal:** 4x average speedup, 50% cost reduction, maintain stability

---

## Step 1: Analysis & Profiling

### Profile Production Traffic

```bash
# Enable production profiling (Python cProfile)
python -m cProfile -o production.prof main.py

# Analyze with NAAb Pivot
./naab/build/naab-lang pivot.naab analyze production.prof --output hotspots.json
```

**Analysis Results:**

| Component | Runtime % | Complexity | Target | Est. Speedup |
|-----------|-----------|------------|--------|--------------|
| `sales_aggregator.py::aggregate_daily_sales` | 23.4% | 87 | Go | 12x |
| `stock_calculator.py::calculate_reorder_points` | 18.7% | 65 | Rust | 8x |
| `discount_engine.py::apply_complex_discounts` | 12.3% | 52 | C++ | 6x |
| `orders.py::process_order_request` | 8.9% | 45 | Go | 7x |
| `recommendations.py::get_product_recommendations` | 7.2% | 72 | Rust | 9x |
| **Top 5 Total** | **70.5%** | — | — | **~8x avg** |

**Insight:** Optimizing just 5 functions covers 70.5% of CPU time!

---

## Step 2: Prioritization Matrix

### Priority Score Formula

```
priority_score = (runtime_percent × 10) + (complexity / 10) + (test_coverage × 50)
```

**Factors:**
- **Runtime %:** Higher = more impact
- **Complexity:** Higher = more optimization potential
- **Test Coverage:** Higher = safer to migrate
- **Dependencies:** Lower = easier to migrate

### Ranked Candidates (Phase 1)

```json
[
  {
    "rank": 1,
    "file": "core/reports/sales_aggregator.py",
    "function": "aggregate_daily_sales",
    "priority_score": 95,
    "runtime_percent": 23.4,
    "complexity": 87,
    "test_coverage": 0.89,
    "dependencies": 2,
    "target": "go",
    "estimated_speedup": "12x",
    "rationale": "Highest impact (23% of runtime), well-tested, few deps"
  },
  {
    "rank": 2,
    "file": "core/inventory/stock_calculator.py",
    "function": "calculate_reorder_points",
    "priority_score": 88,
    "runtime_percent": 18.7,
    "complexity": 65,
    "test_coverage": 0.92,
    "dependencies": 2,
    "target": "rust",
    "estimated_speedup": "8x",
    "rationale": "Second-highest impact, excellent tests, safety-critical"
  },
  {
    "rank": 3,
    "file": "core/pricing/discount_engine.py",
    "function": "apply_complex_discounts",
    "priority_score": 75,
    "runtime_percent": 12.3,
    "complexity": 52,
    "test_coverage": 0.85,
    "dependencies": 1,
    "target": "cpp",
    "estimated_speedup": "6x",
    "rationale": "Good impact, isolated component, good tests"
  }
]
```

---

## Step 3: Migration Phases

### Phase 1: Critical Hotspots (Weeks 1-6)

**Goal:** Optimize the top 3 bottlenecks (54.4% of CPU time)

**Candidates:**
1. `sales_aggregator.py` → Go (12x speedup)
2. `stock_calculator.py` → Rust (8x speedup)
3. `discount_engine.py` → C++ (6x speedup)

**Expected Impact:**
- Overall speedup: **2.1x** (from these 3 alone)
- Cost savings: **$4,200/month**
- Risk: **Low** (well-tested, few dependencies)

**Deliverables:**
- 3 compiled libraries (`.so` files)
- Python FFI wrappers
- Parity validation reports (100% pass)
- Performance benchmarks
- Canary deployment configs

---

### Phase 2: High-Traffic Endpoints (Weeks 7-14)

**Goal:** Reduce API latency for customer-facing endpoints

**Candidates:**
1. `api/v2/orders.py` → Go (2.4M requests/day)
2. `api/v2/products.py` → Rust (3.2M requests/day)
3. `api/v2/customers.py` → Go (1.8M requests/day)

**Expected Impact:**
- API latency: 850ms → 270ms (P95)
- Throughput: 4.2x increase
- Cost savings: **$6,800/month**

**Integration Strategy:**
- Microservices (loosely coupled)
- gRPC for Python ↔ Go communication
- Shared Redis cache

---

### Phase 3: Batch Processing Jobs (Weeks 15-24)

**Goal:** Speed up nightly batch jobs to free up resources

**Candidates:**
1. `jobs/nightly/etl_warehouse.py` → C++ (4.5 hour → 27 min)
2. `jobs/hourly/cache_warmup.py` → Go (48 min → 8 min)

**Expected Impact:**
- Batch job speedup: **10x average**
- Enables more frequent data refreshes
- Cost savings: **$3,500/month**

---

### Phase 4: Business Logic Libraries (Weeks 25-36)

**Goal:** Convert reusable libraries for long-term maintainability

**Candidates:**
1. `lib/tax_calculator.py` → Rust (used by 47 modules)
2. `lib/shipping_calculator.py` → Go (used by 32 modules)

**Expected Impact:**
- Overall codebase speedup: **4.2x cumulative**
- Reduced maintenance burden
- Cost savings: **$5,000/month total**

---

## Step 4: Integration Strategies

### Strategy 1: Foreign Function Interface (FFI)

**Best For:** CPU-intensive functions, minimal I/O, deterministic logic

**Example (Python ↔ Rust via PyO3):**

```rust
// Rust: src/lib.rs
use pyo3::prelude::*;

#[pyfunction]
fn calculate_reorder_points(sales_history: Vec<f64>, lead_time: i32) -> PyResult<f64> {
    // Rust implementation (8x faster than Python)
    let avg_demand = sales_history.iter().sum::<f64>() / sales_history.len() as f64;
    let reorder_point = avg_demand * lead_time as f64 * 1.2;  // 20% safety stock
    Ok(reorder_point)
}

#[pymodule]
fn inventory_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_reorder_points, m)?)?;
    Ok(())
}
```

```python
# Python: calling Rust
import inventory_rust

def calculate_reorder_points(sales_history, lead_time):
    # Seamless call to Rust (8x speedup)
    return inventory_rust.calculate_reorder_points(sales_history, lead_time)
```

**Pros:**
- Low latency (microseconds overhead)
- Transparent to callers
- Easy rollback (swap implementation)

**Cons:**
- Tight coupling
- Cross-language debugging harder
- FFI boundary requires careful data marshaling

---

### Strategy 2: Microservice Architecture

**Best For:** High-traffic APIs, independent deployment, team autonomy

**Example (Python API → Go Microservice):**

```python
# Python: API gateway
import requests

def process_order_request(order_data):
    # Call Go microservice via HTTP
    response = requests.post(
        'http://orders-service:8080/api/v1/process',
        json=order_data,
        timeout=5.0
    )
    return response.json()
```

```go
// Go: Microservice (orders-service)
package main

import (
    "encoding/json"
    "net/http"
)

func processOrderHandler(w http.ResponseWriter, r *http.Request) {
    var order Order
    json.NewDecoder(r.Body).Decode(&order)

    // Process order (7x faster than Python)
    result := processOrder(order)

    json.NewEncoder(w).Encode(result)
}

func main() {
    http.HandleFunc("/api/v1/process", processOrderHandler)
    http.ListenAndServe(":8080", nil)
}
```

**Pros:**
- Independent deployment
- Technology flexibility
- Team autonomy
- Scalability (horizontal scaling)

**Cons:**
- Network latency (10-50ms overhead)
- Operational complexity
- Distributed tracing needed
- More infrastructure

---

### Strategy 3: Hybrid Approach (Recommended)

**Best Practices:**
1. **FFI for compute-heavy functions** (math, algorithms, data processing)
2. **Microservices for APIs** (high traffic, independent scaling)
3. **Batch jobs as standalone binaries** (scheduled, no integration needed)

**Decision Matrix:**

| Workload Type | Integration | Reason |
|---------------|-------------|--------|
| CPU-intensive (algorithms) | FFI | Low latency critical |
| High-traffic API | Microservice | Independent scaling |
| Batch job | Standalone | No integration needed |
| Shared library | FFI | Used by many modules |

---

## Step 5: Validation & Testing

### Parity Validation

**Goal:** Prove that optimized code produces identical results to legacy code.

```bash
# Generate test inputs from production traffic
./naab/build/naab-lang pivot.naab generate-tests \
  --production-logs logs/2026-02-*.log \
  --output test_cases.json \
  --count 10000

# Run parity validation
./naab/build/naab-lang pivot.naab validate \
  --legacy sales_aggregator.py \
  --vessel sales_aggregator_go.so \
  --test-cases test_cases.json \
  --tolerance 0.0001
```

**Output:**
```
✓ Parity CERTIFIED

Test cases: 10,000
Passed: 10,000 (100%)
Failed: 0

Statistical Analysis:
  Max absolute error: 0.00008
  Max relative error: 0.0001%
  Mean absolute error: 0.000012

Performance:
  Legacy: 18.5 minutes
  Vessel: 1.5 minutes
  Speedup: 12.3x

Confidence: 99.99%
```

---

### Load Testing

**Simulate Production Traffic:**

```bash
# Locust load test configuration
# locustfile.py

from locust import HttpUser, task, between

class ERPUser(HttpUser):
    wait_time = between(1, 3)

    @task(10)
    def process_order(self):
        self.client.post("/api/v2/orders", json={
            "customer_id": 12345,
            "items": [{"product_id": 678, "quantity": 2}]
        })

    @task(5)
    def search_products(self):
        self.client.get("/api/v2/products?query=laptop")

# Run load test
locust --headless --users 1000 --spawn-rate 50 --run-time 10m
```

**Results:**

| Metric | Legacy (Python) | Vessel (Go) | Improvement |
|--------|-----------------|-------------|-------------|
| RPS | 1,247 | 8,934 | 7.16x |
| Latency (P50) | 215ms | 32ms | 6.7x lower |
| Latency (P95) | 850ms | 127ms | 6.7x lower |
| Latency (P99) | 1,450ms | 245ms | 5.9x lower |
| Error rate | 0.02% | 0.01% | 2x lower |

---

## Step 6: Gradual Rollout

### Canary Deployment with Feature Flags

**Infrastructure:**

```python
# Feature flag configuration
from feature_flags import FeatureFlag

use_go_aggregator = FeatureFlag('use_go_sales_aggregator', default=False)

def aggregate_daily_sales(records, target_date):
    if use_go_aggregator.is_enabled_for_user(current_user):
        # New: Go implementation (12x faster)
        return sales_aggregator_go.aggregate_daily_sales(records, target_date)
    else:
        # Legacy: Python implementation
        return _legacy_aggregate_daily_sales(records, target_date)
```

**Rollout Stages:**

```
Stage 1: Internal testing (0% production traffic)
  Duration: 3 days
  Criteria: All tests pass, no errors in staging

Stage 2: Canary (1% traffic)
  Duration: 2 days
  Criteria: Error rate < 0.01%, latency improvement visible
  Monitoring: Every 5 minutes

Stage 3: Early adopters (10% traffic)
  Duration: 3 days
  Criteria: No increase in error rate, performance gains confirmed

Stage 4: Half rollout (50% traffic)
  Duration: 5 days
  Criteria: Cost savings visible, system stable

Stage 5: Full rollout (100% traffic)
  Duration: 7 days
  Criteria: Legacy code can be deprecated

Total rollout time: 20 days per component
```

**Rollback Plan:**

```python
# Automatic rollback on error spike
if error_rate_last_hour() > 0.1%:
    use_go_aggregator.disable()
    alert_team("ROLLBACK: Go aggregator disabled due to errors")
    # Recovery time: ~5 minutes
```

---

## Step 7: Monitoring & Tracking

### Key Metrics Dashboard

**Performance Metrics:**
- Execution time (P50, P95, P99)
- Throughput (requests/sec or records/sec)
- Error rate (%)
- Memory usage (MB)
- CPU utilization (%)

**Business Metrics:**
- Cost per request ($)
- Monthly cloud spend ($)
- ROI progress (%)
- Migration completion (%)

**Example Grafana Dashboard:**

```
┌─────────────────────────────────────────────────────────┐
│ NAAb Pivot - Migration Progress                        │
├─────────────────────────────────────────────────────────┤
│ Overall Speedup: 2.8x            Cost Savings: $8,200/mo│
│ Components Migrated: 8/23        ROI: 62% (on track)   │
├─────────────────────────────────────────────────────────┤
│ Phase 1 (Critical Hotspots):     ████████████ 100%     │
│ Phase 2 (API Endpoints):         ████████░░░░  65%     │
│ Phase 3 (Batch Jobs):            ████░░░░░░░░  30%     │
│ Phase 4 (Libraries):             ░░░░░░░░░░░░   0%     │
├─────────────────────────────────────────────────────────┤
│ Latency Trend (P95):                                   │
│   Jan: 850ms  ████████████████████████████            │
│   Feb: 520ms  ███████████████░░░░░░░░░░░░░            │
│   Mar: 280ms  ████████░░░░░░░░░░░░░░░░░░░░            │
│   Apr: 127ms  ████░░░░░░░░░░░░░░░░░░░░░░░░ ← TARGET   │
└─────────────────────────────────────────────────────────┘
```

---

## Timeline & Milestones

### 36-Week Migration Plan

```
Week 1-6:   Phase 1 - Critical Hotspots (3 components)
            Expected: 2.1x overall speedup

Week 7-14:  Phase 2 - API Endpoints (5 endpoints)
            Expected: 3.2x overall speedup

Week 15-24: Phase 3 - Batch Jobs (7 jobs)
            Expected: 3.8x overall speedup

Week 25-36: Phase 4 - Libraries (8 libraries)
            Expected: 4.2x overall speedup

Total Duration: 9 months
Team Size: 5 engineers
Investment: $485,000
ROI: 2 months (break-even), $245K/year savings
```

---

## Risk Mitigation

### Common Risks & Solutions

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Performance regression in edge cases** | High | Comprehensive test suite + production replay |
| **Integration bugs (FFI boundary)** | High | Extensive integration tests + gradual rollout |
| **Increased deployment complexity** | Medium | Automated CI/CD + Docker containers |
| **Team knowledge gap** | Medium | Training + code reviews + pair programming |
| **Two codebases maintenance** | Low | Deprecate legacy code after successful migration |

---

## Success Criteria

### Phase 1 (Week 6)
- ✅ 3 hotspots optimized (54.4% of CPU time)
- ✅ 2.1x overall speedup measured
- ✅ Zero production incidents
- ✅ Parity validation: 100% pass rate
- ✅ Cost savings: $4,200/month

### Phase 2 (Week 14)
- ✅ 5 API endpoints migrated
- ✅ 3.2x overall speedup
- ✅ API latency: < 300ms (P95)
- ✅ Cost savings: $11,000/month cumulative

### Phase 3 (Week 24)
- ✅ Batch jobs complete in < 1 hour
- ✅ 3.8x overall speedup
- ✅ Cost savings: $14,500/month cumulative

### Phase 4 (Week 36 - Complete)
- ✅ 4.2x overall speedup achieved
- ✅ $245,000/year savings ($20,400/month)
- ✅ Legacy code deprecated
- ✅ Team proficient in new stack
- ✅ Documentation complete

---

## Lessons Learned

### What Worked Well

1. **Profile-driven prioritization** - Focus on actual bottlenecks, not assumptions
2. **Incremental rollout** - Canary deployment caught issues early
3. **Parity validation** - Automated testing prevented regressions
4. **Feature flags** - Fast rollback saved us twice
5. **Team training** - Pair programming accelerated learning

### What to Avoid

1. ❌ **Don't migrate everything** - 80/20 rule: optimize 20% that matters
2. ❌ **Don't skip validation** - Silent bugs are worst kind
3. ❌ **Don't rush rollout** - Gradual is safer than fast
4. ❌ **Don't ignore monitoring** - Track metrics from day 1
5. ❌ **Don't work in silos** - Communication is critical

---

## Tools & Resources

### NAAb Pivot Commands

```bash
# Analyze codebase for hotspots
pivot.naab analyze <file> --profile production.prof

# Generate migration plan
pivot.naab migrate <project-dir> --strategy incremental

# Validate parity
pivot.naab validate --legacy <python> --vessel <compiled> --tests <json>

# Track progress
pivot.naab migrate --status
```

### Recommended Tools

- **Profiling:** cProfile (Python), rbspy (Ruby), perf (Linux)
- **Load Testing:** Locust, k6, Apache Bench
- **Monitoring:** Grafana, Datadog, Prometheus
- **Feature Flags:** LaunchDarkly, Unleash, custom
- **CI/CD:** GitHub Actions, GitLab CI, Jenkins

---

## Next Steps

1. **Run profiling** on your production application
2. **Identify top 5 hotspots** using NAAb Pivot analyze
3. **Create migration plan** with prioritization matrix
4. **Start with Phase 1** (lowest risk, highest impact)
5. **Validate continuously** with parity testing
6. **Deploy gradually** with canary releases
7. **Monitor metrics** and adjust strategy
8. **Deprecate legacy** code after successful migration

---

## Key Takeaways

✅ **Profile First:** Optimize what matters (not everything)
✅ **Incremental > Rewrite:** Gradual migration reduces risk
✅ **Validate Always:** Parity testing prevents regressions
✅ **Deploy Gradually:** Canary releases catch issues early
✅ **Monitor Everything:** Track metrics to prove success
✅ **4.2x Speedup:** Achievable in 9 months with 5 engineers
✅ **2-Month ROI:** $485K investment → $245K/year savings

---

**Previous:** [Example 8: Embedded System (Python → Zig, 15x speedup)](../08-embedded-system/)
**Next:** [Example 10: Polyglot Microservices Architecture](../10-polyglot-microservices/)
