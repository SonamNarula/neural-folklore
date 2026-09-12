# Pandas Data Cleaning and Preparation

> Data cleaning transforms noisy, incomplete, and malformed raw datasets into sanitized, high-integrity tabular representations suitable for ML modeling.

---

## 1. Why This Matters

### Why This Concept Exists
Real-world data is dirty: missing values (`NaN`), duplicate rows, corrupted categorical strings, and extreme statistical outliers. Garbage in produces garbage out in machine learning.

### Why Python Developers Need It
Over 70% of an AI/ML engineer's workflow is spent on data cleaning, schema validation, and normalization.

### Why It Matters Specifically in AI/ML/GenAI
- **Missing Value Imputation**: Algorithms like Linear Regression, SVMs, and neural networks crash on `NaN` values. Imputation strategies (mean, median, iterative) must be applied systematically.
- **Categorical Normalization**: Inconsistent text categories (`"Male"`, `"male"`, `" M "`) must be unified before one-hot or target encoding.
- **Outlier Removal**: Skewed target distributions or extreme feature anomalies corrupt loss gradients during model training.

### Where It Appears in Real Projects
- ETL feature pipelines.
- Data validation before fine-tuning datasets.
- Tabular preprocessing in Scikit-Learn pipelines.

---

## 2. Core Concept

### 2.1 Handling Missing Data (`isna`, `dropna`, `fillna`)
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "age": [25, np.nan, 30, 22, np.nan],
    "salary": [50000, 60000, np.nan, 45000, 70000],
    "department": ["AI", "Data", "AI", None, "Eng"]
})

# 1. Detect missingness
print("Missing counts:
", df.isna().sum())

# 2. Impute numeric columns with median (resilient to outliers)
median_age = df["age"].median()
df["age"] = df["age"].fillna(median_age)

# 3. Impute categorical with mode or constant
df["department"] = df["department"].fillna("Unknown")
```

### 2.2 Deduplication and String Sanitization
```python
# Strip whitespace and lowercase strings across column
df["department"] = df["department"].str.strip().str.lower()

# Drop duplicate records based on subset of unique keys
df = df.drop_duplicates(subset=["age", "department"], keep="first")
```

---

## 3. Mental Model

```text
Data Cleaning Pipeline Flow:
Raw Ingestion ──► Strip Whitespace & Lowercase ──► Handle Missing (Impute/Drop)
                       │
                       ▼
             Deduplicate Records ──► Filter Outliers ──► Sanitized Output
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Robust Pre-Training Tabular Sanitizer
A production cleaner that handles missing values, clips outliers via Interquartile Range (IQR), and downcasts dtypes:

```python
import pandas as pd
import numpy as np

class TabularDataCleaner:
    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        cleaned = df.copy()

        # 1. Clean string columns
        for col in cleaned.select_dtypes(include=["object"]).columns:
            cleaned[col] = cleaned[col].astype(str).str.strip().str.lower()

        # 2. Impute numeric missing values with median
        for col in cleaned.select_dtypes(include=[np.number]).columns:
            if cleaned[col].isnull().any():
                med = cleaned[col].median()
                cleaned[col] = cleaned[col].fillna(med)

            # 3. Outlier clipping via IQR (Interquartile Range)
            q25 = cleaned[col].quantile(0.25)
            q75 = cleaned[col].quantile(0.75)
            iqr = q75 - q25
            lower_bound = q25 - (1.5 * iqr)
            upper_bound = q75 + (1.5 * iqr)
            cleaned[col] = cleaned[col].clip(lower=lower_bound, upper=upper_bound)

        return cleaned

raw_df = pd.DataFrame({
    "prompt_length": [50, 45, 10000, 60, np.nan],  # 10000 is an extreme outlier!
    "category": [" NLP ", "cv", np.nan, "NLP", "llm"]
})
processed = TabularDataCleaner.clean(raw_df)
print(processed)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Data Leakage During Imputation
Computing mean or median on the **entire dataset** (train + test) before splitting leaks test set distributions into training data! Always calculate statistics **exclusively on the training split** and use those values to fill both train and test.

### 2. `np.nan == np.nan` Evaluates to `False`!
In accordance with IEEE 754 floating point standard:
```python
print(np.nan == np.nan)  # False!
# ALWAYS use pd.isna() or np.isnan()
print(pd.isna(np.nan))   # True
```

---

## 6. Interview Questions & Coding Traps

### Q1: When should you drop missing rows versus imputing them?
- **Drop**: When missingness is rare (< 2-5%), completely at random (MCAR), and dataset size is large; or when the target label `y` is missing.
- **Impute**: When dropping rows introduces significant data loss or sample selection bias, or when features are informative despite missingness.

### Q2: What is the difference between `dropna(axis=0)` and `dropna(axis=1)`?
- `axis=0` drops **rows** that contain missing values.
- `axis=1` drops entire **columns** that contain missing values.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| `df.isna().sum()` | $O(N \cdot C)$ | $O(C)$ |
| `df.fillna(val)` | $O(N \cdot C)$ | $O(N \cdot C)$ (or $O(1)$ if `inplace=True`) |
| `df.drop_duplicates()` | $O(N)$ hash table deduplication | $O(N)$ |
