# Constructors and Self in Python

> `__new__` is the real constructor that allocates the heap object, `__init__` is the initializer that configures attributes, and `self` is the explicit reference to the instance undergoing execution.

---

## 1. Why This Matters

### Why This Concept Exists
Unlike languages like Java or C++ where `this` is implicitly passed, Python explicitly exposes `self` to maintain the Zen of Python ("Explicit is better than implicit"). Understanding object lifecycle hooks (`__new__` vs `__init__`) allows low-level metaprogramming.

### Why Python Developers Need It
Mastering `__new__` enables singleton architectures and immutability overrides, while `@classmethod` provides elegant alternative factory constructors.

### Why It Matters Specifically in AI/ML/GenAI
- **Singleton Model Weight Loaders**: Ensuring a 14GB LLM model checkpoint is loaded into memory only once across worker threads.
- **Alternative Constructors for Datasets**: Factory classmethods like `Dataset.from_csv()`, `Dataset.from_parquet()`, `Dataset.from_huggingface()`.
- **Custom Tensor/Array Subclassing**: Overriding `__new__` when subclassing `numpy.ndarray` or `torch.Tensor`.

### Where It Appears in Real Projects
- HuggingFace `PreTrainedModel.from_pretrained()`.
- Singleton database connection pools and inference engines.
- Factory initializers in LangChain / LlamaIndex.

---

## 2. Core Concept

### 2.1 `__new__` vs `__init__`
- `__new__(cls, *args, **kwargs)`: Static method responsible for **allocating and returning** the instance object.
- `__init__(self, *args, **kwargs)`: Instance method responsible for **initializing** the newly allocated instance.

```python
class Demo:
    def __new__(cls, *args, **kwargs):
        print("1. __new__ allocating memory for instance")
        instance = super().__new__(cls)
        return instance

    def __init__(self, value: int):
        print("2. __init__ initializing instance state")
        self.value = value

d = Demo(42)
```

### 2.2 Instance Methods vs Class Methods vs Static Methods
- **Instance Method** (`def m(self)`): Operates on a specific instance.
- **Class Method** (`@classmethod def m(cls)`): Operates on the class blueprint; ideal for alternative factory constructors.
- **Static Method** (`@staticmethod def m()`): Isolated utility function belonging to the class's logical namespace.

```python
class LLMConfig:
    def __init__(self, model_name: str, context_window: int):
        self.model_name = model_name
        self.context_window = context_window

    @classmethod
    def gpt4o(cls) -> "LLMConfig":
        """Factory constructor for GPT-4o."""
        return cls(model_name="gpt-4o", context_window=128000)

    @staticmethod
    def is_valid_context(tokens: int) -> bool:
        return 0 < tokens <= 1_000_000

# Using factory method:
cfg = LLMConfig.gpt4o()
print(cfg.model_name, cfg.context_window)  # gpt-4o 128000
```

---

## 3. Mental Model

```text
Object Instantiation Pipeline:
obj = Class(*args)
       │
       ▼
1. Class.__new__(Class, *args) ──► Allocates raw uninitialized PyObject on heap
       │
       ▼ (if instance of Class returned)
2. Class.__init__(obj, *args)  ──► Binds self.x = ..., self.y = ...
       │
       ▼
Returns obj to caller
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Thread-Safe Singleton LLM Model Engine
Ensuring only one instance of an expensive neural network engine exists in memory:

```python
import threading

class SingletonModelServer:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                # Double-checked locking pattern
                if not cls._instance:
                    print("Allocating single GPU model server instance...")
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model_tag: str = "llama-3-8b") -> None:
        # Prevent re-initialization if already initialized
        if not hasattr(self, "_initialized"):
            self.model_tag = model_tag
            self._initialized = True
            print(f"Model server initialized with {model_tag}")

s1 = SingletonModelServer("llama-3-8b")
s2 = SingletonModelServer("different-tag")
print(s1 is s2)  # True -> Exact same memory address!
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. `__init__` Must Return `None`
Attempting to return any value other than `None` from `__init__` raises `TypeError: __init__() should return None, not '...'`.

### 2. Forgetting `self` as the First Parameter
Declaring an instance method as `def method():` raises `TypeError: method() takes 0 positional arguments but 1 was given` when called via `instance.method()`.

---

## 6. Interview Questions & Coding Traps

### Q1: Can `__new__` return an object that is NOT an instance of the class? What happens to `__init__`?
**Answer:** Yes. If `__new__` returns an object that is not an instance of `cls`, Python **will NOT call `__init__`**. The object is returned directly to the caller.

### Q2: Why is `self` not a reserved keyword in Python?
`self` is simply a naming convention. You could technically name it `this` or `me`, but doing so violates PEP 8 and ruins readability. Python's parser only cares that the first argument receives the instance reference.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| `__new__` allocation | $O(1)$ heap allocation | $O(1)$ |
| `__init__` execution | $O(1)$ unless doing heavy computation | $O(1)$ |
