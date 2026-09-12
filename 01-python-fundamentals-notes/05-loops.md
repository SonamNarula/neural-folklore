# Loops and Iteration in Python

> Loops execute repetitive sequences by repeatedly consuming items yielded by the iterator protocol.

---

## 1. Why This Matters

### Why This Concept Exists
Computation is fundamentally about repeating operations over datasets. Python implements iteration via a unified protocol (`__iter__` and `__next__`) rather than index-based pointer arithmetic.

### Why Python Developers Need It
Idiomatic looping (`enumerate`, `zip`, comprehensions) prevents off-by-one errors, bounds errors, and makes code declarative and readable.

### Why It Matters Specifically in AI/ML/GenAI
- **Training Epochs & Batches**: The foundation of deep learning is the nested loop: `for epoch in range(epochs): for batch in dataloader:`.
- **Dataset Streaming**: Iterating through multi-gigabyte datasets line-by-line or batch-by-batch without loading the entire corpus into RAM.
- **Autoregressive Token Generation**: LLM inference runs inside a `while` loop, predicting one token per iteration until an End-of-Sequence (`<EOS>`) token is generated or maximum context length is hit.

### Where It Appears in Real Projects
- Model training loops in PyTorch / JAX.
- Token generation loops in `vLLM` and HuggingFace `generate()`.
- Data transformation pipelines in PySpark and Ray.

---

## 2. Core Concept

### 2.1 For Loops & The Iterator Protocol
A `for` loop in Python does **not** count indices like in C; it requests an iterator via `iter(obj)` and repeatedly calls `next(it)` until `StopIteration` is raised.

```python
# Behind the scenes of: for x in [10, 20]:
items = [10, 20]
it = iter(items)
while True:
    try:
        x = next(it)
        print(x)
    except StopIteration:
        break
```

### 2.2 Built-in Iteration Helpers: `enumerate` and `zip`
```python
tokens = ["Attention", "is", "all", "you", "need"]
ids = [2048, 318, 477, 345, 761]

# enumerate gives (index, value) tuples
for idx, token in enumerate(tokens):
    print(f"Position {idx}: {token}")

# zip combines multiple iterables in lockstep
# zip(strict=True) in Python 3.10+ raises ValueError if lengths differ!
for token, token_id in zip(tokens, ids, strict=True):
    print(f"Token: {token:<12} ID: {token_id}")
```

### 2.3 The Loop `else` Clause
Python loops have an `else` block that executes **only if the loop terminated normally** (did NOT exit via `break`).

```python
# Search for target without boolean flags:
target = 42
numbers = [10, 20, 30, 42, 50]

for n in numbers:
    if n == target:
        print("Found target!")
        break
else:
    print("Target not found in list")
```

---

## 3. Mental Model

```text
The Iterator Protocol Machine:
Iterable (List / Tuple / File)
      │
      ▼  iter(obj)
┌─────────────────────────────────┐
│ Iterator Object                 │
│ Pointer: [ -> 10, 20, 30 ]      │
└─────────────────────────────────┘
      │
      ├─── next() ──► Yields 10
      ├─── next() ──► Yields 20
      ├─── next() ──► Yields 30
      └─── next() ──► Raises StopIteration (Loop cleanly terminates)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Autoregressive LLM Generation Loop with KV-Cache Simulation
Simulating an autoregressive token generation loop stopping on EOS or max tokens:

```python
from typing import List

class MockLLMEngine:
    def __init__(self, eos_token_id: int = 50256) -> None:
        self.eos_token_id: int = eos_token_id

    def forward(self, input_ids: List[int]) -> int:
        """Simulates next-token prediction."""
        last_token = input_ids[-1]
        # Deterministic dummy model: increments token or emits EOS after 5 steps
        if len(input_ids) >= 8:
            return self.eos_token_id
        return last_token + 1

def generate(engine: MockLLMEngine, prompt_ids: List[int], max_new_tokens: int = 10) -> List[int]:
    generated = list(prompt_ids)
    step = 0

    while step < max_new_tokens:
        next_token = engine.forward(generated)
        if next_token == engine.eos_token_id:
            print(f"Generation terminated on EOS token at step {step}")
            break
        generated.append(next_token)
        step += 1
    else:
        print(f"Generation reached max_new_tokens limit ({max_new_tokens})")

    return generated

engine = MockLLMEngine()
output = generate(engine, prompt_ids=[101, 102], max_new_tokens=10)
print(f"Generated sequence: {output}")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Modifying a List While Iterating Over It
Never add or remove elements from a list while iterating over it directly. This shifts internal indices and skips elements silently!

```python
# BUG: Modifying list during iteration
nums = [1, 2, 2, 3]
for n in nums:
    if n == 2:
        nums.remove(n)
print(nums)  # [1, 2, 3] -> Second '2' was SKIPPED because index shifted!

# CORRECT: List comprehension or iterate over a shallow slice copy
nums = [1, 2, 2, 3]
nums = [n for n in nums if n != 2]
print(nums)  # [1, 3]
```

---

## 6. Interview Questions & Coding Traps

### Q1: What is the time complexity of looping over a list of size $N$ and calling `list.pop(0)` each iteration?
$O(N^2)$.
**Explanation:** `pop(0)` removes the first element and shifts all remaining $N-1$ elements in memory one slot to the left. Doing this $N$ times results in $\sum_{i=1}^N i = O(N^2)$. Use `collections.deque` with `popleft()` for $O(N)$ total time ($O(1)$ amortized per pop).

### Q2: What is the output of this code?
```python
for i in range(3):
    if i == 5:
        break
else:
    print("Completed without break")
```
**Output:** `"Completed without break"`
**Explanation:** The loop finished iterating through `[0, 1, 2]` without encountering a `break` statement, so the `else` block executed.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| `for x in list` traversal | $O(N)$ | $O(1)$ |
| `enumerate(list)` | $O(N)$ | $O(1)$ |
| `zip(list1, list2)` | $O(\min(N, M))$ | $O(1)$ |
