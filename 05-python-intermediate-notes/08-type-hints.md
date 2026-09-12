# Type Hints and Static Type Checking in Python

> Type hints (PEP 484) add structural static type annotations to Python code, enabling static analysis tools (`mypy`), IDE autocompletion, and runtime schema validation (`pydantic`) without altering runtime dynamics.

---

## 1. Why This Matters

### Why This Concept Exists
As Python codebases scale from small scripts to massive enterprise systems, dynamic typing causes silent runtime failures. Type hints provide the reliability of statically typed languages while preserving Python's agile development speed.

### Why Python Developers Need It
Type hints make code self-documenting, catch bugs before execution via static linters (`mypy`, `pyright`), and enable advanced runtime validation libraries like Pydantic.

### Why It Matters Specifically in AI/ML/GenAI
- **Tensor Shape & Dimension Validation**: Type hints communicate tensor shapes and dtypes (`Tensor[Batch, SeqLen, HiddenDim]`).
- **Pydantic v2 Models**: Modern LLM structured outputs, JSON schema generation, and FastAPI endpoints rely entirely on type annotations.
- **Generic Inference Pipelines**: Defining reusable pipelines that handle diverse data types using `TypeVar` and `Generic`.

### Where It Appears in Real Projects
- Pydantic models for LLM output extraction.
- Hugging Face Transformers model signatures.
- Type-checked production AI repositories (`mypy --strict`).

---

## 2. Core Concept

### 2.1 Modern Type Annotations (Python 3.10+)
Python 3.10+ simplifies typing syntax by allowing built-in types (`list`, `dict`) and union operators (`|` instead of `Union`).

```python
# Modern Python 3.10+ syntax:
def format_prompt(
    template: str,
    variables: dict[str, str],
    max_tokens: int | None = None  # Replaces Optional[int]
) -> str:
    prompt = template
    for k, v in variables.items():
        prompt = prompt.replace(f"{{{k}}}", v)
    return prompt
```

### 2.2 Advanced Typing Primitives
```python
from typing import Callable, TypeVar, Generic, Any

T = TypeVar("T")  # Generic Type Variable

class DataBuffer(Generic[T]):
    def __init__(self) -> None:
        self.items: list[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

buf: DataBuffer[float] = DataBuffer()
buf.push(0.95)
```

### 2.3 Callable and Literal Types
```python
from typing import Literal, Callable

# Restrict values to specific literals:
DeviceType = Literal["cpu", "cuda", "mps"]

# Type hint for function signatures: Callable[[Arg1, Arg2], ReturnType]
TransformFn = Callable[[list[float]], list[float]]
```

---

## 3. Mental Model

```text
Development Lifecycle with Type Hints:
Source Code + Type Hints
       │
       ├──► Python Runtime (CPython) ──► Ignores annotations! Executes dynamically.
       │
       ├──► Static Linter (Mypy)      ──► Validates type contracts, catches bugs!
       │
       └──► Pydantic v2 Engine        ──► Enforces strict runtime data schemas!
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Generic Pipeline with Type-Checked Component Signatures
A type-safe feature processing pipeline using Generics and Callables:

```python
from typing import TypeVar, Generic, Callable, List

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")

class ProcessingStage(Generic[InputT, OutputT]):
    def __init__(self, name: str, transform: Callable[[InputT], OutputT]) -> None:
        self.name = name
        self.transform = transform

    def execute(self, data: InputT) -> OutputT:
        return self.transform(data)

# Concrete type-safe instances:
stage_tokenize: ProcessingStage[str, List[str]] = ProcessingStage(
    "tokenize",
    lambda text: text.lower().split()
)

stage_embed: ProcessingStage[List[str], List[int]] = ProcessingStage(
    "embed",
    lambda tokens: [hash(t) % 1000 for t in tokens]
)

tokens = stage_tokenize.execute("Hello AI World")
embeddings = stage_embed.execute(tokens)
print("Tokens:", tokens)
print("Embeddings:", embeddings)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Type Hints DO NOT Enforce Runtime Types Automatically
```python
def add(x: int, y: int) -> int:
    return x + y

# Python DOES NOT throw a runtime error here!
print(add("hello ", "world"))  # Prints "hello world"!
```
To enforce runtime validation, use **Pydantic**!

### 2. Mutable Default Arguments in Typed Code
Adding type hints does not fix Python's mutable default trap:
```python
# STILL A BUG:
def append_item(item: str, target: list[str] = []) -> list[str]: ...
```

---

## 6. Interview Questions & Coding Traps

### Q1: What is the difference between `Any` and `object` in type hinting?
- `Any`: An escape hatch that disables all static type checking on that variable. You can call any method or access any attribute on it without `mypy` complaining.
- `object`: The root of Python's type hierarchy. Static type checkers will only allow operations valid on all objects (`str()`, `id()`). Calling `obj.custom_method()` will raise a type-check error.

### Q2: What is `typing.cast()`?
`cast(TargetType, value)` is a static typing instruction that forces `mypy` to treat `value` as `TargetType`. At runtime, `cast` is a no-op that simply returns the value unchanged:
```python
def cast(typ, val):
    return val
```

### Complexity Reference
| Operation | Runtime Cost | Static Analysis Cost |
| :--- | :--- | :--- |
| Parsing Type Hints | Minor one-time overhead at module load | $O(N)$ AST type analysis |
| Runtime Execution of Annotated Function | Zero additional cost (annotations stored in `__annotations__`) | None |
