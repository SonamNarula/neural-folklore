# Recursion in Python

> Recursion is an algorithmic strategy where a function solves a problem by calling copies of itself on smaller sub-problems until reaching a base condition.

---

## 1. Why This Matters

### Why This Concept Exists
Hierarchical data structures (trees, graphs, JSON payloads, ASTs) are recursive by nature. Recursive functions mirror the structural induction of these data representations.

### Why Python Developers Need It
While recursion is conceptually elegant, CPython does **not** optimize tail-calls. Understanding recursion stack overhead and knowing when to convert to iterative stacks is a crucial engineering skill.

### Why It Matters Specifically in AI/ML/GenAI
- **Decision Trees & Random Forests**: Traversing decision tree nodes during inference is naturally modeled recursively.
- **Nested JSON Document Parsing**: Extracting text blocks and metadata from complex nested API outputs or web-scraped JSON structures.
- **Tree-of-Thought (ToT) / MCTS**: Advanced LLM reasoning architectures explore branching thought paths recursively.

### Where It Appears in Real Projects
- AST visitor patterns in code generation and analysis.
- Decision tree traversal in Scikit-Learn.
- Recursive character text splitters in LangChain.

---

## 2. Core Concept

### 2.1 Anatomy of a Recursive Function
1. **Base Case**: The termination condition that returns a value directly without recursing.
2. **Recursive Case**: Breaking the input into smaller sub-problems and calling self.

```python
def factorial(n: int) -> int:
    # 1. Base case
    if n <= 1:
        return 1
    # 2. Recursive case
    return n * factorial(n - 1)
```

### 2.2 Recursion Limit in Python
CPython allocates a new stack frame on the C call stack for every recursive call. To prevent OS segmentation faults, Python sets a hard limit:

```python
import sys
print(sys.getrecursionlimit())  # Typically 1000 frames
# sys.setrecursionlimit(2000)   # Can be adjusted, but risks stack overflow crashes
```

---

## 3. Mental Model

```text
Call Stack Unwinding (factorial(3)):
Push: factorial(3) ──► 3 * factorial(2)
Push:   factorial(2) ──► 2 * factorial(1)
Push:     factorial(1) ──► Returns 1 (Base Case reached!)
Pop:    factorial(2) evaluates: 2 * 1 = 2
Pop:  factorial(3) evaluates: 3 * 2 = 6
Result: 6
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Recursive Nested JSON Document Text Extractor
Extracting all text chunks from deeply nested RAG payloads (dicts, lists, primitives):

```python
from typing import Any, List

def extract_text_chunks_recursive(node: Any) -> List[str]:
    """Recursively walks arbitrary nested JSON structures to extract text blocks."""
    chunks: List[str] = []

    if isinstance(node, str):
        cleaned = node.strip()
        if cleaned:
            chunks.append(cleaned)
    elif isinstance(node, dict):
        for val in node.values():
            chunks.extend(extract_text_chunks_recursive(val))
    elif isinstance(node, (list, tuple)):
        for item in node:
            chunks.extend(extract_text_chunks_recursive(item))

    return chunks

nested_payload = {
    "title": "LLM Architecture",
    "sections": [
        {"header": "Attention", "content": ["Self-attention is key.", "Multi-head expands capacity."]},
        {"header": "FeedForward", "content": "Applies non-linear transformations."}
    ],
    "metadata": {"author": "AI Researcher"}
}

extracted = extract_text_chunks_recursive(nested_payload)
print(f"Extracted {len(extracted)} text chunks:", extracted)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. No Tail-Call Optimization (TCO)
Unlike Scheme, Scala, or ES6, Python does **not** optimize tail calls. A tail-recursive function consumes $O(N)$ stack frames and will overflow at ~1000 calls. Convert deep recursions to iterative loops with explicit stacks!

### 2. Missing Base Case
Forgetting or misconfiguring base cases results in `RecursionError: maximum recursion depth exceeded`.

---

## 6. Interview Questions & Coding Traps

### Q1: How do you eliminate recursion to avoid stack overflow?
Use an **explicit iterative stack** stored on the heap:
```python
def dfs_iterative(root):
    if not root:
        return
    stack = [root]
    while stack:
        node = stack.pop()
        print(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
```

### Q2: What is the time and space complexity of naive recursive Fibonacci vs memoized Fibonacci?
- Naive: Time $O(2^N)$ (exponential branching), Space $O(N)$ (call stack depth).
- Memoized (`@functools.lru_cache`): Time $O(N)$, Space $O(N)$.

### Complexity Reference
| Recursion Pattern | Time Complexity | Call Stack Space |
| :--- | :--- | :--- |
| Single Recursion (Linear) | $O(N)$ | $O(N)$ |
| Tree / Binary Recursion | $O(2^N)$ | $O(N)$ (height of tree) |
| Divide & Conquer (e.g. MergeSort) | $O(N \log N)$ | $O(\log N)$ |
