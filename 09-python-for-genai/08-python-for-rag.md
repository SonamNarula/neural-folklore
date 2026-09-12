# Python for Retrieval-Augmented Generation (RAG)

> Retrieval-Augmented Generation (RAG) grounds LLM completions in authoritative external knowledge by retrieving relevant document embeddings via vector similarity search and injecting them into prompt context.

---

## 1. Why This Matters

### Why This Concept Exists
LLMs suffer from knowledge cutoff dates and hallucinations on private corporate data. Rather than fine-tuning billion-parameter models continuously, RAG retrieves precise factual context on-demand.

### Why Python Developers Need It
RAG is the single most common enterprise Generative AI architecture in production today.

### Why It Matters Specifically in AI/ML/GenAI
- **Mathematical Vector Search**: Understanding dense embeddings, vector indexing, and cosine similarity.
- **Document Chunking & Stride**: Overcoming token limits by segmenting documents into overlapping windows.
- **In-Memory Vector Stores**: Implementing fast nearest-neighbor retrieval without external dependencies for lightweight microservices.

### Where It Appears in Real Projects
- Enterprise internal knowledge search (Slack, Notion, Jira Q&A).
- Customer support automation over technical documentation.
- Legal and medical research assistants.

---

## 2. Core Concept: The 4 Stages of RAG

```text
The RAG Pipeline:
1. Ingestion: Raw Docs ──► Text Chunker ──► Embedding Model ──► Vector Index
2. Retrieval: User Query ──► Embed Query ──► Cosine Similarity Search ──► Top-K Chunks
3. Synthesis: Prompt = System + Retrieved Context + User Query ──► LLM ──► Grounded Answer
```

---

## 3. Mental Model

```text
Vector Embedding Space:
Vector Index:
Embedding("Machine Learning algorithms") ──► [ 0.82,  0.41, -0.15 ]
Embedding("Deep neural networks")        ──► [ 0.79,  0.45, -0.12 ]  <- High Cosine Similarity!
Embedding("Chocolate cookie recipe")     ──► [-0.12, -0.85,  0.64 ]  <- Low Similarity!
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: Complete In-Memory RAG Engine From Scratch (Pure Python & NumPy)
A full working RAG system implementing chunking, embedding simulation, cosine similarity search, and context injection:

```python
import numpy as np
from typing import List, Dict, Any

class SimpleRAGEngine:
    def __init__(self) -> None:
        self.documents: List[str] = []
        self.embeddings: np.ndarray | None = None

    def _mock_embedding(self, text: str) -> np.ndarray:
        """Deterministic mock embedding vector for demonstration (dim=4)."""
        np.random.seed(abs(hash(text)) % (2**32))
        vec = np.random.randn(4).astype(np.float32)
        return vec / np.linalg.norm(vec)  # L2 Normalized

    def add_documents(self, docs: List[str]) -> None:
        self.documents.extend(docs)
        doc_vectors = np.array([self._mock_embedding(doc) for doc in docs])
        if self.embeddings is None:
            self.embeddings = doc_vectors
        else:
            self.embeddings = np.vstack([self.embeddings, doc_vectors])

    def retrieve(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        query_vec = self._mock_embedding(query)
        # Cosine similarity on normalized vectors is simply dot product!
        similarities = np.dot(self.embeddings, query_vec)
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "document": self.documents[idx],
                "score": float(similarities[idx])
            })
        return results

    def format_prompt(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        context_str = "
".join([f"- {d['document']}" for d in retrieved_docs])
        return (
            f"You are a helpful assistant. Use ONLY the following context to answer the user query.

"
            f"Context:
{context_str}

"
            f"User Query: {query}
"
            f"Answer:"
        )

# Execution:
rag = SimpleRAGEngine()
rag.add_documents([
    "Transformers use self-attention mechanisms to process sequence tokens in parallel.",
    "BERT is a bidirectional encoder representation model used for classification.",
    "GPT models are autoregressive decoder models trained for causal language modeling.",
    "Python was created by Guido van Rossum and released in 1991."
])

query = "How do transformers process sequence tokens?"
retrieved = rag.retrieve(query, top_k=2)
grounded_prompt = rag.format_prompt(query, retrieved)
print(grounded_prompt)
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Chunk Size vs Context Fragmentation
- **Too Small** (e.g. 50 tokens): Loses surrounding semantic context; sentence fragments.
- **Too Large** (e.g. 2,000 tokens): Dilutes specific facts; adds irrelevant noise to the LLM prompt.
- **Production Sweet Spot**: 256 to 512 tokens with 10-20% chunk overlap.

### 2. Lost in the Middle Phenomenon
LLMs attend most effectively to the very beginning and very end of the injected context window. Critical facts buried in the middle of long contexts are often ignored! Place highest-scoring retrieved documents at the beginning or end of the prompt context.

---

## 6. Interview Questions & Coding Traps

### Q1: What is the difference between Dense Retrieval and Sparse Retrieval?
- **Dense Retrieval** (Vector Search): Uses deep neural embeddings (e.g. `text-embedding-3`). Captures semantic meaning and synonyms, but can miss exact keyword codes (part numbers, UUIDs).
- **Sparse Retrieval** (BM25 / TF-IDF): Matches exact lexical keywords and frequencies.
- **Hybrid Search**: Combines Dense + Sparse retrieval using Reciprocal Rank Fusion (RRF) for optimal results.

### Complexity Reference
| Step | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Exact Nearest Neighbor Search | $O(N \cdot D)$ linear scan | $O(N \cdot D)$ index matrix |
| Approximate Nearest Neighbor (HNSW) | $O(\log N)$ graph traversal | $O(N \cdot D + 	ext{edges})$ |
