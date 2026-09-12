# API Response Handling and Streaming in GenAI

> Handling LLM API responses requires parsing structured JSON payloads, intercepting granular error schemas, and consuming real-time Server-Sent Events (SSE) token streams.

---

## 1. Why This Matters

### Why This Concept Exists
LLM generation is computationally intensive and takes seconds to complete. Rather than waiting for full generation, modern user experiences stream tokens incrementally as they are sampled from the transformer.

### Why Python Developers Need It
Mastering chunked streaming, HTTP Server-Sent Events (SSE), and schema validation ensures responsive, resilient GenAI applications.

### Why It Matters Specifically in AI/ML/GenAI
- **Server-Sent Events (SSE)**: Consuming `data: {"choices": [{"delta": {"content": "..."}}]}` chunks from the OpenAI/Anthropic stream protocols.
- **Time to First Token (TTFT)**: Streaming provides immediate visual feedback to users within ~200ms rather than a 10-second blank loading spinner.
- **Handling Incomplete Generations**: Detecting when generation was halted by token limit (`finish_reason="length"`) vs natural termination (`finish_reason="stop"`).

### Where It Appears in Real Projects
- Real-time chatbot UI backends.
- Streaming proxy gateways in FastAPI.
- Real-time evaluation monitors.

---

## 2. Core Concept

### 2.1 The OpenAI ChatCompletion Response Structure
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1726000000,
  "model": "gpt-4o",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "Hello! How can I assist you today?"},
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 9,
    "total_tokens": 21
  }
}
```

### 2.2 Server-Sent Events (SSE) Protocol
In streaming mode (`stream=True`), the HTTP response body contains chunks formatted as:
```text
data: {"choices":[{"delta":{"content":"Attention"}}]}

data: {"choices":[{"delta":{"content":" is"}}]}

data: [DONE]
```

---

## 3. Mental Model

```text
Buffered vs Streaming Generation:
Buffered Mode:
[ Request Sent ] ────── 8 Seconds Silence ──────► [ All 200 Tokens Delivered at Once ]

Streaming Mode (SSE):
[ Request Sent ] ──► tok1 ──► tok2 ──► tok3 ──► tok4 ... ──► [DONE]
                     (User reads immediately!)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: SSE Chunk Parser for LLM Streaming
Parsing simulated raw Server-Sent Events line chunks into yieldable string tokens:

```python
import json
from typing import Generator, List

def mock_sse_raw_stream() -> List[str]:
    return [
        'data: {"choices": [{"delta": {"content": "Machine"}}]}',
        'data: {"choices": [{"delta": {"content": " learning"}}]}',
        'data: {"choices": [{"delta": {"content": " models"}}]}',
        'data: {"choices": [{"delta": {"content": " generalize."}}]}',
        'data: [DONE]'
    ]

def parse_sse_token_stream(raw_lines: List[str]) -> Generator[str, None, None]:
    """
    Parses raw SSE lines formatted according to OpenAI streaming protocol.
    Yields individual string tokens.
    """
    for line in raw_lines:
        line = line.strip()
        if not line or not line.startswith("data: "):
            continue

        payload_str = line[len("data: "):]
        if payload_str == "[DONE]":
            break

        try:
            chunk = json.loads(payload_str)
            choices = chunk.get("choices", [])
            if choices:
                delta = choices[0].get("delta", {})
                content = delta.get("content")
                if content:
                    yield content
        except json.JSONDecodeError:
            continue

# Testing token stream consumer:
print("Streaming tokens in real time: ", end="")
for token in parse_sse_token_stream(mock_sse_raw_stream()):
    print(token, end="", flush=True)
print()
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. `finish_reason == "length"` Truncation
If `finish_reason` is `"length"`, the LLM ran out of max token budget mid-sentence or mid-JSON generation, producing invalid JSON or cut-off answers! Always inspect `finish_reason`.

---

## 6. Interview Questions & Coding Traps

### Q1: What is the difference between WebSockets and Server-Sent Events (SSE)?
- **WebSockets**: Bi-directional, full-duplex communication over a single TCP connection. Both client and server can send messages anytime.
- **Server-Sent Events (SSE)**: Mono-directional (server to client) streaming over standard HTTP. Ideal for LLMs where the client sends a single prompt and the server streams tokens back. SSE works natively with HTTP/2 and standard proxies.

### Complexity Reference
| Mode | Memory Consumption | Latency to First Visual Output |
| :--- | :--- | :--- |
| Buffered Full Response | $O(	ext{total tokens})$ buffer in RAM | High (Full generation time) |
| Streaming Response (SSE) | $O(	ext{chunk size})$ transient buffer | Low (~TTFT: 200ms) |
