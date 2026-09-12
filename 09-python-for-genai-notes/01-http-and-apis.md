# HTTP and Web APIs in Generative AI

> HTTP is the stateless request-response application protocol that connects client applications to foundation model inference providers via RESTful endpoints.

---

## 1. Why This Matters

### Why This Concept Exists
State-of-the-art foundation models (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro) are massive multi-hundred-billion parameter clusters hosted remotely in cloud data centers. Accessing them requires communication over standard HTTP/REST protocols.

### Why Python Developers Need It
Understanding HTTP request structure, headers, authentication schemes, status codes, and rate limiting mechanics is required to build reliable LLM applications.

### Why It Matters Specifically in AI/ML/GenAI
- **Bearer Token Authorization**: Transmitting API keys securely via HTTP `Authorization: Bearer <API_KEY>` headers.
- **Handling HTTP Status Codes**: Distinguishing between client errors (400 Bad Request, 401 Unauthorized), rate limits (429 Too Many Requests), and provider outages (500/503 Service Unavailable).
- **Streaming Transfer (`text/event-stream`)**: Consuming token streams via Server-Sent Events (SSE).

### Where It Appears in Real Projects
- Direct HTTP requests to OpenAI, Anthropic, or Mistral endpoints.
- Building custom FastAPI proxy gateways and routing microservices.
- Vector database REST clients (Pinecone, Qdrant).

---

## 2. Core Concept

### 2.1 The HTTP Transaction Anatomy
An HTTP request consists of:
1. **Method**: `POST` (standard for inference generation), `GET` (retrieving model lists), `DELETE` (deleting fine-tunes).
2. **Endpoint URL**: e.g., `https://api.openai.com/v1/chat/completions`.
3. **Headers**: Key-value metadata (`Content-Type: application/json`, `Authorization: Bearer sk-...`).
4. **Body**: JSON payload specifying `model`, `messages`, `temperature`, etc.

### 2.2 Critical HTTP Status Codes in GenAI
| Code | Meaning | GenAI Engineering Handling Strategy |
| :--- | :--- | :--- |
| `200 OK` | Success | Parse JSON response body or stream chunks |
| `400 Bad Request` | Malformed Schema | Fix prompt payload schema, validate against JSON Schema |
| `401 Unauthorized`| Invalid API Key | Check `.env` secrets and credentials |
| `404 Not Found` | Unknown Model | Verify model string identifier (e.g. typos in model name) |
| `429 Too Many Req`| Rate Limit Exceeded | Exponential backoff retry with jitter; check TPM/RPM quota |
| `500 / 503` | Provider Outage | Fallback to secondary provider (e.g. OpenAI -> Anthropic) |

---

## 3. Mental Model

```text
HTTP Request / Response Lifecycle:
Client App (Python)                              LLM Provider (Cloud GPU Cluster)
       │                                                      │
       │─── POST /v1/chat/completions ───────────────────────►│
       │    Headers: Authorization: Bearer sk-..., JSON       │ (Token generation)
       │    Body: {"model": "gpt-4o", "messages": [...]}      │
       │                                                      │
       │◄── HTTP/1.1 200 OK ──────────────────────────────────│
       │    Body: {"choices": [{"message": {"content": ...}}]}│
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Raw Low-Level HTTP Request to LLM Endpoint (Without SDKs)
Executing an LLM completion using Python's standard library `urllib` to understand raw HTTP mechanics:

```python
import urllib.request
import json

def raw_http_chat_completion(prompt: str, api_key: str) -> dict:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.status
            body = response.read().decode("utf-8")
            return {"status": status, "data": json.loads(body)}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {"status": e.code, "error": error_body}

# (Run with valid key in production)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Hardcoding API Keys in Request Headers
Never hardcode raw API keys in source code files. Keys committed to GitHub repositories are scraped by automated bots within seconds! Always inject keys via environment variables.

### 2. Missing Network Timeouts
HTTP requests without timeouts will **hang indefinitely** if the network connection drops or the remote GPU cluster stalls, blocking worker threads. Always pass an explicit `timeout`.

---

## 6. Interview Questions & Coding Traps

### Q1: What is the difference between Tokens Per Minute (TPM) and Requests Per Minute (RPM) rate limits?
- **RPM (Requests Per Minute)**: Limits the raw count of HTTP connections established in a 60-second window.
- **TPM (Tokens Per Minute)**: Limits the total sum of prompt tokens + completion tokens consumed in a 60-second window. A single large request of 50,000 tokens can exhaust a TPM limit even when RPM is well below thresholds.

### Complexity Reference
| Component | Latency Impact |
| :--- | :--- |
| DNS Resolution & TCP Handshake | 20ms - 100ms |
| TLS Handshake (HTTPS) | 30ms - 150ms |
| Time to First Token (TTFT) | 200ms - 2000ms (dependent on model queue & prompt length) |
