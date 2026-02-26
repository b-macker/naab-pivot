# Docker Usage Guide

**Running NAAb Pivot in Containers**

---

## Quick Start

### Pull Image

```bash
docker pull bmacker/naab-pivot:latest
```

### Run Analysis

```bash
docker run --rm \
  -v $(pwd):/workspace \
  bmacker/naab-pivot:latest \
  naab-lang /opt/naab-pivot/pivot.naab analyze /workspace/slow.py
```

### Full Evolution

```bash
docker run --rm \
  -v $(pwd):/workspace \
  bmacker/naab-pivot:latest \
  naab-lang /opt/naab-pivot/pivot.naab evolve /workspace/slow.py
```

---

## Docker Compose

### Basic Setup

**File:** `docker-compose.yml`

```yaml
version: '3.8'

services:
  naab-pivot:
    image: bmacker/naab-pivot:latest
    volumes:
      - ./workspace:/workspace
      - ./vessels:/opt/naab-pivot/vessels
    environment:
      - PIVOT_PROFILE=balanced
      - PIVOT_OUTPUT=/workspace/vessels
```

**Run:**

```bash
docker-compose run naab-pivot naab-lang /opt/naab-pivot/pivot.naab evolve /workspace/slow.py
```

### With Dashboard

```yaml
services:
  naab-pivot:
    image: bmacker/naab-pivot:latest
    volumes:
      - ./workspace:/workspace

  dashboard:
    image: bmacker/naab-pivot:latest
    command: naab-lang /opt/naab-pivot/dashboard/serve.naab
    ports:
      - "8080:8080"
    volumes:
      - ./workspace:/workspace
    depends_on:
      - naab-pivot
```

---

## Building Custom Image

### Dockerfile

```dockerfile
FROM bmacker/naab-pivot:latest

# Add custom templates
COPY templates/my-template.naab /opt/naab-pivot/templates/

# Add custom plugins
COPY plugins/ /opt/naab-pivot/plugins/

# Add custom profiles
COPY profiles/my-profile.json /opt/naab-pivot/profiles/

WORKDIR /workspace
```

**Build:**

```bash
docker build -t my-naab-pivot .
```

---

## Volume Mounts

### Mount Workspace

```bash
docker run --rm \
  -v /path/to/project:/workspace \
  bmacker/naab-pivot:latest \
  naab-lang /opt/naab-pivot/pivot.naab evolve /workspace/slow.py
```

### Mount Vessels Output

```bash
docker run --rm \
  -v $(pwd):/workspace \
  -v $(pwd)/vessels:/opt/naab-pivot/vessels \
  bmacker/naab-pivot:latest \
  naab-lang /opt/naab-pivot/pivot.naab evolve /workspace/slow.py
```

---

## Environment Variables

```bash
docker run --rm \
  -e PIVOT_PROFILE=aggressive \
  -e PIVOT_OUTPUT=/workspace/vessels \
  -e PIVOT_TOLERANCE=0.01 \
  -v $(pwd):/workspace \
  bmacker/naab-pivot:latest \
  naab-lang /opt/naab-pivot/pivot.naab evolve /workspace/slow.py
```

---

## Multi-Stage Builds

### Optimize Then Deploy

**File:** `Dockerfile.multi-stage`

```dockerfile
# Stage 1: Optimize code
FROM bmacker/naab-pivot:latest AS optimizer

COPY src/ /workspace/src/
RUN naab-lang /opt/naab-pivot/pivot.naab evolve /workspace/src/slow.py

# Stage 2: Final image
FROM alpine:latest

COPY --from=optimizer /opt/naab-pivot/vessels/vessel /app/vessel

ENTRYPOINT ["/app/vessel"]
```

---

## Docker in CI/CD

### GitHub Actions

```yaml
- name: Build and Run
  run: |
    docker run --rm \
      -v ${{ github.workspace }}:/workspace \
      bmacker/naab-pivot:latest \
      naab-lang /opt/naab-pivot/pivot.naab evolve /workspace/slow.py
```

---

**Next:** [Migration Guide](migration-guide.md) | [Security](security.md)
