# Feature Engineering in Python

> Feature engineering transforms raw attributes into high-signal numerical representations that expose underlying patterns to machine learning algorithms.

---

## 1. Why This Matters

### Why This Concept Exists
Machine learning algorithms cannot process raw strings, unstructured timestamps, or disparate scales directly. Feature engineering creates the mathematical representations algorithms learn from.

### Why Python Developers Need It
Feature engineering is the single most impactful lever for improving model performance on tabular and text data.

### Why It Matters Specifically in AI/ML/GenAI
- **Scaling for Gradient Descent**: Neural networks and linear models diverge or crawl if feature scales differ wildly (e.g., age 0-100 vs income 0-1,000,000).
- **Categorical Encodings**: High-cardinality categorical variables (e.g., zip codes, product IDs) require target or frequency encoding to avoid dimensional explosion.
- **TF-IDF & N-Gram Text Features**: Combining classical TF-IDF text features with modern dense neural embeddings (Hybrid Search).

### Where It Appears in Real Projects
- Production tabular feature stores.
- Feature extraction pipelines in Scikit-Learn.
- Hybrid search retrieval scoring in vector engines.

---

## 2. Core Concept

### 2.1 Numerical Scalers
- **`StandardScaler`**: Centers to mean $\mu = 0$, unit variance $\sigma = 1$: $z = rac{x - \mu}{\sigma}$. (Assumes normal distribution).
- **`MinMaxScaler`**: Scales to fixed interval $[0, 1]$: $x_{	ext{scaled}} = rac{x - x_{\min}}{x_{\max} - x_{\min}}$.
- **`RobustScaler`**: Uses median and Interquartile Range (IQR): $x_{	ext{scaled}} = rac{x - Q_2}{Q_3 - Q_1}$. (Resilient to extreme outliers!).

### 2.2 Categorical Encoders
- **One-Hot Encoding**: Converts low-cardinality categories into binary columns.
- **Target / Out-of-Fold Encoding**: Replaces categories with the expected target value for high-cardinality features.

### 2.3 Text Vectorization: TF-IDF
$$	ext{TF-IDF}(t, d, D) = 	ext{TF}(t, d) 	imes \log\left(rac{|D|}{|\{d \in D : t \in d\}|}ight)$$

---

## 3. Mental Model

```text
Categorical Transformation:
Category Column: ["AI", "Data", "AI"]
        │
        ├──► One-Hot:    [ [1, 0], [0, 1], [1, 0] ] (Adds D columns)
        └──► Target Enc: [ 0.85,   0.45,   0.85   ] (Replaced with target probability)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Hybrid Feature Pipeline (Tabular Scalers + Text TF-IDF)
Combining structured tabular metrics with unstructured text features:

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.DataFrame({
    "prompt_text": [
        "Explain quantum computing",
        "Generate a Python function",
        "Explain machine learning"
    ],
    "model_tier": ["pro", "free", "pro"],
    "latency_budget_ms": [500.0, 150.0, 300.0]
})

# Composite ColumnTransformer applying distinct transformations per column
preprocessor = ColumnTransformer(
    transformers=[
        ("text", TfidfVectorizer(max_features=10), "prompt_text"),
        ("cat", OneHotEncoder(drop="first"), ["model_tier"]),
        ("num", StandardScaler(), ["latency_budget_ms"])
    ]
)

feature_matrix = preprocessor.fit_transform(data)
print("Engineered Feature Matrix Shape:", feature_matrix.shape)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. High-Cardinality One-Hot Explosion
One-hot encoding a column with 10,000 unique categories creates 10,000 sparse columns, which slows down tree training and risks memory crashes! Use Target Encoding or Frequency Encoding instead.

### 2. Unseen Categories at Inference Time
If test data contains a category not present in training data, `OneHotEncoder` raises an error by default. Always set `handle_unknown="ignore"`.

---

## 6. Interview Questions & Coding Traps

### Q1: When should you use `RobustScaler` over `StandardScaler`?
`StandardScaler` calculates mean and variance, which are heavily distorted by extreme statistical outliers. `RobustScaler` uses the **median** and **Interquartile Range (IQR)**, making it robust against outliers.

### Q2: What is Target Encoding and why can it cause severe overfitting without regularization?
Target encoding replaces each categorical value with the average target value for that category. If a category occurs only once (e.g. `User_999` with target `1`), the model memorizes that `User_999` is a perfect predictor, leading to target leakage and extreme overfitting. Mitigate using Out-Of-Fold (OOF) target encoding or smoothing regularization.

### Complexity Reference
| Transformation | Fit Time | Transform Time |
| :--- | :--- | :--- |
| `StandardScaler` | $O(N \cdot D)$ compute mean/std | $O(N \cdot D)$ |
| `OneHotEncoder` | $O(N \cdot D)$ find unique | $O(N \cdot K)$ where $K = \sum 	ext{cardinality}$ |
| `TfidfVectorizer` | $O(N \cdot L)$ scan vocab | $O(N \cdot L)$ sparse matrix assembly |
