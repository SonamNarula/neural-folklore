# Conditionals and Control Flow in Python

> Conditionals govern program branching by evaluating expressions against truthiness protocols or structural patterns.

---

## 1. Why This Matters

### Why This Concept Exists
Deterministic execution paths must respond dynamically to external data, validation constraints, and system state. Control flow allows conditional branch dispatching.

### Why Python Developers Need It
Clean conditional structures eliminate deeply nested "arrow code", improve readability, and prevent runtime crashes caused by unhandled states.

### Why It Matters Specifically in AI/ML/GenAI
- **LLM Tool Calling & Routing**: When an agentic LLM outputs a tool call (e.g., `{"name": "search_database", "args": {...}}`), Python conditional dispatchers map the structured output to executable functions.
- **Model Checkpoint Routing**: Branching logic manages resuming training from checkpoints, saving best weights on validation improvement, and triggering early stopping.
- **Device Placement**: Directing tensor computation dynamically: `device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"`.

### Where It Appears in Real Projects
- Agentic execution loops in LangGraph, CrewAI, AutoGen.
- Early stopping callbacks during model training.
- Dynamic learning rate scheduler branching.

---

## 2. Core Concept

### 2.1 Standard If-Elif-Else & Ternary Operator
```python
# Ternary operator (inline conditional expression)
device = "cuda" if is_gpu_available else "cpu"

# Guard Clause Pattern (Fail Fast)
def process_batch(batch):
    if not batch:
        return None
    if len(batch) > 1024:
        raise ValueError("Batch size exceeds maximum VRAM limit")
    return [x * 2 for x in batch]
```

### 2.2 Structural Pattern Matching (`match / case` in Python 3.10+)
`match / case` provides structural pattern matching, inspecting both the value and the shape of data structures.

```python
def parse_agent_action(action: dict) -> str:
    match action:
        case {"type": "tool", "name": "search", "query": str(q)}:
            return f"Executing search for: {q}"
        case {"type": "tool", "name": "calc", "expression": str(expr)}:
            return f"Computing math: {expr}"
        case {"type": "final_answer", "text": str(ans)}:
            return f"Returning final response: {ans}"
        case {"type": "error", "code": int(code), "details": details}:
            return f"Handling error code {code}: {details}"
        case _:
            return "Unknown agent action schema"
```

---

## 3. Mental Model

```text
Guard Clause Pipeline:
Input ──► [ Is Valid? ] ──NO──► Return Error / Early Exit
               │ YES
               ▼
          [ In Limits? ] ──NO──► Raise Exception
               │ YES
               ▼
          Process Happy Path
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Early Stopping Controller for Deep Learning
A production-ready early stopping monitor tracking validation loss:

```python
class EarlyStopping:
    """Monitors validation loss to halt training when convergence plateaus."""
    def __init__(self, patience: int = 5, min_delta: float = 1e-4) -> None:
        self.patience: int = patience
        self.min_delta: float = min_delta
        self.best_loss: float = float("inf")
        self.counter: int = 0
        self.should_stop: bool = False

    def step(self, val_loss: float) -> bool:
        if val_loss < (self.best_loss - self.min_delta):
            self.best_loss = val_loss
            self.counter = 0  # Reset patience counter
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
        return self.should_stop

stopper = EarlyStopping(patience=3)
losses = [0.95, 0.82, 0.75, 0.749, 0.748, 0.749]
for epoch, loss in enumerate(losses, 1):
    if stopper.step(loss):
        print(f"Early stopping triggered at epoch {epoch}! Best loss: {stopper.best_loss:.4f}")
        break
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Equality Testing on Singletons (`None`, `True`, `False`)
Never use `==` when checking for `None`. Always use `is`.

```python
class WeirdObject:
    def __eq__(self, other):
        return True  # Overridden equality method

obj = WeirdObject()
print(obj == None)  # True! Bug!
print(obj is None)  # False! Correct memory identity check!
```

### 2. Assignment Expression (Walrus Operator `:=`)
Introduced in Python 3.8, the walrus operator assigns values to variables as part of a larger expression:

```python
# With walrus operator:
data_stream = ["tok1", "tok2", ""]
idx = 0
def read_next():
    global idx
    val = data_stream[idx]
    idx += 1
    return val

while (token := read_next()):
    print(f"Processing: {token}")
```

---

## 6. Interview Questions & Coding Traps

### Q1: What is the exact difference between `if x:` and `if x is not None:`?
- `if x:` evaluates truthiness via `bool(x)`. If `x` is `0`, `""`, `[]`, or `False`, the condition evaluates to `False`.
- `if x is not None:` evaluates strictly whether `x` points to an object other than the `None` singleton. If `x = 0` or `x = ""`, the check evaluates to `True`. In ML hyperparameter checks, `if lr:` fails when `lr = 0.0`!

### Q2: What is the output?
```python
x = 10
res = "High" if x > 20 else "Medium" if x > 5 else "Low"
print(res)
```
**Output:** `"Medium"`
**Explanation:** Python parses nested ternary operators associatively: `"High" if x > 20 else ("Medium" if x > 5 else "Low")`. Since `x = 10`, `x > 20` is false, branching to the second ternary where `10 > 5` is true.

### Complexity Reference
| Structure | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| `if/elif/else` Branch Evaluation | $O(1)$ per branch condition | $O(1)$ |
| `match/case` Pattern Matching | $O(1)$ to $O(K)$ where $K$ is pattern fields | $O(1)$ |
