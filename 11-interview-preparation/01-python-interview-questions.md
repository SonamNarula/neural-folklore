# Top 50 Python Technical & AI Systems Interview Questions

> Comprehensive, rigorous answers to the top 50 core conceptual, systems, and AI-oriented Python questions asked in Tier-1 technical interviews.

---

## Part 1: Core Language & Internals (Q1 - Q15)

### Q1: Explain Python's memory management and garbage collection mechanism.
**Answer:** CPython manages memory using a two-tier architecture:
1. **Reference Counting (Deterministic)**: Every `PyObject` tracks its reference count (`ob_refcnt`). When references hit zero, the memory is freed immediately.
2. **Generational Cyclic Garbage Collector**: Detects reference cycles that reference counting misses. Objects are split into 3 generations (Gen 0, 1, 2) based on survival age. Young generations are collected frequently; older generations are collected less often. Small memory requests (< 512 bytes) are handled by `PyMalloc`, which organizes memory into Arenas (256KB), Pools (4KB), and Blocks.

### Q2: What is the Global Interpreter Lock (GIL) and how does it impact multi-core computing?
**Answer:** The GIL is a mutual exclusion lock in CPython that ensures only one native OS thread executes Python bytecode at any given instant. It prevents race conditions in CPython's non-thread-safe reference counting. Consequently, CPU-bound tasks cannot scale across multiple cores using `threading`. To achieve true multi-core parallelism, developers use `multiprocessing` (separate processes, each with its own GIL) or C-extensions (NumPy, PyTorch) that release the GIL during matrix computations.

### Q3: What is the difference between `==` and `is`?
**Answer:** `==` tests for **value equality** by invoking the object's `__eq__()` magic method. `is` tests for **object identity** by comparing whether two pointer variables share the exact same memory address (`id(a) == id(b)`).

### Q4: Explain the LEGB scope resolution rule.
**Answer:** When looking up an identifier, Python searches namespaces in this order:
1. **L**ocal: Inside the executing function frame.
2. **E**nclosing: Any enclosing outer function closures.
3. **G**lobal: Module-level variables.
4. **B**uilt-in: Python's built-in namespace (`len`, `range`, `ValueError`).

### Q5: What is Method Resolution Order (MRO) and C3 Linearization?
**Answer:** MRO defines the order in which Python resolves methods in class inheritance hierarchies, particularly in multiple inheritance diamonds. CPython uses the C3 Linearization algorithm to guarantee that subclasses precede parent classes, base declaration order is preserved, and class resolution is monotonic.

### Q6: What is the difference between `__new__` and `__init__`?
**Answer:** `__new__` is the static allocator method responsible for returning a new instance of the class from heap memory. `__init__` is the instance initializer responsible for configuring attributes on the newly created instance. `__init__` is only invoked if `__new__` returns an instance of that class.

### Q7: What are `__slots__` and how do they optimize memory?
**Answer:** By default, Python instances store attributes in a dynamic dictionary (`__dict__`), which incurs ~150+ bytes of hash table overhead per instance. Declaring `__slots__ = ('x', 'y')` eliminates `__dict__`, storing attributes in a compact, fixed-size C array of pointers. This slashes memory consumption by 60-80% when storing millions of objects.

### Q8: What is the difference between shallow copy and deep copy?
**Answer:** Assignment (`b = a`) creates an alias to the same object. A shallow copy (`copy.copy`) creates a new outer container but inserts references to the original nested child objects. A deep copy (`copy.deepcopy`) recursively duplicates both the outer container and all nested child objects, providing complete isolation.

### Q9: Why are default arguments evaluated at definition time instead of runtime?
**Answer:** In Python, functions are first-class objects created when the `def` statement executes. Default arguments are evaluated once and stored in the function's `__defaults__` tuple attribute. If a mutable object (`[]`, `{}`) is used as a default, that single object is shared across all subsequent invocations.

### Q10: What is a closure and what does `nonlocal` do?
**Answer:** A closure is an inner function that retains access to variables from its enclosing lexical scope even after the outer function has completed execution. Captured variables are stored in `__closure__` cells. The `nonlocal` keyword allows the inner function to rebind and mutate variables in the nearest enclosing scope without declaring them global.

### Q11: Explain generators and how `yield` works.
**Answer:** A generator is a function containing the `yield` keyword. When invoked, it returns a generator iterator without executing the function body. Calling `next()` executes the body until a `yield` expression is hit, which yields a value and suspends the execution frame in heap memory. Calling `next()` again resumes execution from the exact line where it paused.

### Q12: What is the difference between `Iterable` and `Iterator`?
**Answer:** An `Iterable` is any object that implements `__iter__()`, returning an iterator (e.g., `list`, `str`, `dict`). An `Iterator` is an object that implements both `__iter__()` (returns `self`) and `__next__()` (returns the next element or raises `StopIteration`).

### Q13: How does Python's `with` statement work under the hood?
**Answer:** The `with expr as var:` statement invokes `expr.__enter__()`, binding the return value to `var`. When the block terminates or raises an exception, Python guarantees that `expr.__exit__(exc_type, exc_val, exc_tb)` is executed. If `__exit__` returns `True`, exceptions raised within the block are suppressed.

### Q14: Explain the difference between `list.sort()` and `sorted()`.
**Answer:** `list.sort()` is an in-place mutating method specific to lists that returns `None` and runs in $O(N \log N)$ time using Timsort. `sorted()` is a built-in function that accepts any iterable, leaves the original data unmodified, and returns a new sorted list.

### Q15: What is the difference between `@classmethod` and `@staticmethod`?
**Answer:** `@classmethod` receives the class object (`cls`) as its implicit first argument, allowing it to inspect or instantiate alternative constructors. `@staticmethod` receives no implicit first argument and behaves like an isolated plain function scoped inside the class namespace.

---

## Part 2: Data Structures & Algorithms (Q16 - Q30)

### Q16: How are dictionaries implemented internally in Python 3.7+?
**Answer:** Modern Python dictionaries are compact, ordered hash tables. They decouple storage into a sparse integer array of hash indices (`indices`) and a dense array of entries (`[hash, key_ptr, value_ptr]`) stored in insertion order. Hash collisions are resolved via open addressing with pseudo-random perturbation probing.

### Q17: Why is `collections.deque` preferred over `list` for FIFO queues?
**Answer:** Python lists are dynamic arrays. Removing the first element (`list.pop(0)`) requires shifting all $N-1$ remaining pointers in memory, taking $O(N)$ time. `collections.deque` is implemented as a doubly linked list of fixed-size blocks (typically 64 elements), providing guaranteed $O(1)$ appends and pops at both ends.

### Q18: What is the time complexity of checking membership in a list vs set?
**Answer:** In a list, `x in my_list` requires an $O(N)$ linear scan. In a set, `x in my_set` computes `hash(x)` to look up the bucket index, running in average-case $O(1)$ time ($O(N)$ worst-case under severe hash collisions).

### Q19: What makes an object hashable in Python?
**Answer:** An object is hashable if it has a hash value that never changes during its lifetime (implements `__hash__()`) and can be compared for equality with other objects (implements `__eq__()`). Immutable built-ins (`int`, `str`, `tuple` containing hashables) are hashable; mutable containers (`list`, `dict`, `set`) are unhashable.

### Q20: Explain the Two-Pointer technique.
**Answer:** Two pointers traverse a sequence (often sorted) either toward each other (converging from opposite ends) or in the same direction (fast and slow). It reduces brute-force pair-finding algorithms from $O(N^2)$ to $O(N)$ time with $O(1)$ space.

### Q21: Explain the Sliding Window technique.
**Answer:** A window defined by two pointers slides over an array or string to track subarray/substring properties. By adding the incoming element and subtracting the outgoing element, window properties (e.g. sum, character counts) are updated in $O(1)$ time per step instead of recomputing from scratch in $O(K)$, reducing total complexity to $O(N)$.

### Q22: What is the difference between `list.extend()` and `list.append()`?
**Answer:** `append(x)` inserts `x` as a single element at the end of the list. `extend(iterable)` iterates over the argument and appends each element individually.

### Q23: How does `collections.defaultdict` work?
**Answer:** `defaultdict` takes a factory callable (e.g., `list`, `int`). When a non-existent key is accessed via `d[key]`, the factory function is called with zero arguments to automatically create and insert a default value, eliminating manual `KeyError` checks.

### Q24: What is `collections.Counter` and how does `.most_common(k)` work?
**Answer:** `Counter` is a dictionary subclass for counting hashable items. `.most_common(k)` uses `heapq.nlargest` to extract the top $K$ highest-frequency items in $O(N \log K)$ time.

### Q25: What is the amortized cost of `list.append()`?
**Answer:** While individual appends that trigger dynamic array resizing take $O(N)$ time to allocate new memory and copy pointers, resizing occurs exponentially less frequently as the list grows (growth factor $\sim 1.125$). Spreading the cost over all operations yields an **amortized cost of $O(1)$**.

---

## Part 3: Python for AI, ML, & Vector Computing (Q26 - Q40)

### Q26: What is the fundamental difference between a Python list and a NumPy `ndarray`?
**Answer:** A Python list is a dynamic array of pointers pointing to scattered `PyObject` instances in heap memory, causing cache misses and heavy memory overhead. A NumPy `ndarray` is a contiguous buffer of raw, homogeneous primitive C types (e.g., 32-bit floats) that fits in CPU cache lines and executes using SIMD hardware vector instructions.

### Q27: Explain NumPy array strides.
**Answer:** Strides are a tuple of byte steps required to advance by one index along each dimension. Strides allow zero-copy operations: transposing (`arr.T`) or slicing (`arr[::2]`) simply alters the stride metadata and shape without copying or allocating new underlying data buffers.

### Q28: State the rules of NumPy Broadcasting.
**Answer:** Two shapes are compatible for broadcasting if, starting from trailing (rightmost) dimensions:
1. The dimensions are equal, OR
2. One of the dimensions is 1.
Dimensions of size 1 are virtually stretched without memory replication to match the larger dimension.

### Q29: What is the difference between a view and a copy in NumPy/Pandas?
**Answer:** A view shares the same underlying memory buffer with the original array; mutating elements in a view mutates the original data. A copy allocates an entirely new, independent memory buffer. In NumPy, basic slicing (`arr[1:3]`) returns a view; fancy indexing (`arr[[1, 2]]`) returns a copy.

### Q30: What causes Pandas `SettingWithCopyWarning` and how do you fix it?
**Answer:** Chained indexing like `df[df['a'] > 0]['b'] = 10` causes the warning because Pandas cannot guarantee whether the intermediate slice `df[df['a'] > 0]` is a view or a copy. Fix it by using `.loc` in a single unified step: `df.loc[df['a'] > 0, 'b'] = 10`.

### Q31: Why is `df.iterrows()` considered an anti-pattern?
**Answer:** `df.iterrows()` iterates row-by-row in pure Python, does not preserve dtypes (downcasts mixed types to `object`), and instantiates a new Pandas Series for every single row, making it 100x to 1000x slower than vectorized operations.

### Q32: What is Data Leakage in an ML pipeline?
**Answer:** Data leakage occurs when information from the evaluation/test split is inadvertently exposed to the model during training. Examples include fitting a `StandardScaler` on the entire dataset before splitting, or calculating target encoding on full data. It leads to overly optimistic validation metrics that collapse in production.

### Q33: When should you use Stratified K-Fold over standard K-Fold?
**Answer:** Use `StratifiedKFold` for classification tasks, especially with imbalanced classes. It guarantees that each fold contains the exact same percentage distribution of target classes as the complete dataset.

### Q34: What is the difference between `StandardScaler` and `RobustScaler`?
**Answer:** `StandardScaler` uses mean and standard deviation, which are heavily skewed by extreme outliers. `RobustScaler` uses the **median** and **Interquartile Range (IQR)** ($Q_3 - Q_1$), ensuring feature scaling is not distorted by outliers.

### Q35: How do you build a custom Scikit-Learn transformer?
**Answer:** Inherit from `BaseEstimator` and `TransformerMixin`, and implement `fit(self, X, y=None)` and `transform(self, X)`. `TransformerMixin` provides `fit_transform()` automatically.

---

## Part 4: Generative AI, LLMs, & Systems Engineering (Q36 - Q50)

### Q36: Why is asynchronous I/O (`asyncio`) essential for high-throughput LLM applications?
**Answer:** Foundation model API calls are network-bound and take 2 to 10 seconds per request. Synchronous code blocks the thread during this time. `asyncio` uses an event loop to yield control during network wait times, allowing a single thread to manage thousands of concurrent in-flight LLM requests.

### Q37: How does Pydantic v2 achieve 10x-50x faster validation than v1?
**Answer:** Pydantic v2 rewrote its core validation and serialization engine in **Rust** (`pydantic-core`). Python type hints and validation rules are compiled into a Rust validation tree, executing parsing and constraint validation directly in compiled native code.

### Q38: Explain the Server-Sent Events (SSE) protocol in streaming LLMs.
**Answer:** SSE is a unidirectional streaming protocol over standard HTTP (`Content-Type: text/event-stream`). The server keeps the HTTP connection open and pushes token chunks prefixed with `data: `, terminating with `data: [DONE]`. This allows clients to render tokens with low Time-to-First-Token (TTFT) latency.

### Q39: What is the difference between Token rate limits (TPM) and Request rate limits (RPM)?
**Answer:** RPM limits the number of HTTP connection requests in a 60-second window. TPM limits the cumulative sum of prompt and completion tokens processed in that window. A single massive request with a 50,000-token prompt can exhaust TPM quotas even if RPM is 1.

### Q40: How does Function/Tool Calling work in LLM architectures?
**Answer:** The client provides the LLM with a JSON Schema defining available tools (name, description, parameter types). The LLM recognizes when a tool is required and emits structured JSON containing function arguments. The client runtime parses the JSON, executes the local Python function, and returns the result in the conversation context for final synthesis.

### Q41: What is the difference between Dense Retrieval and Sparse Retrieval in RAG?
**Answer:** Dense retrieval embeds text into continuous vector spaces using deep transformer models and measures semantic similarity via cosine distance. Sparse retrieval (BM25, TF-IDF) matches exact lexical keywords based on term frequency and inverse document frequency. Production systems combine both via Hybrid Search.

### Q42: What is the "Lost in the Middle" phenomenon in RAG?
**Answer:** Studies show that LLMs attend most effectively to information placed at the very beginning and very end of their context window. Relevant documents placed in the middle of long contexts are frequently missed or ignored during generation.

### Q43: What is the role of `asyncio.Semaphore` in batch LLM evaluation?
**Answer:** An `asyncio.Semaphore` limits the number of concurrent tasks entering a critical section. When firing 10,000 evaluation prompts, wrapping calls in `async with sem:` caps active concurrent requests to a safe limit (e.g. 20), preventing HTTP 429 rate-limit errors.

### Q44: How does `tiktoken` differ from Python's standard `len(text.split())`?
**Answer:** Words do not equal tokens. `len(text.split())` counts whitespace-separated words. `tiktoken` executes Byte-Pair Encoding (BPE) subword tokenization in compiled Rust, mapping subword character clusters to vocabulary integer IDs. Punctuation, whitespace, and subwords each count as distinct tokens.

### Q45: What is connection pooling in `requests.Session`?
**Answer:** `requests.Session` maintains a pool of persistent TCP connections (`urllib3.PoolManager`). Instead of performing a new DNS lookup, TCP 3-way handshake, and TLS negotiation for every HTTP call, subsequent calls reuse an open socket, saving 50-200ms per request.

### Q46: Why should you avoid `copy.deepcopy` on PyTorch tensors?
**Answer:** `copy.deepcopy` recursively duplicates all metadata, autograd computation graphs, and underlying CUDA memory buffers, which can cause severe memory bloat. In PyTorch, use `tensor.clone().detach()` to create an isolated tensor buffer detached from the computation graph.

### Q47: What is the difference between `asyncio.gather` and `asyncio.as_completed`?
**Answer:** `asyncio.gather` awaits all coroutines and returns the final results in the exact order tasks were submitted. `asyncio.as_completed` returns an iterator yielding futures as they complete, allowing immediate processing of early responses.

### Q48: How does Python's `multiprocessing` bypass the GIL?
**Answer:** `multiprocessing` spawns independent operating system processes, each running its own Python interpreter, its own memory space, and its own independent GIL. Processes communicate via IPC (Pipes, Queues, Shared Memory).

### Q49: What is the difference between EAFP and LBYL?
**Answer:** EAFP ("Easier to Ask for Forgiveness than Permission") relies on `try/except` blocks to handle failures. LBYL ("Look Before You Leap") uses defensive `if` conditions before attempting operations. EAFP is idiomatic in Python and prevents race conditions (TOCTOU).

### Q50: How do you prevent circular imports in large Python packages?
**Answer:**
1. Refactor shared models or utilities into an independent module (`types.py` or `common.py`).
2. Move imports inside specific functions (deferred imports).
3. Use `if typing.TYPE_CHECKING:` to import types exclusively for static type analysis without runtime execution.
