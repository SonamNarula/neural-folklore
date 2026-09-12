# Tuples in Python

> Tuples are immutable, fixed-size heterogeneous sequences of object references optimized for memory efficiency and hashable compound keys.

---

## 1. Why This Matters

### Why This Concept Exists
Data structures often represent fixed records (coordinates, database rows, hyperparameter grids) whose identity and length must remain immutable throughout execution.

### Why Python Developers Need It
Tuples protect against accidental mutation, use less memory than lists, and can serve as dictionary keys and set elements when all contained items are hashable.

### Why It Matters Specifically in AI/ML/GenAI
- **Tensor Shapes**: In PyTorch, TensorFlow, and NumPy, tensor dimensions and strides are universally represented as tuples: `tensor.shape = (batch_size, seq_len, hidden_dim)`.
- **Cache Keys for Memoization**: When caching LLM embedding calls or model outputs, function arguments are packed into tuples for dictionary lookup keys.
- **Named Records**: `namedtuple` provides lightweight, readable schemas for training batch metadata without the overhead of full classes.

### Where It Appears in Real Projects
- Model parameter shapes: `x.view(-1, 768)`.
- LRU caching decorators: `@functools.lru_cache(maxsize=1024)`.
- Multi-metric evaluation returns: `return loss, accuracy, f1_score`.

---

## 2. Core Concept

### 2.1 Tuple Mechanics
```python
# Definition (comma defines the tuple, parentheses provide grouping)
single_element = (42,)   # Comma is mandatory!
not_a_tuple = (42)       # Evaluates to int 42!

# Unpacking
point = (10, 20, 30)
x, y, z = point

# Extended unpacking with *
first, *middle, last = (1, 2, 3, 4, 5)
print(first, middle, last)  # 1, [2, 3, 4], 5
```

### 2.2 Memory Efficiency: Tuple vs List
Tuples do not need over-allocation buffers because their size is fixed at instantiation.

```python
import sys
l = [1, 2, 3, 4]
t = (1, 2, 3, 4)
print(f"List size: {sys.getsizeof(l)} bytes | Tuple size: {sys.getsizeof(t)} bytes")
# Lists allocate extra capacity for growth; tuples are exact-fit.
```

### 2.3 Named Tuples (`collections.namedtuple` and `typing.NamedTuple`)
Named tuples provide self-documenting field names with zero memory overhead over regular tuples.

```python
from typing import NamedTuple

class ModelOutput(NamedTuple):
    logits: list[float]
    loss: float
    token_count: int

out = ModelOutput(logits=[0.1, 0.9], loss=0.34, token_count=2)
print(out.loss)        # 0.34 (Field access)
print(out[1])          # 0.34 (Tuple index access)
```

---

## 3. Mental Model

```text
List (Mutable, dynamic growth buffer):
[ Header | Size=3 | Cap=6 ] ──► [ Ptr 0 | Ptr 1 | Ptr 2 | NULL | NULL | NULL ]

Tuple (Immutable, fixed compact allocation):
[ Header | Size=3 ] ──────────► [ Ptr 0 | Ptr 1 | Ptr 2 ]
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Compound Cache Key for LLM Embedding Generation
Using tuples to construct hashable cache keys to avoid redundant expensive API calls:

```python
from typing import Dict, Tuple

class EmbeddingCache:
    def __init__(self) -> None:
        # Tuple of (model_name, text, temperature) acts as compound hash key
        self.cache: Dict[Tuple[str, str, float], list[float]] = {}

    def get_or_compute(self, model: str, prompt: str, temp: float) -> list[float]:
        key = (model, prompt, temp)
        if key in self.cache:
            print("Cache HIT: Returning cached embedding")
            return self.cache[key]

        print("Cache MISS: Computing embedding...")
        # Simulated embedding calculation:
        computed_vector = [0.12, -0.45, 0.88]
        self.cache[key] = computed_vector
        return computed_vector

cache = EmbeddingCache()
vec1 = cache.get_or_compute("text-embedding-3-small", "Hello world", 0.0)
vec2 = cache.get_or_compute("text-embedding-3-small", "Hello world", 0.0)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Immutability of Tuple vs Mutability of Its Elements
A tuple's **references** are immutable, but the **objects** it references can still be mutable!

```python
t = (1, [10, 20], 3)
# t[1] = [30]  -> Raises TypeError
t[1].append(30) # VALID! The list inside the tuple is mutated!
print(t)        # (1, [10, 20, 30], 3)

# Hashability trap:
# hash(t)  -> Raises TypeError: unhashable type: 'list'
# A tuple is only hashable if ALL its elements are hashable!
```

---

## 6. Interview Questions & Coding Traps

### Q1: Can a tuple be used as a dictionary key?
**Answer:** Yes, but **only if all elements inside the tuple are immutable and hashable**. A tuple containing a mutable object like a list `(1, [2, 3])` will raise `TypeError: unhashable type: 'list'`.

### Q2: What is the output of `t = (1); type(t)` vs `t = (1,); type(t)`?
`int` and `tuple`.
**Explanation:** Parentheses without a trailing comma are treated as standard mathematical grouping, evaluating `(1)` to integer `1`. A trailing comma `(1,)` designates a 1-element tuple.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Indexing `tuple[i]` | $O(1)$ | $O(1)$ |
| Unpacking `a, b = tup` | $O(1)$ | $O(1)$ |
| Search `x in tup` | $O(N)$ | $O(1)$ |
| Instantiation | $O(N)$ | $O(N)$ (more compact than list) |
