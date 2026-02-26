# CI/CD Integration Guide

**Integrating NAAb Pivot into Continuous Integration/Deployment Pipelines**

---

## GitHub Actions

### Basic Workflow

**File:** `.github/workflows/optimize.yml`

```yaml
name: Code Optimization

on: [push, pull_request]

jobs:
  optimize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive

      - name: Setup NAAb Pivot
        uses: b-macker/naab-pivot@v1

      - name: Evolve Code
        run: |
          naab-lang pivot.naab evolve src/critical_path.py \
            --profile balanced \
            --format json > evolution-report.json

      - name: Upload Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: vessels
          path: vessels/
```

### Performance Regression Detection

```yaml
- name: Benchmark
  run: |
    naab-lang benchmark.naab vessels/ \
      --baseline baseline.json \
      --regression-threshold 5 \
      --format sarif > benchmark.sarif

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: benchmark.sarif
```

---

## GitLab CI

**File:** `.gitlab-ci.yml`

```yaml
stages:
  - optimize
  - test

optimize:
  stage: optimize
  image: bmacker/naab-pivot:latest
  script:
    - naab-lang pivot.naab evolve src/slow_code.py
  artifacts:
    paths:
      - vessels/
    expire_in: 1 week

test_performance:
  stage: test
  script:
    - naab-lang benchmark.naab vessels/ --baseline baseline.json
```

---

## Jenkins

**File:** `Jenkinsfile`

```groovy
pipeline {
    agent any

    stages {
        stage('Optimize') {
            steps {
                sh 'docker run --rm -v $PWD:/workspace bmacker/naab-pivot naab-lang pivot.naab evolve slow_code.py'
            }
        }

        stage('Validate') {
            steps {
                sh 'naab-lang pivot.naab validate slow_code.py vessels/vessel'
            }
        }

        stage('Benchmark') {
            steps {
                sh 'naab-lang benchmark.naab vessels/'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'vessels/**', fingerprint: true
            publishHTML([
                reportDir: 'vessels',
                reportFiles: 'benchmark-report.html',
                reportName: 'Benchmark Report'
            ])
        }
    }
}
```

---

## CircleCI

**File:** `.circleci/config.yml`

```yaml
version: 2.1

jobs:
  optimize:
    docker:
      - image: bmacker/naab-pivot:latest
    steps:
      - checkout
      - run:
          name: Evolve Code
          command: naab-lang pivot.naab evolve src/slow_code.py
      - store_artifacts:
          path: vessels/

workflows:
  version: 2
  optimize-workflow:
    jobs:
      - optimize
```

---

## Travis CI

**File:** `.travis.yml`

```yaml
language: minimal

services:
  - docker

script:
  - docker run --rm -v $PWD:/workspace bmacker/naab-pivot naab-lang pivot.naab evolve slow_code.py
  - docker run --rm -v $PWD:/workspace bmacker/naab-pivot naab-lang benchmark.naab vessels/
```

---

## Docker Compose

**File:** `docker-compose.ci.yml`

```yaml
version: '3.8'

services:
  naab-pivot:
    image: bmacker/naab-pivot:latest
    volumes:
      - ./workspace:/workspace
    command: naab-lang pivot.naab evolve /workspace/slow_code.py
```

**Run:**

```bash
docker-compose -f docker-compose.ci.yml up
```

---

## Best Practices

### 1. Cache Build Artifacts

```yaml
# GitHub Actions
- uses: actions/cache@v3
  with:
    path: |
      vessels/
      .cache/
    key: ${{ runner.os }}-vessels-${{ hashFiles('**/*.py') }}
```

### 2. Parallel Optimization

```yaml
jobs:
  optimize-module-a:
    runs-on: ubuntu-latest
    steps:
      - run: naab-lang pivot.naab evolve src/module_a.py

  optimize-module-b:
    runs-on: ubuntu-latest
    steps:
      - run: naab-lang pivot.naab evolve src/module_b.py
```

### 3. Conditional Execution

```yaml
# Only run on main branch
on:
  push:
    branches: [main]
```

### 4. Fail on Regression

```yaml
- name: Check Performance
  run: |
    naab-lang benchmark.naab vessels/ \
      --baseline baseline.json \
      --regression-threshold 5 \
      || exit 1
```

---

**Next:** [Docker Guide](docker.md) | [Performance Tuning](performance-tuning.md)
