# Algorithmic Patterns and Basic Problems

> Algorithmic patterns are reusable structural strategies (Two Pointers, Sliding Window, Frequency Hashing) that reduce brute-force time complexities from $O(N^2)$ to $O(N)$.

---

## 1. Why This Matters

### Why This Concept Exists
Raw syntax is useless without structured algorithmic techniques. Algorithmic patterns provide standardized templates to solve complex data manipulation problems efficiently.

### Why Python Developers Need It
Coding interviews at top-tier companies (Google, Meta, OpenAI, Anthropic) evaluate candidates on their ability to recognize these patterns and write clean, bug-free implementations in Python.

### Why It Matters Specifically in AI/ML/GenAI
- **Context Window Truncation (Sliding Window)**: Managing conversation history or chunking documents for RAG within token limits requires sliding window algorithms.
- **Top-K Vector Search Filtering**: Fast candidate retrieval and vocabulary ranking rely on heap/hash patterns.
- **Data Deduplication**: Preprocessing multi-terabyte web crawls (e.g., Common Crawl for LLM training) requires two-pointer merging and frequency maps.

### Where It Appears in Real Projects
- Fixed-size token chunkers for document embedding pipelines.
- Deduplicating training datasets via min-hashing / sliding n-grams.
- Online streaming metric computation (e.g., moving average loss).

---

## 2. Core Concept: The 3 Foundational Patterns

### 2.1 Two-Pointer Technique
Used on sorted arrays or sequences to find pairs, partitions, or palindromes in $O(N)$ time and $O(1)$ space.

```python
def two_sum_sorted(arr: list[int], target: int) -> tuple[int, int] | None:
    left, right = 0, len(arr) - 1
    while left < right:
        current = arr[left] + arr[right]
        if current == target:
            return (left, right)
        elif current < target:
            left += 1
        else:
            right -= 1
    return None
```

### 2.2 Sliding Window Pattern
Maintains a contiguous window over a sequence to optimize subarray/substring queries from $O(N \cdot K)$ to $O(N)$.

```python
def max_subsequence_sum(nums: list[int], k: int) -> int:
    if len(nums) < k:
        return 0
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

### 2.3 Frequency Hashing Pattern
Uses hash maps (`collections.Counter` or `dict`) to track item occurrences in $O(1)$ lookup time.

```python
from collections import Counter

def find_majority_token(tokens: list[int]) -> int:
    counts = Counter(tokens)
    return counts.most_common(1)[0][0]
```

---

## 3. Mental Model

```text
Two Pointers (Inward Convergence):
[ 1,  3,  5,  7,  11,  15 ]     Target = 16
  ▲                     ▲
left                  right     Sum = 1 + 15 = 16 -> MATCH!

Sliding Window (Fixed Width k=3):
Step 1: [ 2, 4, 6 ], 1, 9   Sum = 12
Step 2: 2, [ 4, 6, 1 ], 9   Sum = 12 - 2 + 1 = 11 (O(1) update!)
Step 3: 2, 4, [ 6, 1, 9 ]   Sum = 11 - 4 + 9 = 16 (O(1) update!)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Sliding Window Document Chunker with Overlap
A production-grade text chunker used for RAG embeddings generation:

```python
from typing import List

def chunk_text_sliding_window(
    tokens: List[str],
    chunk_size: int = 100,
    chunk_overlap: int = 20
) -> List[List[str]]:
    """
    Chunks token lists into overlapping segments for RAG embeddings.
    Stride = chunk_size - chunk_overlap.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be strictly less than chunk_size")

    stride = chunk_size - chunk_overlap
    chunks = []

    for i in range(0, len(tokens), stride):
        chunk = tokens[i : i + chunk_size]
        chunks.append(chunk)
        if i + chunk_size >= len(tokens):
            break

    return chunks

doc_tokens = [f"tok_{i}" for i in range(250)]
chunks = chunk_text_sliding_window(doc_tokens, chunk_size=100, chunk_overlap=25)
print(f"Total chunks created: {len(chunks)}")
print(f"Chunk 0 length: {len(chunks[0])}, Chunk 1 length: {len(chunks[1])}")
print(f"Overlap tokens: {chunks[0][-25:] == chunks[1][:25]}")  # True
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Off-by-One in Stride Calculation
When `chunk_overlap >= chunk_size`, `stride <= 0`, causing an **infinite loop**! Always enforce strict validation assertions.

### 2. Empty or Undersized Inputs
Handling edge cases where sequence length is smaller than window size $K$:
```python
if len(sequence) < window_size:
    return [sequence] if sequence else []
```

---

## 6. Interview Questions & Coding Traps

### Q1: Given a list of integers, reverse it in-place using $O(1)$ extra space.
```python
def reverse_in_place(arr: list[int]) -> None:
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```
**Complexity:** Time: $O(N)$, Space: $O(1)$.

### Q2: What is the optimal time complexity to check if two strings are anagrams?
$O(N)$ time and $O(1)$ space (since the alphabet size is bounded to 26 lowercase ASCII or 256 byte characters). In Python, `collections.Counter(s1) == collections.Counter(s2)` runs in $O(N)$ time.

### Complexity Reference
| Pattern | Typical Time Complexity | Typical Space Complexity |
| :--- | :--- | :--- |
| Two Pointers | $O(N)$ | $O(1)$ |
| Sliding Window | $O(N)$ | $O(K)$ or $O(1)$ |
| Frequency Hash Map | $O(N)$ | $O(U)$ where $U$ is unique elements |
