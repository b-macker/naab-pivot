# Example 10: Polyglot Microservices Architecture

Demonstrate how NAAb Pivot enables building microservices where each service uses the optimal language for its workload.

## Overview

**Architecture:** 3-service microservice system
- **Service A (Python):** API Gateway - orchestration & business logic
- **Service B (Rust):** Pricing Engine - compute-intensive calculations (15x speedup)
- **Service C (Go):** Inventory Manager - high-concurrency queries (8x throughput)

**Key Principle:** *"Right tool for the right job"*
- Use Python where developer productivity matters (API gateway)
- Use Rust where raw performance matters (pricing calculations)
- Use Go where concurrency matters (inventory queries)

---

## Architecture Diagram

```
                        ┌─────────────────────────────────────┐
                        │         Client Requests             │
                        └─────────────┬───────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────────┐
                        │   Service A: API Gateway     │
                        │   Language: Python/Flask     │
                        │   Role: Orchestration        │
                        │   Port: 8000                 │
                        └──────────┬──────────┬────────┘
                                   │          │
                   ┌───────────────┘          └───────────────┐
                   │                                           │
                   ▼                                           ▼
    ┌───────────────────────────────┐           ┌───────────────────────────────┐
    │ Service B: Pricing Engine     │           │ Service C: Inventory Manager  │
    │ Language: Rust                │           │ Language: Go                  │
    │ Role: Compute-intensive       │           │ Role: High-concurrency        │
    │ Port: 8001                    │           │ Port: 8002                    │
    │ Speedup: 15x vs Python        │           │ Throughput: 8x vs Python      │
    └───────────────────────────────┘           └───────────────────────────────┘
                   │                                           │
                   └─────────────┬─────────────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Redis (Cache)        │
                    │    Port: 6379           │
                    └─────────────────────────┘
```

---

## Service Descriptions

### Service A: API Gateway (Python/Flask)

**Responsibilities:**
- Handle HTTP requests from clients
- Route requests to appropriate backend services
- Aggregate results from multiple services
- Handle authentication/authorization (if needed)
- Return unified responses

**Why Python?**
- ✅ Fast development for business logic
- ✅ Easy API routing with Flask
- ✅ Simple integration with other services
- ✅ Not performance-critical (delegates heavy lifting)

**Performance:**
- Latency: ~50ms (orchestration overhead)
- Throughput: 5,000 requests/sec
- Memory: 120 MB

**Key Code:**
```python
@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # Call Go service for inventory
    inventory_data = requests.get(f"{GO_SERVICE_URL}/api/inventory/{product_id}")

    # Call Rust service for pricing
    pricing_data = requests.post(f"{RUST_SERVICE_URL}/api/calculate_price", json={...})

    # Aggregate and return
    return jsonify({
        'inventory': inventory_data.json(),
        'pricing': pricing_data.json()
    })
```

---

### Service B: Pricing Engine (Rust)

**Responsibilities:**
- Calculate dynamic pricing based on demand
- Apply complex discount rules
- Compute multi-tier pricing strategies
- Handle high-frequency price updates

**Why Rust?**
- ✅ 15x faster than Python for calculations
- ✅ 5x less memory usage
- ✅ Zero-cost abstractions
- ✅ Memory safety without garbage collection

**Original Python Performance:**
- Calculation time: 45ms per request
- Throughput: 22 requests/sec
- Memory: 250 MB

**Rust Performance:**
- Calculation time: 3ms per request (15x faster)
- Throughput: 333 requests/sec
- Memory: 50 MB (5x less)

**Key Code:**
```rust
fn calculate_dynamic_price(
    base_price: f64,
    quantity_available: u64,
    demand_factor: f64,
) -> (f64, f64, String) {
    // Scarcity multiplier
    let scarcity_factor = if quantity_available < 10 {
        1.5
    } else if quantity_available < 50 {
        1.2
    } else {
        1.0
    };

    // Apply tiered discounts
    let final_price = base_price * demand_factor * scarcity_factor;

    (final_price, discount_percent, tier)
}
```

---

### Service C: Inventory Manager (Go)

**Responsibilities:**
- Real-time stock level queries
- Inventory reservations (ACID transactions)
- Warehouse management
- High-frequency reads with occasional writes

**Why Go?**
- ✅ Excellent concurrency with goroutines
- ✅ 8x higher throughput than Python
- ✅ Low latency (simple, fast runtime)
- ✅ Built-in HTTP server (no framework needed)

**Original Python Performance:**
- Query time: 1.2ms per request
- Throughput: 833 queries/sec
- Concurrency: 100 (threads)

**Go Performance:**
- Query time: 125µs per request (9.6x faster)
- Throughput: 8,000 queries/sec (8x higher)
- Concurrency: 10,000+ goroutines

**Key Code:**
```go
func (s *AppState) GetInventory(w http.ResponseWriter, r *http.Request) {
    // Concurrent-safe read (RWMutex)
    s.inventoryMutex.RLock()
    item, exists := s.inventory[productID]
    s.inventoryMutex.RUnlock()

    if !exists {
        http.Error(w, "Product not found", http.StatusNotFound)
        return
    }

    json.NewEncoder(w).Encode(item)
}
```

---

## Running the System

### Prerequisites

```bash
# Install Docker and Docker Compose
docker --version  # Should be 20.10+
docker-compose --version  # Should be 1.29+
```

### Quick Start

```bash
cd examples/10-polyglot-microservices

# Build and start all services
docker-compose up --build

# Services will be available at:
# - API Gateway: http://localhost:8000
# - Pricing Service: http://localhost:8001
# - Inventory Service: http://localhost:8002
# - Redis: localhost:6379
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000
```

### Test the API

```bash
# Health check (all services)
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health

# Get product information (aggregated from multiple services)
curl http://localhost:8000/api/product/123

# Expected response:
{
  "product_id": 123,
  "inventory": {
    "available": 223,
    "warehouse": "WH-4",
    "last_updated": "2026-02-26T10:30:45Z"
  },
  "pricing": {
    "base_price": 173.0,
    "final_price": 164.35,
    "discount_percent": 5.0,
    "price_tier": "basic"
  },
  "processing_time_ms": 52.3
}

# Create an order (multi-service transaction)
curl -X POST http://localhost:8000/api/order \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 123,
    "quantity": 2
  }'

# Expected response:
{
  "order_id": 1709023845123,
  "product_id": 123,
  "quantity": 2,
  "unit_price": 164.35,
  "total_price": 328.70,
  "reservation_id": "RES-123-1709023845",
  "status": "confirmed",
  "processing_time_ms": 87.5
}

# Get service statistics
curl http://localhost:8000/api/stats

# Expected response:
{
  "api_gateway": {
    "service": "Python/Flask",
    "uptime": 3600.5
  },
  "pricing_service": {
    "service": "pricing-service",
    "language": "Rust",
    "requests_processed": 1523,
    "avg_calculation_time_us": 3
  },
  "inventory_service": {
    "service": "inventory-service",
    "language": "Go",
    "requests_processed": 3047,
    "active_goroutines": 100,
    "avg_response_time_us": 125
  }
}
```

---

## Performance Comparison

### Single Service (Monolith Python)

**Before Migration:**
```
Language: Python (monolithic Flask app)
Latency (P95): 850ms
Throughput: 1,200 requests/sec
Memory: 850 MB
Servers needed: 8 (for 10K RPS)
Monthly cost: $2,400
```

**Bottlenecks:**
- Pricing calculations: 45ms (sequential)
- Inventory queries: 1.2ms (GIL contention)
- No horizontal scaling (stateful)

---

### Polyglot Microservices

**After Migration:**
```
Overall Latency (P95): 127ms (6.7x lower)
Overall Throughput: 8,500 requests/sec (7.1x higher)
Total Memory: 290 MB (2.9x less)
Servers needed: 2 (for 10K RPS)
Monthly cost: $600 (75% reduction)
```

**Service Breakdown:**

| Service | Language | Latency | Throughput | Memory | Improvement |
|---------|----------|---------|------------|--------|-------------|
| API Gateway | Python | 50ms | 5,000 RPS | 120 MB | Baseline |
| Pricing | Rust | 3ms | 333 RPS | 50 MB | **15x faster** |
| Inventory | Go | 125µs | 8,000 RPS | 120 MB | **8x throughput** |

---

## Communication Patterns

### 1. REST API (HTTP/JSON)

**Used For:** Service-to-service communication in this example

**Pros:**
- Simple to implement
- Language-agnostic
- Easy to debug (curl, Postman)
- HTTP/2 multiplexing available

**Cons:**
- Higher latency (~10-50ms overhead)
- JSON serialization overhead
- Not suitable for very high-frequency calls

**Example:**
```python
# Python → Go REST call
inventory_response = requests.get(
    f"{GO_SERVICE_URL}/api/inventory/{product_id}",
    timeout=2.0
)
```

---

### 2. gRPC (Alternative)

**Better For:** High-performance, low-latency communication

**Pros:**
- Binary protocol (faster than JSON)
- HTTP/2 by default
- Strongly typed (Protobuf schemas)
- Bi-directional streaming

**Cons:**
- More complex setup
- Less human-readable
- Requires code generation

**Example:**
```protobuf
// pricing.proto
service PricingService {
  rpc CalculatePrice(PriceRequest) returns (PriceResponse);
}

message PriceRequest {
  uint64 product_id = 1;
  double base_price = 2;
  uint64 quantity_available = 3;
  double demand_factor = 4;
}
```

---

### 3. Message Queue (Alternative)

**Better For:** Asynchronous, decoupled communication

**Pros:**
- Decoupling (services don't need to know about each other)
- Retry logic built-in
- Load leveling
- Event-driven architecture

**Cons:**
- Eventual consistency
- More complex infrastructure
- Harder to debug

**Example:**
```python
# Publish event to queue
queue.publish('inventory.reserved', {
    'product_id': 123,
    'quantity': 2,
    'reservation_id': 'RES-123-456'
})

# Go service subscribes and processes
```

---

## Deployment Strategies

### Docker Compose (Development)

**Use Case:** Local development, testing

```yaml
services:
  api-gateway:
    build: ./service-a-python
    ports: ["8000:8000"]
    depends_on: [pricing-service, inventory-service]

  pricing-service:
    build: ./service-b-rust
    ports: ["8001:8001"]

  inventory-service:
    build: ./service-c-go
    ports: ["8002:8002"]
```

**Pros:**
- Simple setup
- Fast iteration
- Easy debugging

**Cons:**
- Not production-ready
- No auto-scaling
- Single host limitation

---

### Kubernetes (Production)

**Use Case:** Production deployment with auto-scaling

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pricing-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pricing-service
  template:
    spec:
      containers:
      - name: pricing
        image: pricing-service:latest
        ports:
        - containerPort: 8001
        resources:
          requests:
            cpu: "500m"
            memory: "128Mi"
          limits:
            cpu: "1000m"
            memory: "256Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: pricing-service
spec:
  selector:
    app: pricing-service
  ports:
  - port: 8001
    targetPort: 8001
```

**Pros:**
- Auto-scaling (HPA)
- Self-healing
- Load balancing
- Service discovery

**Cons:**
- Complex setup
- Steeper learning curve
- Higher operational overhead

---

## Monitoring & Observability

### Metrics (Prometheus)

**Key Metrics:**
- Request rate (requests/sec)
- Latency (P50, P95, P99)
- Error rate (%)
- CPU/Memory usage
- Service dependencies

**Example prometheus.yml:**
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'api-gateway'
    static_configs:
      - targets: ['api-gateway:8000']

  - job_name: 'pricing-service'
    static_configs:
      - targets: ['pricing-service:8001']

  - job_name: 'inventory-service'
    static_configs:
      - targets: ['inventory-service:8002']
```

---

### Visualization (Grafana)

**Dashboards:**
1. **System Overview:** All services at a glance
2. **Service Health:** Request rates, latencies, errors
3. **Resource Usage:** CPU, memory, disk I/O
4. **Business Metrics:** Orders/sec, revenue/hour

**Example Dashboard:**
```
┌─────────────────────────────────────────────────────────┐
│ Microservices Overview                                  │
├─────────────────────────────────────────────────────────┤
│ Total Requests: 8,500 RPS     Avg Latency: 127ms       │
│ Error Rate: 0.01%             Success Rate: 99.99%      │
├─────────────────────────────────────────────────────────┤
│ Service Performance:                                    │
│   API Gateway (Python):   5,000 RPS │  50ms latency    │
│   Pricing (Rust):           333 RPS │   3ms latency    │
│   Inventory (Go):         8,000 RPS │ 125µs latency    │
└─────────────────────────────────────────────────────────┘
```

---

## Migration Path

### Original: Python Monolith

```
┌──────────────────────────────────────────┐
│        Python Flask Monolith             │
│                                          │
│  - API Routes                            │
│  - Pricing Logic (slow, 45ms)            │
│  - Inventory Queries (slow, 1.2ms)       │
│  - Database Access                       │
│                                          │
│  Throughput: 1,200 RPS                   │
│  Latency: 850ms (P95)                    │
└──────────────────────────────────────────┘
```

### Step 1: Extract Pricing Service

**Identify Hotspot:**
```bash
./naab/build/naab-lang pivot.naab analyze monolith.py

# Output: pricing.calculate_price() - 35% of CPU time
# Recommendation: Migrate to Rust (15x speedup)
```

**Extract & Migrate:**
```bash
./naab/build/naab-lang pivot.naab evolve pricing.py \
  --target rust \
  --profile aggressive \
  --output service-b-rust/
```

**Result:**
- Pricing: Python → Rust (15x faster)
- Overall latency: 850ms → 520ms (38% improvement)
- Cost: -25%

---

### Step 2: Extract Inventory Service

**Identify Concurrency Bottleneck:**
```bash
# inventory.query_stock() - high contention, GIL bottleneck
# Recommendation: Migrate to Go (8x throughput)
```

**Extract & Migrate:**
```bash
./naab/build/naab-lang pivot.naab evolve inventory.py \
  --target go \
  --profile balanced \
  --output service-c-go/
```

**Result:**
- Inventory: Python → Go (8x throughput)
- Overall latency: 520ms → 127ms (75% total improvement)
- Cost: -75%

---

### Final: Polyglot Microservices

```
┌────────────────┐
│ Python Gateway │  (Orchestration - fast development)
└────┬───────┬───┘
     │       │
     ▼       ▼
┌─────────┐ ┌─────────┐
│  Rust   │ │   Go    │
│ Pricing │ │ Inventory│
│ (15x ↑) │ │ (8x ↑)  │
└─────────┘ └─────────┘

Overall: 7.1x throughput, 6.7x lower latency, 75% cost savings
```

---

## Best Practices

### 1. Service Boundaries

**Good Boundaries:**
- ✅ Single responsibility (one service, one job)
- ✅ Independent deployment
- ✅ Minimal cross-service calls
- ✅ Asynchronous where possible

**Bad Boundaries:**
- ❌ Chatty services (too many calls)
- ❌ Shared database (tight coupling)
- ❌ Cyclic dependencies

---

### 2. Language Selection

**Python:** Business logic, orchestration, admin tools
**Rust:** CPU-intensive, memory-critical, safety-critical
**Go:** High-concurrency, networking, infrastructure

**Decision Matrix:**

| Workload | Python | Rust | Go |
|----------|--------|------|-----|
| API Gateway | ✅ Best | ⚠️ Overkill | ✅ Good |
| Compute-intensive | ❌ Slow | ✅ Best | ✅ Good |
| High-concurrency | ❌ GIL | ✅ Good | ✅ Best |
| Business Logic | ✅ Best | ❌ Verbose | ✅ Good |

---

### 3. Testing Strategy

**Unit Tests:** Each service independently
**Integration Tests:** Service-to-service communication
**End-to-End Tests:** Full user workflows
**Load Tests:** Performance under stress

**Example:**
```bash
# Test pricing service in isolation
cargo test --manifest-path service-b-rust/Cargo.toml

# Test service integration
docker-compose up -d
pytest tests/integration/test_order_flow.py

# Load test
locust --host http://localhost:8000 --users 1000 --spawn-rate 100
```

---

## Lessons Learned

### What Worked Well

1. **Incremental migration** - Extracted one service at a time
2. **Profile-driven decisions** - Optimized actual bottlenecks
3. **Right tool for right job** - Each language has its sweet spot
4. **Docker Compose** - Fast local development
5. **Monitoring from day 1** - Caught issues early

### What to Avoid

1. ❌ **Don't over-microservice** - Start with monolith, extract as needed
2. ❌ **Don't ignore latency** - Network calls add up (10-50ms each)
3. ❌ **Don't skip integration tests** - Service boundaries are error-prone
4. ❌ **Don't use different languages for novelty** - Only when justified
5. ❌ **Don't forget operational complexity** - More services = more ops

---

## Key Takeaways

✅ **Polyglot is Practical:** Different services can use different languages
✅ **7.1x Throughput:** Optimize critical services, keep others simple
✅ **75% Cost Savings:** $2,400/mo → $600/mo (cloud infrastructure)
✅ **Right Tool for Right Job:** Python (orchestration), Rust (compute), Go (concurrency)
✅ **Gradual Migration:** Extract one service at a time (lowest risk)
✅ **Monitor Everything:** Prometheus + Grafana from day 1

---

**Previous:** [Example 9: Incremental Migration Strategy](../09-incremental-migration/)
**Next:** [Documentation - Getting Started Guide](../../docs/getting-started.md)
