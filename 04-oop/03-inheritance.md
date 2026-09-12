# Inheritance and MRO in Python

> Inheritance models hierarchical "is-a" relationships; Method Resolution Order (MRO) algorithmically determines method dispatch ordering across complex multiple inheritance graphs using C3 Linearization.

---

## 1. Why This Matters

### Why This Concept Exists
Hierarchical code reuse enables base architectures to provide shared abstractions (logging, parameters, device management) while specialized subclasses implement specific mathematical variants.

### Why Python Developers Need It
Python natively supports **multiple inheritance**. Without understanding C3 Linearization and cooperative `super()` calls, developers introduce subtle bugs in inheritance diamonds.

### Why It Matters Specifically in AI/ML/GenAI
- **PyTorch Layer Hierarchies**: `torch.nn.Linear` inherits from `torch.nn.Module`, inheriting tensor registration, device migration (`.to('cuda')`), and hook management.
- **Custom Transformers & Attention Blocks**: Subclassing standard attention modules to inject custom flash attention or rotary position embeddings (RoPE).
- **Agent Tool Inheritance**: Base agent tools defining common execution signatures and error handling.

### Where It Appears in Real Projects
- Custom PyTorch Layers & Loss functions (`nn.Module`).
- Scikit-learn custom estimators (`BaseEstimator`, `ClassifierMixin`).
- Base Vector Store abstractions in LlamaIndex.

---

## 2. Core Concept

### 2.1 Single Inheritance & `super()`
`super()` does not simply refer to "the parent class"; it delegates method calls to the **next class in the MRO chain**.

```python
class BaseEmbeddingModel:
    def __init__(self, dim: int):
        self.dim = dim

    def encode(self, text: str) -> list[float]:
        raise NotImplementedError

class MockEmbeddingModel(BaseEmbeddingModel):
    def __init__(self, dim: int, mock_val: float = 0.5):
        super().__init__(dim)  # Cooperative call to BaseEmbeddingModel
        self.mock_val = mock_val

    def encode(self, text: str) -> list[float]:
        return [self.mock_val] * self.dim

m = MockEmbeddingModel(dim=4)
print(m.encode("hello"))  # [0.5, 0.5, 0.5, 0.5]
```

### 2.2 Multiple Inheritance & The Diamond Problem
When class `D` inherits from `B` and `C`, and both inherit from `A`:
Which `__init__` or method executes?

```python
class A:
    def process(self):
        return "A"

class B(A):
    def process(self):
        return f"B -> {super().process()}"

class C(A):
    def process(self):
        return f"C -> {super().process()}"

class D(B, C):
    def process(self):
        return f"D -> {super().process()}"

d = D()
print(d.process())  # D -> B -> C -> A
```

### 2.3 Inspecting MRO
Every class has an `.mro()` method and `.__mro__` attribute.

```python
print([cls.__name__ for cls in D.mro()])
# ['D', 'B', 'C', 'A', 'object']
```

---

## 3. Mental Model

```text
The Diamond Problem & C3 Linearization:
        A
       ▲ ▲
      /        B     C
      ▲   ▲
       \ /
        D

MRO Linearization: D ──► B ──► C ──► A ──► object
`super()` in B calls C, NOT A! (Cooperative Multiple Inheritance)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Custom PyTorch-Style Layer Module
Simulating the fundamental `Module` and `Linear` inheritance pattern from PyTorch:

```python
from typing import Dict, Any

class Module:
    """Base class for all neural network modules."""
    def __init__(self) -> None:
        self._parameters: Dict[str, Any] = {}
        self.training: bool = True

    def register_parameter(self, name: str, param: Any) -> None:
        self._parameters[name] = param

    def eval(self) -> None:
        self.training = False

    def forward(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Subclasses must implement forward()")

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        # Pre-hooks would run here
        output = self.forward(*args, **kwargs)
        # Post-hooks would run here
        return output

class Linear(Module):
    """Specialized Linear layer subclass."""
    def __init__(self, in_features: int, out_features: int) -> None:
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        # Dummy weight allocation:
        self.register_parameter("weights", [[0.1] * in_features for _ in range(out_features)])

    def forward(self, x: list[float]) -> list[float]:
        # Simple dot product simulation
        weights = self._parameters["weights"]
        return [sum(w_i * x_i for w_i, x_i in zip(row, x)) for row in weights]

layer = Linear(in_features=3, out_features=2)
layer.eval()
print("Forward output:", layer([1.0, 2.0, 3.0]))
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Inconsistent MRO (`TypeError: Cannot create a consistent method resolution order`)
If class definitions create cyclical or contradictory inheritance constraints, Python rejects class compilation at runtime.

```python
class X: pass
class Y(X): pass
# class Z(X, Y): pass
# Raises: TypeError: Cannot create a consistent method resolution order (MRO) for bases X, Y
# Because Y inherits from X, Y must precede X in the MRO!
class Z(Y, X): pass  # Correct order!
```

---

## 6. Interview Questions & Coding Traps

### Q1: What algorithm does Python use to calculate MRO?
Python uses **C3 Linearization**. It guarantees three properties:
1. Subclasses precede parent classes.
2. The order of bases listed in the class definition is preserved.
3. Monotonicity: if class A precedes class B in any base's MRO, A must precede B in all derived classes.

### Q2: Why should you always call `super().__init__()` instead of `ParentClass.__init__(self)`?
Directly calling `ParentClass.__init__(self)` bypasses the MRO. In multiple inheritance diamonds, this causes the common ancestor's `__init__` to run multiple times and skips sibling cooperative classes.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Method Dispatch via MRO | $O(D)$ where $D$ is inheritance depth (cached) | $O(1)$ |
| MRO Calculation (at class definition) | $O(N^2)$ where $N$ is class count | $O(N)$ |
