# Shallow vs Deep Copy in Python

> Assignment creates an alias to the same object; a shallow copy creates a new container populated with references to original items; a deep copy recursively duplicates the container and all nested objects.

---

## 1. Why This Matters

### Why This Concept Exists
Nested data structures (lists of dicts, matrices, tree nodes) require distinct copying semantics depending on whether internal elements should be shared or completely isolated.

### Why Python Developers Need It
Accidentally modifying shared nested state across cloned objects is one of the most insidious bugs in Python software engineering.

### Why It Matters Specifically in AI/ML/GenAI
- **Cloning Model Checkpoints**: Deep-copying model weights when maintaining an exponential moving average (EMA) model during training.
- **Agentic Conversation Branching**: Forking a conversation tree to explore alternative LLM reasoning branches without corrupting the primary history.
- **Hyperparameter Grid Exploration**: Cloning configuration dictionaries before applying mutations.

### Where It Appears in Real Projects
- `copy.deepcopy(model)` in EMA weight trackers.
- Monte Carlo Tree Search (MCTS) tree state branching.
- Prompt variation testing harnesses.

---

## 2. Core Concept

### 2.1 The Three Copy Levels
1. **Assignment (`b = a`)**: No copy. Creates a second pointer to the exact same object.
2. **Shallow Copy (`copy.copy(a)` or `a.copy()` or `a[:]`)**: Allocates a new outer container, but inserts references to the original nested objects.
3. **Deep Copy (`copy.deepcopy(a)`)**: Recursively copies the outer container and all nested child objects.

```python
import copy

original = [[1, 2], [3, 4]]

# 1. Assignment
alias = original

# 2. Shallow Copy
shallow = copy.copy(original)

# 3. Deep Copy
deep = copy.deepcopy(original)

# Mutate nested element:
original[0][0] = 999

print("Original:", original)  # [[999, 2], [3, 4]]
print("Alias:   ", alias)     # [[999, 2], [3, 4]] (Aliased!)
print("Shallow: ", shallow)   # [[999, 2], [3, 4]] (Nested list was shared!)
print("Deep:    ", deep)      # [[1, 2], [3, 4]]   (Completely isolated!)
```

---

## 3. Mental Model

```text
Memory Architecture:
Original:  [ Ptr A | Ptr B ] ──► Ptr A points to [ 1, 2 ]
                 ▲
Shallow:   [ Ptr A | Ptr B ] (New outer list, but Ptr A points to SAME inner list!)

Deep:      [ Ptr X | Ptr Y ] ──► Ptr X points to NEW [ 1, 2 ] (Completely isolated copy!)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Model Weights Exponential Moving Average (EMA) Tracker
Deep-copying weights to maintain a smoothed EMA shadow model:

```python
import copy
from typing import Dict, Any

class EMAModelTracker:
    """Maintains Exponential Moving Average of model parameters."""
    def __init__(self, model_weights: Dict[str, list[float]], decay: float = 0.999) -> None:
        self.decay = decay
        # Deep copy ensures shadow weights are completely decoupled from model
        self.shadow_weights: Dict[str, list[float]] = copy.deepcopy(model_weights)

    def update(self, current_weights: Dict[str, list[float]]) -> None:
        for name, current_vals in current_weights.items():
            shadow_vals = self.shadow_weights[name]
            for i in range(len(shadow_vals)):
                # Shadow = decay * Shadow + (1 - decay) * Current
                shadow_vals[i] = (self.decay * shadow_vals[i]) + ((1.0 - self.decay) * current_vals[i])

weights = {"layer1": [1.0, 2.0], "layer2": [0.5, -0.5]}
ema = EMAModelTracker(weights, decay=0.9)
# Mutating original weights does NOT affect shadow weights:
weights["layer1"][0] = 5.0
ema.update(weights)
print("Updated Shadow Weights:", ema.shadow_weights)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. `copy.deepcopy()` on PyTorch Tensors
Calling `copy.deepcopy()` on PyTorch tensors or models duplicates autograd graphs and underlying CUDA buffers, which can cause severe VRAM bloat and performance slowdowns. In PyTorch, use `tensor.clone().detach()` for tensor isolation!

### 2. Infinite Recursion in Cyclic Objects
`copy.deepcopy()` maintains an internal memo dictionary (`memo={}`) to track already-copied object IDs, automatically preventing infinite loops on cyclical graphs.

---

## 6. Interview Questions & Coding Traps

### Q1: How do you implement custom copying logic on a class?
Implement `__copy__(self)` for shallow copying and `__deepcopy__(self, memo)` for deep copying.

### Complexity Reference
| Strategy | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Assignment (`b = a`) | $O(1)$ | $O(1)$ |
| Shallow Copy (`copy.copy`) | $O(K)$ outer elements | $O(K)$ new container |
| Deep Copy (`copy.deepcopy`) | $O(N)$ full graph traversal | $O(N)$ complete object duplication |
