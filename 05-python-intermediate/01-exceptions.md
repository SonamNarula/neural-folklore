# Exceptions and Error Handling in Python

> Exceptions are anomalous runtime events that interrupt standard execution flow, unwinding the call stack until intercepted by a matching handler.

---

## 1. Why This Matters

### Why This Concept Exists
Uncontrolled failures crash production systems. Structured exception handling allows systems to degrade gracefully, retry transient network faults, and emit structured diagnostic logs.

### Why Python Developers Need It
Python follows the EAFP philosophy: **"Easier to Ask for Forgiveness than Permission"** (preferring `try/except` over dozens of defensive `if/else` checks).

### Why It Matters Specifically in AI/ML/GenAI
- **API Failure Handling**: Transient network blips, HTTP 429 Rate Limits, and HTTP 503 Overloaded errors when querying LLM endpoints must be caught and retried.
- **Malformed Dataset Rows**: Corrupt images or malformed JSON records in billion-token training pipelines must be logged and discarded without crashing the entire multi-day training job.
- **CUDA Out-of-Memory Recovery**: Catching `torch.cuda.OutOfMemoryError` to dynamically reduce batch sizes.

### Where It Appears in Real Projects
- LLM API gateway retry loops.
- Dataset loading pipelines in PyTorch DataLoader workers.
- Pydantic validation error handling in FastAPI endpoints.

---

## 2. Core Concept

### 2.1 The Complete `try / except / else / finally` Flow
- `try`: Code that might raise an exception.
- `except`: Code executed if a matching exception occurs.
- `else`: Executed **only if no exception was raised** in the `try` block.
- `finally`: Guaranteed execution regardless of whether an exception occurred or was handled (resource cleanup).

```python
def safe_divide_and_log(a: float, b: float) -> float | None:
    result = None
    try:
        result = a / b
    except ZeroDivisionError as e:
        print(f"Handled error: Division by zero ({e})")
    else:
        print(f"Computation succeeded: {result}")
    finally:
        print("Cleanup: Operation cycle finalized.")
    return result

safe_divide_and_log(10, 2)
safe_divide_and_log(10, 0)
```

### 2.2 Exception Hierarchy & Custom Domain Exceptions
Always inherit custom exceptions from `Exception` (never `BaseException`, which catches `KeyboardInterrupt` and `SystemExit`).

```python
class ModelInferenceError(Exception):
    """Base domain exception for inference failures."""
    pass

class RateLimitExceeded(ModelInferenceError):
    def __init__(self, retry_after: int):
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds.")
        self.retry_after = retry_after
```

### 2.3 Exception Chaining (`raise ... from e`)
Preserves root cause tracebacks when wrapping low-level errors into domain exceptions.

```python
import json

def parse_model_response(raw_str: str) -> dict:
    try:
        return json.loads(raw_str)
    except json.JSONDecodeError as err:
        # Chain original err to preserve root cause
        raise ModelInferenceError("LLM failed to output valid JSON schema") from err
```

---

## 3. Mental Model

```text
EAFP Flow Architecture:
[ Try Block ] ─── Exception raised?
      │
      ├─── YES ──► [ Match Except Block? ]
      │                    │
      │                    ├── YES ──► Execute Except Handler
      │                    └── NO  ──► Bubble up call stack
      │
      └─── NO  ──► [ Execute Else Block ]
                        │
                        ▼
            [ Execute Finally Block ] (Guaranteed)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Resilient Batch Dataset Loader with Fault Tolerance
A production pipeline loader that catches corrupted samples without terminating training:

```python
import logging
from typing import List, Dict, Any

class CorruptSampleError(Exception):
    pass

def parse_sample(raw_record: Dict[str, Any]) -> Dict[str, Any]:
    if "input_ids" not in raw_record:
        raise CorruptSampleError("Missing 'input_ids' field")
    if not isinstance(raw_record["input_ids"], list):
        raise CorruptSampleError("'input_ids' must be a list")
    return raw_record

def safe_batch_loader(raw_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    valid_batch = []
    skipped_count = 0

    for idx, record in enumerate(raw_records):
        try:
            valid_sample = parse_sample(record)
            valid_batch.append(valid_sample)
        except CorruptSampleError as e:
            skipped_count += 1
            logging.warning(f"Skipping record {idx}: {e}")
        except Exception as e:
            # Unexpected critical failure
            logging.error(f"Critical error on record {idx}: {e}")
            raise e

    print(f"Batch processed: {len(valid_batch)} valid samples, {skipped_count} skipped.")
    return valid_batch

records = [
    {"input_ids": [101, 205, 102]},
    {"corrupt_key": "junk"},
    {"input_ids": "not_a_list"}
]
safe_batch_loader(records)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Bare `except:` Catches System Exits!
Catching bare `except:` intercepts `KeyboardInterrupt` (Ctrl+C) and `SystemExit`, preventing scripts from terminating cleanly! Always catch specific exceptions or at least `except Exception:`.

### 2. Swallowing Exceptions Silently
```python
# ANTI-PATTERN:
try:
    load_weights()
except Exception:
    pass  # Model silently uses random weights! Catastrophic bug!
```

---

## 6. Interview Questions & Coding Traps

### Q1: What is the exact difference between EAFP and LBYL?
- **EAFP** (*Easier to Ask for Forgiveness than Permission*): Attempt the operation directly inside a `try/except` block. Pythonic and avoids race conditions (e.g., file deleted between existence check and file open).
- **LBYL** (*Look Before You Leap*): Check prerequisites with defensive `if` conditions before executing. Can lead to race conditions (Time-of-Check to Time-of-Use - TOCTOU).

### Q2: What happens if both `try` and `finally` have `return` statements?
The `return` statement in the `finally` block **overrides** the `return` statement in the `try` block!
```python
def test():
    try: return 1
    finally: return 2
print(test())  # 2
```

### Complexity Reference
| Mechanism | Overhead |
| :--- | :--- |
| Entering `try` block (No exception raised) | Nearly zero overhead in Python 3.11+ ("zero-cost" exception tables) |
| Exception Raised & Caught | High cost (Stack unwinding, traceback assembly) |
