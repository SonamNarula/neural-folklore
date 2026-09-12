# Operators in Python

> Operators are symbolic instructions that execute fundamental mathematical, logical, and bitwise manipulations or dispatch to object dunder methods.

---

## 1. Why This Matters

### Why This Concept Exists
Operators provide expressive syntactic sugar for core computational operations. In Python, operators map directly to magic dunder methods (`+` maps to `__add__`, `==` to `__eq__`, `&` to `__and__`), allowing seamless object polymorphism.

### Why Python Developers Need It
Understanding operator precedence, short-circuit evaluation, and identity semantics prevents logical bugs and optimizes runtime execution.

### Why It Matters Specifically in AI/ML/GenAI
- **Matrix Multiplication**: In modern Python/NumPy/PyTorch, the `@` operator (`__matmul__`) represents tensor dot-product/matrix multiplication, distinguishing it from `*` (element-wise Hadamard product).
- **Bitwise Masking**: Attention masks, image binary masks, and feature presence flags rely on bitwise operators (`&`, `|`, `^`, `~`).
- **Short-Circuiting in Guard Clauses**: Efficiently validating API configurations, guarding against `None` references before accessing model attributes.

### Where It Appears in Real Projects
- Transformer multi-head attention: `scores = (Q @ K.T) / math.sqrt(d_k)`.
- Attention mask combinations: `combined_mask = causal_mask & padding_mask`.
- Fallback configuration pipelines: `api_key = env_key or config_key or default_key`.

---

## 2. Core Concept

### 2.1 Operator Categories
1. **Arithmetic**: `+`, `-`, `*`, `/` (true division -> float), `//` (floor division), `%` (modulo), `**` (exponentiation).
2. **Comparison**: `==`, `!=`, `<`, `<=`, `>`, `>=`.
3. **Identity & Membership**: `is`, `is not`, `in`, `not in`.
4. **Logical**: `and`, `or`, `not` (Short-circuiting).
5. **Bitwise**: `&` (AND), `|` (OR), `^` (XOR), `~` (NOT), `<<` (left shift), `>>` (right shift).
6. **Matrix Multiplication**: `@` (`__matmul__`).

### 2.2 Short-Circuit Evaluation
Logical operators `and` and `or` do not return boolean `True`/`False`; they return the **exact operand that determined the outcome**:
- `A and B`: If `A` is falsy, returns `A` immediately without evaluating `B`. Otherwise returns `B`.
- `A or B`: If `A` is truthy, returns `A` immediately without evaluating `B`. Otherwise returns `B`.

```python
# Practical fallback configuration pattern:
api_key = None or "" or "sk-production-12345"
print(api_key)  # "sk-production-12345"
```

### 2.3 Comparison Chaining
Python natively supports chained comparisons:

```python
val = 0.75
# Evaluated as: (0.0 <= val) and (val <= 1.0)
if 0.0 <= val <= 1.0:
    print("Valid probability score")
```

---

## 3. Mental Model

```text
Operator Dispatching:
a + b   ─────────► type(a).__add__(a, b)
a @ b   ─────────► type(a).__matmul__(a, b)
a == b  ─────────► type(a).__eq__(a, b)
a is b  ─────────► Compare pointer addresses: id(a) == id(b) (no dunder call)

Short-Circuit Flow (A or B):
[ Eval A ] ─── Is truthy? ──► YES ──► Return A (B never executed)
    │
    └──► NO ──► Return B
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Fast Bitwise Feature Flagging for Preprocessing
Representing multiple boolean preprocessing pipeline steps using bitwise integer masks:

```python
class PreprocessFlags:
    NONE         = 0       # 00000000
    LOWERCASE    = 1 << 0  # 00000001 (1)
    REMOVE_PUNCT = 1 << 1  # 00000010 (2)
    STRIP_HTML   = 1 << 2  # 00000100 (4)
    NORMALIZE    = 1 << 3  # 00001000 (8)

def clean_document(text: str, flags: int) -> str:
    cleaned = text
    if flags & PreprocessFlags.STRIP_HTML:
        cleaned = cleaned.replace("<br>", " ").replace("<p>", " ")
    if flags & PreprocessFlags.LOWERCASE:
        cleaned = cleaned.lower()
    if flags & PreprocessFlags.REMOVE_PUNCT:
        for char in "!?,.:;":
            cleaned = cleaned.replace(char, "")
    return cleaned

# Enable LOWERCASE and REMOVE_PUNCT using bitwise OR
active_flags = PreprocessFlags.LOWERCASE | PreprocessFlags.REMOVE_PUNCT
sample = "<p>Transformers: State-of-the-Art NLP!</p>"
print(clean_document(sample, active_flags))
# Output: <p>transformers state-of-the-art nlp</p>
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Division: `/` vs `//`
`/` always returns a `float`. `//` returns the mathematical floor (rounds down towards negative infinity).

```python
print(7 / 2)    # 3.5 (float)
print(7 // 2)   # 3 (int)
print(-7 // 2)  # -4 (NOT -3! Floored towards -infinity)
```

### 2. Bitwise vs Logical Operator Precedence
Bitwise operators have higher precedence than comparison operators, leading to subtle bugs without parentheses.

```python
x = 5
# WRONG: evaluated as x == (4 & 1) -> x == 0 -> False
# print(x == 4 & 1)

# CORRECT:
print((x == 4) & 1)  # 0
```

---

## 6. Interview Questions & Coding Traps

### Q1: What does `[] or {} or 0 or "winner" or 42` evaluate to?
`"winner"`.
**Explanation:** Python evaluates left to right: `[]` (falsy) -> `{}` (falsy) -> `0` (falsy) -> `"winner"` (truthy). It stops and returns `"winner"`.

### Q2: What is the output of `False == False in [False]`?
`True`.
**Explanation:** Python treats this as chained comparison: `(False == False) and (False in [False])`. Both sub-expressions evaluate to `True`, so the result is `True`.

### Complexity Reference
| Operator | Time Complexity (Primitives) | Space Complexity |
| :--- | :--- | :--- |
| Arithmetic (`+`, `-`, `*`) | $O(1)$ | $O(1)$ |
| Arbitrary precision `int` multiplication | $O(N^{\log_2 3})$ Karatsuba | $O(N)$ |
| Logical (`and`, `or`) | $O(1)$ | $O(1)$ |
| Identity (`is`) | $O(1)$ | $O(1)$ |
