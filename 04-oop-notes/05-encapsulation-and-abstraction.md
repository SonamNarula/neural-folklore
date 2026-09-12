# Encapsulation and Property Descriptors in Python

> Encapsulation restricts direct state access via naming conventions, while property descriptors expose managed attribute access with validation and lazy evaluation.

---

## 1. Why This Matters

### Why This Concept Exists
Exposing raw object attributes allows external callers to corrupt internal state (e.g., setting a learning rate to negative numbers or an embedding dimension to zero). Encapsulation establishes access boundaries.

### Why Python Developers Need It
Unlike Java or C++, Python has no `private` keyword. Python uses naming conventions (`_protected`, `__private` with name mangling) and the `@property` decorator for idiomatic access control.

### Why It Matters Specifically in AI/ML/GenAI
- **Hyperparameter Validation**: Using `@property.setter` to guarantee values like learning rates (`lr > 0`), dropout (`0.0 <= p < 1.0`), and batch sizes remain within valid mathematical domains.
- **Read-Only Model Weights**: Preventing accidental reassignment of frozen model layers during fine-tuning.
- **Lazy Evaluation**: Computing expensive statistics (e.g., covariance matrix, vocab size) only when accessed.

### Where It Appears in Real Projects
- `torch.nn.Module.training` mode flags.
- Validated model configuration classes in Transformers.
- Read-only property getters in Scikit-Learn estimators.

---

## 2. Core Concept

### 2.1 Python Access Conventions
1. **Public** (`self.name`): Unrestricted access.
2. **Protected** (`self._name`): Internal convention; signals to developers: "Do not touch outside this class/subclass".
3. **Private / Name-Mangled** (`self.__name`): CPython automatically mangles the identifier to `_ClassName__name` to prevent accidental namespace collisions in subclasses.

```python
class Optimizer:
    def __init__(self, lr: float):
        self.public_name = "AdamW"
        self._protected_state = {"step": 0}
        self.__secret_salt = "0xdeadbeef"

opt = Optimizer(1e-3)
print(opt.public_name)          # "AdamW"
print(opt._protected_state)     # Accessible, but violates convention!
# opt.__secret_salt             -> Raises AttributeError!
print(opt._Optimizer__secret_salt)  # "0xdeadbeef" (Accessible via mangled name!)
```

### 2.2 The `@property` Decorator (Getters, Setters, Deleters)
Exposes methods as if they were simple attributes while executing validation logic:

```python
class TrainingConfig:
    def __init__(self, learning_rate: float):
        self._learning_rate = learning_rate

    @property
    def learning_rate(self) -> float:
        """Getter: returns learning rate."""
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, value: float) -> None:
        """Setter: validates mathematical bounds."""
        if value <= 0.0:
            raise ValueError(f"Learning rate must be strictly positive, got: {value}")
        self._learning_rate = value

cfg = TrainingConfig(0.001)
cfg.learning_rate = 0.0005  # Executes setter!
# cfg.learning_rate = -0.1   -> Raises ValueError!
```

---

## 3. Mental Model

```text
Attribute Assignment Flow:
cfg.learning_rate = 0.01
          │
          ▼
Is 'learning_rate' a Descriptor / Property on TrainingConfig?
          │
     ┌────┴────┐
     ▼ YES     ▼ NO
Executes:      Direct write to cfg.__dict__['learning_rate']
TrainingConfig.learning_rate.fset(cfg, 0.01)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Validated Hyperparameter Configuration with Lazy Computation
A production configuration class that validates probability bounds and lazily computes embedding norms:

```python
import math
from typing import List

class LayerNormConfig:
    def __init__(self, eps: float = 1e-5, weights: List[float] | None = None):
        self.eps = eps  # Triggers eps.setter
        self._weights: List[float] = weights or [1.0, 1.0, 1.0]
        self._cached_l2_norm: float | None = None

    @property
    def eps(self) -> float:
        return self._eps

    @eps.setter
    def eps(self, value: float) -> None:
        if value <= 0 or value > 1e-2:
            raise ValueError(f"Epsilon must be between 0 and 1e-2, got {value}")
        self._eps = value

    @property
    def l2_norm(self) -> float:
        """Lazy property: calculates L2 norm on-demand and caches result."""
        if self._cached_l2_norm is None:
            print("Calculating L2 norm on-demand...")
            self._cached_l2_norm = math.sqrt(sum(w**2 for w in self._weights))
        return self._cached_l2_norm

cfg = LayerNormConfig(eps=1e-5)
print("Norm 1:", cfg.l2_norm)  # Computes and caches
print("Norm 2:", cfg.l2_norm)  # Returns cached value immediately!
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Infinite Recursion in Property Setters
Using the exact same property name inside the setter causes infinite recursive calls!

```python
# CATASTROPHIC BUG:
class Broken:
    @property
    def x(self): return self.x
    @x.setter
    def x(self, val):
        self.x = val  # Calls setter again! Infinite recursion! RecursionError!

# FIX: Store in an underlying private or protected attribute (_x):
class Fixed:
    @property
    def x(self): return self._x
    @x.setter
    def x(self, val): self._x = val
```

---

## 6. Interview Questions & Coding Traps

### Q1: Is private name mangling (`__var`) true security in Python?
**Answer:** No. It is **security by convention** designed to avoid attribute collisions in class inheritance. Any caller can still access and mutate the attribute via `_ClassName__var`.

### Q2: How do you create a truly read-only attribute?
Define a `@property` getter **without** defining a corresponding `@property.setter`. Any attempt to assign to `obj.attr` will raise `AttributeError: can't set attribute`.

### Complexity Reference
| Mechanism | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Property Getter / Setter Call | $O(1)$ function call overhead | $O(1)$ |
| Name Mangling Translation | $O(1)$ compile-time resolution | $O(1)$ |
