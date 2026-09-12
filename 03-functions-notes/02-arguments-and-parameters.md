# Arguments and Parameters in Python

> Parameters define the variable contract in a function declaration; arguments are the concrete values passed during invocation across positional, keyword, and variadic channels.

---

## 1. Why This Matters

### Why This Concept Exists
Modern APIs require flexible interfaces that balance strict positional inputs, self-documenting keyword options, and arbitrary variadic forwarding.

### Why Python Developers Need It
Understanding parameter unpacking (`*args`, `**kwargs`), positional-only (`/`), and keyword-only (`*`) boundaries ensures robust, ergonomic library design.

### Why It Matters Specifically in AI/ML/GenAI
- **Configurable Hyperparameter Forwarding**: Deep learning modules and HuggingFace pipelines routinely accept `**kwargs` to forward optional generation configurations (e.g., `temperature`, `top_p`, `max_new_tokens`) down multiple abstraction layers.
- **The Mutable Default Argument Trap**: Initializing lists or dicts inside default function arguments (`def train(batch, weights=[])`) causes shared state contamination across training iterations.
- **API Cleanliness**: Enforcing keyword-only arguments (`*`) prevents callers from confusing positional floats like `lr=0.001` and `weight_decay=0.01`.

### Where It Appears in Real Projects
- `torch.nn.Module` forward pass signatures.
- OpenAI and Anthropic SDK client methods.
- Scikit-learn estimator initializers.

---

## 2. Core Concept

### 2.1 The Complete Parameter Hierarchy
In Python 3.8+, parameters follow a strict sequence:
`def func(pos_only, /, standard, *args, kw_only, **kwargs):`

```python
def configure_layer(
    dim: int,                     # Positional-only before '/'
    /,
    activation: str = "relu",     # Standard (positional or keyword)
    *,
    dropout: float = 0.1,         # Keyword-only after '*'
    use_bias: bool = True
) -> dict:
    return {
        "dim": dim,
        "activation": activation,
        "dropout": dropout,
        "use_bias": use_bias
    }

# Valid calls:
print(configure_layer(512, "gelu", dropout=0.2))
print(configure_layer(512, activation="gelu", dropout=0.2, use_bias=False))

# INVALID calls:
# configure_layer(dim=512) -> TypeError (dim is positional-only!)
# configure_layer(512, "gelu", 0.2) -> TypeError (dropout is keyword-only!)
```

### 2.2 Variadic Arguments: `*args` and `**kwargs`
- `*args` packs extra positional arguments into a `tuple`.
- `**kwargs` packs extra keyword arguments into a `dict`.

```python
def forward_pass(*tensors, **meta):
    print(f"Received {len(tensors)} tensor inputs")
    print(f"Metadata options: {meta}")

forward_pass("x1", "x2", device="cuda:0", precision="fp16")
```

---

## 3. Mental Model

```text
Parameter Layout Boundary:
def model( a, b,  / ,   c, d,   * ,   e, f ):
          └───────┘    └───────┘     └──────┘
          Positional   Standard      Keyword-Only
          ONLY         (Both OK)     (Must specify name=value)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Safe LLM Request Forwarder with Kwargs Passthrough
A wrapper that validates required parameters while forwarding arbitrary engine hyperparameters:

```python
from typing import Dict, Any

def query_llm(
    prompt: str,
    *,
    model: str = "claude-3-5-sonnet",
    temperature: float = 0.7,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Safely constructs an LLM request payload.
    Forces model and temperature to be keyword-only to prevent accidental transposition.
    """
    payload = {
        "prompt": prompt,
        "model": model,
        "temperature": temperature,
        "parameters": kwargs  # Forward remaining optional args (e.g. top_p, stream)
    }
    return payload

request = query_llm(
    "Explain backpropagation",
    model="gpt-4o",
    temperature=0.2,
    top_p=0.95,
    max_tokens=2048
)
print("Constructed Request Payload:", request)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. THE MUTABLE DEFAULT ARGUMENT TRAP (Classic Interview Favorite!)
Default arguments are evaluated **ONCE when the function definition is executed**, not each time the function is called!

```python
# CATASTROPHIC BUG:
def append_token(token: str, history: list = []):
    history.append(token)
    return history

print(append_token("tok1"))  # ['tok1']
print(append_token("tok2"))  # ['tok1', 'tok2'] -> Shared state retained across calls!

# PRODUCTION PATTERN: Use None as default sentinel
def append_token_safe(token: str, history: list | None = None) -> list:
    if history is None:
        history = []
    history.append(token)
    return history

print(append_token_safe("tok1"))  # ['tok1']
print(append_token_safe("tok2"))  # ['tok2'] -> Correct! Fresh list allocated!
```

---

## 6. Interview Questions & Coding Traps

### Q1: What does `def f(a, b=1, *args, c, d=2, **kwargs)` enforce?
- `a`: Required positional/keyword.
- `b`: Optional positional/keyword (default 1).
- `*args`: Absorbs excess positional args as a tuple.
- `c`: **Required keyword-only argument** (no default provided!).
- `d`: Optional keyword-only argument (default 2).
- `**kwargs`: Absorbs excess keyword args as a dict.

### Q2: What is the output of the following code?
```python
def func(a, b, c):
    return a + b + c

args = [1, 2]
kwargs = {"c": 3}
print(func(*args, **kwargs))
```
**Output:** `6`
**Explanation:** `*args` unpacks the list into positional arguments `a=1`, `b=2`. `**kwargs` unpacks the dict into keyword argument `c=3`.

### Complexity Reference
| Mechanism | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Argument Unpacking `*args` | $O(K)$ where $K = len(args)$ | $O(K)$ tuple |
| Keyword Unpacking `**kwargs`| $O(M)$ where $M = len(kwargs)$| $O(M)$ dict |
