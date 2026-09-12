# Functions in Python

> Functions in Python are first-class objects encapsulated in heap memory, capable of being assigned to variables, passed as arguments, and returned from other functions.

---

## 1. Why This Matters

### Why This Concept Exists
Functions decompose complex systems into modular, reusable, testable units of logic. In Python, treating functions as first-class objects bridges object-oriented and functional programming paradigms.

### Why Python Developers Need It
Mastering call frames, pure functions, side-effect isolation, and functional composition enables developers to build clean architectures without tight coupling.

### Why It Matters Specifically in AI/ML/GenAI
- **Loss Functions & Activation Functions**: In PyTorch/TensorFlow, activations (`relu`, `gelu`, `softmax`) and loss criteria (`cross_entropy`) are passed as first-class callable functions into training loops and optimizer steps.
- **Pipeline Callbacks**: Training harnesses (HuggingFace Trainer, PyTorch Lightning) accept custom callback functions triggered at `on_step_end`, `on_epoch_end`.
- **Agentic Tool Execution**: In LLM agent frameworks, functions represent tools that the LLM invokes dynamically based on JSON schema signatures.

### Where It Appears in Real Projects
- Activation dispatchers in neural network architectures.
- Callback hooks in PyTorch Lightning.
- Dynamic tool registration in LangChain / LlamaIndex.

---

## 2. Core Concept

### 2.1 First-Class Functions
```python
def relu(x: float) -> float:
    return max(0.0, x)

# 1. Assigned to variables
activation = relu
print(activation(-2.5))  # 0.0

# 2. Passed as arguments
def apply_activation(values: list[float], fn) -> list[float]:
    return [fn(v) for v in values]

print(apply_activation([-1.0, 2.0, -0.5], relu))  # [0.0, 2.0, 0.0]
```

### 2.2 Pure Functions vs Side Effects
A **pure function** depends solely on its inputs and produces no side effects (no mutation of external state, no I/O mutations). Pure functions are easy to parallelize, test, and cache.

```python
# Impure Function (Mutates external state):
global_loss_history = []
def log_loss_impure(loss: float):
    global_loss_history.append(loss)  # Side effect!

# Pure Function:
def compute_normalized_loss(loss: float, scale_factor: float) -> float:
    return loss / scale_factor
```

---

## 3. Mental Model

```text
Function as First-Class Heap Object:
def relu(x): ...
       │
       ▼
Local Namespace:
  "relu" ──► ┌─────────────────────────────────────┐
             │ PyFunctionObject (Heap)             │
             │ ─────────────────────────────────── │
             │ __name__   = "relu"                 │
             │ __code__   = <code object: bytecode>│
             │ __call__   = C-level dispatch       │
             └─────────────────────────────────────┘
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Dynamic Model Architecture Dispatcher
A functional registry mapping model architectures to factory builder functions:

```python
from typing import Callable, Dict, Any

# Registry pattern using first-class functions
MODEL_REGISTRY: Dict[str, Callable[..., Any]] = {}

def register_model(name: str):
    def decorator(fn: Callable[..., Any]):
        MODEL_REGISTRY[name] = fn
        return fn
    return decorator

@register_model("transformer_encoder")
def build_encoder(d_model: int = 512, n_heads: int = 8):
    return {"type": "encoder", "d_model": d_model, "heads": n_heads}

@register_model("causal_decoder")
def build_decoder(d_model: int = 1024, layers: int = 32):
    return {"type": "causal_decoder", "d_model": d_model, "layers": layers}

def get_model(arch: str, **kwargs) -> Any:
    if arch not in MODEL_REGISTRY:
        raise ValueError(f"Unknown architecture: {arch}. Available: {list(MODEL_REGISTRY.keys())}")
    return MODEL_REGISTRY[arch](**kwargs)

model = get_model("causal_decoder", d_model=2048)
print(f"Created architecture: {model}")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. The Call Stack Limit
Python enforces a default recursion/call stack depth limit (typically 1000 frames) via `sys.getrecursionlimit()`. Recursive functions without base cases raise `RecursionError`.

### 2. Overwriting Built-in Functions
Accidentally naming a variable `max`, `min`, `sum`, or `list` shadows the built-in function in the local namespace.

```python
# DANGEROUS:
# sum = 10 + 20
# print(sum([1, 2, 3]))  -> TypeError: 'int' object is not callable
```

---

## 6. Interview Questions & Coding Traps

### Q1: What happens when a function executes without an explicit `return` statement?
Python implicitly appends `return None` to the end of every function block.

### Q2: What is the output of the following code?
```python
def outer():
    x = 10
    def inner():
        x = 20
    inner()
    return x

print(outer())
```
**Output:** `10`
**Explanation:** `x = 20` inside `inner()` creates a new local variable `x` within `inner`'s frame; it does not mutate the enclosing `x` in `outer()`. To mutate it, `inner()` would require the `nonlocal x` declaration.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Function Call Overhead | $O(1)$ stack frame allocation | $O(1)$ frame memory |
| Function Definition | $O(1)$ heap allocation | $O(1)$ bytecode object |
