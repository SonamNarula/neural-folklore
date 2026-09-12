# NumPy and the ndarray Architecture

> An `ndarray` is a contiguous block of homogeneous memory wrapped with metadata (shape, strides, dtype) that enables hardware-accelerated SIMD numerical computing.

---

## 1. Why This Matters

### Why This Concept Exists
Python lists store pointers to scattered heap objects, suffering from cache misses, pointer indirection, and object overhead (~8 bytes per pointer + ~28 bytes per integer). NumPy bypasses the Python heap, packing raw numerical bytes into contiguous hardware arrays.

### Why Python Developers Need It
NumPy is the foundational substrate of all numerical, scientific, and machine learning computing in Python. PyTorch, TensorFlow, Pandas, and Scikit-Learn are all built on NumPy's memory model.

### Why It Matters Specifically in AI/ML/GenAI
- **Dense Vector Embeddings**: Document embeddings (e.g., 1536-dimensional vectors from OpenAI or 768-dim from BERT) are stored and manipulated as NumPy arrays or PyTorch tensors.
- **Weights & Activations**: Neural network weights are multi-dimensional arrays of homogeneous floats (`float32`, `float16`, `bfloat16`).
- **Zero-Copy Memory Interop**: NumPy arrays share underlying memory buffers directly with PyTorch tensors (`torch.from_numpy(arr)`).

### Where It Appears in Real Projects
- Ingestion pipelines converting image pixels into tensors.
- Cosine similarity calculations in vector search.
- Token probability distribution softmax calculations.

---

## 2. Core Concept

### 2.1 Anatomy of an `ndarray`
A NumPy array consists of:
1. **Data Buffer**: A raw, contiguous block of C/Fortran memory holding values.
2. **dtype**: Data type describing byte size and interpretation (e.g., `float32` = 4 bytes IEEE float).
3. **shape**: Tuple defining dimensions (e.g., `(3, 4)` = 3 rows, 4 columns).
4. **strides**: Tuple of byte steps needed to jump to the next element along each dimension!

```python
import numpy as np

# Allocate a 2D array of 32-bit floats
arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=np.float32)

print("Shape:", arr.shape)          # (2, 3)
print("Dtype:", arr.dtype)          # float32 (4 bytes per element)
print("Item size:", arr.itemsize)    # 4 bytes
print("Strides:", arr.strides)      # (12, 4) -> Jump 12 bytes for next row, 4 bytes for next col!
```

### 2.2 Memory Layout: C-Order vs Fortran-Order
- **C-Contiguous** (Row-Major, default): Successive elements of a row are adjacent in memory.
- **Fortran-Contiguous** (Column-Major): Successive elements of a column are adjacent in memory.
Iterating along contiguous strides utilizes hardware CPU L1/L2 cache lines efficiently.

---

## 3. Mental Model

```text
Python List of Ints (Pointer Indirection):
List: [ Ptr 0 | Ptr 1 | Ptr 2 ]
          │       │       │
          ▼       ▼       ▼
       Heap:   Heap:   Heap:
       [28B]   [28B]   [28B]  (Scattered in RAM -> Cache Misses!)

NumPy ndarray (Contiguous Memory Buffer):
Buffer: [ 01 00 00 00 | 02 00 00 00 | 03 00 00 00 ] (Packed 4-byte ints in CPU Cache line!)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Fast Cosine Similarity Matrix for Embeddings
Computing pairwise cosine similarity between query embeddings and a corpus matrix:

```python
import numpy as np

def cosine_similarity_matrix(query_vec: np.ndarray, doc_matrix: np.ndarray) -> np.ndarray:
    """
    Computes cosine similarity between a 1D query vector and a 2D document matrix.
    Cosine Similarity = (A . B) / (||A|| * ||B||)
    """
    # 1. Compute dot product (Numerator)
    dot_products = np.dot(doc_matrix, query_vec)

    # 2. Compute L2 norms (Denominator)
    query_norm = np.linalg.norm(query_vec)
    doc_norms = np.linalg.norm(doc_matrix, axis=1)

    # 3. Normalized similarity scores
    return dot_products / (query_norm * doc_norms + 1e-9)

# Simulation: 100 documents with 4-dimensional embeddings
np.random.seed(42)
corpus = np.random.randn(100, 4).astype(np.float32)
query = np.array([0.5, -0.2, 0.8, 0.1], dtype=np.float32)

scores = cosine_similarity_matrix(query, corpus)
top_idx = np.argmax(scores)
print(f"Top matching document index: {top_idx} with score: {scores[top_idx]:.4f}")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. View vs Copy
Slicing a NumPy array returns a **view** (shared memory buffer), NOT a copy!

```python
orig = np.array([10, 20, 30])
view_slice = orig[:2]
view_slice[0] = 999
print(orig)  # [999, 20, 30] -> Original array was mutated!

# FIX: Explicitly call .copy() if isolation is required:
safe_copy = orig[:2].copy()
```

### 2. Silent Type Casting (Downcasting Overflow)
```python
x = np.array([255, 256], dtype=np.uint8)
print(x)  # [255, 0] -> 256 overflowed to 0 silently!
```

---

## 6. Interview Questions & Coding Traps

### Q1: What are array strides and why are they important?
Strides are a tuple of integers specifying how many bytes to step in memory to advance by one index along each dimension. Strides allow operations like transposing (`arr.T`) or reshaping to occur in $O(1)$ constant time without moving or copying any data in memory—NumPy simply adjusts the strides and shape metadata!

### Q2: What is the output of `np.array([1, 2, "3"])`?
`array(['1', '2', '3'], dtype='<U21')`.
**Explanation:** NumPy arrays must be homogeneous. It automatically upcasts all elements to the lowest common denominator type (string).

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Slicing `arr[i:j]` | $O(1)$ (metadata view) | $O(1)$ |
| Reshaping `arr.reshape(...)` | $O(1)$ (stride update) | $O(1)$ |
| Transposing `arr.T` | $O(1)$ (stride swap) | $O(1)$ |
| Element-wise Math `arr1 + arr2` | $O(N)$ SIMD parallel | $O(N)$ new array |
