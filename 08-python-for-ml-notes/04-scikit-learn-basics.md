# Scikit-Learn Architecture and Custom Pipelines

> Scikit-Learn standardizes machine learning through three core object protocols: Estimators (`fit`), Transformers (`transform`), and Predictors (`predict`), unified via composite `Pipeline` execution.

---

## 1. Why This Matters

### Why This Concept Exists
Disparate ML algorithms historically exposed incompatible function signatures. Scikit-Learn revolutionized Python data science by unifying all algorithms behind consistent object-oriented interfaces.

### Why Python Developers Need It
Mastering Scikit-Learn's API conventions allows you to write custom data preprocessing and model components that seamlessly plug into enterprise ML pipelines.

### Why It Matters Specifically in AI/ML/GenAI
- **Production Preprocessing Pipelines**: Wrapping tokenizers, feature scaling, and categorical encoders into a single serialized `Pipeline` artifact (`joblib.dump(pipeline)`).
- **Custom Model Wrappers**: Wrapping proprietary LLM inference endpoints or deep learning embeddings into a Scikit-Learn `BaseEstimator` interface.
- **Leak-Free Cross-Validation**: `Pipeline` guarantees that transformations are fit strictly on training folds during cross-validation.

### Where It Appears in Real Projects
- Model deployment artifacts (`pipeline.pkl`).
- Custom feature extraction transformers in production.
- Model evaluation harnesses.

---

## 2. Core Concept: The Unified API

### 2.1 The Three Core Interfaces
1. **Estimator**: Initializes parameters; implements `fit(X, y)` to learn from data.
2. **Transformer**: Preprocesses data; implements `transform(X)` and `fit_transform(X, y)`.
3. **Predictor**: Makes inferences; implements `predict(X)` and `predict_proba(X)`.

### 2.2 Custom Transformer Protocol
To create a custom transformer compatible with Scikit-Learn:
- Inherit from `BaseEstimator` (provides `get_params` and `set_params`).
- Inherit from `TransformerMixin` (provides `fit_transform` automatically).
- Implement `fit(self, X, y=None)` and `transform(self, X)`.

```python
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

class OutlierClipper(BaseEstimator, TransformerMixin):
    def __init__(self, lower_percentile: float = 1.0, upper_percentile: float = 99.0):
        self.lower_percentile = lower_percentile
        self.upper_percentile = upper_percentile

    def fit(self, X, y=None):
        # Calculate thresholds strictly on training data
        self.lower_bound_ = np.percentile(X, self.lower_percentile, axis=0)
        self.upper_bound_ = np.percentile(X, self.upper_percentile, axis=0)
        return self

    def transform(self, X):
        return np.clip(X, self.lower_bound_, self.upper_bound_)

clipper = OutlierClipper()
data = np.array([[1.0], [50.0], [1000.0]])
clipped = clipper.fit_transform(data)
```

---

## 3. Mental Model

```text
Scikit-Learn Composite Pipeline:
Raw X ──► [ Transformer 1 (Imputer) ] ──► Imputed X
               │
               ▼
          [ Transformer 2 (Scaler)  ] ──► Scaled X
               │
               ▼
          [ Predictor (Classifier)   ] ──► Final Predictions y_hat
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Custom Document Length Feature Extractor in a Pipeline
Building a custom text feature extractor integrated into an end-to-end classification pipeline:

```python
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

class TextLengthFeatureExtractor(BaseEstimator, TransformerMixin):
    """Custom transformer computing character and word counts from text."""
    def fit(self, X, y=None):
        return self  # No state to learn

    def transform(self, X):
        # Expects a list or Series of strings
        features = []
        for text in X:
            char_count = len(text)
            word_count = len(text.split())
            features.append([char_count, word_count])
        return np.array(features)

# Pipeline chaining custom transformer with estimator:
pipeline = Pipeline([
    ("extractor", TextLengthFeatureExtractor()),
    ("classifier", LogisticRegression())
])

train_texts = ["Short prompt", "This is a significantly longer detailed query prompt", "Tiny text"]
train_labels = [0, 1, 0]

# Fit and predict seamlessly!
pipeline.fit(train_texts, train_labels)
predictions = pipeline.predict(["Another long query prompt explaining technical mechanics"])
print("Pipeline Prediction:", predictions)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. `*args` and `**kwargs` in Custom Estimator `__init__`
Scikit-Learn's `BaseEstimator` inspects `__init__` constructor signatures to implement cloning and parameter grid searches. **Never use `*args` or `**kwargs` in `__init__`!** Explicitly list all parameters with defaults.

### 2. Mutating Constructor Arguments in `__init__`
Never modify parameters in `__init__` (e.g., `self.param = param.lower()`). Store constructor arguments unmodified; execute mutations inside `fit()`.

---

## 6. Interview Questions & Coding Traps

### Q1: Why is wrapping transformers and estimators in a `Pipeline` superior to manual preprocessing?
1. **Prevents Data Leakage**: In cross-validation, `Pipeline` automatically calls `fit()` only on training folds and `transform()` on validation folds.
2. **Atomic Deployment**: Serializing a single pipeline object encapsulates all preprocessing rules, eliminating training-serving skew in production.

### Q2: What does a trailing underscore on an attribute name (e.g., `self.mean_`) denote in Scikit-Learn?
By convention, trailing underscores denote **learned parameters** estimated from data during `fit()` (e.g., `coef_`, `intercept_`, `classes_`), as opposed to user-configured hyperparameters set in `__init__`.

### Complexity Reference
| Component | fit() Cost | transform() / predict() Cost |
| :--- | :--- | :--- |
| `Pipeline.fit()` | $\sum 	ext{fit() and transform() of each step}$ | N/A |
| `Pipeline.predict()` | N/A | $\sum 	ext{transform() of steps} + 	ext{predict()}$ |
