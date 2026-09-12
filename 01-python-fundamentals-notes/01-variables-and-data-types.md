# Variables and Data Types in Python

> Python variables are not memory boxes holding values; they are dynamically bound pointer labels (references) pointing to heap-allocated objects.

---

## 1. Why This Matters

### Why This Concept Exists
In statically typed languages like C, C++, or Rust, declaring `int x = 42;` allocates 4 bytes directly on the execution stack. In Python, everything—numbers, functions, modules, classes—is a first-class object (`PyObject`) allocated on the heap. Python variables are merely reference pointers stored in a namespace mapping.

### Why Python Developers Need It
Understanding how variables reference heap memory prevents catastrophic unintended side-effects (e.g., mutating an array in one function modifying it globally) and eliminates confusion regarding object lifetimes, garbage collection, and variable scope.

### Why It Matters Specifically in AI/ML/GenAI
- **Weights & Tensor Aliasing**: When passing neural network weights (`torch.Tensor`, `np.ndarray`), slicing or assignment creates a view/reference rather than copying data. If you modify a tensor slice, you mutate model weights in place.
- **Precision & Numeric Underflow**: Python's `int` has arbitrary precision (grows indefinitely), whereas `float` is a 64-bit IEEE 754 double. In deep learning, tensors run on 16-bit (`fp16`, `bfloat16`) or 8-bit (`int8`, `fp8`). Misunderstanding scalar types leads to silent precision casting errors and gradient vanishing/exploding.
- **Autograd Memory Leaks**: Assigning a training loss tensor (`loss = criterion(pred, target)`) to a tracking list without calling `.item()` holds the entire backwards computation graph in VRAM, causing GPU Out-of-Memory (OOM) errors.

### Where It Appears in Real Projects
- Model parameter checkpoint loading (`model.load_state_dict()`).
- Loss tracking and metrics logging in training loops.
- Token ID buffers and vocabulary index mappings in LLM tokenizers.

---

## 2. Core Concept

### 2.1 Variables as Pointer References
In Python, assigning a value creates an object in heap memory and points a variable label to it:

```python
x = 1000
y = x
print(id(x) == id(y))  # True -> both point to the exact same PyObject
```

### 2.2 Built-in Primitive Types
| Type | Mutability | Internal C Type | ML / GenAI Role |
| :--- | :--- | :--- | :--- |
| `int` | Immutable | `PyLongObject` (digit array) | Token indices, vocabulary size, epoch counter |
| `float` | Immutable | `PyFloatObject` (C double, 64-bit) | Loss values, learning rates, attention weights |
| `bool` | Immutable | `PyBoolObject` (subtype of int) | Padding masks, causal attention flags |
| `str` | Immutable | `PyUnicodeObject` (UTF-8/16/32) | Prompt text, document chunks, LLM outputs |
| `bytes` | Immutable | `PyBytesObject` (raw 8-bit bytes) | Binary embeddings, audio buffers, image bytes |
| `NoneType`| Immutable | Singleton (`Py_None`) | Optional hyperparams, uncomputed gradients |

### 2.3 Dynamic Typing vs Strong Typing
Python is **dynamically typed** (types are checked at runtime, variables have no fixed type) and **strongly typed** (Python will not silently coerce incompatible types like adding a string and an integer).

```python
# Dynamically typed:
val = 42            # val references an int
val = "temperature" # val now references a str

# Strongly typed:
# val + 5  -> Raises TypeError: can only concatenate str (not "int") to str
```

---

## 3. Mental Model

```text
C-style Memory Model (Fixed Stack Box):
Address: 0x7fff0010 [ 00000000 00000000 00000010 10101000 ]  (x = 680)

Python Memory Model (Nametag bound to Heap Object):
Local Namespace Dictionary:
   "x" ───(pointer)───┐
                      ▼
             ┌───────────────────────────────┐
             │ Heap: PyLongObject            │
             │ ───────────────────────────── │
             │ ob_refcnt = 1                 │
             │ ob_type   = &PyLong_Type      │
             │ ob_digit  = [680]             │
             └───────────────────────────────┘
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Safe Metric Tracker (Preventing PyTorch Autograd Graph Leaks)
A production training loop pattern that captures scalar values without holding GPU autograd computation graphs.

```python
from typing import Dict, List

class MetricTracker:
    """Tracks scalar metrics without keeping PyTorch autograd graph references."""
    def __init__(self) -> None:
        self.metrics: Dict[str, List[float]] = {}

    def log(self, key: str, value: float) -> None:
        # Crucial: explicitly cast to float to detach from torch.Tensor autograd graphs
        scalar_val = float(value)
        if key not in self.metrics:
            self.metrics[key] = []
        self.metrics[key].append(scalar_val)

    def get_epoch_mean(self, key: str) -> float:
        vals = self.metrics.get(key, [])
        return sum(vals) / len(vals) if vals else 0.0

tracker = MetricTracker()
tracker.log("loss", 0.6931)
tracker.log("loss", 0.4520)
print(f"Mean loss: {tracker.get_epoch_mean('loss'):.4f}")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Small Integer Interning (-5 to 256)
CPython pre-allocates global singletons for integers from `-5` to `256`. Outside this range, separate allocations occur.

```python
a = 256
b = 256
print(a is b)  # True (interned global singleton)

x = 1000
y = 1000
print(x is y)  # False (two distinct heap objects, compared by memory address)
print(x == y)  # True (compared by value)
```

### 2. Floating-Point Roundoff in Loss Convergence
Binary representation cannot exactly represent decimal fractions like `0.1`.

```python
print(0.1 + 0.2 == 0.3)  # False (0.30000000000000004)

# Production Fix:
import math
print(math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-7))  # True
```

---

## 6. Interview Questions & Coding Traps

### Q1: What happens in memory when you execute `a = [1, 2]`; `b = a`; `a = a + [3]` versus `a += [3]`?
- `a = a + [3]` creates an entirely new list object and rebinds `a`. `b` still points to `[1, 2]`.
- `a += [3]` invokes `list.__iadd__()`, mutating the list in-place. Both `a` and `b` reflect `[1, 2, 3]`.

### Q2: What is the output of the following code snippet?
```python
x = [None] * 3
x[0] = "prompt"
print(x)

matrix = [[0] * 3] * 3
matrix[0][0] = 1
print(matrix)
```
**Output:**
```text
['prompt', None, None]
[[1, 0, 0], [1, 0, 0], [1, 0, 0]]
```
**Explanation:** `[None] * 3` creates a list containing 3 references to `None`. Changing `x[0]` rebinds index 0. However, `[[0] * 3] * 3` creates an outer list containing 3 references to the **exact same inner list**! Modifying `matrix[0][0]` mutates all 3 rows.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Variable Assignment | $O(1)$ | $O(1)$ pointer |
| `id(obj)` | $O(1)$ | $O(1)$ |
| `type(obj)` | $O(1)$ | $O(1)$ |
