<div align="center">

# neural-folklore

### *from software engineer to AI engineer, one broken cell at a time*
### *Schritt für Schritt — step by step*

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/status-shipped_%26_cooking-success?style=for-the-badge" alt="Status"/>
<img src="https://img.shields.io/badge/focus-AI%20Engineering-7C3AED?style=for-the-badge" alt="Focus"/>
<img src="https://img.shields.io/badge/Deutsch-lernend-FFCC00?style=for-the-badge&logoColor=black" alt="German — learning"/>

<img src="https://img.shields.io/github/last-commit/SonamNarula/neural-folklore?style=for-the-badge&color=0EA5E9" alt="Last Commit"/>
<img src="https://img.shields.io/github/repo-size/SonamNarula/neural-folklore?style=for-the-badge&color=64748B" alt="Repo Size"/>

</div>

<br/>

### 📖 what even is this

I'm Sonam — final-year CSE, placement season breathing down my neck, and somewhere in between I decided to become an **AI Engineer**. Not "train models from scratch in a basement" AI engineer — the other kind: building actual things on top of LLMs. RAG pipelines, agents, tools that do stuff.

**Step zero: Python.** Turns out competitive-programming C++ did not prepare me for this at all. So this repo is me getting fluent, one topic at a time, in public, mistakes included.

No polish for polish's sake. No "10x engineer" cosplay. Just serious, implementation-first engineering notes that I can use for **AI/ML, Generative AI, LLM systems, technical interviews, and production projects**.

> **the backstory:** 500+ LeetCode, Knight tier, AtCoder Brown — the problem-solving muscle already exists, it just needs to learn Python from first principles to production systems.

<br/>

### 🇩🇪 the long game

Python isn't the only language currently under construction. **Ziel: Deutschland, vor August 2027** — the goal is to be working there before August 2027, and this repo is one half of getting ready.

<div align="center">

<img src="https://img.shields.io/badge/Ziel-Deutschland-000000?style=for-the-badge" alt="Ziel: Deutschland"/><img src="https://img.shields.io/badge/vor-August%202027-DD0000?style=for-the-badge" alt="vor August 2027"/><img src="https://img.shields.io/badge/Fortschritt-läuft-FFCE00?style=for-the-badge" alt="läuft"/>

</div>

Two skill trees, one deadline: the AI engineering stack makes me hire-able, the German gets me *there*. Neither gets to be the excuse for skipping the other — they run in parallel, on the same clock.

<br/>

---

### 🗺️ the scoreboard — 12 modules shipped

| module | status | what's inside |
|:---|:---:|:---|
| [`01-python-fundamentals`](./01-python-fundamentals) | ✅ shipped | Dynamic typing, pointer labels, formatting & CLI I/O, bitwise operators, pattern matching (`match/case`), loop protocols, and foundational two-pointer / sliding-window patterns |
| [`02-data-structures`](./02-data-structures) | ✅ shipped | String immutability & tokenization, dynamic array over-allocation, compact hash tables (dicts), sets, `collections.deque` vs `list` queues, and list/dict/set comprehensions |
| [`03-functions`](./03-functions) | ✅ shipped | First-class citizens, `*args`/`**kwargs`, positional-only (`/`) and keyword-only (`*`), lambda/map/filter/reduce, LEGB scope & closures, recursion limits, and resilient retry decorators |
| [`04-oop`](./04-oop) | ✅ shipped | Class vs instance namespaces, `__slots__` memory savings, `__new__` vs `__init__`, MRO & C3 Linearization, polymorphism & ABCs, property descriptors, and PyTorch `__call__`/`__getitem__` dunders |
| [`05-python-intermediate`](./05-python-intermediate) | ✅ shipped | Exception hierarchies & chaining, chunked file streaming for 50GB datasets, JSONL parsing, modules & circular import fixes, `uv` & venvs, generators (`yield`/`yield from`), and static typing (`mypy`) |
| [`06-python-for-data`](./06-python-for-data) | ✅ shipped | NumPy `ndarray` architecture, strides, SIMD vectorization, broadcasting rules, Pandas `loc`/`iloc`, `SettingWithCopyWarning`, data cleaning, GroupBy Split-Apply-Combine, Time Series, and Polars |
| [`07-visualization`](./07-visualization) | ✅ shipped | Matplotlib Object-Oriented API (`fig, ax`), multi-plot grids, Seaborn statistical distributions & heatmaps, and ML diagnostics (ROC-AUC, Precision-Recall, Confusion Matrix, loss curves) |
| [`08-python-for-ml`](./08-python-for-ml) | ✅ shipped | Leak-free data pipelines, feature scaling (`RobustScaler`), categorical encodings, Stratified K-Fold & TimeSeries cross-validation, and Scikit-Learn custom `BaseEstimator` / `Pipeline` wrappers |
| [`09-python-for-genai`](./09-python-for-genai) | ✅ shipped | HTTP/REST fundamentals, `requests.Session` connection pooling, secret management, Server-Sent Events (SSE) token streaming, Pydantic v2 schemas, `asyncio` & `Semaphore`, tool calling, and RAG from scratch |
| [`10-advanced-python`](./10-advanced-python) | ✅ shipped | Reference counting, generational cyclic GC, mutability gotchas, shallow vs deep copy, CPython bytecode & the GIL, profiling (`cProfile`/`timeit`), and Multiprocessing vs Threading vs AsyncIO |
| [`11-interview-preparation`](./11-interview-preparation) | ✅ shipped | Top 50 conceptual & systems interview Q&As, 25 classic Python traps, 30 tricky output-prediction puzzles with line-by-line traces, 5 core coding patterns, and a master Big-O cheat sheet |
| [`12-project-patterns`](./12-project-patterns) | ✅ shipped | Production ETL pipeline architecture, modular ML repository template, production FastAPI GenAI microservice blueprint, and a comprehensive enterprise production checklist |

*no vibes-based progress here — every module is implemented with first-principles explanations, mental models, real AI/ML code, and interview traps.*

<br/>

---

### 🧠 the deep dives that actually slap

- [**Memory Management & Garbage Collection**](./10-advanced-python/01-memory-management.md) — Not hand-waving "Python has GC", but how `ob_refcnt` works in C, how the generational collector reclaims cyclical islands, why `del` doesn't immediately delete objects, and why Meta/Instagram disabled GC on their web workers to save 10% RAM.
- [**RAG Engine from Scratch**](./09-python-for-genai/08-python-for-rag.md) — Building an in-memory vector retrieval engine using pure Python and NumPy: chunking strategies, dense embedding vectors, cosine similarity dot products, and contextual prompt injection.
- [**25 Classic Python Traps**](./11-interview-preparation/02-common-traps.md) — The ultimate candidate survival guide: mutable default arguments, late binding closures in loops, small integer caching (-5 to 256), `matrix = [[0]*3]*3` aliasing, tuple with mutable list edge cases, and walrus operator scope leaks.
- [**CPython Internals, Bytecode & the GIL**](./10-advanced-python/04-python-internals.md) — Decompiling bytecode with `dis`, the `PyObject` C-struct, why NumPy and PyTorch bypass the GIL during tensor math, and what PEP 703 (Free-threaded Python 3.13) means for multi-core AI computing.
- [**Pydantic v2 & Structured LLM Outputs**](./09-python-for-genai/05-pydantic.md) — Rust-backed `pydantic-core` validation, field validators, extracting reliable JSON schemas for tool calling, and self-correcting schema errors.
- [**AsyncIO & Concurrency Limits**](./09-python-for-genai/06-async-python.md) — Single-threaded cooperative multitasking, why threads don't speed up CPU-bound tasks, and using `asyncio.Semaphore` to run high-throughput batch LLM evaluations without hitting HTTP 429 rate limits.
- [**Top 50 Interview Questions**](./11-interview-preparation/01-python-interview-questions.md) — Rigorous technical answers covering language fundamentals, data structures, vector computing, and Generative AI systems architecture.

<br/>

---

### 🧵 the hands-on practice reps

*Übung macht den Meister* — practice makes the master. The repository also preserves every hands-on Jupyter notebook I ran and broke:

- [`1. PYTHON BASICS/`](./1.%20PYTHON%20BASICS) — Variables, data types, type casting, operators + warm-up builds (*Largest of Two Numbers*, *Driving Eligibility*).
- [`2. CONTROL FLOW/`](./2.%20CONTROL%20FLOW) — If/elif/else, while and for loops, break/continue/pass, nested loop pattern printing, interactive calculator, and a running `common_errors.ipynb` diary.
- [`3. Data Structures/`](./3.%20Data%20Structures) — Hands-on notebooks for Lists (`3.1-Lists`), Tuples (`3.2-Tuples`), and Dictionaries (`3.3-Dictionaries`).
- [`4. Functions/`](./4.%20Functions) — `4.1-functions` and `4.2-Lambda Functions`, plus six mini builds: *FactorialUsingRecursion*, *PalindromeString*, *PasswordStrengthChecker*, *Shopping Cart Total*, *temperatureConversion*, and *ReadAFileAndCountTheFrequencyOfEachWord*.
- [`LIST IRL EXAMPLES/`](./LIST%20IRL%20EXAMPLES) — Real-world list applications (*ToDoList*, *CollectingUserFeedback*, *StudentsGrades*, *ManagingInventory*).

<br/>

---

### 🧭 curated learning tracks

Depending on what you're prepping for, follow these reading orders:

#### Track 1: The Generative AI & LLM Engineer
*Goal: Build scalable agentic workflows, production RAG pipelines, and high-throughput async LLM services.*
1. [`01-python-fundamentals/01-variables-and-data-types.md`](./01-python-fundamentals/01-variables-and-data-types.md) & [`03-functions/06-decorators.md`](./03-functions/06-decorators.md)
2. [`05-python-intermediate/03-json.md`](./05-python-intermediate/03-json.md) & [`05-python-intermediate/08-type-hints.md`](./05-python-intermediate/08-type-hints.md)
3. **Full Module**: [`09-python-for-genai/`](./09-python-for-genai) (HTTP, Requests Pooling, Pydantic v2, AsyncIO, LLM SDKs, RAG from Scratch)
4. [`12-project-patterns/03-genai-project-structure.md`](./12-project-patterns/03-genai-project-structure.md)

#### Track 2: The Machine Learning & Data Science Engineer
*Goal: Master high-performance vectorized operations, leak-free feature pipelines, and Scikit-Learn architecture.*
1. [`02-data-structures/02-lists.md`](./02-data-structures/02-lists.md) & [`02-data-structures/07-comprehensions.md`](./02-data-structures/07-comprehensions.md)
2. **Full Module**: [`06-python-for-data/`](./06-python-for-data) (NumPy Strides, SIMD Vectorization, Pandas, Time Series, Polars)
3. **Full Module**: [`07-visualization/`](./07-visualization) (Matplotlib OO, Seaborn, ML Diagnostics)
4. **Full Module**: [`08-python-for-ml/`](./08-python-for-ml) (Leak-free Pipelines, Feature Engineering, CV Workflow)
5. [`12-project-patterns/01-data-processing-project.md`](./12-project-patterns/01-data-processing-project.md) & [`12-project-patterns/02-ml-project-structure.md`](./12-project-patterns/02-ml-project-structure.md)

#### Track 3: Senior Python & Technical Interview Mastery
*Goal: Ace coding assessments, output-prediction rounds, and deep systems interviews.*
1. [`01-python-fundamentals/`](./01-python-fundamentals) & [`02-data-structures/`](./02-data-structures)
2. [`04-oop/`](./04-oop) & [`05-python-intermediate/`](./05-python-intermediate)
3. **Full Module**: [`10-advanced-python/`](./10-advanced-python) (Memory Management, Mutability, Copies, Bytecode/GIL, Concurrency)
4. **Full Module**: [`11-interview-preparation/`](./11-interview-preparation) (Top 50 Q&A, 25 Classic Traps, 30 Output Puzzles, Coding Patterns, Cheat Sheet)

<br/>

---

### 🛠️ tech stack — live in rotation

<div align="center">

<img src="https://img.shields.io/badge/Python%203.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+"/>
<img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=4DABCF" alt="NumPy"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn"/>
<img src="https://img.shields.io/badge/Pydantic%20v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic v2"/>
<img src="https://img.shields.io/badge/AsyncIO-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="AsyncIO"/>
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
<img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter"/>
<img src="https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white" alt="VS Code"/>

</div>

<br/>

<div align="center">

*building in the open > building in silence*  
*Alles auf Anfang, aber mit Plan — starting over, but with a plan*

</div>\n