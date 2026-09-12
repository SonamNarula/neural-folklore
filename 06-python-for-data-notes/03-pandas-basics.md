# Pandas Fundamentals: Series and DataFrames

> A Series is a 1D labeled homogeneous array; a DataFrame is an aligned 2D tabular container composed of column Series sharing a common Index.

---

## 1. Why This Matters

### Why This Concept Exists
Raw NumPy arrays lack labeled column names, heterogeneous column types, and relational index alignment. Pandas provides tabular data structures designed for structured data analysis and feature engineering.

### Why Python Developers Need It
Pandas is the primary tool for ingesting, exploring, and preprocessing tabular datasets prior to feeding features into ML models.

### Why It Matters Specifically in AI/ML/GenAI
- **Feature Matrices for Classical ML**: Preparing `X` (features DataFrame) and `y` (target Series) for Scikit-Learn / XGBoost / LightGBM models.
- **RAG Metadata Filtering**: Tabular metadata stores (document author, date, category) are queried and filtered with Pandas before passing retrieved documents to LLMs.
- **Prompt Generation from Datasets**: Converting CSV/Parquet tabular records into natural language prompt inputs.

### Where It Appears in Real Projects
- Exploratory Data Analysis (EDA) in Jupyter notebooks.
- Data ingestion pipelines reading CSV, Parquet, and SQL databases.
- Feature store preprocessing.

---

## 2. Core Concept

### 2.1 Series and DataFrame Architecture
```python
import pandas as pd

# Series: 1D labeled array
scores = pd.Series([0.95, 0.82, 0.77], index=["doc_A", "doc_B", "doc_C"], name="similarity")
print(scores["doc_A"])  # 0.95

# DataFrame: 2D table of aligned columns
df = pd.DataFrame({
    "doc_id": ["doc_A", "doc_B", "doc_C"],
    "similarity": [0.95, 0.82, 0.77],
    "token_count": [128, 256, 64]
})
```

### 2.2 Explicit Indexing: `loc` vs `iloc`
- **`loc`**: Label-based indexing (selects by index name / column name). Inclusive of both endpoints!
- **`iloc`**: Integer position-based indexing (selects by numeric 0-indexed position). Exclusive of stop endpoint!

```python
# Select first 2 rows by integer position:
print(df.iloc[0:2, :])

# Select by boolean condition using loc:
high_sim = df.loc[df["similarity"] > 0.80, ["doc_id", "similarity"]]
print(high_sim)
```

---

## 3. Mental Model

```text
Pandas DataFrame Structure:
          Column: "doc_id"   Column: "similarity"   Column: "tokens"
Index 0:    "doc_A"                0.95                  128
Index 1:    "doc_B"                0.82                  256
Index 2:    "doc_C"                0.77                   64
              ▲                      ▲                     ▲
              └───────── Each column is a NumPy ndarray ───┘
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Dataset Ingestion and Memory Footprint Audit
Inspecting and summarizing large dataset distributions before ML feature extraction:

```python
import pandas as pd
import numpy as np

def audit_dataset(df: pd.DataFrame) -> None:
    print("=== DATASET AUDIT ===")
    print(f"Dimensions: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / (1024**2):.2f} MB")
    print("
Missing Values Count:")
    print(df.isnull().sum())
    print("
Data Types:")
    print(df.dtypes)

sample_data = pd.DataFrame({
    "user_id": [f"usr_{i}" for i in range(1000)],
    "latency_ms": np.random.uniform(50, 300, 1000),
    "tokens": np.random.randint(10, 500, 1000),
    "error_code": [None if i % 10 != 0 else "TIMEOUT" for i in range(1000)]
})
audit_dataset(sample_data)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. `SettingWithCopyWarning`
Occurs when chaining indexers (`df[cond]['col'] = val`). Pandas cannot determine whether the slice is a view or a copy!

```python
# CATASTROPHIC BUG / WARNING:
# df[df["tokens"] > 100]["tokens"] = 100

# CORRECT: Use .loc in a single step!
sample_data.loc[sample_data["tokens"] > 100, "tokens"] = 100
```

### 2. Iterating with `for row in df.iterrows()` is Extremely Slow!
`iterrows()` converts each row into a Pandas Series, creating massive overhead. Always use vectorized column operations or `.to_dict('records')`.

---

## 6. Interview Questions & Coding Traps

### Q1: Why should you avoid `df.iterrows()` in production data pipelines?
`iterrows()` does not preserve dtypes across rows (it downcasts mixed types to `object`), and it executes in pure Python without vectorization, making it **100x to 1000x slower** than vectorized expressions or NumPy arrays.

### Q2: How does `df.loc[1:3]` differ from `df.iloc[1:3]`?
- `df.loc[1:3]` looks for index labels `1`, `2`, and `3`, and is **inclusive** of label `3`.
- `df.iloc[1:3]` looks strictly at positions 1 and 2, and is **exclusive** of position 3.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| `df[col]` | $O(1)$ column pointer retrieval | $O(1)$ |
| `df.iloc[i]` | $O(C)$ where $C$ is column count | $O(C)$ Series object |
| Vectorized column math (`df['a'] + df['b']`) | $O(N)$ contiguous C loop | $O(N)$ new Series |
