# Magic (Dunder) Methods in Python

> Magic methods are reserved double-underscore methods (`__method__`) that hook into CPython language protocols, enabling operator overloading, custom indexing, context management, and callable objects.

---

## 1. Why This Matters

### Why This Concept Exists
Python avoids hardcoded language rules by delegating syntactic operations to dunder protocols: `len(x)` calls `x.__len__()`, `x[i]` calls `x.__getitem__(i)`, `x()` calls `x.__call__()`.

### Why Python Developers Need It
Mastering dunder methods enables developers to build custom domain-specific libraries that feel like native Python built-ins.

### Why It Matters Specifically in AI/ML/GenAI
- **PyTorch `Dataset` Protocol**: Every custom PyTorch dataset implements `__len__()` and `__getitem__(idx)`.
- **PyTorch `nn.Module` Callable Protocol**: Modules implement `__call__()` so instances can be invoked like functions: `output = model(inputs)`.
- **Custom Loss Tensor Arithmetic**: Overriding `__add__`, `__mul__`, `__matmul__` to implement autograd and tensor mathematical engines.

### Where It Appears in Real Projects
- `torch.utils.data.Dataset` (`__len__`, `__getitem__`).
- `torch.nn.Module` (`__call__`).
- Custom context managers (`__enter__`, `__exit__`).

---

## 2. Core Concept: The Essential Dunder Methods

### 2.1 String Representations: `__repr__` vs `__str__`
- `__repr__`: Unambiguous developer representation, ideally executable code.
- `__str__`: User-friendly human-readable representation.

```python
class TensorShape:
    def __init__(self, *dims: int):
        self.dims = dims

    def __repr__(self) -> str:
        return f"TensorShape{self.dims}"

    def __str__(self) -> str:
        return " x ".join(map(str, self.dims))

ts = TensorShape(32, 3, 224, 224)
print(repr(ts))  # TensorShape(32, 3, 224, 224)
print(str(ts))   # 32 x 3 x 224 x 224
```

### 2.2 Sequence Protocol: `__len__` and `__getitem__`
```python
class TokenSequence:
    def __init__(self, tokens: list[str]):
        self._tokens = tokens

    def __len__(self) -> int:
        return len(self._tokens)

    def __getitem__(self, idx: int) -> str:
        return self._tokens[idx]

seq = TokenSequence(["[CLS]", "Hello", "[SEP]"])
print(len(seq))      # 3 (Calls __len__)
print(seq[1])        # "Hello" (Calls __getitem__)
# Slicing and iteration work automatically because __getitem__ is implemented!
print([tok for tok in seq])  # ['[CLS]', 'Hello', '[SEP]']
```

### 2.3 Callable Objects: `__call__`
Allows an instance of a class to be invoked as a function.

```python
class Multiplier:
    def __init__(self, factor: float):
        self.factor = factor

    def __call__(self, x: float) -> float:
        return x * self.factor

scale = Multiplier(2.5)
print(scale(10.0))  # 25.0 (Calls __call__)
```

---

## 3. Mental Model

```text
Syntax to Dunder Protocol Translation:
len(obj)          ─────────► type(obj).__len__(obj)
obj[idx]          ─────────► type(obj).__getitem__(obj, idx)
obj(arg1, arg2)   ─────────► type(obj).__call__(obj, arg1, arg2)
a @ b             ─────────► type(a).__matmul__(a, b)
with obj:         ─────────► obj.__enter__() ... obj.__exit__()
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Production PyTorch-Style Custom Dataset Wrapper
Implementing a custom dataset with caching and transformations conforming to the standard dataset protocol:

```python
from typing import Dict, Any, List

class LLMTextDataset:
    """
    Simulates a PyTorch Dataset for fine-tuning LLMs.
    Implements the sequence dunder protocol: __len__ and __getitem__.
    """
    def __init__(self, texts: List[str], max_seq_len: int = 128) -> None:
        self.texts: List[str] = texts
        self.max_seq_len: int = max_seq_len

    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        raw_text = self.texts[idx]
        # Simulated subword tokenization
        dummy_tokens = [hash(word) % 10000 for word in raw_text.split()]
        # Truncate to max sequence length
        token_ids = dummy_tokens[: self.max_seq_len]
        attention_mask = [1] * len(token_ids)

        return {
            "text": raw_text,
            "input_ids": token_ids,
            "attention_mask": attention_mask
        }

corpus = [
    "Transformer architectures rely on multi-head attention.",
    "Prompt engineering guides LLM reasoning paths.",
    "Fine-tuning adapts pre-trained weights to specific tasks."
]

dataset = LLMTextDataset(corpus)
print(f"Total dataset samples: {len(dataset)}")
sample = dataset[0]
print(f"Sample 0 keys: {list(sample.keys())} | Token count: {len(sample['input_ids'])}")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. `__eq__` Overrides Invalidate `__hash__`
If you define `__eq__` in a class without defining `__hash__`, Python automatically sets `__hash__ = None`, making instances **unhashable**!

```python
class Item:
    def __init__(self, val): self.val = val
    def __eq__(self, other): return self.val == other.val
    # FIX: Implement __hash__ if instances should be stored in sets or dict keys!
    def __hash__(self): return hash(self.val)

item = Item(10)
s = {item}  # Works only because __hash__ is explicitly defined!
```

### 2. Dunder Methods Looked Up on the Class, Not the Instance
Assigning a dunder method directly to an instance will NOT work. CPython looks up dunder methods on `type(self)`.

---

## 6. Interview Questions & Coding Traps

### Q1: What is the difference between `__getitem__` and `__getattr__`?
- `__getitem__(self, key)` handles sequence or dictionary indexing (`obj[key]`).
- `__getattr__(self, name)` is a fallback called only when an attribute is accessed via dot notation (`obj.name`) and is **not found** in the instance or class dictionaries.

### Q2: What must `__len__` return?
`__len__` **must return a non-negative integer**. Returning a float or negative number raises `TypeError` or `ValueError`.

### Complexity Reference
| Dunder Method | Invocation Syntax | Standard Time Complexity |
| :--- | :--- | :--- |
| `__len__` | `len(obj)` | $O(1)$ |
| `__getitem__` | `obj[key]` | $O(1)$ array/hash lookup |
| `__call__` | `obj(*args)` | Function execution time |
| `__repr__` / `__str__` | `repr(obj)` / `str(obj)` | $O(K)$ string assembly |
