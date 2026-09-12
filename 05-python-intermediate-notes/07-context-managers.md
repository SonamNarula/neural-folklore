# Context Managers in Python

> Context managers govern resource lifecycles by guaranteeing deterministic setup and teardown actions around code blocks via the `__enter__` and `__exit__` protocol.

---

## 1. Why This Matters

### Why This Concept Exists
System resources (file descriptors, database connections, thread locks, GPU VRAM tensors) must be released reliably. Relying on manual cleanup or garbage collection causes resource exhaustion bugs.

### Why Python Developers Need It
The `with` statement encapsulates `try...finally` resource management into reusable, elegant abstractions.

### Why It Matters Specifically in AI/ML/GenAI
- **Disabling PyTorch Autograd**: `torch.no_grad()` is a context manager that disables autograd calculation, slashing VRAM consumption during model evaluation.
- **Timer and Benchmark Blocks**: Accurately measuring layer forward-pass latency: `with Timer("Attention Layer"): ...`.
- **GPU Device Switching**: Temporarily directing computation to a secondary GPU device: `with torch.cuda.device(1): ...`.

### Where It Appears in Real Projects
- `torch.no_grad()` and `torch.inference_mode()`.
- Thread locks and multiprocessing semaphores: `with lock: ...`.
- Database transaction sessions in SQLAlchemy.

---

## 2. Core Concept

### 2.1 The Context Manager Protocol
A class becomes a context manager by implementing:
1. `__enter__(self)`: Executes setup logic; return value is bound to the `as target` variable.
2. `__exit__(self, exc_type, exc_val, exc_tb)`: Executes teardown logic. Returning `True` suppresses any exception that occurred inside the block!

```python
class ManagedLock:
    def __enter__(self):
        print("1. Acquiring lock...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("2. Releasing lock deterministically...")
        if exc_type:
            print(f"Intercepted exception: {exc_val}")
        return False  # Do NOT suppress exception

with ManagedLock():
    print("Executing critical section...")
```

### 2.2 Functional Context Managers (`contextlib.contextmanager`)
Using a generator function decorated with `@contextmanager` eliminates boilerplate class code. Everything before `yield` is setup; everything after is teardown.

```python
from contextlib import contextmanager
import time

@contextmanager
def execution_timer(label: str):
    start = time.perf_counter()
    try:
        yield  # Control transfers to the with-block
    finally:
        elapsed = time.perf_counter() - start
        print(f"[{label}] Elapsed: {elapsed:.6f}s")

with execution_timer("Matrix Dot Product"):
    total = sum(i * 2 for i in range(500_000))
```

---

## 3. Mental Model

```text
The 'with' Execution Lifecycle:
with ContextManager() as target:
        │
        ▼
1. cm.__enter__() ──► Return value bound to 'target'
        │
        ▼
2. Body of with-block executes
        │
        ├── Exception occurs?
        │         ├── YES ──► cm.__exit__(exc_type, exc_val, tb)
        │         └── NO  ──► cm.__exit__(None, None, None)
        ▼
3. Block exits safely
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Custom `torch.no_grad()` Autograd Freeze Context Manager
Simulating PyTorch's gradient calculation toggle using a context manager:

```python
class AutogradContext:
    _grad_enabled: bool = True

    @classmethod
    def is_grad_enabled(cls) -> bool:
        return cls._grad_enabled

class no_grad:
    """Context manager that disables gradient computation graph tracking."""
    def __enter__(self) -> None:
        self.prev_state = AutogradContext.is_grad_enabled()
        AutogradContext._grad_enabled = False

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        AutogradContext._grad_enabled = self.prev_state  # Restore prior state

# Demonstration:
print("Before context: Grad enabled?", AutogradContext.is_grad_enabled())  # True
with no_grad():
    print("Inside context: Grad enabled?", AutogradContext.is_grad_enabled())  # False
    # Forward pass tensors do not allocate backward graph nodes!
print("After context: Grad enabled?", AutogradContext.is_grad_enabled())   # True
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Accidentally Suppressing Exceptions
If `__exit__` returns `True`, Python **swallows all exceptions** raised inside the block!
```python
class AccidentalSwallower:
    def __enter__(self): pass
    def __exit__(self, *args): return True  # DANGEROUS! Swallows ALL errors silently!
```

### 2. Forgetting `try...finally` in `@contextmanager`
If an exception occurs inside the `with` block and your generator does not wrap the `yield` in a `try...finally`, code after `yield` **will never execute**, leaking resources!

---

## 6. Interview Questions & Coding Traps

### Q1: What parameters does `__exit__` receive when an exception occurs?
It receives:
1. `exc_type`: The exception class (e.g., `ValueError`).
2. `exc_val`: The exception instance containing error message.
3. `exc_tb`: The traceback object.
If no exception occurred, all three parameters are `None`.

### Q2: What is `contextlib.ExitStack` used for?
`ExitStack` manages a dynamic or programmatically determined number of context managers (e.g., opening a variable list of files simultaneously):
```python
from contextlib import ExitStack

with ExitStack() as stack:
    files = [stack.enter_context(open(fname)) for fname in ["f1.txt", "f2.txt"]]
    # All files guaranteed closed when block exits!
```

### Complexity Reference
| Mechanism | Overhead |
| :--- | :--- |
| `__enter__` & `__exit__` | $O(1)$ method dispatch |
| `@contextmanager` generator | $O(1)$ generator frame allocation |
