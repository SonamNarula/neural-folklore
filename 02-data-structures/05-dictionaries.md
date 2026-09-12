# Dictionaries in Python

> A dictionary is an ordered, compact hash table mapping hashable keys to arbitrary object pointers with $O(1)$ average-time lookups, insertions, and updates.

---

## 1. Why This Matters

### Why This Concept Exists
Key-value mapping is the most universal associative abstraction in computer science. Python's dictionary is the central engine of the language itself—classes, modules, global scopes, and local scopes are all powered by hash maps.

### Why Python Developers Need It
Mastering dictionaries, their memory layouts, and high-performance collection wrappers (`defaultdict`, `Counter`) enables elegant, optimal solutions to data structuring problems.

### Why It Matters Specifically in AI/ML/GenAI
- **JSON / REST Payloads**: Every interaction with OpenAI, Anthropic, or Hugging Face APIs uses JSON payloads that deserialize directly into Python dictionaries.
- **Model Checkpoints**: In PyTorch, weights are stored in `state_dict`, which is an `OrderedDict` mapping layer names (strings) to weight tensors.
- **Vocabulary Index Maps**: Tokenizer vocabularies map `token_string -> token_id` and reverse `token_id -> token_string`.

### Where It Appears in Real Projects
- Model state dictionaries: `model.state_dict()`.
- API request/response payloads in GenAI applications.
- Document inverted indices in search engines and RAG vector stores.

---

## 2. Core Concept

### 2.1 Architecture: Compact Hash Table (Python 3.6+)
Since Python 3.6 (formally standard in 3.7), Python dicts preserve **insertion order** and consume 20-25% less memory by splitting storage into:
1. A sparse hash indices array (`indices`).
2. A dense array of entries (`entries`) stored in insertion order: `[hash, key_ptr, value_ptr]`.

```python
# Construction
config = {"model": "gpt-4o", "temperature": 0.2, "max_tokens": 512}

# Safe lookup with defaults
timeout = config.get("timeout", 30)  # Returns 30 if key is absent

# Mutating dictionary
config["stream"] = True
```

### 2.2 Advanced Specialized Mappings (`collections`)
```python
from collections import defaultdict, Counter

# defaultdict eliminates KeyError and manual presence checks:
grouped_docs = defaultdict(list)
grouped_docs["nlp"].append("Attention Paper")
print(grouped_docs["nlp"])  # ['Attention Paper']

# Counter for frequency tabulation:
tokens = ["the", "model", "and", "the", "weights"]
counts = Counter(tokens)
print(counts.most_common(1))  # [('the', 2)]
```

### 2.3 Dictionary Views: `.keys()`, `.values()`, `.items()`
Dict views provide dynamic, memory-efficient read-only windows into dictionary data without creating list copies.

---

## 3. Mental Model

```text
Compact Dict Architecture (Python 3.7+):
Hash Indices Table (Sparse array of small ints):
[-1, 1, -1, 0, -1, 2, -1]

Entries Array (Dense, ordered by insertion):
Index 0: [ hash("model"),       "model",       "gpt-4o" ]
Index 1: [ hash("temperature"), "temperature", 0.2      ]
Index 2: [ hash("max_tokens"),  "max_tokens",  512      ]
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Inverted Index for Keyword Search / Hybrid RAG
Building an in-memory inverted index mapping vocabulary terms to document IDs:

```python
from collections import defaultdict
from typing import Dict, List, Set

class InvertedIndex:
    """Inverted index mapping tokens to document IDs for fast BM25 / hybrid retrieval."""
    def __init__(self) -> None:
        self.index: Dict[str, Set[int]] = defaultdict(set)

    def add_document(self, doc_id: int, content: str) -> None:
        tokens = content.lower().split()
        for token in tokens:
            self.index[token].add(doc_id)

    def search(self, query: str) -> Set[int]:
        query_tokens = query.lower().split()
        if not query_tokens:
            return set()
        # Find documents containing ALL query terms (Set intersection)
        matching_docs = self.index.get(query_tokens[0], set()).copy()
        for tok in query_tokens[1:]:
            matching_docs &= self.index.get(tok, set())
        return matching_docs

idx = InvertedIndex()
idx.add_document(1, "Large language models optimize autoregressive loss")
idx.add_document(2, "Language models require high throughput training")
idx.add_document(3, "Diffusion models generate photorealistic images")

print("Docs matching 'language models':", idx.search("language models"))
# Docs matching 'language models': {1, 2}
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Mutating a Dictionary During Iteration
Attempting to add or delete keys while iterating directly over a dictionary raises `RuntimeError: dictionary changed size during iteration`.

```python
d = {"a": 1, "b": 2, "c": 3}
# BUG:
# for k in d:
#     if d[k] % 2 != 0:
#         del d[k]

# CORRECT: Iterate over a list snapshot of keys
for k in list(d.keys()):
    if d[k] % 2 != 0:
        del d[k]
```

### 2. In-Place Mutation with `setdefault()`
`d.setdefault(k, [])` always evaluates the default argument expression, even when the key exists. Prefer `defaultdict` for performance-critical loops.

---

## 6. Interview Questions & Coding Traps

### Q1: How are hash collisions handled internally in Python dictionaries?
Python uses **open addressing with pseudo-random probing**:
When a hash collision occurs ($j = (5j + 1 + 	ext{perturb}) \pmod{	ext{size}}$), Python probes alternative slots in the sparse indices table until an empty slot is located. The perturbation variable incorporates higher-order bits of the original hash code to prevent clustering.

### Q2: What is the output of the following snippet?
```python
d = {}
d[1] = "integer"
d[1.0] = "float"
d[True] = "boolean"
print(len(d), d[1])
```
**Output:** `1 boolean`
**Explanation:** `1 == 1.0 == True` and `hash(1) == hash(1.0) == hash(True)`. The keys overwrite each other in place; the final write assigns `"boolean"` to the existing entry!

### Complexity Reference
| Operation | Average Case | Worst Case | Space Complexity |
| :--- | :--- | :--- | :--- |
| Get / Set / Delete `d[k]` | $O(1)$ | $O(N)$ (collision storm) | $O(1)$ |
| Key Membership `k in d` | $O(1)$ | $O(N)$ | $O(1)$ |
| Iteration `for k, v in d.items()` | $O(N)$ | $O(N)$ | $O(1)$ |
