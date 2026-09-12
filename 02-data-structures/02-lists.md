# Lists in Python

> A list is a dynamically sized, contiguous array of object pointers supporting $O(1)$ random access and amortized $O(1)$ append operations.

---

## 1. Why This Matters

### Why This Concept Exists
Programs need flexible sequential containers that can expand, shrink, and hold heterogeneous elements without requiring manual heap allocation and reallocation logic.

### Why Python Developers Need It
Lists are Python's primary sequence workhorse. Understanding their internal dynamic array growth factor prevents costly reallocations and suboptimal index mutations.

### Why It Matters Specifically in AI/ML/GenAI
- **Batch Buffering**: Collecting training samples, conversation messages, or token embeddings before converting them into NumPy arrays or PyTorch tensors (`torch.tensor(batch_list)`).
- **Beam Search Candidates**: Maintaining candidate hypothesis beams during LLM sequence decoding.
- **Dynamic Feature Accumulation**: Collecting feature columns during exploratory data analysis.

### Where It Appears in Real Projects
- PyTorch custom Dataset `__getitem__` batch accumulation.
- Conversation history tracking in LangChain / LlamaIndex.
- Graph adjacency lists in Graph Neural Networks (GNNs).

---

## 2. Core Concept

### 2.1 Internal Architecture: Dynamic Array of Pointers
A Python list is a `PyListObject` consisting of:
- `ob_size`: Number of elements currently in the list.
- `allocated`: Actual capacity allocated in heap memory.
- `ob_item`: A contiguous C array of pointers (`PyObject**`) pointing to items.

```python
import sys

nums = []
print(f"Empty list overhead: {sys.getsizeof(nums)} bytes")
# Python over-allocates memory to achieve amortized O(1) appends:
for i in range(10):
    nums.append(i)
    print(f"Items: {len(nums):<2} | Capacity/Size in memory: {sys.getsizeof(nums)} bytes")
```

### 2.2 List Operations & Mutability
```python
# List mutability: elements can be modified in-place
items = [10, 20, 30]
items[1] = 99  # In-place modification: items is now [10, 99, 30]

# Extending vs Appending
items.append([1, 2])  # Adds single element: [10, 99, 30, [1, 2]]
items.pop()
items.extend([1, 2])  # Unpacks and appends each: [10, 99, 30, 1, 2]
```

### 2.3 Slicing Creates Shallow Copies
`sub = items[1:3]` allocates a **brand new list** containing pointers to elements 1 and 2.

---

## 3. Mental Model

```text
Python List Memory Layout:
PyListObject Header:
[ ob_refcnt | ob_type | ob_size = 3 | allocated = 6 ]
   ob_item ──► Contiguous array of pointers (C Array):
               [ Ptr 0 | Ptr 1 | Ptr 2 | NULL | NULL | NULL ]
                   │       │       │
                   ▼       ▼       ▼
                Heap:   Heap:   Heap:
                [10]    [20]    [30]
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: High-Performance Mini-Batch Generator
Batching arbitrary dataset sequences without loading everything into memory simultaneously:

```python
from typing import List, Generator, Any

def create_mini_batches(dataset: List[Any], batch_size: int) -> Generator[List[Any], None, None]:
    """
    Yields slices of data as mini-batches.
    Slicing creates shallow copies of pointers, fast and memory-safe.
    """
    for i in range(0, len(dataset), batch_size):
        yield dataset[i : i + batch_size]

# Simulation:
samples = [{"id": i, "embedding": [0.1 * i, 0.2 * i]} for i in range(10)]
for batch_idx, batch in enumerate(create_mini_batches(samples, batch_size=4)):
    print(f"Batch {batch_idx} length: {len(batch)} | Sample IDs: {[s['id'] for s in batch]}")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. The Matrix Multiplication Trap (`[[0]*N]*M`)
```python
# BUG: Creates M references to the SAME inner list
bad_matrix = [[0] * 3] * 3
bad_matrix[0][0] = 7
print(bad_matrix)  # [[7, 0, 0], [7, 0, 0], [7, 0, 0]]

# CORRECT: List comprehension generates distinct list objects
good_matrix = [[0] * 3 for _ in range(3)]
good_matrix[0][0] = 7
print(good_matrix)  # [[7, 0, 0], [0, 0, 0], [0, 0, 0]]
```

### 2. `insert(0, val)` and `pop(0)` are $O(N)$
Inserting or removing from the head of a list requires shifting all subsequent elements in memory. Use `collections.deque` for $O(1)$ operations at both ends.

---

## 6. Interview Questions & Coding Traps

### Q1: Why does `list.append()` have an amortized $O(1)$ time complexity instead of strictly $O(1)$?
When the list reaches its pre-allocated capacity (`allocated == ob_size`), CPython must allocate a larger contiguous block of memory (growth factor roughly $\sim 1.125 	imes$ + constant padding) and copy all existing pointers over. This reallocation takes $O(N)$ time. However, because capacity grows proportionally, reallocations occur exponentially less often, giving an **amortized cost of $O(1)$** per append.

### Q2: Predict the output:
```python
a = [1, 2, 3]
b = a[:]
print(a == b, a is b)
```
**Output:** `True False`
**Explanation:** `a[:]` creates a new shallow copy of the list. Values are equal (`==` is `True`), but memory addresses are distinct (`is` is `False`).

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Indexing `list[i]` | $O(1)$ | $O(1)$ |
| Appending `list.append(x)` | $O(1)$ amortized | $O(1)$ |
| Slicing `list[i:j]` | $O(K)$ where $K = j - i$ | $O(K)$ |
| Insert / Pop at index 0 | $O(N)$ | $O(1)$ |
| Search `x in list` | $O(N)$ | $O(1)$ |
