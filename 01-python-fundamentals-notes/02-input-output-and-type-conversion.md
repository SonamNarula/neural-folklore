# Input/Output and Type Conversion in Python

> I/O bridges external data streams to in-memory objects; type conversion explicitly bridges data representations between raw serialization formats and structured types.

---

## 1. Why This Matters

### Why This Concept Exists
External data (CLI flags, files, REST API payloads, Kafka streams) always enters Python as unparsed strings or raw byte buffers. Programs require explicit mechanisms to parse, validate, and convert these inputs into structured primitives.

### Why Python Developers Need It
Without robust I/O handling and type conversion, applications fail upon malformed user input, corrupt database insertions, or crash during type mismatches.

### Why It Matters Specifically in AI/ML/GenAI
- **CLI Model Training Scripts**: CLI arguments (hyperparameters like `--lr 1e-4`, `--batch-size 64`) parsed via `sys.argv` or `argparse` enter as strings and must be cast cleanly.
- **LLM Prompt Interpolation**: F-strings are the primary mechanism for dynamic prompt assembly. Formatting specifiers control floating-point rounding for token cost minimization.
- **Streaming Token Output**: Real-time GenAI output requires non-buffered `sys.stdout.write()` with `flush=True` to simulate typewriter token streaming.

### Where It Appears in Real Projects
- Command-line interfaces for training (`argparse`, `click`).
- Prompt engineering templates for Claude/OpenAI API requests.
- Serializing embeddings and dataset metadata to disk.

---

## 2. Core Concept

### 2.1 String Interpolation (F-Strings)
Introduced in Python 3.6, formatted string literals (f-strings) are evaluated at runtime with C-level speed.

```python
model_name = "llama-3-70b"
temperature = 0.7000
tokens = 1420
cost_per_1k = 0.002

# Advanced format specifiers: .2f (precision), >15 (alignment), , (separator)
summary = f"Model: {model_name:<15} | Temp: {temperature:.2f} | Cost: ${tokens * cost_per_1k / 1000:.6f}"
print(summary)
```

### 2.2 Type Conversion (Type Casting)
Python provides explicit conversion constructors: `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()`, `bytes()`.

```python
# String to numeric with base parsing
raw_hex = "0xff"
print(int(raw_hex, 16))  # 255

# String to float with scientific notation
lr_str = "1e-4"
lr_float = float(lr_str)
print(lr_float)  # 0.0001
```

### 2.3 Truthiness & Boolean Conversion
`bool(x)` evaluates to `False` for **falsy** objects:
- `None`, `False`
- Numeric zeros: `0`, `0.0`, `0j`
- Empty sequences: `""`, `()`, `[]`, `{}`, `set()`, `range(0)`
All other objects evaluate to `True`.

---

## 3. Mental Model

```text
External World (Raw Text / Bytes)
         │
         ▼  sys.stdin / input() / requests.get()
   "1e-4" (str: sequence of ASCII chars '1', 'e', '-', '4')
         │
         ▼  float("1e-4")
   0.0001 (float: 64-bit IEEE 754 binary floating point)
         │
         ▼  f"{0.0001:.2e}"
   "1.00e-04" (str: formatted for logging or LLM prompt)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Streaming LLM Token Printer to Terminal
Simulating real-time LLM token generation without buffering delays:

```python
import sys
import time
from typing import Iterator

def mock_llm_stream() -> Iterator[str]:
    response = "The attention mechanism computes a weighted sum of values based on query-key dot products."
    for token in response.split(" "):
        yield token + " "
        time.sleep(0.05)

def stream_to_cli() -> None:
    sys.stdout.write("AI: ")
    for chunk in mock_llm_stream():
        # flush=True forces immediate terminal rendering bypassing stdio buffer
        sys.stdout.write(chunk)
        sys.stdout.flush()
    sys.stdout.write("
")

if __name__ == "__main__":
    stream_to_cli()
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. `bool("False")` Evaluates to `True`
Non-empty strings are always truthy, regardless of contents.

```python
flag = "False"
print(bool(flag))  # True! This causes silent misconfiguration in CLI flags!

# Production Safe Pattern:
is_enabled = flag.strip().lower() in ("true", "1", "yes")
print(is_enabled)  # False
```

### 2. Truncation vs Rounding
`int(3.99)` truncates towards zero; it does **not** round.

```python
print(int(3.99))   # 3
print(int(-3.99))  # -3
print(round(3.99)) # 4
```

---

## 6. Interview Questions & Coding Traps

### Q1: How does Python's `round()` handle tie-breaking (`round(2.5)` vs `round(3.5)`)?
Python uses **banker's rounding** (round half to even) to eliminate statistical bias:
- `round(2.5) == 2`
- `round(3.5) == 4`
- `round(4.5) == 4`

### Q2: What is the output of `print(str([1, 2, 3]))` vs `repr([1, 2, 3])`?
Both print `'[1, 2, 3]'`. `str()` produces a human-readable representation, while `repr()` produces an unambiguous representation that can ideally be passed to `eval()` to recreate the object.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| `int(str_num)` | $O(N)$ where $N$ is digit count | $O(1)$ |
| `float(str_num)` | $O(N)$ | $O(1)$ |
| F-string interpolation | $O(N + M)$ string buffer concatenation | $O(N + M)$ |
