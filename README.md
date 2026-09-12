<div align="center">

# neural-folklore

### *from software engineer to AI engineer, one broken cell at a time*
### *Schritt für Schritt — step by step*

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/status-cooking-F97316?style=for-the-badge" alt="Status"/>
<img src="https://img.shields.io/badge/focus-AI%20Engineering-7C3AED?style=for-the-badge" alt="Focus"/>
<img src="https://img.shields.io/badge/Deutsch-lernend-FFCC00?style=for-the-badge&logoColor=black" alt="German — learning"/>

<img src="https://img.shields.io/github/last-commit/SonamNarula/neural-folklore?style=for-the-badge&color=0EA5E9" alt="Last Commit"/>
<img src="https://img.shields.io/github/repo-size/SonamNarula/neural-folklore?style=for-the-badge&color=64748B" alt="Repo Size"/>

</div>

<br/>

### 📖 what even is this

I'm Sonam — final-year CSE, placement season breathing down my neck, and somewhere in between I decided to become an **AI Engineer**. Not "train models from scratch in a basement" AI engineer — the other kind: building actual things on top of LLMs. RAG pipelines, agents, tools that do stuff.

**Step zero: Python.** Turns out competitive-programming C++ did not prepare me for this at all. So this repo is me getting fluent, one notebook at a time, in public, mistakes included.

No polish for polish's sake. No "10x engineer" cosplay. Just receipts.

> **the backstory:** 500+ LeetCode, Knight tier, AtCoder Brown — the problem-solving muscle already exists, it just needs to learn a new language. Literally.

<br/>

### 🇩🇪 the long game

Python isn't the only language currently under construction. **Ziel: Deutschland, vor August 2027** — the goal is to be working there before August 2027, and this repo is one half of getting ready.

<div align="center">

<img src="https://img.shields.io/badge/Ziel-Deutschland-000000?style=for-the-badge" alt="Ziel: Deutschland"/><img src="https://img.shields.io/badge/vor-August%202027-DD0000?style=for-the-badge" alt="vor August 2027"/><img src="https://img.shields.io/badge/Fortschritt-läuft-FFCE00?style=for-the-badge" alt="läuft"/>

</div>

Two skill trees, one deadline: the AI engineering stack makes me hire-able, the German gets me *there*. Neither gets to be the excuse for skipping the other — they run in parallel, on the same clock.

<br/>

### 🗺️ the scoreboard

| module | status | the actual loot |
|:---|:---:|:---|
| `1. PYTHON BASICS` | ✅ shipped | variables, data types, casting, operators + 2 warm-ups (*largest of two numbers*, *driving-eligibility check*) |
| `2. CONTROL FLOW` | ✅ shipped | if/elif/else, loops, break/continue/pass, pattern printing, a calculator, and a hall-of-shame file for every loop bug I fell for |
| `3. Data Structures` | ✅ shipped | lists, tuples, dictionaries — mutability, `.sort()` vs `sorted()`, comprehensions, and real-world use cases (stacks, queues, data pipelines) |
| `4. Functions` — functions + lambda | ✅ shipped | `*args`/`**kwargs`, the mutable-default-argument trap, lambda vs `def`, plus six mini builds putting it to work (factorial via recursion, palindrome checker, password strength checker, shopping-cart total, temp converter, word-frequency file reader) |
| Map / Filter | 📝 notes shipped, reps pending | `map()`, `filter()`, the `filter(None, iterable)` trick for stripping falsy junk, chaining both together — written up, no notebook yet |
| NumPy / Pandas | ⏳ in the queue | — |

*no vibes-based progress here — a module only gets a ✅ when it's actually done.*

<br/>

<br/>

---

# 🧠 The Master Python for AI, ML & GenAI Curriculum

> A first-principles, implementation-first, interview-ready Python engineering compendium engineered for AI/ML researchers, LLM engineers, data scientists, and technical candidates.

---

## 1. Repository Architecture & Modules

All 12 modules and 70+ in-depth technical guides are organized topic-wise directly in this repository:

```text
neural-folklore/
│
├── 01-python-fundamentals/                   # Core language mechanics & control flow
│   ├── 01-variables-and-data-types.md         # References, id(), dynamic typing, numeric limits
│   ├── 02-input-output-and-type-conversion.md # Formatting, CLI interfaces, coercion, parsing
│   ├── 03-operators.md                        # Bitwise masks, identity vs equality, short-circuiting
│   ├── 04-conditionals.md                     # Pattern matching, dispatch tables, branch optimization
│   ├── 05-loops.md                            # Loop protocols, iterators, zip, enumerate, loop-else
│   └── 06-patterns-and-basic-problems.md      # Sliding window, two-pointer, matrix traversal
│
├── 02-data-structures/                       # Built-in data structures & memory layouts
│   ├── 01-strings.md                          # Immutability, slicing internals, tokenization, regex
│   ├── 02-lists.md                            # Dynamic array over-allocation, slicing, amortized O(1)
│   ├── 03-tuples.md                           # Immutability, hashing, namedtuples, memory footprint
│   ├── 04-sets.md                             # Hash tables, set algebra, deduplication, O(1) checks
│   ├── 05-dictionaries.md                     # Compact dicts, hash collision resolution, defaultdict
│   ├── 06-stack-and-queue.md                  # Deque vs list, thread-safe queues, LIFO/FIFO in AI
│   └── 07-comprehensions.md                   # List/Dict/Set comprehensions, generator expressions
│
├── 03-functions/                             # Functional programming & execution models
│   ├── 01-functions.md                        # First-class citizens, frame stack, pure functions
│   ├── 02-arguments-and-parameters.md         # *args, **kwargs, positional/keyword-only, mutable trap
│   ├── 03-lambda-map-filter-reduce.md         # Higher-order functions, functional pipelines
│   ├── 04-scope-and-closures.md               # LEGB rule, nonlocal, state retention, closures
│   ├── 05-recursion.md                        # Stack limits, tree traversals, memoization vs DP
│   └── 06-decorators.md                       # Wrapping, parametrized decorators, caching, retries
│
├── 04-oop/                                   # Object-Oriented Architecture for ML Systems
│   ├── 01-classes-and-objects.md              # Class vs instance namespaces, __dict__, slots
│   ├── 02-constructors-and-self.md            # __new__ vs __init__, factory classmethods
│   ├── 03-inheritance.md                      # MRO, C3 linearization, super() mechanics
│   ├── 04-polymorphism.md                     # Duck typing, ABCs, runtime protocols
│   ├── 05-encapsulation-and-abstraction.md    # Name mangling, property descriptors, public/private
│   └── 06-magic-methods.md                    # Dunder methods: __call__, __getitem__, PyTorch wrappers
│
├── 05-python-intermediate/                   # Production-grade tooling & mechanics
│   ├── 01-exceptions.md                       # Exception hierarchy, custom errors, defensive pipelines
│   ├── 02-file-handling.md                    # Large file chunking, memory-mapped files, I/O buffers
│   ├── 03-json.md                             # JSONL streaming, custom serializers, NumPy serialization
│   ├── 04-modules-and-packages.md             # sys.path, __init__.py, circular import resolution
│   ├── 05-virtual-environments-and-pip.md     # uv, pip, poetry, wheels, binary dependency management
│   ├── 06-iterators-and-generators.md         # yield, yield from, batch streaming in training loops
│   ├── 07-context-managers.md                 # __enter__/__exit__, contextlib, torch.no_grad() pattern
│   └── 08-type-hints.md                       # Static typing, TypeVar, Generics, Protocol, mypy
│
├── 06-python-for-data/                       # Vectorized numerical & tabular computing
│   ├── 01-numpy.md                            # ndarray structure, strides, C- vs Fortran-order, dtypes
│   ├── 02-numpy-indexing-and-vectorization.md # SIMD vectorization, broadcasting rules, fancy indexing
│   ├── 03-pandas-basics.md                    # Series, DataFrames, loc vs iloc, SettingWithCopyWarning
│   ├── 04-pandas-data-cleaning.md             # Imputation, categorical types, outlier filtering
│   ├── 05-pandas-groupby-merge-join.md        # Split-Apply-Combine, merge_asof, high-speed joins
│   ├── 06-pandas-time-series.md               # Resampling, lag features, rolling windows for forecasting
│   └── 07-data-processing-patterns.md         # Vectorized feature transformations, Polars contrast
│
├── 07-visualization/                         # Diagnostic & exploratory data graphics
│   ├── 01-matplotlib.md                       # Figure/Axes object-oriented API, custom layouts
│   ├── 02-seaborn.md                          # Statistical distributions, correlation heatmaps, pairplots
│   └── 03-visualization-for-ml.md             # ROC-AUC, PR curves, Confusion Matrix, Loss diagnostics
│
├── 08-python-for-ml/                         # Classical ML architecture & engineering
│   ├── 01-ml-data-pipeline.md                 # Leak-free ingestion, deterministic partitioning
│   ├── 02-feature-engineering-with-python.md  # Encoders, scalers, interactions, TF-IDF vectorization
│   ├── 03-train-test-workflow.md              # K-Fold, Stratified K-Fold, TimeSeries cross-validation
│   └── 04-scikit-learn-basics.md              # Custom BaseEstimator & TransformerMixin, Pipelines
│
├── 09-python-for-genai/                      # LLM apps, RAG, async APIs & modern schemas
│   ├── 01-http-and-apis.md                    # REST, headers, bearer tokens, rate limits, status codes
│   ├── 02-requests.md                         # Connection pooling, exponential backoff, retry adapters
│   ├── 03-environment-variables.md            # python-dotenv, secret sanitation, 12-factor config
│   ├── 04-api-response-handling.md            # Server-sent events (SSE), chunk processing, schema fails
│   ├── 05-pydantic.md                         # Pydantic v2 BaseModel, field validators, structured outputs
│   ├── 06-async-python.md                     # asyncio event loop, gather, Semaphore concurrency control
│   ├── 07-python-for-llm-applications.md      # OpenAI/Anthropic/Gemini SDKs, prompt engines, token counting
│   └── 08-python-for-rag.md                   # RAG engine from scratch: chunking, cosine math, in-mem vector DB
│
├── 10-advanced-python/                       # Systems, CPython internals & performance
│   ├── 01-memory-management.md                # Reference counting, generational GC, cyclic garbage
│   ├── 02-mutability-and-immutability.md      # Object identity, in-place mutating traps, freeze patterns
│   ├── 03-shallow-vs-deep-copy.md             # copy vs deepcopy, custom __deepcopy__, tensor references
│   ├── 04-python-internals.md                 # CPython bytecode, dis, AST, PyObject, the GIL
│   ├── 05-performance.md                      # cProfile, line_profiler, slots, algorithmic tuning
│   └── 06-concurrency.md                      # Threads vs Processes vs Coroutines, CPU-bound multiprocessing
│
├── 11-interview-preparation/                 # Interview dominance & coding mastery
│   ├── 01-python-interview-questions.md       # 50 tough conceptual & architectural interview Q&As
│   ├── 02-common-traps.md                     # 25 classic Python traps & counter-intuitive gotchas
│   ├── 03-output-based-questions.md           # 30 output-prediction puzzles with line-by-line traces
│   ├── 04-coding-patterns.md                  # Two Pointers, Sliding Window, Monotonic Queue, Top-K
│   └── 05-python-cheat-sheet.md               # Master Big-O tables, built-in method quick references
│
├── 12-project-patterns/                      # Production software engineering templates
│   ├── 01-data-processing-project.md          # Robust ETL pipeline with logging, validation & parquet
│   ├── 02-ml-project-structure.md             # Production ML repo blueprint with config management
│   ├── 03-genai-project-structure.md          # Production FastAPI + Pydantic + Async RAG service
│   └── 04-production-python-checklist.md      # Ruff, Black, pytest, pre-commit, Docker, CI/CD
│
└── 🧵 Practice Notebook Reps:
    ├── 1. PYTHON BASICS/                      # Early code reps & fundamentals
    ├── 2. CONTROL FLOW/                       # Loop & conditional notebooks
    ├── 3. Data Structures/                    # Lists, tuples, dicts notebooks
    ├── 4. Functions/                          # Function builds & mini-projects
    └── LIST IRL EXAMPLES/                     # Real-world list applications
```

---

## 2. Curated Learning Tracks

### Track A: The Generative AI & LLM Engineer
Focuses on asynchronous API consumption, prompt formatting, token manipulation, structured Pydantic schemas, and vector retrieval.
1. `01-python-fundamentals/01-variables-and-data-types.md`
2. `02-data-structures/05-dictionaries.md`
3. `03-functions/06-decorators.md`
4. `05-python-intermediate/03-json.md` & `05-python-intermediate/08-type-hints.md`
5. **Full Module**: `09-python-for-genai/` (all 8 files)
6. `12-project-patterns/03-genai-project-structure.md`

### Track B: The Machine Learning & Data Science Engineer
Focuses on vectorized calculations, high-throughput feature pipelines, cross-validation, and leak-free transformations.
1. `02-data-structures/02-lists.md` & `07-comprehensions.md`
2. **Full Module**: `06-python-for-data/` (all 7 files)
3. **Full Module**: `07-visualization/` (all 3 files)
4. **Full Module**: `08-python-for-ml/` (all 4 files)
5. `12-project-patterns/01-data-processing-project.md` & `02-ml-project-structure.md`

### Track C: Senior Interview & Python Systems Mastery
Focuses on CPython execution, memory management, the GIL, reference cycles, and interview trap patterns.
1. **Full Module**: `01-python-fundamentals/`
2. **Full Module**: `02-data-structures/`
3. **Full Module**: `04-oop/` & `05-python-intermediate/`
4. **Full Module**: `10-advanced-python/` (all 6 files)
5. **Full Module**: `11-interview-preparation/` (all 5 files)

---

## 3. Standard Chapter Structure

Every single markdown document in this curriculum adheres to a strict, rigorous pedagogical layout:
- **Title & One-Line Mental Model**: Immediate intuitive grounding.
- **1. Why This Matters**: Engineering necessity, role in AI/ML/GenAI, real-world occurrence.
- **2. Core Concept**: First-principles explanation progressing from foundational basics to advanced systems.
- **3. Mental Model**: ASCII diagrams, memory layouts, and visual mental models.
- **4. Practical Implementation & AI/ML/GenAI Use Cases**: Runnable, real-world code (tokenizers, data loaders, async inference, vector math).
- **5. Edge Cases, Pitfalls & Common Bugs**: Silent bugs, memory leaks, mutation gotchas, floating-point traps.
- **6. Interview Questions & Coding Traps**: Concept checks, output prediction snippets, and algorithmic complexity analysis.

<br/>

<div align="center">

*building in the open > building in silence*  
*Alles auf Anfang, aber mit Plan — starting over, but with a plan*

</div>
