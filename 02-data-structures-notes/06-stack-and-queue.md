# Stacks and Queues in Python

> Stacks enforce Last-In-First-Out (LIFO) access, while Queues enforce First-In-First-Out (FIFO) access; both represent fundamental constrained sequences for traversal, scheduling, and buffering.

---

## 1. Why This Matters

### Why This Concept Exists
Unconstrained lists allow arbitrary insertion and deletion at any index, which can introduce $O(N)$ memory-shifting penalties. Stacks and queues restrict access to collection endpoints, guaranteeing $O(1)$ performance.

### Why Python Developers Need It
Using a standard Python `list` as a FIFO queue (`pop(0)`) is one of the most common performance bugs in Python engineering, turning linear algorithms into quadratic disasters.

### Why It Matters Specifically in AI/ML/GenAI
- **Token Streaming Buffers**: Managing incoming tokens in sliding context windows and generation queues.
- **Asynchronous Task Scheduling**: Work queues distributing image rendering or inference requests across GPU workers.
- **Tree and Graph Search in Reasoning Models**: Depth-First Search (DFS via Stack) and Breadth-First Search (BFS via Queue) in Monte Carlo Tree Search (MCTS) algorithms powering reasoning models like OpenAI o1.

### Where It Appears in Real Projects
- Graph traversal in LangGraph state machines.
- Task queues in Celery and Ray (`ray.util.queue.Queue`).
- Sliding window KV-cache eviction queues in vLLM.

---

## 2. Core Concept

### 2.1 Stack (LIFO): Python `list`
Python lists are ideal for stacks because `append()` and `pop()` operate at the end of the array in $O(1)$ amortized time.

```python
stack = []
stack.append(10)  # Push
stack.append(20)
top = stack.pop() # Pop -> 20 (LIFO)
```

### 2.2 Queue (FIFO): `collections.deque`
A standard Python list performs `pop(0)` in $O(N)$ time. `collections.deque` is implemented as a **doubly linked list of fixed-size blocks**, allowing $O(1)$ insertions and pops at both ends.

```python
from collections import deque

queue = deque()
queue.append("task_1")     # Enqueue
queue.append("task_2")
first = queue.popleft()    # Dequeue -> 'task_1' in O(1) time!
```

### 2.3 Priority Queue: `heapq`
For queues ordered by priority (e.g., shortest job first, lowest loss):

```python
import heapq

pq = []
heapq.heappush(pq, (2, "medium_priority_task"))
heapq.heappush(pq, (1, "high_priority_task"))
heapq.heappush(pq, (3, "low_priority_task"))

# Always pops the item with smallest priority number
priority, task = heapq.heappop(pq)
print(f"Executing: {task} (Priority {priority})")  # high_priority_task
```

---

## 3. Mental Model

```text
Stack (LIFO - Stack of Plates):
Push ──► [ Item C ] ──► Pop (Top)
         [ Item B ]
         [ Item A ] (Bottom)

Queue (FIFO - Line at Coffee Shop):
Enqueue ──► [ Item C | Item B | Item A ] ──► Dequeue (Item A exits first)
(Rear)                                       (Front)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Sliding Context Window Token Buffer with `maxlen`
Using `collections.deque` with fixed `maxlen` to automatically evict oldest tokens when new tokens arrive:

```python
from collections import deque
from typing import List

class RollingContextBuffer:
    """Fixed-capacity sliding context buffer that discards oldest tokens automatically in O(1)."""
    def __init__(self, max_tokens: int) -> None:
        self.buffer: deque[str] = deque(maxlen=max_tokens)

    def add_tokens(self, new_tokens: List[str]) -> None:
        self.buffer.extend(new_tokens)

    def get_current_prompt(self) -> str:
        return " ".join(self.buffer)

buf = RollingContextBuffer(max_tokens=6)
buf.add_tokens(["User:", "Hello,", "how", "are", "you?"])
print("Buffer 1:", buf.get_current_prompt())

buf.add_tokens(["AI:", "I", "am", "doing", "well!"])
# Oldest tokens ("User:", "Hello,", etc.) automatically evicted!
print("Buffer 2:", buf.get_current_prompt())
# Buffer 2: are you? AI: I am doing
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Accidentally Using `list.pop(0)` for Queues
In a pipeline processing 100,000 items, `deque.popleft()` takes ~0.01 seconds, whereas `list.pop(0)` takes ~5 seconds!

### 2. Random Access in `deque` is $O(N)$
While `deque` provides $O(1)$ operations at endpoints, accessing middle elements (`deque[i]`) requires traversing pointers, taking $O(N)$ time. If frequent random indexing is required, use `list`.

---

## 6. Interview Questions & Coding Traps

### Q1: How do you implement a Queue using two Stacks?
```python
class QueueWithTwoStacks:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def pop(self) -> int:
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        if not self.out_stack:
            raise IndexError("pop from empty queue")
        return self.out_stack.pop()
```
**Complexity:** Amortized $O(1)$ per pop, $O(1)$ push.

### Complexity Reference
| Structure | Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| `list` (Stack) | `append()` / `pop()` | $O(1)$ amortized | $O(N)$ |
| `list` (Bad Queue) | `pop(0)` | $O(N)$ | $O(N)$ |
| `deque` (Queue) | `append()` / `popleft()` | $O(1)$ guaranteed | $O(N)$ |
| `heapq` (Priority) | `heappush()` / `heappop()` | $O(\log N)$ | $O(N)$ |
