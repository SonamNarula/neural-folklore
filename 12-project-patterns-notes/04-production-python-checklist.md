# Production Python Engineering & Quality Checklist

> The definitive software engineering checklist for bringing Python AI/ML/GenAI applications into production with enterprise-grade reliability, testing, linting, and containerization.

---

## 1. Code Quality & Static Analysis

### 1.1 Linting and Formatting (`ruff` and `black`)
Use **Ruff** (written in Rust), which executes 10x-50x faster than Flake8, Black, and isort combined.

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort (import sorting)
    "UP",  # pyupgrade (modern Python syntax)
    "B",   # flake8-bugbear (common bug patterns)
]
```

Run checks:
```bash
ruff check . --fix
ruff format .
```

### 1.2 Static Type Checking (`mypy`)
```bash
mypy src/ --strict --ignore-missing-imports
```

---

## 2. Automated Testing Suite (`pytest`)

### 2.1 Testing Rules
- Unit test all data preprocessing transformations.
- Mock external LLM API endpoints (`pytest-mock` or `respx`) to test without incurring API costs.
- Enforce minimum 80% test coverage in CI pipelines.

```python
# test_sample.py
import pytest

def test_token_chunker():
    from src.chunker import chunk_text
    chunks = chunk_text("one two three four", chunk_size=2)
    assert len(chunks) == 2
    assert chunks[0] == ["one", "two"]
```

Run test suite:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## 3. Observability, Logging, and Error Handling

### 3.1 Structured Logging (JSON)
Never use plain `print()` statements in production services. Use structured logging (`logging` with JSON formatter or `loguru`):

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno
        }
        return json.dumps(log_obj)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("production_app")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

---

## 4. Docker Containerization Best Practices

### Multi-Stage Dockerfile for Python AI Apps
```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final Minimal Runtime Image
FROM python:3.11-slim AS runner

WORKDIR /app
# Copy installed wheels from builder
COPY --from=builder /root/.local /root/.local
COPY src/ /app/src/

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 5. Master Production Readiness Checklist

| Category | Requirement | Verification Command / Metric |
| :--- | :--- | :--- |
| **Formatting** | Ruff / Black formatting enforced | `ruff format --check .` |
| **Linting** | Zero critical lint or bugbear errors | `ruff check .` |
| **Types** | Type annotations on all public functions | `mypy src/` |
| **Tests** | Unit tests passing with code coverage | `pytest --cov=src` |
| **Security** | No secrets or `.env` files in git | Check `.gitignore` |
| **Logging** | Structured JSON logs with trace IDs | Inspect log stream output |
| **Container** | Non-root container with multi-stage build | `docker build -t app .` |
