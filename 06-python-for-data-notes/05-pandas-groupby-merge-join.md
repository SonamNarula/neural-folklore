# Pandas GroupBy, Merge, and Join

> GroupBy implements the Split-Apply-Combine pattern for group-level aggregations; Merge and Join perform relational database joins across shared key indices.

---

## 1. Why This Matters

### Why This Concept Exists
Single tabular records rarely tell the full story. Data must be sliced, categorized, aggregated, and joined against external dimensions to extract meaningful analytical and predictive signals.

### Why Python Developers Need It
Relational joins and aggregation are core SQL concepts that Python developers must execute natively within memory.

### Why It Matters Specifically in AI/ML/GenAI
- **Group-Level Aggregation Features**: Creating rolling user features (e.g., user mean transaction amount, session token velocity).
- **Evaluating Metrics by Slice**: In GenAI, evaluating model accuracy across task categories (`df.groupby('task_type')['accuracy'].mean()`).
- **Joining Feature Stores**: Merging static user demographic tables with dynamic real-time event logs.

### Where It Appears in Real Projects
- Feature stores (Feast, Hopsworks).
- Model evaluation and error analysis dashboards.
- Multi-table dataset preparation.

---

## 2. Core Concept

### 2.1 The Split-Apply-Combine Paradigm
1. **Split**: Break DataFrame into chunks based on distinct key values.
2. **Apply**: Compute a function (e.g., `mean`, `sum`, custom lambda) on each chunk independently.
3. **Combine**: Assemble results back into a consolidated DataFrame.

```python
import pandas as pd

eval_df = pd.DataFrame({
    "model": ["gpt-4o", "gpt-4o", "claude-3-5", "claude-3-5"],
    "task": ["coding", "math", "coding", "math"],
    "latency": [1.2, 0.8, 1.1, 0.9],
    "score": [92, 88, 95, 84]
})

# GroupBy with multiple aggregations:
summary = eval_df.groupby("model").agg(
    avg_latency=("latency", "mean"),
    max_score=("score", "max")
)
print(summary)
```

### 2.2 Relational Merges (`merge` vs `join`)
- `pd.merge(df1, df2, on="key", how="inner|outer|left|right")`: Joins on arbitrary columns.
- `df1.join(df2)`: Convenience method joining primarily on Index keys.

```python
users = pd.DataFrame({"user_id": [1, 2, 3], "tier": ["free", "pro", "enterprise"]})
logs = pd.DataFrame({"user_id": [1, 1, 2], "tokens_used": [150, 200, 500]})

# Left join preserves all logs and attaches user tier:
merged = pd.merge(logs, users, on="user_id", how="left")
print(merged)
```

---

## 3. Mental Model

```text
Split-Apply-Combine:
Table               Split by Model         Apply Mean             Combine
[ gpt-4o    | 92 ]  ──► [ 92, 88 ] ──► mean = 90.0 ──► [ gpt-4o    | 90.0 ]
[ gpt-4o    | 88 ]
[ claude-35 | 95 ]  ──► [ 95, 84 ] ──► mean = 89.5 ──► [ claude-35 | 89.5 ]
[ claude-35 | 84 ]
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Model Benchmark Performance Analyzer by Category
Aggregating LLM benchmark runs to identify domain weaknesses:

```python
import pandas as pd

benchmarks = pd.DataFrame({
    "model_name": ["ModelA", "ModelA", "ModelA", "ModelB", "ModelB", "ModelB"],
    "domain": ["medical", "legal", "coding", "medical", "legal", "coding"],
    "accuracy": [0.85, 0.90, 0.72, 0.88, 0.84, 0.91],
    "latency_sec": [2.1, 1.8, 3.4, 1.5, 1.4, 2.0]
})

# Transform: Add group mean as a column without collapsing rows (useful for feature engineering!)
benchmarks["domain_avg_acc"] = benchmarks.groupby("domain")["accuracy"].transform("mean")

# Relative performance vs domain benchmark:
benchmarks["diff_from_avg"] = benchmarks["accuracy"] - benchmarks["domain_avg_acc"]
print(benchmarks[["model_name", "domain", "accuracy", "diff_from_avg"]])
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. The `merge` Cartesian Explosion
If duplicate keys exist in both DataFrames during a merge, Pandas creates the **Cartesian product** of all matching rows, multiplying row counts exponentially and causing out-of-memory crashes! Always verify key uniqueness before merging.

### 2. GroupBy Drops Missing Keys by Default
In older Pandas versions, `groupby` automatically drops `NaN` keys. Use `dropna=False` to preserve missing groupings: `df.groupby("category", dropna=False)`.

---

## 6. Interview Questions & Coding Traps

### Q1: What is the difference between `.agg()` and `.transform()` in GroupBy?
- `.agg()` reduces each group to a **single summary scalar value**, returning a DataFrame with row count equal to the number of unique groups.
- `.transform()` computes an aggregation but returns an array with the **exact same row count and index as the original DataFrame**, broadcasting the group scalar back to every row in that group.

### Q2: What is `pd.merge_asof` and where is it used?
`pd.merge_asof` is an approximate join on ordered keys (such as timestamps). Instead of requiring exact key matches, it matches on the nearest key (e.g., joining quotes to trades where the trade timestamp occurred within 10ms of the quote). Crucial for financial and high-frequency time-series ML pipelines.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| `df.groupby('col').mean()` | $O(N)$ hash-based partitioning | $O(K)$ unique groups |
| Hash Merge (`how='inner'`) | $O(N + M)$ | $O(N + M)$ |
| Transform (`groupby.transform`)| $O(N)$ | $O(N)$ |
