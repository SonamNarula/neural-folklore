# Decorators in Python

> A decorator is a callable syntactic wrapper (`@wrapper`) that takes a function or class as an argument, extends or alters its runtime behavior, and returns a replacement callable.

---

## 1. Why This Matters

### Why This Concept Exists
Cross-cutting concerns (logging, authentication, caching, retry logic, profiling) clutter core business logic if embedded inline. Decorators adhere to the Single Responsibility Principle and Aspect-Oriented Programming (AOP).

### Why Python Developers Need It
Decorators are the standard Python mechanism for code instrumentation, API routing, and function modification without altering underlying source code.

### Why It Matters Specifically in AI/ML/GenAI
- **API Retry with Exponential Backoff**: When querying rate-limited LLM endpoints (OpenAI, Anthropic), decorators automatically catch 429 / 503 errors and retry with jittered delays.
- **Latency & GPU Timing**: Benchmarking inference latency of model components: `@measure_execution_time`.
- **Response Caching**: Caching expensive deterministic LLM queries or embeddings: `@functools.lru_cache`.

### Where It Appears in Real Projects
- FastAPI route decorators: `@app.get("/predict")`.
- Caching: `@functools.lru_cache(maxsize=128)`.
- Tenacity retry library: `@retry(stop=stop_after_attempt(3))`.

---

## 2. Core Concept

### 2.1 Basic Decorator Mechanics
`@decorator` syntax is exact syntactic sugar for: `func = decorator(func)`.

```python
from functools import wraps
import time

def timer(func):
    @wraps(func)  # Preserves func's docstring, name, and signature!
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[{func.__name__}] Execution took: {elapsed:.6f}s")
        return result
    return wrapper

@timer
def heavy_matrix_computation(n: int) -> float:
    """Computes sum of squares."""
    return sum(i**2 for i in range(n))

print(heavy_matrix_computation(100_000))
print("Function name preserved:", heavy_matrix_computation.__name__)  # 'heavy_matrix_computation'
```

### 2.2 Parameterized Decorators (Decorators Taking Arguments)
To pass arguments to a decorator, you add an outer factory layer:

```python
def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    print(f"Attempt {attempts} failed ({e}). Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator
```

---

## 3. Mental Model

```text
Decorator Execution Structure:
@retry(max_attempts=3)
def fetch_embedding(text): ...

Translates to:
fetch_embedding = retry(max_attempts=3)(fetch_embedding)

Execution Stack:
Caller ──► wrapper(*args, **kwargs) ──► Original Function ──► wrapper returns to Caller
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Production Resilient LLM API Caller with Exponential Backoff
A decorator that catches simulated network errors and retries with exponential backoff:

```python
import time
import random
from functools import wraps
from typing import Callable, Any

def retry_with_backoff(max_retries: int = 3, base_delay: float = 0.5):
    """Retries a flaky network or LLM API call with exponential backoff and jitter."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    retries += 1
                    if retries > max_retries:
                        print(f"Max retries ({max_retries}) exceeded for {func.__name__}")
                        raise exc

                    # Exponential backoff: base_delay * 2^(retries - 1) + jitter
                    sleep_time = (base_delay * (2 ** (retries - 1))) + random.uniform(0.01, 0.1)
                    print(f"Call failed: {exc}. Retrying attempt {retries}/{max_retries} in {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
        return wrapper
    return decorator

# Simulation of flaky API endpoint:
attempt_count = 0
@retry_with_backoff(max_retries=3, base_delay=0.2)
def call_flaky_llm_api(prompt: str) -> str:
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise ConnectionResetError("429 Too Many Requests (Rate limit hit)")
    return f"Response to: '{prompt}'"

print(call_flaky_llm_api("Explain attention mechanism"))
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Forgetting `@functools.wraps`
If you omit `@wraps(func)`, the decorated function loses its identity: its `__name__` becomes `'wrapper'`, its docstring is overwritten, and introspection tools (like Sphinx or FastAPI schema generators) break!

### 2. Decorator Order Execution
When multiple decorators are stacked:
```python
@decorator_a
@decorator_b
def func(): pass
```
They execute as: `decorator_a(decorator_b(func))`. `decorator_b` wraps `func` first, then `decorator_a` wraps `decorator_b`.

---

## 6. Interview Questions & Coding Traps

### Q1: Can a decorator be applied to a class?
**Answer:** Yes! Class decorators receive the class object, can modify its attributes or methods, and return the modified class or a wrapper class. `@dataclass` from the standard library is a premier example of a class decorator.

### Q2: What is the output of this code?
```python
def make_bold(fn):
    return lambda: "<b>" + fn() + "</b>"

def make_italic(fn):
    return lambda: "<i>" + fn() + "</i>"

@make_bold
@make_italic
def hello():
    return "hello"

print(hello())
```
**Output:** `<b><i>hello</i></b>`
**Explanation:** `make_italic` executes first, wrapping `"hello"` in `<i>...</i>`. `make_bold` wraps the result in `<b>...</b>`.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Decorator Application (at definition) | $O(1)$ one-time evaluation | $O(1)$ closure object |
| Decorated Function Invocation | $O(1)$ overhead + wrapped runtime | $O(1)$ additional stack frame |
