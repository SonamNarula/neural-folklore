# Train-Test Workflow and Cross-Validation

> Cross-validation systematically rotates training and validation partitions across the dataset to produce unbiased performance estimates and guide hyperparameter optimization.

---

## 1. Why This Matters

### Why This Concept Exists
Evaluating a model on a single train/test split introduces statistical variance—the model might perform well simply because it got lucky with an easy test split. Cross-validation provides robust confidence intervals on performance.

### Why Python Developers Need It
Every production ML pipeline requires systematic validation schemes to select hyperparameters, prevent overfitting, and ensure generalizability.

### Why It Matters Specifically in AI/ML/GenAI
- **Hyperparameter Optimization**: Systematically tuning tree depth, regularization parameters, learning rates, or prompt template variations.
- **Evaluating Small Datasets**: In domain-specific NLP (e.g., medical clinical notes), datasets are small (< 2,000 samples). K-Fold CV ensures every sample is used for validation.
- **TimeSeries Cross-Validation**: Evaluating forecasting models without violating causality.

### Where It Appears in Real Projects
- Model hyperparameter tuning scripts with Optuna and Scikit-Learn.
- Model card benchmark evaluation reporting.
- Offline reward modeling in Reinforcement Learning from Human Feedback (RLHF).

---

## 2. Core Concept: Cross-Validation Strategies

### 2.1 K-Fold Cross-Validation
Partitions data into $K$ equal folds. For each fold $k$, trains on $K-1$ folds and validates on fold $k$. Final score is the mean across all $K$ iterations.

### 2.2 Stratified K-Fold (Classification)
Guarantees that each fold preserves the **exact class percentage balance** of the original dataset. Mandatory for imbalanced datasets!

### 2.3 TimeSeriesSplit (Temporal Data)
Never trains on future data to validate on the past. Uses rolling or expanding windows forward in time.

```python
from sklearn.model_selection import StratifiedKFold
import numpy as np

X = np.random.randn(10, 2)
y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])  # 50% class balance

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
    val_labels = y[val_idx]
    print(f"Fold {fold} Val labels: {val_labels} (Preserves exact 50/50 balance!)")
```

---

## 3. Mental Model

```text
K-Fold Cross Validation (K=3):
Iteration 1: [ FOLD 1 (Val) ] [ FOLD 2 (Train) ] [ FOLD 3 (Train) ] ──► Metric 1
Iteration 2: [ FOLD 1 (Train) ] [ FOLD 2 (Val) ] [ FOLD 3 (Train) ] ──► Metric 2
Iteration 3: [ FOLD 1 (Train) ] [ FOLD 2 (Train) ] [ FOLD 3 (Val) ] ──► Metric 3
Average Validation Performance = Mean(Metric 1, 2, 3)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Automated Hyperparameter Grid Search within Cross-Validation
Tuning hyperparameter combinations while preventing validation contamination:

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier

# Generate synthetic dataset
X, y = make_classification(n_samples=200, n_features=10, random_state=42)

# Parameter search space
param_grid = {
    "n_estimators": [20, 50],
    "max_depth": [3, 5, None],
    "min_samples_split": [2, 5]
}

rf = RandomForestClassifier(random_state=42)
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

# Execute grid search across CV folds
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=cv,
    scoring="accuracy",
    n_jobs=-1  # Parallel execution across CPU cores
)

grid_search.fit(X, y)
print("Best Parameters:", grid_search.best_params_)
print(f"Best CV Accuracy: {grid_search.best_score_:.4f}")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Shuffling Time Series Data
Using standard K-Fold or `shuffle=True` on sequential or time-series data destroys temporal order, resulting in forward-looking data leakage. Always use `TimeSeriesSplit`!

---

## 6. Interview Questions & Coding Traps

### Q1: What is the computational trade-off of 5-Fold vs 10-Fold Cross-Validation?
- 10-Fold CV uses 90% of data for training in each fold, reducing estimation bias. However, it requires training the model 10 separate times (2x more compute than 5-Fold).
- 5-Fold CV is computationally cheaper (5 training runs), but uses only 80% of data per training run.

### Q2: What is nested cross-validation and why is it used?
Nested CV uses an inner loop for hyperparameter tuning (e.g. grid search) and an outer loop for unbiased model performance estimation. Without nested CV, selecting hyperparameters and reporting the best score on the same validation folds introduces optimistic selection bias!

### Complexity Reference
| Strategy | Compute Overhead | Number of Models Trained |
| :--- | :--- | :--- |
| Simple Train-Test Split | $1	imes$ | 1 model |
| K-Fold Cross Validation | $K 	imes$ | $K$ models |
| Grid Search with K-Fold | $K 	imes \prod |	ext{param\_grid}|$ | $K \cdot |	ext{combinations}|$ |
