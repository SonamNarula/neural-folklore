# Advanced Data Processing Patterns & Polars Comparison

> Production data engineering emphasizes memory optimization, zero-copy transformations, columnar efficiency, and migration from Pandas to Rust-backed Polars.

---

## 1. Why This Matters

### Why This Concept Exists
Pandas creates multiple intermediate copies of DataFrames and relies on single-threaded execution, causing performance degradation on multi-gigabyte datasets. Modern pipelines leverage memory downcasting, categorical encodings, and modern engines like Polars.

### Why Python Developers Need It
Knowing how to process 10GB datasets on a machine with 16GB of RAM without crashing separates senior data engineers from novices.

### Why It Matters Specifically in AI/ML/GenAI
- **Feature Pipeline Scaling**: Preparing multi-million row training datasets without exceeding cluster RAM limits.
- **Categorical Memory Optimization**: Converting high-cardinality string columns to categorical indices can slash memory consumption by 80-90%.
- **Polars Integration**: Polars is now widely adopted in production AI pipelines due to multi-threaded execution and lazy evaluation query optimization.

### Where It Appears in Real Projects
- Offline feature engineering pipelines in Spark, Ray, and Polars.
- Dataset preparation scripts in large-scale LLM training clusters.
- Low-latency feature generation in inference serving APIs.

---

## 2. Core Concept

### 2.1 Memory Optimization via Dtype Downcasting
By default, Pandas assigns 64-bit types (`int64`, `float64`). Downcasting to `int8`, `int16`, or `float32` drastically reduces memory consumption:

```python
import pandas as pd
import numpy as np

def downcast_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Downcasts float64 and int64 columns to lowest safe precision."""
    optimized = df.copy()
    for col in optimized.select_dtypes(include=["int64"]).columns:
        optimized[col] = pd.to_numeric(optimized[col], downcast="integer")
    for col in optimized.select_dtypes(include=["float64"]).columns:
        optimized[col] = pd.to_numeric(optimized[col], downcast="float")
    return optimized
```

### 2.2 Categorical Dtypes for String Optimization
Converting repetitive string columns (e.g., country codes, status flags) to `category` stores strings once in a lookup table and replaces column entries with compact integer pointers.

```python
s = pd.Series(["approved", "pending", "rejected"] * 100_000)
print(f"Object string size: {s.memory_usage(deep=True) / (1024**2):.2f} MB")
s_cat = s.astype("category")
print(f"Categorical size:   {s_cat.memory_usage(deep=True) / (1024**2):.2f} MB")  # ~90% memory reduction!
```

### 2.3 Pandas vs Polars: The Architectural Shift
| Feature | Pandas | Polars |
| :--- | :--- | :--- |
| Backend Engine | C / Python | Written in Rust (Apache Arrow memory format) |
| Execution Model | Single-threaded | Multi-threaded parallelism across all CPU cores |
| Evaluation Mode | Eager (executes line-by-line) | Lazy Evaluation (optimizes entire query plan via `scan_parquet`) |
| Memory Copies | Frequent intermediate copies | Zero-copy slicing & streaming execution |

---

## 3. Mental Model

```text
Pandas Eager vs Polars Lazy Pipeline:
Pandas (Eager):
Step 1: Read CSV (Loads entire 10GB into RAM) ──►
Step 2: Filter Rows (Allocates another 4GB)   ──►
Step 3: GroupBy (Allocates another 1GB)       ──► Result

Polars (Lazy):
pl.scan_csv("data.csv").filter(...).group_by(...)
        │
        ▼ Query Optimizer (Pushes filter down to CSV scanner)
Streams ONLY required columns and matching rows directly into memory!
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Modern High-Performance Pipeline with Polars
Demonstrating lazy execution and multi-threaded grouping in Polars:

```python
# Conceptual Polars workflow (runnable if polars installed):
"""
import polars as pl

# 1. Define LazyFrame (Query execution plan, not executed yet!)
lazy_query = (
    pl.scan_parquet("large_dataset.parquet")
    .filter(pl.col("latency_ms") > 100)
    .group_by("model_name")
    .agg([
        pl.col("tokens").mean().alias("avg_tokens"),
        pl.col("latency_ms").max().alias("max_latency")
    ])
    .sort("avg_tokens", descending=True)
)

# 2. Execute optimized query plan in parallel:
result_df = lazy_query.collect()
"""
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. In-place Mutation Fallacy in Pandas
Methods like `df.dropna(inplace=True)` often do NOT save memory! In many internal operations, Pandas still creates an internal copy before rebinding pointers. Modern Pandas best practices discourage `inplace=True`.

---

## 6. Interview Questions & Coding Traps

### Q1: What is Apache Arrow and why does it matter for modern data processing?
Apache Arrow is an open-source, language-independent columnar memory format. It allows zero-copy data exchange between Python, Rust, C++, and GPU memory (PyTorch) without serialization or deserialization overhead.

### Q2: What are the primary optimization techniques to process datasets larger than available RAM in Python?
1. **Chunked Reading**: Process data in mini-batches via `chunksize` parameter in `pd.read_csv()`.
2. **Column Pruning**: Specify `usecols` to load only the subset of columns required.
3. **Type Downcasting & Categoricals**: Downcast `float64` to `float32`, `int64` to `int32/int16`, strings to `category`.
4. **Parquet with Polars/DuckDB**: Use columnar formats that support predicate pushdown and memory streaming.

### Complexity Reference
| Strategy | Memory Reduction | Throughput Improvement |
| :--- | :--- | :--- |
| Downcasting floats & ints | ~50% | 1.5x - 2x faster cache hits |
| Object to Categorical | 80% - 95% | 2x - 5x faster grouping |
| Polars Lazy Execution | Up to 80% peak RAM reduction | 5x - 30x faster (multi-core parallelism) |
