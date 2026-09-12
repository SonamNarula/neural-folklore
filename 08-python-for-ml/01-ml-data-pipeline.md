# Machine Learning Data Pipelines and Leakage Prevention

> An ML data pipeline is a reproducible, isolated directed acyclic graph (DAG) transforming raw records into model tensors while preventing information leakage between training and evaluation splits.

---

## 1. Why This Matters

### Why This Concept Exists
Machine learning models fail in production not because of algorithmic flaws, but because of **Data Leakage**—unintentionally exposing information from the test or validation set to the training phase.

### Why Python Developers Need It
Building isolated, leak-free preprocessing pipelines ensures offline validation scores match real-world production performance.

### Why It Matters Specifically in AI/ML/GenAI
- **Feature Standardization Leakage**: Fitting a `StandardScaler` on the entire dataset before splitting leaks the test set's mean and variance into training features.
- **Target Encoding Leakage**: Calculating category target probabilities using the full dataset results in catastrophic overfitting.
- **RAG Evaluation Contamination**: Including test queries in the retrieval knowledge base causes inflated retrieval precision.

### Where It Appears in Real Projects
- Production training scripts in Kubeflow, Airflow, and MLflow.
- Kaggle competition winning pipelines.
- Feature engineering in Scikit-Learn pipelines.

---

## 2. Core Concept

### 2.1 Types of Data Leakage
1. **Train-Test Contamination**: Fitting transformers (imputers, scalers, encoders) on the entire dataset before splitting.
2. **Temporal Leakage**: In time-series forecasting, using future records to predict past events (random splitting instead of time-ordered splitting).
3. **Group / Duplication Leakage**: Having multiple records from the same patient/user split across both train and test sets.

```python
# CATASTROPHIC LEAKAGE:
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np

X = np.random.randn(100, 5)
y = np.random.randint(0, 2, 100)

# BUG: Scaler fitted on test data!
# scaler = StandardScaler().fit(X)  <-- LEAK!
# X_train, X_test, y_train, y_test = train_test_split(scaler.transform(X), y)

# CORRECT LEAK-FREE PIPELINE:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Fit ONLY on training data!
X_test_scaled = scaler.transform(X_test)        # Transform test using train statistics!
```

---

## 3. Mental Model

```text
The Leak-Free Firewall:
Raw Data
   │
   ▼
[ Train / Test Split ] (Strict Firewall)
   │               │
   ▼ (Train Set)   ▼ (Test Set - Held Out Vault)
Fit Scaler         │
Transform Train    │
   │               │
   ▼               ▼
Train Model ──► Evaluate on Test (Transformed using Train Scaler)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Deterministic Partitioning with Group-Aware Splitting
Ensuring multiple records from the same user never span across both train and validation sets:

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

def split_by_group_leak_free(
    df: pd.DataFrame,
    group_col: str,
    test_size: float = 0.2
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Partitions DataFrame ensuring all records from any given group
    appear strictly in train OR test, never in both.
    """
    gss = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=42)
    train_idx, test_idx = next(gss.split(df, groups=df[group_col]))

    train_df = df.iloc[train_idx].reset_index(drop=True)
    test_df = df.iloc[test_idx].reset_index(drop=True)

    # Verification assertion:
    overlap = set(train_df[group_col]) & set(test_df[group_col])
    assert len(overlap) == 0, f"Leakage detected! Shared groups: {overlap}"

    return train_df, test_df

# Simulation: Multiple interactions per user
sample_data = pd.DataFrame({
    "user_id": ["usr_1", "usr_1", "usr_2", "usr_3", "usr_3", "usr_4"],
    "interaction_score": [0.8, 0.9, 0.4, 0.95, 0.7, 0.3],
    "target": [1, 1, 0, 1, 1, 0]
})

train_split, test_split = split_by_group_leak_free(sample_data, group_col="user_id")
print("Train Users:", train_split["user_id"].unique())
print("Test Users: ", test_split["user_id"].unique())
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Imbalanced Target Splits
Using standard `train_test_split` on rare-event data (e.g., 1% positive class) can result in a test set containing **zero** positive samples! Always use `stratify=y`.

---

## 6. Interview Questions & Coding Traps

### Q1: What is target leakage and how do you detect it?
Target leakage occurs when an input feature includes information that is only available *after* the target event occurs (e.g., using "hospital_discharge_date" to predict "patient_length_of_stay"). It is typically detected when a model achieves unrealistically high validation metrics (e.g. 0.999 AUC) and feature importance shows one dominant feature.

### Complexity Reference
| Split Strategy | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Random Train-Test Split | $O(N)$ | $O(N)$ copies |
| Stratified / Group Split | $O(N \log N)$ (sorting groups/labels) | $O(N)$ |
