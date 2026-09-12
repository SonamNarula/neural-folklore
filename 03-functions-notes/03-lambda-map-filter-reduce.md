# Lambda, Map, Filter, and Reduce in Python

> Lambda expressions provide single-line anonymous function constructs, while map, filter, and reduce form the classical trinity of functional sequence transformations.

---

## 1. Why This Matters

### Why This Concept Exists
Writing full `def` blocks for trivial, one-time transformations creates visual noise. Functional primitives allow concise, inline operations over iterables.

### Why Python Developers Need It
While comprehensions are often preferred in modern Python, `lambda` functions remain indispensable for custom sorting keys, functional pipeline composition, and dynamic callbacks.

### Why It Matters Specifically in AI/ML/GenAI
- **Custom Ranking & Sorting**: Sorting retrieved RAG documents by similarity score: `docs.sort(key=lambda d: d["score"], reverse=True)`.
- **HuggingFace Dataset Mapping**: `dataset.map(lambda batch: tokenize(batch["text"]))` applies tokenization in parallel across dataset splits.
- **Gradient Accumulation**: `functools.reduce` is used to compute cumulative products of tensor dimensions or chain tensor transformations.

### Where It Appears in Real Projects
- HuggingFace `datasets.Dataset.map()`.
- Sorting vector search results in Milvus/ChromaDB clients.
- `functools.reduce(operator.mul, tensor.shape)` to calculate total tensor elements.

---

## 2. Core Concept

### 2.1 Lambda Functions
Syntax: `lambda arg1, arg2, ...: expression` (implicitly returns the expression result).

```python
# Sorting complex data structures
documents = [
    {"id": "doc_1", "score": 0.82},
    {"id": "doc_2", "score": 0.94},
    {"id": "doc_3", "score": 0.71},
]

# Sort descending by similarity score
documents.sort(key=lambda doc: doc["score"], reverse=True)
print("Top document:", documents[0]["id"])  # doc_2
```

### 2.2 Map and Filter
Both return lazy iterators in Python 3.

```python
embeddings = [0.12, -0.45, 0.99, -0.01]

# map: applies function to every element
abs_embeddings = list(map(abs, embeddings))

# filter: retains elements where predicate evaluates to True
positive_embeddings = list(filter(lambda x: x > 0, embeddings))
print("Positives:", positive_embeddings)  # [0.12, 0.99]
```

### 2.3 Reduce (`functools.reduce`)
Iteratively applies a function of two arguments to elements of a sequence, reducing the sequence to a single cumulative value.

```python
from functools import reduce
import operator

# Calculate total parameter count across layer dimensions:
layer_dims = [768, 12, 64]  # hidden_dim, num_heads, head_dim
total_elements = reduce(operator.mul, layer_dims)
print(f"Total elements: {total_elements}")  # 589824
```

---

## 3. Mental Model

```text
Map:    [ x1,    x2,    x3 ] ──► map(f)    ──► [ f(x1), f(x2), f(x3) ]
Filter: [ x1,    x2,    x3 ] ──► filter(p) ──► [ x1,          x3 ] (where p(x2) is False)
Reduce: [ x1,    x2,    x3 ] ──► reduce(f) ──► f(f(x1, x2), x3)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: RAG Document Re-Ranker with Score Cutoff
Filtering and sorting retrieved knowledge chunks using functional pipelines:

```python
from typing import List, Dict, Any

raw_chunks: List[Dict[str, Any]] = [
    {"text": "Attention mechanism computes alignment scores.", "sim": 0.89},
    {"text": "Python was released in 1991 by Guido van Rossum.", "sim": 0.42},
    {"text": "Transformer architecture dispenses with recurrence.", "sim": 0.95},
    {"text": "Cooking recipe for chocolate chip cookies.", "sim": 0.15},
]

# 1. Filter out low-similarity chunks (cutoff threshold = 0.70)
relevant_chunks = list(filter(lambda c: c["sim"] >= 0.70, raw_chunks))

# 2. Sort remaining chunks descending by similarity
ranked_chunks = sorted(relevant_chunks, key=lambda c: c["sim"], reverse=True)

for rank, chunk in enumerate(ranked_chunks, 1):
    print(f"Rank {rank} [Score: {chunk['sim']:.2f}]: {chunk['text']}")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Readability Degradation
Overly complex lambdas hinder maintainability. If a lambda requires multiple lines, condition checks, or complex logic, always refactor to a named `def` function.

### 2. Single-Pass Consumption of `map` and `filter`
`map` and `filter` return iterators. Once consumed, they cannot be re-iterated!

```python
m = map(lambda x: x*2, [1, 2, 3])
print(list(m))  # [2, 4, 6]
print(list(m))  # [] (Iterator is now exhausted!)
```

---

## 6. Interview Questions & Coding Traps

### Q1: What is the difference between `list.sort()` and `sorted()`?
- `list.sort()` mutates the list **in-place** and returns `None`. It is only available on list objects.
- `sorted(iterable)` accepts any iterable, leaves the original data untouched, and returns a **new sorted list**.

### Q2: How does `functools.reduce` behave when an empty sequence is passed?
If an empty sequence is passed without an initial value, `reduce` raises `TypeError: reduce() of empty sequence with no initial value`. Always provide an initializer: `reduce(fn, seq, initial_value)`.

### Complexity Reference
| Function | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| `lambda` evaluation | $O(1)$ | $O(1)$ |
| `map()` / `filter()` construction | $O(1)$ lazy iterator | $O(1)$ memory |
| `list(map(...))` | $O(N)$ | $O(N)$ |
| `reduce(...)` | $O(N)$ | $O(1)$ |
