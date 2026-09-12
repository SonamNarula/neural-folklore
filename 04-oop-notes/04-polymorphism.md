# Polymorphism and Abstraction in Python

> Polymorphism allows different object types to respond to identical method interfaces; abstraction hides internal implementation complexity behind Abstract Base Classes and runtime Protocols.

---

## 1. Why This Matters

### Why This Concept Exists
Software systems scale by depending on abstractions rather than concrete implementations. Swapping out a vector database (Pinecone -> Milvus) or an LLM provider (OpenAI -> Anthropic) should require zero changes to downstream business logic.

### Why Python Developers Need It
Python's dynamic nature allows **Duck Typing** ("If it walks like a duck and quacks like a duck, it's a duck"). Combining duck typing with formal Abstract Base Classes (`abc.ABC`) and structural typing (`typing.Protocol`) enables robust enterprise architecture.

### Why It Matters Specifically in AI/ML/GenAI
- **Pluggable Vector Databases**: Designing a unified `VectorStore` interface implemented by `ChromaStore`, `PineconeStore`, and `QdrantStore`.
- **Model Agnostic Inference Clients**: Standardizing generation signatures across OpenAI, Anthropic, and local vLLM models.
- **Scikit-Learn Estimator Interface**: All estimators adhere to the uniform `.fit(X, y)` and `.predict(X)` polymorphic contract.

### Where It Appears in Real Projects
- Vector store connectors in LangChain / LlamaIndex.
- Model wrappers in HuggingFace `AutoModel`.
- Custom transformers implementing `fit`/`transform` in Scikit-Learn.

---

## 2. Core Concept

### 2.1 Duck Typing (Implicit Polymorphism)
```python
class OpenAIClient:
    def generate(self, prompt: str) -> str:
        return f"OpenAI completion for {prompt}"

class AnthropicClient:
    def generate(self, prompt: str) -> str:
        return f"Anthropic completion for {prompt}"

def run_pipeline(llm, query: str):
    # No inheritance required! As long as llm has .generate(), it works!
    return llm.generate(query)
```

### 2.2 Formal Abstraction with `abc.ABC` (Nominal Subtyping)
Using the `abc` module to enforce implementation contracts at instantiation time:

```python
from abc import ABC, abstractmethod

class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, top_k: int) -> list[str]:
        """Subclasses MUST implement this method."""
        pass

class DenseRetriever(BaseRetriever):
    def retrieve(self, query: str, top_k: int) -> list[str]:
        return [f"dense_doc_{i}" for i in range(top_k)]

# r = BaseRetriever() -> TypeError: Can't instantiate abstract class BaseRetriever with abstract method retrieve
r = DenseRetriever()
print(r.retrieve("query", 2))  # ['dense_doc_0', 'dense_doc_1']
```

### 2.3 Structural Subtyping with `typing.Protocol` (Python 3.8+)
Protocols allow static type checkers (like `mypy`) to verify duck typing without requiring nominal class inheritance.

```python
from typing import Protocol

class Summarizer(Protocol):
    def summarize(self, text: str) -> str: ...

# Any class implementing summarize() satisfies the Summarizer Protocol!
```

---

## 3. Mental Model

```text
Abstract Interface Contract:
┌──────────────────────────────────────────────┐
│           BaseRetriever (ABC)                │
│       retrieve(query, top_k) -> List         │
└──────────────────────────────────────────────┘
                       ▲
        ┌──────────────┴──────────────┐
        │                             │
┌───────────────────────┐   ┌───────────────────────┐
│     DenseRetriever    │   │     SparseRetriever   │
│ (Embeddings + Cosine) │   │     (BM25 Inverted)   │
└───────────────────────┘   └───────────────────────┘
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Pluggable Multi-Provider LLM Gateway
A production-ready polymorphic gateway allowing runtime switching between LLM providers:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str, temperature: float) -> str:
        pass

class OpenAIGateway(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def complete(self, prompt: str, temperature: float) -> str:
        return f"[OpenAI gpt-4o]: Generated answer for '{prompt}' (temp={temperature})"

class AnthropicGateway(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def complete(self, prompt: str, temperature: float) -> str:
        return f"[Anthropic claude-3-5]: Generated answer for '{prompt}' (temp={temperature})"

# Consumer pipeline depends exclusively on the abstraction:
class AgentWorkflow:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def run(self, user_goal: str) -> str:
        return self.provider.complete(user_goal, temperature=0.1)

agent1 = AgentWorkflow(OpenAIGateway("sk-mock-123"))
agent2 = AgentWorkflow(AnthropicGateway("sk-mock-456"))
print(agent1.run("Calculate ROI"))
print(agent2.run("Summarize paper"))
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Partial Implementation of Abstract Methods
If a subclass implements only 2 out of 3 abstract methods, attempting to instantiate it will raise `TypeError: Can't instantiate abstract class with abstract method ...`.

### 2. `@abstractmethod` Decorator Order
When combining `@abstractmethod` with other decorators (`@classmethod`, `@property`), `@abstractmethod` must always be the **innermost** decorator!

```python
from abc import ABC, abstractmethod

class Config(ABC):
    @property
    @abstractmethod
    def schema_version(self) -> str:
        pass
```

---

## 6. Interview Questions & Coding Traps

### Q1: What is the difference between nominal subtyping (`abc.ABC`) and structural subtyping (`typing.Protocol`)?
- **Nominal Subtyping** (`abc.ABC`): Explicit inheritance is required (`class Child(Base)`). Relationships are checked at runtime via `issubclass()` and `isinstance()`.
- **Structural Subtyping** (`typing.Protocol`): No explicit inheritance is declared. If a class implements the matching method signatures, it satisfies the type contract. Checked primarily at static analysis time (`mypy`).

### Complexity Reference
| Mechanism | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Polymorphic Method Call | $O(1)$ dynamic dispatch | $O(1)$ |
| `isinstance()` against ABC | $O(1)$ to $O(D)$ hierarchy check | $O(1)$ |
