# Production Machine Learning Project Architecture

> A production ML repository isolates dataset engineering, model architecture definitions, configuration management (Hydra/YAML), training harnesses, and artifact registries.

---

## 1. Why This Matters

### Why This Concept Exists
Machine learning projects that live in monolithic Jupyter notebooks cannot be tested, version-controlled, or deployed cleanly into automated CI/CD pipelines.

### Why Python Developers Need It
Standardizing repository layout separates business logic from ML experiment code, ensuring team collaboration and reproducible model retraining.

### Why It Matters Specifically in AI/ML/GenAI
- **Config-Driven Experiments**: Swapping models (BERT -> RoBERTa), learning rates, and batch sizes via YAML configs without editing Python code.
- **Model Checkpointing & Early Stopping**: Reliably saving best model weights and training state dictionaries.
- **Decoupled Training and Serving**: Reusing the same model architecture class in both the multi-GPU training cluster and the lightweight inference API.

---

## 2. Standard Production ML Repository Blueprint

```text
ml_project/
├── configs/
│   ├── config.yaml            # Main configuration entrypoint
│   ├── model/
│   │   ├── bert.yaml          # Architecture parameters
│   │   └── llama.yaml
│   └── training/
│       └── default.yaml       # Epochs, lr, scheduler, batch_size
├── data/
│   ├── raw/                   # Immutable raw datasets
│   └── processed/             # Cleaned feature parquets
├── models/                    # Saved weights & checkpoint artifacts (.pt, .safetensors)
├── src/
│   ├── __init__.py
│   ├── dataset.py             # Custom Dataset and DataLoader definitions
│   ├── model.py               # Neural network architecture (nn.Module)
│   ├── trainer.py             # Training loop, validation, metrics
│   └── utils.py               # Seed setting, device management
├── tests/
│   ├── test_dataset.py
│   └── test_model_forward.py  # Smoke tests on forward pass shapes
├── requirements.txt
└── train.py                   # Master entrypoint script
```

---

## 3. Practical Production Implementation

### Complete Modular ML Pipeline Harness
```python
import os
import random
import numpy as np

# 1. Reproducibility Utility
def seed_everything(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    print(f"Global random seed set to {seed}")

# 2. Configurable Trainer Harness
class ModelTrainer:
    def __init__(self, config: dict):
        self.config = config
        self.epochs = config.get("epochs", 5)
        self.lr = config.get("lr", 1e-3)
        self.best_val_loss = float("inf")

    def train_epoch(self, epoch: int) -> float:
        # Simulate batch training loop
        simulated_loss = 1.0 / (epoch + 1) + random.uniform(0.01, 0.05)
        return simulated_loss

    def validate(self, epoch: int) -> float:
        # Simulate validation loop
        simulated_val_loss = 1.0 / (epoch + 1) + random.uniform(0.02, 0.08)
        return simulated_val_loss

    def save_checkpoint(self, epoch: int, val_loss: float) -> None:
        print(f"[*] Best validation loss improved ({val_loss:.4f}). Saving checkpoint: model_epoch_{epoch}.pt")

    def run(self) -> None:
        seed_everything(self.config.get("seed", 42))
        print(f"Starting training run: {self.config.get('model_name')} for {self.epochs} epochs.")

        for epoch in range(1, self.epochs + 1):
            train_loss = self.train_epoch(epoch)
            val_loss = self.validate(epoch)
            print(f"Epoch {epoch:02d}/{self.epochs:02d} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")

            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                self.save_checkpoint(epoch, val_loss)

if __name__ == "__main__":
    experiment_config = {
        "model_name": "TransformerClassifier",
        "lr": 2e-5,
        "epochs": 4,
        "seed": 1337
    }
    trainer = ModelTrainer(experiment_config)
    trainer.run()
```

---

## 4. Production ML Quality Checklist
- [ ] **Deterministic Seed**: All pseudo-random number generators seeded at startup (`random`, `numpy`, `torch`).
- [ ] **Shape Assertions**: Unit tests verifying model output shapes given dummy input tensors.
- [ ] **Config Decoupling**: Zero hardcoded hyperparameters in `.py` model files.
