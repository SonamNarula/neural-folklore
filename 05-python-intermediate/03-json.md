# JSON and Serialization in Python

> JSON serialization translates in-memory Python object graphs into standard UTF-8 text representations (`dumps`) and reconstructs object graphs from text (`loads`).

---

## 1. Why This Matters

### Why This Concept Exists
Heterogeneous systems (browsers, Python servers, Rust microservices, C++ inference runtimes) require language-agnostic data serialization. JSON is the universal lingua franca of the web.

### Why Python Developers Need It
Interacting with APIs, storing experiment configs, and formatting LLM outputs all depend heavily on robust JSON serialization and custom encoders.

### Why It Matters Specifically in AI/ML/GenAI
- **LLM Structured Outputs & Function Calling**: Modern GenAI relies on asking models to emit JSON conforming to rigid JSON Schema definitions.
- **Fine-Tuning Datasets (`.jsonl`)**: OpenAI, Anthropic, and HuggingFace fine-tuning data is standardized on JSON Lines format.
- **Model Metadata & Tokenizer Configs**: Model configurations (`config.json`, `tokenizer.json`) are stored as JSON.

### Where It Appears in Real Projects
- OpenAI Structured Outputs (`response_format={"type": "json_object"}`).
- Hugging Face `tokenizer.json` files.
- ML experiment tracking configuration dumps.

---

## 2. Core Concept

### 2.1 The Standard Trinity: `dump`, `dumps`, `load`, `loads`
- `dumps(obj)`: Serializes Python object to a JSON **string**.
- `loads(json_str)`: Deserializes JSON string into a Python object.
- `dump(obj, file)`: Serializes Python object directly to an open **file**.
- `load(file)`: Deserializes JSON directly from an open **file**.

```python
import json

data = {"model": "llama-3", "quantization": "int8", "layers": 32}
# Serialize to string
json_str = json.dumps(data, indent=2)
# Deserialize back to dict
reconstructed = json.loads(json_str)
```

### 2.2 Custom JSON Encoders
By default, `json.dumps()` raises `TypeError` when encountering non-standard objects like `datetime`, `set`, `numpy.ndarray`, or custom classes.

```python
import json
from datetime import datetime

class CustomMLEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

payload = {"created_at": datetime.now(), "features": {"age", "income"}}
serialized = json.dumps(payload, cls=CustomMLEncoder)
print(serialized)
```

---

## 3. Mental Model

```text
JSON Serialization Mapping:
Python Type                     JSON Type
dict         ◄────────────────► object { ... }
list, tuple  ◄────────────────► array  [ ... ]
str          ◄────────────────► string " ... "
int, float   ◄────────────────► number 12, 3.14
True / False ◄────────────────► true / false
None         ◄────────────────► null
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: OpenAI Fine-Tuning JSONL Dataset Validator
Validating chat completion schemas prior to uploading to OpenAI Fine-Tuning endpoints:

```python
import json
from typing import List, Dict, Any

class FineTuningValidator:
    REQUIRED_ROLES = {"system", "user", "assistant"}

    @classmethod
    def validate_row(cls, row_idx: int, raw_line: str) -> tuple[bool, str]:
        try:
            data = json.loads(raw_line)
        except json.JSONDecodeError as err:
            return False, f"Row {row_idx}: Malformed JSON syntax ({err})"

        if not isinstance(data, dict) or "messages" not in data:
            return False, f"Row {row_idx}: Must contain top-level 'messages' key"

        messages = data["messages"]
        if not isinstance(messages, list) or len(messages) < 2:
            return False, f"Row {row_idx}: 'messages' must be a list with at least 2 turns"

        for m_idx, msg in enumerate(messages):
            if "role" not in msg or "content" not in msg:
                return False, f"Row {row_idx}, message {m_idx}: Missing 'role' or 'content'"
            if msg["role"] not in cls.REQUIRED_ROLES:
                return False, f"Row {row_idx}: Invalid role '{msg['role']}'"

        return True, "Valid"

sample_row = json.dumps({
    "messages": [
        {"role": "system", "content": "You are a coding assistant."},
        {"role": "user", "content": "Write quicksort in Python."},
        {"role": "assistant", "content": "def quicksort(arr): ..."}
    ]
})
valid, msg = FineTuningValidator.validate_row(0, sample_row)
print("Validation Result:", valid, "|", msg)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Tuples Become Lists in Round-Trip Serialization
JSON has no tuple type. Serializing a tuple converts it to a JSON array; deserializing returns a Python `list`!

```python
tup = (1, 2, 3)
res = json.loads(json.dumps(tup))
print(type(res), res)  # <class 'list'> [1, 2, 3]!
```

### 2. Dictionary Keys Must Be Strings
In Python, `d = {1: "one"}` is valid. In JSON, all keys must be strings. `json.dumps(d)` converts the integer key `1` to string `"1"`.

---

## 6. Interview Questions & Coding Traps

### Q1: Why is `orjson` or `ujson` preferred over the standard `json` module in high-throughput LLM serving?
The standard `json` module is written in pure Python with C accelerators, but it does not vectorize UTF-8 encoding. Third-party libraries like `orjson` (written in Rust) are **10x-20x faster**, handle `numpy` arrays and `dataclasses` natively, and output raw bytes directly for ASGI servers.

### Q2: What is the output of `json.dumps(float('nan'))`?
The standard Python `json` library serializes `float('nan')` to `NaN`. However, `NaN` is **strictly invalid JSON** per RFC 8259! Passing `allow_nan=False` forces Python to raise `ValueError`.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| `json.dumps(obj)` | $O(N)$ object graph traversal | $O(N)$ string buffer |
| `json.loads(s)` | $O(N)$ token scanning & parsing | $O(N)$ dict/list heap objects |
