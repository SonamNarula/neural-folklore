# Environment Variables and Secrets Management

> Environment variables decouple sensitive runtime credentials and deployment configurations from static source code, adhering to 12-Factor Application principles.

---

## 1. Why This Matters

### Why This Concept Exists
Source code must remain identical across environments (local development, staging, production). Secrets (API keys, database passwords) and dynamic configurations belong in the execution environment, never in version control.

### Why Python Developers Need It
Accidental leakage of API keys via Git commits is one of the most common and costly security incidents in modern software engineering.

### Why It Matters Specifically in AI/ML/GenAI
- **LLM API Keys**: Securing credentials (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `HUGGINGFACE_HUB_TOKEN`).
- **Endpoint Routing**: Dynamically pointing to different vector databases or inference endpoints between local test containers and production VPCs.
- **Model Storage Paths**: Setting cache directories: `HF_HOME=/mnt/nvme/models`.

### Where It Appears in Real Projects
- `.env` files loaded with `python-dotenv`.
- Production Kubernetes secret injection.
- Pydantic `BaseSettings` configuration management.

---

## 2. Core Concept

### 2.1 Reading Environment Variables (`os.environ`)
`os.environ` is a dictionary-like mapping of process environment variables:

```python
import os

# 1. Access with KeyError if missing (Good for strictly mandatory secrets!)
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Mandatory OPENAI_API_KEY environment variable is not set!")

# 2. Access with default fallback
app_env = os.environ.get("APP_ENV", "development")
max_workers = int(os.environ.get("MAX_WORKERS", "4"))
```

### 2.2 Local Development with `python-dotenv`
Loads key-value pairs from a local `.env` file into `os.environ`:

```python
from dotenv import load_dotenv

# Loads .env from current directory if present
load_dotenv(override=False)  # override=False preserves existing shell env vars!
```

---

## 3. Mental Model

```text
12-Factor Configuration Hierarchy:
[ Shell Environment / Docker / K8s Secrets ]  (Highest Priority)
                     │
                     ▼
             [ .env Local File ]               (Development Fallback)
                     │
                     ▼
      [ Python os.environ / Pydantic ]         (Application Runtime)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Type-Safe Configuration Engine with Fallbacks and Secret Masking
A production configuration manager that validates required keys and masks sensitive tokens in logs:

```python
import os
from typing import Optional

class AppConfig:
    def __init__(self) -> None:
        self.openai_api_key: str = self._get_required("OPENAI_API_KEY")
        self.model_name: str = os.environ.get("MODEL_NAME", "gpt-4o")
        self.temperature: float = float(os.environ.get("TEMPERATURE", "0.2"))
        self.max_tokens: int = int(os.environ.get("MAX_TOKENS", "1024"))

    @staticmethod
    def _get_required(key: str) -> str:
        val = os.environ.get(key)
        if not val or not val.strip():
            # For demonstration, set dummy fallback if unset:
            return "sk-mock-1234567890abcdef"
        return val.strip()

    def get_masked_key(self) -> str:
        """Returns masked API key safe for logging (e.g. sk-mo...cdef)."""
        key = self.openai_api_key
        if len(key) <= 8:
            return "****"
        return f"{key[:5]}...{key[-4:]}"

config = AppConfig()
print(f"Loaded config for model: {config.model_name} | Key: {config.get_masked_key()}")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Committing `.env` to Git
Always include `.env` in your `.gitignore` immediately upon project initialization! Commit a sanitized `.env.example` file instead.

### 2. All Environment Variables are Strings!
`os.environ["DEBUG"] = "False"` evaluates to `bool(os.environ["DEBUG"]) == True`! Always parse explicitly:
```python
is_debug = os.environ.get("DEBUG", "false").lower() in ("true", "1")
```

---

## 6. Interview Questions & Coding Traps

### Q1: What is the difference between `os.environ['KEY']` and `os.getenv('KEY')`?
- `os.environ['KEY']` raises `KeyError` if `'KEY'` is not found.
- `os.getenv('KEY', default=None)` returns `None` (or a specified default) without raising an error.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| `os.environ.get()` | $O(1)$ dictionary lookup | $O(1)$ |
| `load_dotenv()` | $O(F)$ parsing lines in `.env` | $O(F)$ |
