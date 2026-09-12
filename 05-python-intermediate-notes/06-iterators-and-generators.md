# Iterators and Generators in Python

> An iterator is a stateful object advancing through a sequence via `__next__()`; a generator is a function that lazily yields values on-demand, suspending its execution frame between calls.

---

## 1. Why This Matters

### Why This Concept Exists
Generating and holding a billion elements in RAM consumes gigabytes of memory and halts execution. Lazy streams compute each item on-the-fly, allowing infinite or massive sequences with $O(1)$ memory consumption.

### Why Python Developers Need It
Generators and the iterator protocol power Python's data pipelines, file streaming, and streaming responses from LLMs.

### Why It Matters Specifically in AI/ML/GenAI
- **PyTorch Training Batch Streaming**: Deep learning datasets never load entire corpora into RAM; `DataLoader` instances are generators that yield mini-batches on-the-fly.
- **LLM Token Streaming**: When ChatGPT or Claude streams tokens in real-time, the backend API client yields tokens lazily as they arrive over HTTP SSE chunks.
- **Infinite Data Augmentation**: Training loops running for arbitrary epochs consume infinite generator pipelines of augmented images or synthetic prompts.

### Where It Appears in Real Projects
- Custom PyTorch `IterableDataset`.
- Streaming responses in OpenAI SDK (`stream=True`).
- Preprocessing pipelines in Apache Beam and Ray.

---

## 2. Core Concept

### 2.1 The Iterator Protocol
To be an iterator, an object must implement:
1. `__iter__()`: Returns `self`.
2. `__next__()`: Returns the next value in the sequence, or raises `StopIteration` when exhausted.

```python
class CountDown:
    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val

for num in CountDown(3):
    print(num)  # 3, 2, 1
```

### 2.2 Generators and the `yield` Keyword
Any function containing the `yield` keyword is compiled into a **generator function**. When called, it does not execute the body; it returns a generator object.

```python
def fibonacci_stream():
    a, b = 0, 1
    while True:  # Infinite generator! O(1) memory!
        yield a
        a, b = b, a + b

gen = fibonacci_stream()
for _ in range(5):
    print(next(gen), end=" ")  # 0 1 1 2 3
print()
```

### 2.3 Sub-Generators: `yield from`
Delegates iteration to a sub-generator or iterable:

```python
def multi_source_stream(source_a, source_b):
    yield from source_a  # Efficiently delegates yielding
    yield from source_b
```

---

## 3. Mental Model

```text
Standard Function vs Generator:
def standard():            def generator():
    return val                 yield val_1  <-- Frame suspended in heap!
    (Frame destroyed)          ...
                               yield val_2  <-- Resumes from exact line!
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Streaming LLM Token Decoder with Stop Sequences
Consuming an asynchronous or synchronous token stream and halting when a custom stop token is encountered:

```python
from typing import Generator, List

def mock_llm_token_stream() -> Generator[str, None, None]:
    tokens = ["Deep", " ", "learning", " ", "transforms", " ", "NLP", ".", "<STOP>", "Extra", "tokens"]
    for t in tokens:
        yield t

def stream_with_stop_sequence(
    token_stream: Generator[str, None, None],
    stop_words: List[str]
) -> Generator[str, None, None]:
    """Yields tokens until a stop token is detected, then cleanly terminates."""
    for token in token_stream:
        if token in stop_words:
            print(f"
[Detected stop sequence '{token}' -> Halting stream]")
            return
        yield token

# Consumer:
stream = stream_with_stop_sequence(mock_llm_token_stream(), stop_words=["<STOP>"])
for chunk in stream:
    print(chunk, end="", flush=True)
print()
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Iterators are Single-Use (Exhaustion Trap)
Once an iterator or generator raises `StopIteration`, it is permanently exhausted. Iterating over it a second time yields zero elements!

```python
gen = (x**2 for x in [1, 2, 3])
print(list(gen))  # [1, 4, 9]
print(list(gen))  # [] (Exhausted!)
```

### 2. Returning Values from Generators
In Python 3.3+, `return value` inside a generator raises `StopIteration(value)`. The return value is attached to the exception and can only be captured via `yield from`.

---

## 6. Interview Questions & Coding Traps

### Q1: What is the memory complexity difference between a list comprehension and a generator expression?
- List comprehension `[x for x in range(N)]`: Allocates $O(N)$ heap memory to store all pointers simultaneously.
- Generator expression `(x for x in range(N))`: Consumes $O(1)$ constant memory, computing each item only when requested.

### Q2: What are generator `.send()`, `.throw()`, and `.close()` methods?
Generators are full coroutines:
- `gen.send(value)`: Resumes generator execution and sends a value into the `yield` expression (`received = yield`).
- `gen.throw(type)`: Raises an exception inside the generator at the point of suspension.
- `gen.close()`: Raises `GeneratorExit` inside the generator to trigger cleanup blocks.

### Complexity Reference
| Structure | Time Complexity (Per Item) | Space Complexity |
| :--- | :--- | :--- |
| Iterator `next(it)` | $O(1)$ | $O(1)$ |
| Generator `yield` | $O(1)$ | $O(1)$ frame suspension |
