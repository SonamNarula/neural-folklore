# Strings in Python

> Strings are immutable, contiguous sequences of Unicode code points optimized for fast slicing and indexed lookups.

---

## 1. Why This Matters

### Why This Concept Exists
Text is fundamentally distinct from binary data. Python 3 strictly separates Unicode strings (`str`) from raw bytes (`bytes`), ensuring cross-platform text integrity across character encodings.

### Why Python Developers Need It
Understanding string immutability, memory interning, and slicing mechanics is critical to prevent quadratic $O(N^2)$ string concatenation bottlenecks.

### Why It Matters Specifically in AI/ML/GenAI
- **LLM Tokenization**: Subword tokenizers (BPE, WordPiece, SentencePiece) perform millions of string splits, prefixes, and unicode normalizations during token generation.
- **Prompt Engineering**: Dynamic prompt templating, prompt injection sanitization, and regex-based output parsing require advanced string methods.
- **Corpus Preprocessing**: Cleaning gigabytes of web scraping text requires memory-efficient string manipulation and regex matching.

### Where It Appears in Real Projects
- HuggingFace `tokenizers` and OpenAI `tiktoken`.
- Regex output extractors for structured JSON from LLMs.
- Text cleaning in NLP pipelines (stripping HTML, unicode normalization).

---

## 2. Core Concept

### 2.1 String Immutability and Memory Layout
Once allocated, a `str` object cannot be modified in-place. Any operation that modifies a string (`replace`, `lower`, `strip`, `+`) allocates a **new** `PyUnicodeObject` in heap memory.

```python
s = "Attention"
# s[0] = "a"  -> TypeError: 'str' object does not support item assignment
s_new = "a" + s[1:]  # Creates a new string object
```

### 2.2 Slicing Mechanics (`[start:stop:step]`)
String slicing returns a new string containing elements from `start` up to (but excluding) `stop` with stride `step`.

```python
text = "Transformers"
print(text[0:5])    # "Trans"
print(text[::-1])   # "sremrofsnarT" (Reverse string)
print(text[::2])    # "Tasmr" (Every second char)
```

### 2.3 Unicode Normalization (NFC, NFD, NFKC, NFKD)
In NLP, characters can be represented by different unicode code points (e.g., `é` as a single character vs `e` + combining accent).

```python
import unicodedata

s1 = "café"            # Composed (NFC)
s2 = "café"       # Decomposed (NFD)
print(s1 == s2)        # False!
# Normalize to NFC for consistent vocabulary matching in NLP:
print(unicodedata.normalize("NFC", s1) == unicodedata.normalize("NFC", s2))  # True
```

---

## 3. Mental Model

```text
String Immutability:
Original: 's' ──► [ 'P', 'y', 't', 'h', 'o', 'n' ] (Read-only contiguous C array)

s += " 3"
New Heap Allocation:
Old:      [ 'P', 'y', 't', 'h', 'o', 'n' ] (Unchanged, awaiting GC if refcount=0)
New: 's' ─► [ 'P', 'y', 't', 'h', 'o', 'n', ' ', '3' ]
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Fast Tokenizer Normalizer & Stop-Word Filter
Production NLP regex pipeline for token normalization and stopword elimination:

```python
import re
from typing import List, Set

class TextNormalizer:
    def __init__(self, stop_words: Set[str] | None = None) -> None:
        self.stop_words: Set[str] = stop_words or set()
        # Compile regex once at initialization for maximum throughput
        self.clean_regex = re.compile(r"[^a-zA-Z0-9\s]")
        self.whitespace_regex = re.compile(r"\s+")

    def clean_and_tokenize(self, raw_text: str) -> List[str]:
        # 1. Lowercase
        text = raw_text.lower()
        # 2. Remove punctuation
        text = self.clean_regex.sub(" ", text)
        # 3. Collapse multiple whitespace
        text = self.whitespace_regex.sub(" ", text).strip()
        # 4. Tokenize and filter stopwords
        return [tok for tok in text.split(" ") if tok and tok not in self.stop_words]

normalizer = TextNormalizer(stop_words={"the", "is", "a", "of"})
prompt = "The Large Language Model (LLM) is capable of reasoning!"
tokens = normalizer.clean_and_tokenize(prompt)
print(f"Cleaned tokens: {tokens}")
# ['large', 'language', 'model', 'llm', 'capable', 'reasoning']
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Quadratic String Concatenation in Loops
Repeatedly appending strings in a loop with `+=` creates $N$ intermediate strings, leading to $O(N^2)$ execution time.

```python
# ANTI-PATTERN: O(N^2) time
result = ""
for tok in ["tok1", "tok2", "tok3"]:
    result += tok + " "

# PRODUCTION PATTERN: O(N) time using join
result = " ".join(["tok1", "tok2", "tok3"])
```

### 2. `split()` with No Arguments vs `split(" ")`
`s.split()` collapses multiple whitespace and strips leading/trailing spaces. `s.split(" ")` keeps empty string entries!

```python
s = "  hello   world  "
print(s.split())     # ['hello', 'world']
print(s.split(" ")) # ['', '', 'hello', '', '', 'world', '', '']
```

---

## 6. Interview Questions & Coding Traps

### Q1: What is string interning and when does Python perform it?
CPython automatically interns string literals that look like valid Python identifiers (letters, digits, underscores). Interning ensures that identical string literals share the same memory location, allowing constant-time $O(1)$ pointer comparisons via `is` instead of $O(N)$ character-by-character comparisons via `==`.

### Q2: Write an algorithm to check if a string contains valid parentheses:
```python
def is_valid_parentheses(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    return not stack
```
**Complexity:** Time: $O(N)$, Space: $O(N)$.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Indexing `s[i]` | $O(1)$ | $O(1)$ |
| Slicing `s[i:j]` | $O(K)$ where $K = j - i$ | $O(K)$ |
| `"sep".join(list_of_strings)` | $O(N)$ total characters | $O(N)$ |
| String Concatenation in Loop (`+=`) | $O(N^2)$ | $O(N^2)$ |
