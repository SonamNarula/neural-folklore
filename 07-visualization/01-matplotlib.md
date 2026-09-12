# Matplotlib and the Object-Oriented Interface

> Matplotlib renders 2D/3D visualizations through an explicit, hierarchical object model (`Figure` -> `Axes` -> `Axis` -> `Artist`).

---

## 1. Why This Matters

### Why This Concept Exists
Data scientists and ML engineers must diagnose distribution anomalies, monitor loss convergence, and communicate empirical findings. Matplotlib provides pixel-level graphic control.

### Why Python Developers Need It
Avoiding the confusing stateful `pyplot` interface (`plt.plot()`) and mastering the explicit **Object-Oriented (OO) API** (`fig, ax = plt.subplots()`) is essential for writing bug-free multi-plot figures.

### Why It Matters Specifically in AI/ML/GenAI
- **Training Loss Curves**: Visualizing training vs validation loss across epochs to diagnose overfitting, underfitting, and learning rate instability.
- **Attention Heatmaps**: Rendering multi-head attention weight matrices across input token sequences.
- **Embedding Projections**: Plotting 2D t-SNE / UMAP dimensional reductions of high-dimensional token embeddings.

### Where It Appears in Real Projects
- Weights & Biases / TensorBoard custom figure logging.
- Model evaluation reports and research papers.
- Exploratory data analysis in research notebooks.

---

## 2. Core Concept

### 2.1 The Object-Oriented Hierarchy (`Figure` and `Axes`)
- **`Figure`**: The top-level canvas containing all subplots, titles, and legends.
- **`Axes`**: The actual subplot area where data is rendered (contains x-axis, y-axis, lines, markers).

```python
import matplotlib.pyplot as plt
import numpy as np

# Create figure and a 1x2 grid of Axes explicitly
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4), dpi=100)

# Subplot 1: Training curve
epochs = np.arange(1, 11)
loss = 1.0 / epochs
ax1.plot(epochs, loss, color="royalblue", marker="o", label="Training Loss")
ax1.set_title("Convergence Curve")
ax1.set_xlabel("Epoch")
ax1.set_ylabel("Loss")
ax1.grid(True, linestyle="--", alpha=0.6)
ax1.legend()

# Subplot 2: Token distribution
tokens_per_doc = [120, 150, 180, 220, 300, 350, 500]
ax2.hist(tokens_per_doc, bins=5, color="teal", edgecolor="black")
ax2.set_title("Token Distribution")
ax2.set_xlabel("Tokens")

plt.tight_layout()
plt.savefig("sample_training_plot.png")
plt.close(fig)  # Release figure memory deterministically!
```

---

## 3. Mental Model

```text
Matplotlib Object Hierarchy:
┌─────────────────────────────────────────────────────────────┐
│ Figure (The Top-Level Canvas)                               │
│                                                             │
│  ┌───────────────────────────┐ ┌──────────────────────────┐ │
│  │ Axes 1                    │ │ Axes 2                   │ │
│  │  - X-Axis & Y-Axis        │ │  - X-Axis & Y-Axis       │ │
│  │  - Lines, Bars, Scatters  │ │  - Title, Legend, Labels │ │
│  └───────────────────────────┘ └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Multi-Head Attention Matrix Heatmap
Visualizing an attention weight matrix between queries and keys:

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_attention_matrix(attention_weights: np.ndarray, tokens: list[str], output_path: str):
    """
    Renders a square attention heatmap for transformer self-attention visualization.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.matshow(attention_weights, cmap="viridis")

    # Set tick labels to tokens
    ax.set_xticks(range(len(tokens)))
    ax.set_yticks(range(len(tokens)))
    ax.set_xticklabels(tokens, rotation=45, ha="left")
    ax.set_yticklabels(tokens)

    # Colorbar
    fig.colorbar(cax)
    ax.set_title("Self-Attention Weights", pad=20)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)

# Simulation:
tokens = ["The", "model", "understands", "context"]
mock_attn = np.array([
    [0.7, 0.1, 0.1, 0.1],
    [0.1, 0.6, 0.2, 0.1],
    [0.05, 0.15, 0.5, 0.3],
    [0.1, 0.1, 0.2, 0.6]
])
plot_attention_matrix(mock_attn, tokens, "attention_heatmap.png")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Memory Leaks from Unclosed Figures
Calling `plt.figure()` inside training loops without calling `plt.close(fig)` retains all figures in the global GUI manager, rapidly leaking hundreds of megabytes of RAM!

### 2. Thread Safety
Matplotlib's default backend is **not thread-safe**. When rendering plots inside background web workers (FastAPI / Celery), configure the headless backend:
```python
import matplotlib
matplotlib.use("Agg")  # Non-interactive, thread-safe headless backend
```

---

## 6. Interview Questions & Coding Traps

### Q1: What is the difference between `plt.plot()` and `ax.plot()`?
`plt.plot()` relies on the implicit stateful MATLAB-like state machine, applying modifications to the "current active figure". `ax.plot()` uses the explicit Object-Oriented interface, directing operations directly to a specific `Axes` instance. The OO interface is cleaner, modular, and essential for multi-subplot figures.

### Complexity Reference
| Operation | Cost |
| :--- | :--- |
| Creating Figure & Subplots | $O(1)$ object hierarchy instantiation |
| Rendering Points / Lines | $O(N)$ rasterization / vector assembly |
