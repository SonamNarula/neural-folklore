# Scope and Closures in Python

> Variable resolution adheres strictly to the LEGB rule; a closure is an inner function that retains access to its enclosing lexical scope even after that enclosing scope has returned.

---

## 1. Why This Matters

### Why This Concept Exists
Scopes prevent namespace pollution and isolate variable lifetimes across execution frames. Closures enable stateful functions without requiring full object-oriented class definitions.

### Why Python Developers Need It
Understanding scope rules prevents subtle variable shadowing bugs, while closures form the conceptual backbone of decorators and stateful factory functions.

### Why It Matters Specifically in AI/ML/GenAI
- **Stateful Decorators**: Rate limiters, latency profiling timers, and API retry mechanisms wrap functions and store invocation metrics in closure state.
- **Factory Functions**: Dynamically creating custom learning rate schedules: `lr_fn = make_cosine_annealing(initial_lr=1e-3, min_lr=1e-6)`.
- **Late-Binding Bug in Async/Parallel Tasks**: When firing async requests or training worker processes in a loop, variable references can bind to the final loop value instead of the iteration value.

### Where It Appears in Real Projects
- Decorator implementations throughout FastAPI, Flask, and PyTorch.
- Custom learning rate scheduler factories.
- Asynchronous task worker pools.

---

## 2. Core Concept

### 2.1 The LEGB Scope Resolution Rule
When a variable name is referenced, Python searches namespaces in this exact order:
1. **L**ocal: Inside the current function.
2. **E**nclosing: In any outer enclosing function scopes (from inner to outer).
3. **G**lobal: In the module-level namespace.
4. **B**uilt-in: In the Python `builtins` module (`len`, `range`, `ValueError`).

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print("Inner sees:", x)  # "local"
    inner()
    print("Outer sees:", x)      # "enclosing"

outer()
print("Module sees:", x)         # "global"
```

### 2.2 Closures & The `nonlocal` Keyword
A closure occurs when an inner function references variables in an enclosing scope. The enclosing scope's variables are preserved in the inner function's `__closure__` attribute.

```python
def make_exponential_decay(initial_lr: float, decay_rate: float):
    current_lr = initial_lr  # Enclosed variable

    def step() -> float:
        nonlocal current_lr  # Modifies variable in enclosing scope!
        current_lr *= decay_rate
        return current_lr

    return step

scheduler = make_exponential_decay(initial_lr=0.1, decay_rate=0.9)
print(scheduler())  # 0.09
print(scheduler())  # 0.081
print(scheduler())  # 0.0729
```

---

## 3. Mental Model

```text
LEGB Search Hierarchy:
[ Local Scope (Current Function) ]
        │ (not found)
        ▼
[ Enclosing Scope (Outer Function Closure) ]
        │ (not found)
        ▼
[ Global Scope (Module Level) ]
        │ (not found)
        ▼
[ Built-in Scope (Python Internals: len, int, etc.) ]
        │ (not found)
        ▼
[ Raise NameError! ]
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Token Rate-Limiting Guard via Closure
A stateful closure that regulates API requests per second to avoid HTTP 429 Rate Limit errors:

```python
import time
from typing import Callable

def create_rate_limiter(max_calls_per_second: float) -> Callable[[], None]:
    min_interval = 1.0 / max_calls_per_second
    last_called = 0.0

    def acquire() -> None:
        nonlocal last_called
        now = time.time()
        elapsed = now - last_called
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        last_called = time.time()

    return acquire

limiter = create_rate_limiter(max_calls_per_second=5.0)  # Max 5 calls/sec
for i in range(3):
    limiter.acquire()
    print(f"API Call {i} executed at timestamp: {time.time():.4f}")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Late-Binding in Closures (The Classic Loop Trap)
Python closures bind to variables **by reference, not by value**.

```python
# BUG: All lambdas reference the SAME variable 'i'
multipliers = [lambda x: x * i for i in range(3)]
print([m(10) for m in multipliers])  # [20, 20, 20]!

# FIX: Force early binding using default argument trick
multipliers_fixed = [lambda x, i=i: x * i for i in range(3)]
print([m(10) for m in multipliers_fixed])  # [0, 10, 20]!
```

### 2. UnboundLocalError
Referencing a variable before assignment when a local write exists in that frame:

```python
count = 0
def increment():
    # count += 1  -> UnboundLocalError: local variable 'count' referenced before assignment
    # Python sees assignment 'count = ...' and treats count as local, shadowing global!
    global count
    count += 1
```

---

## 6. Interview Questions & Coding Traps

### Q1: What is stored in a function's `__closure__` attribute?
When a function is a closure, `__closure__` is a tuple of `cell` objects. Each cell contains a `cell_contents` attribute pointing to the captured variable from the enclosing scope.

### Q2: What is the difference between `global` and `nonlocal`?
- `global` tells Python to bind the variable to the outermost module-level namespace.
- `nonlocal` tells Python to bind the variable to the nearest enclosing function scope (excluding the global namespace).

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Local Variable Access | $O(1)$ fast array lookup | $O(1)$ |
| Enclosing / Closure Lookup | $O(1)$ cell pointer dereference | $O(1)$ |
| Global Variable Access | $O(1)$ hash table lookup | $O(1)$ |
