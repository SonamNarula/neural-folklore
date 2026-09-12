# Classes and Objects in Python

> A class is a blueprint object defining attributes and methods; an instance is a concrete heap object with its own instance namespace bound to that class blueprint.

---

## 1. Why This Matters

### Why This Concept Exists
State and behavior must be bundled together. Object-Oriented Programming (OOP) in Python models stateful entities with clear boundaries, interfaces, and lifecycles.

### Why Python Developers Need It
Understanding class versus instance namespaces, attribute lookup order, and memory layouts (`__dict__` vs `__slots__`) separates junior scripters from senior systems engineers.

### Why It Matters Specifically in AI/ML/GenAI
- **PyTorch Models**: Every deep learning neural network in PyTorch inherits from `torch.nn.Module`, overriding methods and managing tensor parameters as instance attributes.
- **LLM Agent Tools**: Agent tools are modeled as classes holding authentication credentials, API endpoints, rate limiter state, and execution methods.
- **Memory Optimization (`__slots__`)**: Storing millions of token or vector metadata objects without consuming massive RAM via dynamic dictionaries.

### Where It Appears in Real Projects
- Custom neural network layers (`nn.Module`).
- Vector database connectors and client sessions.
- Data preprocessing transformation steps.

---

## 2. Core Concept

### 2.1 Class vs Instance Attributes
- **Class Attributes**: Defined directly inside the class body, shared across all instances.
- **Instance Attributes**: Assigned to `self` (typically in `__init__`), unique to each instance.

```python
class ModelConfig:
    framework: str = "PyTorch"  # Class attribute (shared)

    def __init__(self, model_name: str, hidden_dim: int) -> None:
        self.model_name = model_name  # Instance attribute (unique)
        self.hidden_dim = hidden_dim  # Instance attribute (unique)

c1 = ModelConfig("bert-base", 768)
c2 = ModelConfig("gpt-2", 1024)

print(c1.framework, c2.framework)  # PyTorch PyTorch
# Mutating via instance creates an instance-level attribute that shadows the class attribute!
c1.framework = "JAX"
print(c1.framework, c2.framework)  # JAX PyTorch
```

### 2.2 Namespaces and `__dict__`
Every standard Python object and class has an internal `__dict__` storing its writable attributes.

```python
print("c1 instance namespace:", c1.__dict__)
# {'model_name': 'bert-base', 'hidden_dim': 768, 'framework': 'JAX'}
```

### 2.3 Memory Optimization with `__slots__`
By default, every instance allocates a `dict` for `__dict__`, consuming ~150+ bytes of overhead. Declaring `__slots__` tells Python to use a compact fixed-size C array of pointers instead.

```python
import sys

class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedPoint:
    __slots__ = ('x', 'y')  # Eliminates __dict__
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = RegularPoint(1.0, 2.0)
p2 = SlottedPoint(1.0, 2.0)
print(f"Regular instance size: {sys.getsizeof(p1) + sys.getsizeof(p1.__dict__)} bytes")
print(f"Slotted instance size: {sys.getsizeof(p2)} bytes")  # ~3x-5x more memory efficient!
```

---

## 3. Mental Model

```text
Namespace Lookup Hierarchy:
instance.attr
     │
     ├── 1. Found in instance.__dict__? ──► YES ──► Return value
     │
     ├── 2. Found in Class.__dict__?    ──► YES ──► Return value
     │
     ├── 3. Found in Base Classes?      ──► YES ──► Return value
     │
     └── 4. Not found ──────────────────► Raise AttributeError
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: High-Density Document Chunk Metadata with `__slots__`
Storing 1,000,000 document vector chunks in memory with minimal memory footprint:

```python
class VectorChunk:
    __slots__ = ("chunk_id", "doc_id", "token_count", "embedding_norm")

    def __init__(self, chunk_id: str, doc_id: str, token_count: int, embedding_norm: float) -> None:
        self.chunk_id = chunk_id
        self.doc_id = doc_id
        self.token_count = token_count
        self.embedding_norm = embedding_norm

# Benchmark storage:
chunks = [VectorChunk(f"c_{i}", f"doc_{i//10}", 128, 1.0) for i in range(1000)]
print(f"Successfully allocated {len(chunks)} high-density vector chunks.")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Mutable Class Attributes
If a class attribute is mutable (e.g., a list), modifying it via an instance mutates the shared object across ALL instances!

```python
# CATASTROPHIC BUG:
class ModelRegistry:
    loaded_weights = []  # Shared across all instances!

r1 = ModelRegistry()
r2 = ModelRegistry()
r1.loaded_weights.append("bert.pt")
print(r2.loaded_weights)  # ['bert.pt'] -> Leaked into other instance!
```

---

## 6. Interview Questions & Coding Traps

### Q1: What is the exact sequence of attribute lookup when accessing `obj.x`?
1. Checks class descriptors (data descriptors with `__get__` and `__set__`).
2. Checks `obj.__dict__` (instance namespace).
3. Checks non-data descriptors and regular class attributes on `type(obj)`.
4. Traverses parent classes via the Method Resolution Order (MRO).
5. Calls `obj.__getattr__('x')` if defined; otherwise raises `AttributeError`.

### Q2: What happens if you try to dynamically add an attribute not defined in `__slots__`?
Python raises `AttributeError: 'SlottedClass' object has no attribute 'new_attr'` because the instance lacks a dynamic `__dict__`.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Instance attribute access `self.x` | $O(1)$ hash/slot lookup | $O(1)$ |
| Instance instantiation | $O(1)$ | $O(1)$ |
