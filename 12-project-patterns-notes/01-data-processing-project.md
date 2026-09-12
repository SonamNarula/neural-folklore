# Production Data Processing Pipeline Pattern

> A production ETL pipeline decouples ingestion, validation, transformation, and storage with structured logging, defensive retries, and columnar Parquet serialization.

---

## 1. Why This Matters

### Why This Concept Exists
Ad-hoc Python scripts in Jupyter notebooks fail silently when encountering malformed data, run out of memory on large files, and lack observability. Production pipelines must be deterministic, fault-tolerant, and idempotent.

### Why Python Developers Need It
Every enterprise AI application requires continuous data pipelines to ingest raw logs, clean training text, and feed feature stores.

### Why It Matters Specifically in AI/ML/GenAI
- **Pretraining Data Curation**: Ingesting web-scraped documents, stripping PII, deduplicating via MinHash, and writing to compressed Parquet.
- **RAG Knowledge Base Sync**: Continuously syncing internal Notion/Confluence docs into embedded vector chunks.
- **Batch Feature Generation**: Calculating rolling user interaction vectors for recommendation systems.

### Where It Appears in Real Projects
- Airflow and Prefect DAG task definitions.
- Ray Data distributed batch processing jobs.
- Spark and Polars feature pipelines.

---

## 2. Architecture & Directory Layout

```text
data_pipeline/
├── configs/
│   └── etl_config.yaml
├── src/
│   ├── __init__.py
│   ├── extract.py      # Raw I/O, API clients, S3 downloaders
│   ├── transform.py    # Vectorized cleaning, normalization
│   ├── validate.py     # Schema checking, anomaly rejection
│   └── load.py         # Columnar parquet writer
├── tests/
│   └── test_pipeline.py
├── requirements.txt
└── run_pipeline.py     # Orchestrator CLI entrypoint
```

---

## 3. Practical Production Implementation

### Complete Standalone Robust ETL Pipeline
```python
import logging
import sys
from typing import List, Dict, Any
import pandas as pd
import numpy as np

# Configure Structured Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ETLPipeline")

class DataProcessingPipeline:
    def __init__(self, raw_data_path: str, output_path: str):
        self.raw_data_path = raw_data_path
        self.output_path = output_path

    def extract(self) -> pd.DataFrame:
        logger.info(f"Extracting raw data from {self.raw_data_path}...")
        # Simulating raw ingestion
        return pd.DataFrame({
            "doc_id": [f"doc_{i}" for i in range(100)],
            "raw_text": ["  Transformer self-attention mechanism  " if i % 2 == 0 else "   " for i in range(100)],
            "token_estimate": [len("Transformer self-attention mechanism".split()) if i % 2 == 0 else 0 for i in range(100)],
            "quality_score": np.random.uniform(0.1, 1.0, 100)
        })

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Validating schema and rejecting malformed records...")
        initial_len = len(df)

        # 1. Reject empty text
        valid_df = df[df["raw_text"].str.strip().str.len() > 0].copy()

        # 2. Reject low quality scores (threshold < 0.20)
        valid_df = valid_df[valid_df["quality_score"] >= 0.20]

        dropped = initial_len - len(valid_df)
        logger.info(f"Validation completed: {len(valid_df)} records retained, {dropped} dropped.")
        return valid_df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Applying vectorized transformations...")
        transformed = df.copy()

        # Clean text
        transformed["cleaned_text"] = transformed["raw_text"].str.strip().str.lower()
        # Compute exact word count
        transformed["word_count"] = transformed["cleaned_text"].str.split().str.len()
        # Downcast floats to float32
        transformed["quality_score"] = transformed["quality_score"].astype(np.float32)

        return transformed.drop(columns=["raw_text"])

    def load(self, df: pd.DataFrame) -> None:
        logger.info(f"Writing {len(df)} records to columnar Parquet at {self.output_path}...")
        df.to_parquet(self.output_path, index=False, compression="snappy")
        logger.info("Pipeline execution completed successfully.")

    def run(self) -> None:
        raw_df = self.extract()
        valid_df = self.validate(raw_df)
        transformed_df = self.transform(valid_df)
        self.load(transformed_df)

if __name__ == "__main__":
    pipeline = DataProcessingPipeline("raw_input.jsonl", "curated_dataset.parquet")
    pipeline.run()
```

---

## 4. Edge Cases & Defensive Checklist
1. **Idempotency**: Rerunning the pipeline with identical inputs must produce the exact same output without duplicating records.
2. **Atomic Writes**: Write output to a temporary staging file first (`temp.parquet`), then atomically rename it to target destination to prevent corrupted reads if the job crashes mid-write.
