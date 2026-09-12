# Mutability and Immutability in Python

> Mutable objects can alter their internal state in-place at the same memory address; immutable objects cannot be modified once instantiated, requiring new object allocations for changes.

---

## 1. Why This Matters

### Why This Concept Exists
Immutability provides mathematical determinism, thread safety, and hashability. Mutability enables high-performance in-place updates without continuous memory reallocations.

### Why Python Developers Need It
Confusion regarding mutability is the single largest source of bugs in Python applications (unintended aliasing mutations, mutable default arguments, unhashable dictionary key errors).

### Why It Matters Specifically in AI/ML/GenAI
- **In-Place Tensor Operations (`add_`, `mul_`)**: In PyTorch, methods with a trailing underscore mutate tensors in-place, conserving precious GPU VRAM.
- **Model Parameter Freezing**: Freezing neural network weights for transfer learning by setting `param.requires_grad = False`.
- **Immutable Configuration Schemas**: Freezing configuration objects to ensure hyperparameters cannot be altered mid-training.

### Where It Appears in Real Projects
- In-place tensor operations in PyTorch.
- Frozen dataclasses and Pydantic models.
- Immutable dictionary keys in cache stores.

---

## 2. Core Concept

### 2.1 Categorization of Python Types
| Category | Types | Memory Address Behavior on Change |
| :--- | :--- | :--- |
| **Immutable** | `int`, `float`, `str`, `tuple`, `bytes`, `frozenset`, `bool`, `None` | Always allocates a new object (`id` changes) |
| **Mutable** | `list`, `dict`, `set`, `bytearray`, custom class instances | Modifies in-place (`id` remains identical) |

```python
# Immutable Demonstration:
x = 10
old_id = id(x)
x += 1
print("Immutable int changed address:", old_id != id(x))  # True!

# Mutable Demonstration:
items = [1, 2]
old_id = id(items)
items.append(3)
print("Mutable list kept same address:", old_id == id(items))  # True!
```

### 2.2 The Tuple Containing Mutable Elements Edge Case
A tuple is immutable in its references, but the objects it references may be mutable!

```python
t = (1, [10, 20])
# t[1] = [30]  -> Raises TypeError
t[1].append(30) # Valid! Modifies inner list in-place!
print(t)        # (1, [10, 20, 30])
```

---

## 3. Mental Model

```text
Memory Address Mutation:
Mutable (List):
id: 0x1000 [ 1, 2 ] ──► items.append(3) ──► id: 0x1000 [ 1, 2, 3 ] (Same ID!)

Immutable (Int):
id: 0x2000 [ 10 ]   ──► x += 1          ──► id: 0x3500 [ 11 ] (New Heap Object!)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Frozen Immutable Configuration with `@dataclass(frozen=True)`
Creating an unalterable experiment configuration object:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ExperimentHyperparameters:
    learning_rate: float
    batch_size: int
    optimizer: str = "AdamW"

config = ExperimentHyperparameters(learning_rate=1e-4, batch_size=32)
print("Config:", config.learning_rate)

# Attempting mutation raises FrozenInstanceError!
try:
    config.learning_rate = 5e-4
except Exception as e:
    print(f"Mutation blocked: {type(e).__name__} - {e}")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. In-Place Operators: `+=` on List vs Tuple
```python
# Tricky interview favorite:
t = (1, 2, [3, 4])
try:
    t[2] += [5]
except TypeError:
    pass

print(t)  # (1, 2, [3, 4, 5])!
```
**Explanation:** `+=` executes `list.__iadd__()` on the list, modifying it in-place. Then Python attempts to assign the result back to `t[2]`, which raises a `TypeError` because tuples reject item assignment! The mutation succeeded despite the exception!

---

## 6. Interview Questions & Coding Traps

### Q1: Why can't mutable objects be used as dictionary keys?
Dictionary keys must be **hashable**. If a mutable object were allowed as a key and its contents mutated, its hash code would change, making the dictionary lookup bucket unreachable and corrupting the hash table.

### Q2: What is the output of this code?
```python
def modify(arr, val):
    arr = arr + [val]
    return arr

x = [1, 2]
modify(x, 3)
print(x)
```
**Output:** `[1, 2]`
**Explanation:** `arr = arr + [val]` creates a brand new list and rebinds the local variable `arr`. It does NOT mutate the original list `x`. To mutate in-place, use `arr.append(val)` or `arr += [val]`.

### Complexity Reference
| Operation | Time Complexity | Memory Impact |
| :--- | :--- | :--- |
| In-place List Append | Amortized $O(1)$ | Modifies existing buffer |
| String / Tuple Concatenation (`+`) | $O(N + M)$ | Allocates fresh object in RAM |
