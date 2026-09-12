# The `requests` Library and Resilient HTTP

> `requests` provides high-level HTTP client abstractions; `requests.Session` enables TCP connection pooling and persistent header management for high-throughput API communication.

---

## 1. Why This Matters

### Why This Concept Exists
Python's standard library `urllib` is verbose and does not implement connection pooling by default. The `requests` library abstracts lower-level socket handling into clean, readable code.

### Why Python Developers Need It
Every synchronous API integration, scraper, and web connector in Python relies on `requests`.

### Why It Matters Specifically in AI/ML/GenAI
- **TCP Connection Pooling (`requests.Session`)**: Establishing new TLS/TCP connections for every single LLM call adds 50-200ms of latency per call. A persistent `Session` reuses existing sockets across thousands of sequential queries.
- **Automated HTTP Adapters & Retries**: Configuring automatic retries for transient HTTP errors (500, 502, 503, 504) via `urllib3.util.Retry`.
- **Streaming Large Embeddings**: Streaming responses line-by-line without buffering large JSON payloads into RAM.

### Where It Appears in Real Projects
- Custom API wrappers for self-hosted vLLM / Ollama servers.
- Document downloading in web-scraping RAG loaders.
- Internal microservice HTTP calls.

---

## 2. Core Concept

### 2.1 Basic Requests vs Session Pooling
```python
import requests

# INNEFFICIENT: Creates a brand new TCP + TLS connection each call!
# resp1 = requests.post("https://api.openai.com/...", headers=...)
# resp2 = requests.post("https://api.openai.com/...", headers=...)

# PRODUCTION PATTERN: Reuses underlying connection pool
session = requests.Session()
session.headers.update({"Authorization": "Bearer sk-mock", "Content-Type": "application/json"})
# Fast subsequent requests over existing keep-alive socket:
# resp1 = session.post("https://api.openai.com/...", json=payload)
```

### 2.2 Built-in Retry Adapters (`HTTPAdapter`)
Configuring automatic socket-level retry logic:

```python
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

retries = Retry(
    total=3,
    backoff_factor=0.5,  # Delays: 0.5s, 1s, 2s...
    status_forcelist=[500, 502, 503, 504],
    raise_on_status=False
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
```

---

## 3. Mental Model

```text
Without Session (Connection Thrashing):
Request 1: [ TCP SYN ] ──► [ TLS Handshake ] ──► Send Data ──► Close Socket
Request 2: [ TCP SYN ] ──► [ TLS Handshake ] ──► Send Data ──► Close Socket

With Session Connection Pool:
Request 1: [ TCP SYN ] ──► [ TLS Handshake ] ──► Send Data ──► Keep Alive
Request 2: ────────────────────────────────────► Send Data ──► Keep Alive (Zero Handshake Overhead!)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Resilient Production LLM Client with Session Pooling & Backoff
A production-grade synchronous HTTP client for querying self-hosted vLLM or cloud API endpoints:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from typing import Dict, Any

class ResilientLLMClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "GenAI-Pipeline/1.0"
        })

        # Configure automatic retries for transient infrastructure errors
        retry_strategy = Retry(
            total=3,
            backoff_factor=1.0,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST", "GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=20)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def generate(self, model: str, prompt: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/completions"
        payload = {"model": model, "prompt": prompt, **kwargs}

        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()  # Raises HTTPError if status is 4xx or 5xx
            return response.json()
        except requests.exceptions.Timeout:
            raise TimeoutError(f"LLM request timed out after {self.timeout}s")
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HTTP error occurred: {response.status_code} - {response.text}") from e

client = ResilientLLMClient("https://api.openai.com", "sk-mock-key")
print("Initialized resilient HTTP client with connection pooling.")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. `response.json()` vs `response.text`
Calling `response.json()` on an error response that returned an HTML error page (e.g. Cloudflare 502 page) raises `json.JSONDecodeError` instead of showing the actual error message. Always inspect `response.status_code` first!

### 2. Timeouts Must Cover Both Connect and Read
Passing a single float `timeout=5.0` applies to both connect and read. Passing a tuple `timeout=(3.0, 30.0)` sets 3 seconds to connect and 30 seconds to read the token stream.

---

## 6. Interview Questions & Coding Traps

### Q1: What is the benefit of `pool_connections` and `pool_maxsize` in `HTTPAdapter`?
- `pool_connections`: The number of distinct hostnames to cache connection pools for.
- `pool_maxsize`: The maximum number of concurrent persistent TCP connections kept open in the pool for each host. Crucial for multithreaded scrapers to prevent connection exhaustion.

### Complexity Reference
| Strategy | Latency Savings |
| :--- | :--- |
| Reusing TCP/TLS Connection via `Session` | Saves 50ms - 200ms per request |
| Socket Retry Adapter | Eliminates manual retry boilerplate |
