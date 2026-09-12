# NumPy Indexing, Broadcasting, and Vectorization

> Vectorization replaces explicit Python loops with C-level SIMD instructions; broadcasting automatically stretches smaller arrays across larger dimensions without memory replication.

---

## 1. Why This Matters

### Why This Concept Exists
Standard Python loops over millions of elements are notoriously slow due to interpreter overhead, dynamic type checking, and pointer dereferencing on every cycle. Vectorization executes array operations directly in compiled C loops utilizing CPU SIMD (Single Instruction, Multiple Data) registers.

### Why Python Developers Need It
Writing vectorized code speeds up numerical operations by 100x to 1000x and produces cleaner, more declarative code.

### Why It Matters Specifically in AI/ML/GenAI
- **Batch Loss Computation**: Computing cross-entropy loss across mini-batches of 1024 samples simultaneously.
- **Attention Masking**: Applying causal or padding masks via boolean indexing: `scores[mask == 0] = -1e9`.
- **Broadcasting Bias Vectors**: Adding a 1D bias vector of shape `(hidden_dim,)` to a 3D activation tensor of shape `(batch, seq_len, hidden_dim)`.

### Where It Appears in Real Projects
- Multi-head attention implementations.
- Feature scaling (subtracting column means and dividing by standard deviation).
- Image pixel normalization in computer vision.

---

## 2. Core Concept

### 2.1 The Broadcasting Rules
NumPy compares shapes element-wise from **right to left** (trailing dimensions first). Two dimensions are compatible if:
1. They are equal, OR
2. One of them is 1 (the dimension with 1 is virtually stretched to match the larger dimension).

```python
import numpy as np

A = np.ones((4, 1, 6))
B = np.ones((3, 6))
# Trailing: 6 == 6 (Compatible)
# Next:     1 vs 3 (Compatible -> stretched to 3)
# Leading:  4 vs None (Compatible -> stretched to 4)
C = A + B
print("Broadcasted Shape:", C.shape)  # (4, 3, 6)
```

### 2.2 Boolean Masking & Fancy Indexing
- **Boolean Masking**: Filter arrays using boolean conditions (returns 1D array of matching values).
- **Fancy Indexing**: Select elements using integer index arrays (always returns a copy).

```python
vals = np.array([10, -5, 20, -1, 30])

# Boolean mask:
positives = vals[vals > 0]
print("Positives:", positives)  # [10, 20, 30]

# Replace negatives with 0 (ReLU simulation):
vals[vals < 0] = 0
print("ReLU result:", vals)      # [10, 0, 20, 0, 30]
```

---

## 3. Mental Model

```text
Broadcasting in Action:
Matrix (3, 3)          Vector (1, 3)          Broadcast Result (3, 3)
[ 1, 2, 3 ]            [ 10, 20, 30 ]         [ 11, 22, 33 ]
[ 4, 5, 6 ]     +      (virtually copied) ──► [ 14, 25, 36 ]
[ 7, 8, 9 ]            [ 10, 20, 30 ]         [ 17, 28, 39 ]
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Numerically Stable Softmax Implementation
Computing the softmax activation across logits with numerical stabilization to prevent exponential overflow:

```python
import numpy as np

def stable_softmax(logits: np.ndarray, axis: int = -1) -> np.ndarray:
    """
    Computes numerically stable softmax using broadcasting.
    Subtracts max(logits) to prevent exp() floating-point overflow.
    Softmax(x_i) = exp(x_i - max(x)) / sum(exp(x_j - max(x)))
    """
    # Keepdims=True ensures shape compatibility for broadcasting
    max_val = np.max(logits, axis=axis, keepdims=True)
    exp_logits = np.exp(logits - max_val)
    sum_exp = np.sum(exp_logits, axis=axis, keepdims=True)
    return exp_logits / sum_exp

# Simulation: Batch of 2 samples, 4 class probabilities
sample_logits = np.array([
    [1000.0, 1002.0, 1001.0, 999.0],  # Naive np.exp() would overflow to infinity!
    [1.0, 2.0, 3.0, 4.0]
], dtype=np.float32)

probs = stable_softmax(sample_logits, axis=-1)
print("Probabilities Shape:", probs.shape)
print("Sample 0 Probs Sum:", np.sum(probs[0]))  # 1.0
print("Sample 0 Probabilities:
", probs[0])
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Incompatible Broadcasting Dimensions
Attempting to broadcast `(3, 4)` and `(3,)` fails because trailing dimensions `4` and `3` do not match!
```python
# BUG:
# np.ones((3, 4)) + np.ones((3,)) -> ValueError: operands could not be broadcast together

# FIX: Add dimension via np.newaxis or None:
res = np.ones((3, 4)) + np.ones((3, 1))  # Valid! Broadcasts to (3, 4)
```

---

## 6. Interview Questions & Coding Traps

### Q1: What is the difference between `arr[1:3]` and `arr[[1, 2]]`?
- `arr[1:3]` is basic slicing and returns a **view** sharing the underlying memory buffer.
- `arr[[1, 2]]` is **fancy indexing** with an integer array and **always returns a memory copy**.

### Q2: How do you vectorize a loop that computes pairwise Euclidean distances between two sets of vectors $X \in \mathbb{R}^{M 	imes D}$ and $Y \in \mathbb{R}^{N 	imes D}$?
Use broadcasting by expanding dimensions:
```python
# (M, 1, D) - (1, N, D) broadcasts to (M, N, D)
dists = np.sqrt(np.sum((X[:, np.newaxis, :] - Y[np.newaxis, :, :]) ** 2, axis=-1))
```

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Slicing View | $O(1)$ | $O(1)$ |
| Fancy Indexing | $O(K \cdot D)$ | $O(K \cdot D)$ copy |
| Vectorized Element-wise Math | $O(N)$ SIMD parallel | $O(N)$ |
| Broadcasting Memory Overhead | $O(1)$ (no memory copied for broadcasted dimensions) | $O(1)$ |
