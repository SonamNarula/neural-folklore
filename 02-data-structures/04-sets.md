# Sets in Python

> A set is an unordered collection of unique, hashable objects backed by an open-addressing hash table offering $O(1)$ average time complexity for lookups, insertions, and deletions.

---

## 1. Why This Matters

### Why This Concept Exists
Checking for item membership in an array takes $O(N)$ linear time. Sets utilize hash codes to check membership in $O(1)$ constant time, while mathematically enforcing uniqueness.

### Why Python Developers Need It
Deduplication and membership testing are ubiquitous. Sets also implement mathematical set algebra (unions, intersections, differences) natively in C.

### Why It Matters Specifically in AI/ML/GenAI
- **Vocabulary Deduplication**: Building tokenizer vocabularies from raw corpora requires extracting distinct tokens across billions of words.
- **Fast Stopword Removal**: Filtering stopwords or toxic phrases from text prompts in $O(1)$ time per token rather than $O(M)$ list scans.
- **Feature Column Matching**: Validating that production inference payloads match training dataset schemas via set differences: `missing = set(train_cols) - set(input_cols)`.

### Where It Appears in Real Projects
- Schema validation in ML pipelines.
- Vocabulary construction in HuggingFace tokenizers.
- Graph traversal algorithms tracking `visited` nodes.

---

## 2. Core Concept

### 2.1 Set Operations and Hash Table Engine
A `set` requires every element to implement `__hash__()` and `__eq__()`.

```python
# Creation
s = {1, 2, 3, 3, 2}
print(s)  # {1, 2, 3} (Duplicates automatically dropped)

# Adding and Removing
s.add(4)
s.discard(2)  # Does NOT raise KeyError if element is absent
# s.remove(99)  -> Raises KeyError
```

### 2.2 Mathematical Set Algebra
| Math Operation | Python Operator | Method Equivalent |
| :--- | :--- | :--- |
| Union ($A \cup B$) | `a | b` | `a.union(b)` |
| Intersection ($A \cap B$) | `a & b` | `a.intersection(b)` |
| Difference ($A \setminus B$) | `a - b` | `a.difference(b)` |
| Symmetric Diff ($A \Delta B$) | `a ^ b` | `a.symmetric_difference(b)` |
| Subset Check ($A \subseteq B$) | `a <= b` | `a.issubset(b)` |

```python
train_features = {"age", "income", "credit_score", "zipcode"}
inference_features = {"age", "income", "credit_score"}

# Verify no missing features:
missing = train_features - inference_features
print(f"Missing features: {missing}")  # {'zipcode'}
```

### 2.3 `frozenset` (Immutable Set)
`frozenset` is an immutable set. Because it is immutable and hashable, it can be stored inside another set or used as a dictionary key.

---

## 3. Mental Model

```text
Set Hash Table:
Key: "token" ──► hash("token") % table_size ──► Bucket Index 3
Bucket 0: NULL
Bucket 1: NULL
Bucket 2: [ Hash code | Pointer to "embedding" ]
Bucket 3: [ Hash code | Pointer to "token" ]  <-- Found in O(1) time!
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Fast Production Feature Schema Validator
Validating incoming ML prediction payloads against expected feature schemas:

```python
from typing import Dict, Any, Set

class FeatureSchemaValidator:
    def __init__(self, expected_features: Set[str]) -> None:
        self.expected: Set[str] = expected_features

    def validate(self, payload: Dict[str, Any]) -> tuple[bool, str]:
        received = set(payload.keys())
        missing = self.expected - received
        unexpected = received - self.expected

        if missing:
            return False, f"Missing required features: {missing}"
        if unexpected:
            return False, f"Unexpected extra features: {unexpected}"
        return True, "Schema validation passed"

validator = FeatureSchemaValidator(expected_features={"user_id", "embedding", "query_timestamp"})
valid, msg = validator.validate({"user_id": "usr_10", "embedding": [0.1, 0.2]})
print(f"Valid: {valid} | Message: {msg}")
# Valid: False | Message: Missing required features: {'query_timestamp'}
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Sets Cannot Contain Mutable Objects
Lists, dicts, and regular sets cannot be inserted into a set because they are not hashable.

```python
# BUG:
# s = {[1, 2], [3, 4]}  -> TypeError: unhashable type: 'list'

# CORRECT: Use tuples
s = {(1, 2), (3, 4)}
```

### 2. Set Ordering is Non-Deterministic Across Runs
Python randomizes hash seeds (`PYTHONHASHSEED`) on startup for security. Never rely on the iteration order of a set!

---

## 6. Interview Questions & Coding Traps

### Q1: What is the time complexity of checking `x in my_set` versus `x in my_list`?
- `x in my_set`: Average case $O(1)$, worst case $O(N)$ (under catastrophic hash collisions).
- `x in my_list`: $O(N)$ linear scan.

### Q2: What is the output of `{True, 1, 1.0}`?
`{True}`
**Explanation:** In Python, `bool` is a subclass of `int`. `True == 1 == 1.0`, and `hash(True) == hash(1) == hash(1.0)`. Since all three have identical values and hash codes, the set treats them as identical duplicates and retains only the first element inserted (`True`).

### Complexity Reference
| Operation | Average Time Complexity | Worst Case Time | Space Complexity |
| :--- | :--- | :--- | :--- |
| `add(x)` | $O(1)$ | $O(N)$ | $O(1)$ |
| `x in s` | $O(1)$ | $O(N)$ | $O(1)$ |
| `s1 & s2` (Intersection) | $O(\min(|s1|, |s2|))$ | $O(|s1| \cdot |s2|)$ | $O(\min(|s1|, |s2|))$ |
| `s1 | s2` (Union) | $O(|s1| + |s2|)$ | $O(|s1| + |s2|)$ | $O(|s1| + |s2|)$ |
