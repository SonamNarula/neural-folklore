# Concurrency: Multithreading vs Multiprocessing vs AsyncIO

> Python offers three distinct concurrency paradigms: Multithreading (I/O-bound, shared memory), Multiprocessing (CPU-bound, true parallel processes), and AsyncIO (I/O-bound cooperative coroutines).

---

## 1. Why This Matters

### Why This Concept Exists
Modern machines have dozens of CPU cores and high-bandwidth network interfaces. Single-threaded synchronous execution leaves 90%+ of hardware capacity idle.

### Why Python Developers Need It
Selecting the wrong concurrency model (e.g. using threads for CPU-bound computer vision augmentations) will **slow down** your program due to GIL lock contention.

### Why It Matters Specifically in AI/ML/GenAI
- **CPU-Bound: Data Augmentation (`multiprocessing`)**: Preprocessing raw images, calculating audio spectrograms, and tokenizing large text corpora across all CPU cores.
- **I/O-Bound: High-Throughput Scraping & API Calling (`asyncio`)**: Querying 1,000 LLM endpoints or downloading millions of web pages concurrently.
- **I/O-Bound: Legacy Thread Pools (`ThreadPoolExecutor`)**: Interfacing with blocking third-party SDKs concurrently without rewriting in async.

### Where It Appears in Real Projects
- PyTorch `DataLoader(num_workers=8)` (uses `multiprocessing`).
- Ray distributed cluster computing.
- Concurrent benchmark harnesses.

---

## 2. Core Concept: The Concurrency Matrix

| Feature | AsyncIO (`async/await`) | Multithreading (`threading`) | Multiprocessing (`multiprocessing`) |
| :--- | :--- | :--- | :--- |
| **Best For** | I/O-bound (Web/APIs) | I/O-bound (Blocking C/SDKs) | CPU-bound (Data Prep, ML Math) |
| **Memory** | Shared (Single Thread) | Shared Memory Space | Separate Process Memory Spaces |
| **GIL Impact** | Bound by GIL (Single thread) | Bound by GIL (1 thread at a time) | **Bypasses GIL** (Separate Python process per core) |
| **Overhead** | Microscopic (~2KB / task) | Medium (~8MB stack / thread) | High (Full process spawn / fork) |
| **Communication** | Coroutine variables | Shared memory + Locks | IPC, Queues, Pipes, Pickle |

---

## 3. Mental Model

```text
The 3 Concurrency Models:
1. AsyncIO:
   Single Thread ──► [ Coroutine 1 ] ──(I/O wait)──► [ Coroutine 2 ] (Cooperative)

2. Multithreading:
   Thread 1 ──► [ GIL Acquired: Executing ] ──► [ GIL Released ]
   Thread 2 ──► [ Waiting for GIL....... ] ──► [ GIL Acquired: Executing ] (Preemptive)

3. Multiprocessing:
   Core 1: Process 1 (Own GIL, Own RAM) ──► 100% CPU Parallelism!
   Core 2: Process 2 (Own GIL, Own RAM) ──► 100% CPU Parallelism!
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: High-Performance CPU Parallel Data Preprocessing with `ProcessPoolExecutor`
Parallelizing CPU-heavy text tokenization across all available CPU cores:

```python
from concurrent.futures import ProcessPoolExecutor
import os
import time
from typing import List

def cpu_heavy_preprocess(doc_text: str) -> dict:
    """Simulates CPU-heavy parsing, regex, and feature extraction."""
    # Heavy computation:
    tokens = doc_text.lower().split()
    token_count = len(tokens)
    hash_checksum = sum(hash(t) % 10000 for t in tokens)
    return {
        "pid": os.getpid(),
        "token_count": token_count,
        "checksum": hash_checksum
    }

def run_parallel_pipeline(documents: List[str]):
    # Uses all available CPU cores
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(cpu_heavy_preprocess, documents))
    return results

if __name__ == "__main__":
    docs = [f"Sample document content for index {i} with repeated tokens" * 100 for i in range(20)]
    start = time.perf_counter()
    output = run_parallel_pipeline(docs)
    elapsed = time.perf_counter() - start

    unique_pids = set(r["pid"] for r in output)
    print(f"Processed {len(docs)} documents in {elapsed:.2f}s across {len(unique_pids)} CPU worker processes.")
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. The Fork vs Spawn Trap on macOS/Linux
In Python 3.8+, macOS defaults to `'spawn'` instead of `'fork'`. In `'spawn'`, worker processes import the main script from scratch. If your script lacks `if __name__ == '__main__':`, it creates an **infinite recursive process bomb**!

### 2. IPC Pickling Overhead
`multiprocessing` communicates by serializing objects with `pickle`. If you pass huge datasets (e.g. a 5GB DataFrame) to worker functions, the time spent pickling/unpickling across process pipes can completely erase all multi-core speedups! Use shared memory (`multiprocessing.shared_memory`) or memory-mapped files.

---

## 6. Interview Questions & Coding Traps

### Q1: When would you choose `ThreadPoolExecutor` over `ProcessPoolExecutor`?
When the task is **I/O-bound** (e.g. making HTTP requests or reading files from disk) or calls C-extensions that release the GIL (e.g. NumPy matrix operations). Threads share the same memory space, eliminating the heavy process creation and IPC pickling overhead of multiprocessing.

### Complexity Reference
| Paradigm | Task Suitability | Hardware Scaling |
| :--- | :--- | :--- |
| `threading` | I/O-bound | Limited to 1 core for Python bytecode |
| `multiprocessing` | CPU-bound | Scales linearly across $N$ physical cores |
| `asyncio` | High-concurrency I/O | Single core, handles 50,000+ sockets |
