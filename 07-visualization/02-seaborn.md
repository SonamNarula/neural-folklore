# Seaborn and Statistical Visualizations

> Seaborn is a high-level statistical visualization library built on top of Matplotlib, tightly integrated with Pandas DataFrames.

---

## 1. Why This Matters

### Why This Concept Exists
Matplotlib requires dozens of lines of imperative code to compute and format statistical graphics (boxplots, kernel density estimations, regression intervals). Seaborn provides concise declarative APIs for statistical exploration.

### Why Python Developers Need It
Seaborn accepts Pandas DataFrames directly, automatically mapping categorical columns to hues, facets, and marker aesthetics.

### Why It Matters Specifically in AI/ML/GenAI
- **Feature Correlation Matrices**: Identifying multicollinearity prior to model training using annotated heatmaps (`sns.heatmap(df.corr())`).
- **Target Distribution Diagnostics**: Inspecting class imbalances and skewed continuous distributions via `sns.histplot(kde=True)`.
- **Error Analysis Faceting**: Segmenting model error rates across multi-dimensional customer tiers.

### Where It Appears in Real Projects
- Exploratory Data Analysis (EDA) reports.
- Feature importance and correlation analysis.
- Post-hoc model error diagnosis.

---

## 2. Core Concept

### 2.1 Core Statistical Functions
- `sns.histplot(df, x="val", kde=True)`: Distribution histogram with Kernel Density Estimate.
- `sns.boxplot(df, x="cat", y="val")`: Five-number summary detecting outliers.
- `sns.heatmap(data, annot=True)`: 2D color-encoded matrix.
- `sns.pairplot(df, hue="target")`: Grid of pairwise bivariate distributions.

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "prompt_tokens": np.random.normal(200, 50, 300),
    "latency_ms": np.random.normal(150, 30, 300),
    "model": np.random.choice(["gpt-4o", "claude-3-5"], 300)
})

# High-level statistical visualization:
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    data=df,
    x="prompt_tokens",
    y="latency_ms",
    hue="model",
    palette="viridis",
    ax=ax
)
ax.set_title("Token Count vs Latency by Model")
plt.savefig("sns_scatter.png")
plt.close(fig)
```

---

## 3. Mental Model

```text
Seaborn Abstraction Layer:
[ User DataFrame ]
        │
        ▼ (Declarative API: data=df, x='col', hue='group')
[ Seaborn Statistical Computation Engine (KDE, quantiles, regressions) ]
        │
        ▼ (Renders via explicit Matplotlib OO backend)
[ Matplotlib Figure and Axes ]
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Feature Correlation Matrix Heatmap for ML Pipelines
Visualizing multicollinearity across numeric feature candidates:

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_correlation_heatmap(df: pd.DataFrame, output_path: str):
    """Generates an annotated correlation heatmap for feature selection."""
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()

    # Generate a mask for the upper triangle (symmetric redundancy reduction)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        ax=ax
    )
    ax.set_title("Feature Correlation Matrix (Lower Triangle)")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)

sample_df = pd.DataFrame(np.random.randn(100, 5), columns=[f"feat_{i}" for i in range(5)])
plot_correlation_heatmap(sample_df, "corr_matrix.png")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. High-Dimensional Pairplot Crashes
Executing `sns.pairplot(df)` on a DataFrame with 50+ columns generates $50 	imes 50 = 2500$ subplots, which exhausts memory and freezes execution! Always filter to a small subset of features (e.g. top 5-8).

---

## 6. Interview Questions & Coding Traps

### Q1: When is a heatmap preferred over a pairplot?
A correlation heatmap evaluates global bivariate linear relationships across dozens of features simultaneously in $O(C^2)$ matrix calculations. A pairplot renders detailed scatter plots between every pair of features, which is only feasible for small feature subsets (< 10).

### Complexity Reference
| Chart Type | Computation Cost | Rendering Cost |
| :--- | :--- | :--- |
| `sns.heatmap(corr)` | $O(N \cdot C^2)$ correlation matrix | $O(C^2)$ rectangle elements |
| `sns.pairplot(k)` | $O(k^2 \cdot N)$ scatter calculations | $O(k^2)$ distinct subplots |
