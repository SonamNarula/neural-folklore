# File Handling and Large File Processing in Python

> File handling streams bytes between persistent disk storage and memory buffers using OS-level file descriptors wrapped in context-managed streams.

---

## 1. Why This Matters

### Why This Concept Exists
RAM is volatile and finite; disk storage is persistent and expansive. Programs require buffered stream interfaces to read, write, and seek data without loading multi-gigabyte datasets into memory all at once.

### Why Python Developers Need It
Mastering chunked reading, line streaming, and memory-mapped files (`mmap`) prevents Out-Of-Memory (OOM) crashes when processing massive datasets.

### Why It Matters Specifically in AI/ML/GenAI
- **Multi-Gigabyte Pretraining Corpora**: Pretraining corpora (RedPajama, Dolma, FineWeb) span hundreds of gigabytes of text. They must be streamed line-by-line (`.jsonl`).
- **Checkpoint Serialization**: Saving and loading model weight checkpoints (`.pt`, `.bin`, `.safetensors`).
- **Logging & Tracing**: Streaming real-time inference telemetry to append-only log files.

### Where It Appears in Real Projects
- Streaming HuggingFace datasets (`streaming=True`).
- Reading `.jsonl` files for fine-tuning OpenAI models.
- Safetensors zero-copy model weight deserialization.

---

## 2. Core Concept

### 2.1 File Modes and Context Management
The `with open(...)` context manager guarantees that the underlying OS file descriptor is closed immediately upon exiting the block, even if exceptions occur.

| Mode | Purpose | File Pointer Position |
| :--- | :--- | :--- |
| `'r'` | Read text (default) | Start of file |
| `'w'` | Write text (truncates existing file!) | Start of file |
| `'a'` | Append text | End of file |
| `'rb'` / `'wb'` | Read / Write raw binary bytes | Start of file |

```python
# Idiomatic write and read:
with open("model_meta.txt", "w", encoding="utf-8") as f:
    f.write("vocab_size: 32000
hidden_dim: 4096
")

with open("model_meta.txt", "r", encoding="utf-8") as f:
    for line in f:  # Streams line-by-line with minimal memory!
        print(line.strip())
```

### 2.2 Streaming vs Loading Entire Files
```python
# CATASTROPHIC for a 50GB file:
# lines = f.readlines()  -> Loads entire 50GB into RAM at once!

# MEMORY SAFE (O(1) memory overhead):
with open("massive_dataset.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        process(line)
```

---

## 3. Mental Model

```text
Buffered File I/O Stream:
Disk Storage (50GB File)
          │
          ▼ OS Kernel Buffer
    [ Read Buffer (8KB chunk) ] ──► Python Iterator yields 1 line at a time
          │
          ▼
    Python Process RAM (< 100MB footprint!)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: High-Throughput Chunked JSONL Dataset Streamer
Streaming multi-gigabyte training files in batches without exceeding memory constraints:

```python
import json
from typing import Generator, List, Dict, Any

def stream_jsonl_batches(
    filepath: str,
    batch_size: int = 1000
) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Streams a JSONL file in fixed-size batches.
    Memory consumption remains strictly O(batch_size).
    """
    batch = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            batch.append(json.loads(line_str))
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

# Testing streamer:
with open("mock_dataset.jsonl", "w", encoding="utf-8") as f:
    for i in range(25):
        f.write(json.dumps({"id": i, "text": f"Sample pretraining document {i}"}) + "
")

for b_idx, b in enumerate(stream_jsonl_batches("mock_dataset.jsonl", batch_size=10)):
    print(f"Yielded batch {b_idx} with {len(b)} samples")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Forgetting `encoding="utf-8"`
Omitting `encoding` causes Python to use the operating system default (which is `Windows-1252` on many Windows systems), resulting in `UnicodeDecodeError` when processing international training datasets.

### 2. Windows vs Unix Newlines (`
` vs `
`)
Python's universal newline mode translates newlines automatically in text mode. In binary mode (`'rb'`), raw `
` bytes are preserved.

---

## 6. Interview Questions & Coding Traps

### Q1: What does `f.seek(0)` and `f.tell()` do?
- `f.tell()` returns the current integer byte offset of the file read/write pointer.
- `f.seek(offset, whence)` moves the file pointer to a specific byte offset. `whence=0` (from start), `1` (from current position), `2` (from end).

### Q2: How does memory-mapped file I/O (`mmap`) differ from standard `read()`?
Standard `read()` copies data from disk to kernel buffers, then from kernel buffers to Python user space. `mmap` maps the file directly into the process's virtual address space, avoiding user-space buffer copies (zero-copy I/O), which is critical for loading large neural network weight binaries like Safetensors.

### Complexity Reference
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| `for line in f:` | $O(N)$ total bytes | $O(	ext{max\_line\_length})$ |
| `f.read()` (full) | $O(N)$ total bytes | $O(N)$ full file in RAM |
| `f.seek()` | $O(1)$ | $O(1)$ |
