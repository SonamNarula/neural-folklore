# Pydantic v2 and Structured Data Validation

> Pydantic enforces data contracts and type safety at runtime using Rust-backed validation (`pydantic-core`), generating OpenAPI / JSON Schema specifications for LLM structured outputs.

---

## 1. Why This Matters

### Why This Concept Exists
Type hints in standard Python provide static verification (`mypy`), but zero runtime enforcement. External data from users or LLMs often contains missing keys, wrong types, and invalid bounds. Pydantic guarantees runtime data integrity.

### Why Python Developers Need It
Pydantic is the foundational data validation layer of FastAPI, LangChain, Instructor, and modern OpenAI structured output frameworks.

### Why It Matters Specifically in AI/ML/GenAI
- **LLM Structured Outputs**: Modern LLM APIs accept Pydantic models directly to constrain model generation to valid JSON Schema schemas (`client.beta.chat.completions.parse(response_format=MySchema)`).
- **Agent Tool Parameter Validation**: Validating that arguments emitted by an LLM for tool calling strictly match required types and constraints.
- **API Request/Response Schemas**: Powering FastAPI inference endpoints.

### Where It Appears in Real Projects
- OpenAI `response_format=PydanticModel`.
- FastAPI route validation schemas.
- Instructor library for reliable entity extraction.

---

## 2. Core Concept

### 2.1 Pydantic v2 `BaseModel` & `Field`
```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal

class ExtractedEntity(BaseModel):
    name: str = Field(..., description="The full name of the identified entity")
    category: Literal["PERSON", "ORG", "LOCATION"]
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")

class DocumentEntities(BaseModel):
    document_id: str
    entities: List[ExtractedEntity]
```

### 2.2 Field Validators & Model Validators
- `@field_validator`: Validates individual attributes.
- `@model_validator`: Validates relationships across multiple attributes.

```python
from pydantic import field_validator

class GenerationConfig(BaseModel):
    temperature: float = 0.7
    max_tokens: int = 512

    @field_validator("temperature")
    @classmethod
    def validate_temp(cls, v: float) -> float:
        if not (0.0 <= v <= 2.0):
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v
```

### 2.3 Generating JSON Schema for LLMs
Pydantic models convert directly to JSON Schema:
```python
schema = DocumentEntities.model_json_schema()
# Passed directly to OpenAI or Anthropic tool definitions!
```

---

## 3. Mental Model

```text
Pydantic Validation Funnel:
Raw Untrusted JSON (from LLM or HTTP request)
                 │
                 ▼
     [ Pydantic-Core Engine (Rust) ]
      - Type Coercion ("42" -> 42)
      - Constraint Checks (ge=0.0, le=1.0)
      - Custom Validator Execution
                 │
          ┌──────┴──────┐
          ▼ Valid       ▼ Invalid
   Verified Object     ValidationError (Detailed JSON error report)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Structured LLM Output Extractor with Schema Self-Correction
Validating and enforcing structured outputs extracted from unstructured text:

```python
from pydantic import BaseModel, Field, ValidationError
from typing import List

class SentimentAnalysisReport(BaseModel):
    sentiment: str = Field(..., description="Must be 'positive', 'neutral', or 'negative'")
    confidence: float = Field(..., ge=0.0, le=1.0)
    key_phrases: List[str] = Field(default_factory=list, max_length=5)

def safe_parse_llm_json(raw_json_str: str) -> SentimentAnalysisReport | None:
    try:
        # Pydantic v2: model_validate_json directly parses JSON strings at Rust speed!
        report = SentimentAnalysisReport.model_validate_json(raw_json_str)
        return report
    except ValidationError as err:
        print("Schema validation failed! Errors:")
        for error in err.errors():
            print(f" - Field '{error['loc'][0]}': {error['msg']}")
        return None

# Valid JSON payload:
valid_json = '{"sentiment": "positive", "confidence": 0.94, "key_phrases": ["fast inference", "accurate"]}'
report = safe_parse_llm_json(valid_json)
print("Parsed report successfully:", report.sentiment, report.confidence)

# Invalid JSON payload (triggers validation error):
invalid_json = '{"sentiment": "positive", "confidence": 1.5}'
safe_parse_llm_json(invalid_json)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Pydantic v1 vs v2 Syntax Migrations
- `.dict()` is deprecated; use `.model_dump()` in v2.
- `.parse_raw()` is deprecated; use `.model_validate_json()` in v2.
- `.schema()` is deprecated; use `.model_json_schema()` in v2.

### 2. Unintended Type Coercion
By default, Pydantic coerces compatible types (e.g., string `"123"` coerced to integer `123`). If strict typing is required, configure `model_config = ConfigDict(strict=True)`.

---

## 6. Interview Questions & Coding Traps

### Q1: Why is Pydantic v2 so much faster than Pydantic v1?
Pydantic v2 rewrote the core validation and serialization logic in **Rust** (`pydantic-core`). Python types and validation rules are compiled into a Rust validation tree, speeding up parsing by **5x to 50x**.

### Complexity Reference
| Operation | Pydantic v1 (Pure Python) | Pydantic v2 (Rust Core) |
| :--- | :--- | :--- |
| Model Validation | $O(N)$ Python bytecode loops | $O(N)$ compiled Rust routines (~10x-50x faster) |
| JSON Serialization | Python dict conversion + `json.dumps` | Direct Rust-level byte serialization |
