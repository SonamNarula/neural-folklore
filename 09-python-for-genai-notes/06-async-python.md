# Asynchronous Python and Concurrency with `asyncio`

> `asyncio` implements single-threaded cooperative multitasking using an Event Loop to interleave non-blocking I/O operations across coroutines.

---

## 1. Why This Matters

### Why This Concept Exists
Synchronous I/O halts the entire Python process while waiting for network responses. In GenAI, where individual LLM API requests take 2 to 10 seconds, running 1,000 requests sequentially takes hours. Asynchronous I/O executes hundreds of requests concurrently on a single thread.

### Why Python Developers Need It
Mastering `async`/`await`, `asyncio.gather`, and concurrency semaphores is essential for building scalable web servers and data scrapers.

### Why It Matters Specifically in AI/ML/GenAI
- **High-Throughput LLM Evaluation**: Running offline benchmark evaluations (e.g., scoring 10,000 prompts across multiple models) concurrently without spawning thousands of OS threads.
- **FastAPI LLM Microservices**: Serving concurrent user chat requests asynchronously on high-performance ASGI web servers (Uvicorn).
- **Concurrency Rate Limiting (`Semaphore`)**: Limiting simultaneous inflight requests to avoid exceeding provider rate limits.

### Where It Appears in Real Projects
- Async OpenAI and Anthropic SDKs (`AsyncOpenAI`).
- FastAPI route handlers (`async def predict()`).
- High-throughput asynchronous RAG retrieval pipelines.

---

## 2. Core Concept

### 2.1 The Event Loop and Coroutines
- `async def`: Defines a **coroutine function**. Calling it returns a coroutine object without executing the body.
- `await`: Yields execution back to the **Event Loop**, allowing other pending tasks to run while waiting for an I/O operation to complete.

```python
import asyncio

async def fetch_completion(prompt_id: int, delay: float) -> str:
    print(f"Task {prompt_id}: Request sent...")
    # asyncio.sleep yields control to the event loop (non-blocking!)
    await asyncio.sleep(delay)
    print(f"Task {prompt_id}: Response received!")
    return f"Result {prompt_id}"

async def main():
    # Run 3 coroutines concurrently:
    results = await asyncio.gather(
        fetch_completion(1, 0.2),
        fetch_completion(2, 0.1),
        fetch_completion(3, 0.15)
    )
    print("All tasks finished:", results)

# asyncio.run(main())
```

---

## 3. Mental Model

```text
Synchronous vs Asynchronous I/O:
Sync (Blocking):
Task 1: [ Send ] ── WAITING (Idle CPU) ──► [ Receive ]
Task 2:                                                [ Send ] ── WAITING ──► [ Receive ]
Total Time: 4 Seconds

Async Event Loop (Cooperative):
Task 1: [ Send ] ──┐ (Yields control to loop)
Task 2:            └──► [ Send ] ──┐
Task 3:                            └──► [ Send ]
Event loop checks: Task 2 ready! ──► [ Receive ] ──► Task 1 ready! ──► [ Receive ]
Total Time: ~1 Second (Concurrent execution!)
```

---

## 4. Practical Implementation & AI/ML/GenAI Patterns

### Pattern: High-Throughput Batch LLM Evaluator with `asyncio.Semaphore`
Executing 50 concurrent requests while strictly capping maximum inflight queries to 5:

```python
import asyncio
import time
from typing import List

async def mock_async_llm_call(prompt: str, sem: asyncio.Semaphore) -> str:
    """Acquires semaphore to ensure max concurrent requests is never exceeded."""
    async with sem:
        # Critical section: max N tasks execute here simultaneously
        await asyncio.sleep(0.05)  # Simulate network latency
        return f"Completed: {prompt}"

async def run_batch_evaluation(prompts: List[str], max_concurrency: int = 5) -> List[str]:
    sem = asyncio.Semaphore(max_concurrency)
    tasks = [mock_async_llm_call(p, sem) for p in prompts]
    return await asyncio.gather(*tasks)

async def test_runner():
    prompts = [f"Prompt query {i}" for i in range(20)]
    start = time.perf_counter()
    results = await run_batch_evaluation(prompts, max_concurrency=5)
    elapsed = time.perf_counter() - start
    print(f"Evaluated {len(results)} prompts in {elapsed:.2f}s with max concurrency 5.")

# Run async test:
asyncio.run(test_runner())
```

---

## 5. Edge Cases, Pitfalls & Common Bugs

### 1. Blocking the Event Loop with Synchronous Code
Executing blocking operations (`time.sleep()`, synchronous `requests.get()`, heavy CPU matrix loops) inside an `async def` halts the entire event loop, freezing all other concurrent tasks! Use `asyncio.to_thread()` to run blocking code on a background thread.

### 2. Forgetting to `await`
Calling a coroutine without `await` (`fetch_data()`) does not execute the function; it creates an unawaited coroutine object and emits `RuntimeWarning: coroutine '...' was never awaited`.

---

## 6. Interview Questions & Coding Traps

### Q1: Does `asyncio` make CPU-bound machine learning training faster?
**No.** `asyncio` is single-threaded cooperative multitasking designed exclusively for **I/O-bound** operations (network calls, disk reads). It does not execute across multiple CPU cores. For CPU-bound operations (matrix multiplications, image rendering), use `multiprocessing`.

### Q2: What is the difference between `asyncio.gather()` and `asyncio.as_completed()`?
- `asyncio.gather()` waits for **all** tasks to complete and returns results in the original submission order.
- `asyncio.as_completed()` yields an iterator of tasks as they finish, allowing you to process results immediately as each task completes.

### Complexity Reference
| Concurrency Model | Concurrency Scale | Memory Footprint per Task |
| :--- | :--- | :--- |
| OS Threads (`threading`) | Hundreds (~1,000 max) | High (~8MB stack per thread) |
| Coroutines (`asyncio`) | Tens of thousands (100,000+) | Extremely low (~2KB per coroutine frame) |
