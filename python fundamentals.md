# Python Fundamentals — Notes (with Interview Prep)

Covers: Variables, Data Types, Operators, Control Flow.
(Data Structures — Lists/Tuples/Dicts — kept out, saving that for tomorrow.)

---

## 1. Variables in Python

### Core Concept
- A variable is just a **name bound to an object** in memory. Python is dynamically typed — the type lives with the *value*, not the variable name.
```python
x = 10          # x → int object 10
x = "ten"       # x now → str object "ten", no error
```

### Naming Rules
- Start with a letter or `_`, never a digit.
- Letters, digits, underscores only — no spaces, no hyphens.
- Case-sensitive: `total` ≠ `Total`.
- Can't use reserved keywords: `if`, `class`, `def`, `lambda`, `None`, `True`, `False`, etc.

### Multiple Assignment
```python
a, b, c = 1, 2, 3
x = y = z = 0            # all three names → same object initially
a, b = b, a               # classic swap, no temp variable needed
```

### Tips & Tricks
- **Swap without temp**: `a, b = b, a` — interviewers love asking "swap two variables without a third variable," and this is the Pythonic answer (behind the scenes it's tuple packing/unpacking).
- **Chained assignment danger with mutables**:
```python
x = y = []
x.append(1)
print(y)     # [1] — because x and y point to the SAME list object
```
  This trips people up constantly. Use `x = []; y = []` if you want independent objects.
- **Underscore `_` convention**: used for "throwaway" variables.
```python
for _ in range(5):
    print("hi")
```
- **Multiple return unpacking**: since Python functions can return tuples, this pattern is everywhere:
```python
def min_max(nums):
    return min(nums), max(nums)
lo, hi = min_max([3,1,4,1,5])
```

### Interview Angles
- *"Is Python pass-by-value or pass-by-reference?"* → Neither, exactly. Python is **pass-by-object-reference** (aka "pass by assignment"). The reference to the object is passed by value — so reassigning a parameter inside a function doesn't affect the caller, but mutating a mutable object does.
```python
def f(lst):
    lst.append(4)     # mutates original — visible outside
def g(lst):
    lst = [9,9,9]      # rebinds local name only — invisible outside
```
- *"Why does `id()` matter?"* — `id(x)` gives the memory address; useful to demonstrate whether two names point to the same object (`id(a) == id(b)` is essentially what `is` checks).
- *"What's variable shadowing?"* — a local variable with the same name as a global one "hides" it inside that scope. Common gotcha with loop variables leaking into enclosing scope in Python (unlike C++/Java, `for` loop variables aren't block-scoped).

---

## 2. Data Types in Python

### The Core Types
| Type | Example | Mutable? |
|---|---|---|
| `int` | `42`, `-7` | No |
| `float` | `3.14` | No |
| `str` | `"hi"` | No |
| `bool` | `True` | No |
| `complex` | `2+3j` | No |
| `NoneType` | `None` | — |

### Type Conversion (Casting)
```python
int("42")        # 42
int(3.99)        # 3 (truncates, doesn't round!)
float("3.14")    # 3.14
str(42)          # "42"
bool("")         # False
bool("False")    # True — any non-empty string is truthy!
```

### Tips & Tricks
- **`int()` truncates toward zero**, it does not round:
```python
int(3.9)    # 3
int(-3.9)   # -3  (not -4)
```
  Use `round()` if you actually want rounding — and note `round()` uses **banker's rounding** (round-half-to-even):
```python
round(2.5)   # 2, not 3!
round(3.5)   # 4
```
  This is a classic interview gotcha — Python doesn't round 0.5 up the way most people expect.

- **`bool("False")` is `True`** — this trips everyone up once. Non-empty strings are always truthy regardless of content.

- **`int` has no size limit** in Python (arbitrary precision) — unlike C++/Java where `int` overflows at ~2^31 or 2^63. So `2**1000` just works, no overflow.

- **Float precision**: floats are IEEE-754 doubles, so:
```python
0.1 + 0.2 == 0.3   # False!  → 0.30000000000000004
```
  Classic interview/trick question. Always compare floats with a tolerance: `abs(a-b) < 1e-9`.

- **`type()` vs `isinstance()`**: prefer `isinstance()` in real code because it respects inheritance.
```python
isinstance(True, int)   # True — bool IS a subclass of int!
type(True) == int       # False — type() is exact match only
```
  `True == 1` and `False == 0` evaluate to `True` — because `bool` is literally a subclass of `int` in Python. Popular "gotcha" interview question: *"What is `True + True`?"* → `2`.

### Interview Angles
- *"Is Python strongly or weakly typed?"* → **Strongly typed** (no implicit conversion between unrelated types like `"5" + 5` → error) but **dynamically typed** (type checked at runtime, not compile time). Don't confuse strong/weak with static/dynamic — different axes entirely.
- *"What is `None` vs `False` vs `0` vs `""`?"* → All falsy in boolean context, but distinct objects/types. `None` means "absence of value," not zero/false.
- *"Everything in Python is an object"* — even functions and classes. This is why `type(type(int))` type questions show up — worth being comfortable explaining that ints, functions, and classes are all first-class objects with an `id()` and a `type()`.

---

## 3. Operators in Python

### Arithmetic
| Op | Meaning | Example | Result |
|---|---|---|---|
| `+ - * /` | standard | `7 / 2` | `3.5` |
| `//` | floor division | `7 // 2` | `3` |
| `//` | floor division (negative!) | `-7 // 2` | `-4` (rounds toward -∞, not 0) |
| `%` | modulus | `-7 % 2` | `1` (sign follows divisor) |
| `**` | power | `2 ** 10` | `1024` |

### Tips & Tricks
- **`//` and `%` with negative numbers behave differently from C++!** In C++, `-7 / 2 == -3` (truncation toward zero) and `-7 % 2 == -1`. In Python, `-7 // 2 == -4` (floors toward negative infinity) and `-7 % 2 == 1`. This is a **very common CP (competitive programming) gotcha** when porting logic between C++ and Python — always double check sign behavior with negative operands.
- **Chained comparisons** are valid and evaluate left to right, unlike most languages:
```python
1 < x < 10          # equivalent to (1 < x) and (x < 10)
```
- **`**` right-associativity**: `2 ** 3 ** 2` → `2 ** (3 ** 2)` = `2**9` = `512`, not `(2**3)**2 = 64`.

### Comparison & Logical
- `==` compares value, `is` compares identity (same object in memory).
```python
a = [1,2,3]
b = [1,2,3]
a == b     # True (same values)
a is b     # False (different objects)
```
- **Small integer caching**: CPython caches integers from -5 to 256. So:
```python
x = 100
y = 100
x is y     # True (cached)

x = 1000
y = 1000
x is y     # False (not cached, separate objects) — behavior, not guaranteed by spec!
```
  Frequently asked as a "why does this behave weirdly" trick question. **Never rely on `is` for value comparison** — always use `==`.

- **Short-circuit evaluation**: `and`/`or` stop evaluating as soon as the result is determined.
```python
def noisy():
    print("called")
    return True

False and noisy()   # "called" never printed
True or noisy()     # "called" never printed
```
  Useful trick: `x and y` returns `y` if `x` is truthy, else returns `x` itself (not necessarily a bool!). Same for `or`. This is used for default-value idioms:
```python
name = user_input or "Guest"     # fallback if user_input is falsy/empty
```

### Assignment / Walrus Operator
- Standard: `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`
- **Walrus operator `:=`** (Python 3.8+) — assign within an expression:
```python
while (n := int(input())) != 0:
    print(n)

# useful in comprehensions too:
data = [y for x in nums if (y := x * 2) > 10]
```
  Good to mention in interviews to show you know modern Python.

### Membership & Identity
```python
3 in [1,2,3]          # True
"a" not in "abc"      # False
x is None              # preferred way to check for None (not x == None)
```
- **Tip**: always use `is None` / `is not None`, never `== None`. It's both the idiomatic style (PEP 8) and technically safer (avoids relying on `__eq__` overrides).

### Interview Angles
- *"What's the output of `5 / 2` vs `5 // 2` vs `5 % 2`?"* → `2.5`, `2`, `1`. Then follow-up with negative numbers to test if you know the floor-toward-negative-infinity behavior.
- *"Explain operator overloading."* — Python operators map to dunder methods (`+` → `__add__`, `==` → `__eq__`, etc.), which is why custom classes can define their own operator behavior. Good to mention even at a basic level — shows depth.
- *"Difference between `is` and `==`?"* — asked constantly. Answer: `==` → value equality (`__eq__`), `is` → identity equality (same memory address, same as `id(a) == id(b)`).

---

## 4. Control Flow

### Conditionals
```python
if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
else:
    grade = "C"
```
- **Ternary / conditional expression**:
```python
status = "pass" if score >= 40 else "fail"
```
- **No switch-case** in Python (until 3.10's `match-case`) — traditionally handled with `if/elif` chains or dictionaries:
```python
# dict-based "switch" — classic Pythonic trick
action = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
}.get(op, lambda a, b: None)(x, y)
```
- **`match-case`** (Python 3.10+) — actual structural pattern matching:
```python
match command:
    case "start":
        print("Starting")
    case "stop":
        print("Stopping")
    case _:
        print("Unknown")
```
  Worth mentioning if asked "does Python have switch statements" — yes, since 3.10, and it's more powerful (pattern matching, not just value matching).

### Loops
```python
for i in range(5):        # 0..4
    ...
for i in range(2, 10, 2):  # start, stop, step → 2,4,6,8
    ...
for i in range(10, 0, -1): # countdown
    ...

while condition:
    ...
```

### Loop Control
- `break` — exit loop immediately.
- `continue` — skip to next iteration.
- `pass` — no-op placeholder (syntactically required block, does nothing).
- **`for...else` / `while...else`** — the `else` block runs only if the loop completes *without* a `break`. Extremely underused but a favorite "do you really know Python" interview question.
```python
def is_prime(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            break
    else:
        return True     # only runs if loop never broke
    return False
```

### Tips & Tricks
- **`enumerate()`** — avoid manual index tracking:
```python
for idx, val in enumerate(my_list):
    print(idx, val)
for idx, val in enumerate(my_list, start=1):   # custom start index
    ...
```
- **`zip()`** — iterate multiple sequences together:
```python
names = ["a", "b"]
scores = [90, 80]
for name, score in zip(names, scores):
    print(name, score)
```
- **`range()` is lazy** (a generator-like object, not a list) — memory efficient for large ranges. `range(10**9)` doesn't allocate a billion-element list.
- **List comprehension is often faster than an explicit loop** for building lists — because the loop runs in C internally rather than the Python bytecode interpreter loop. Good micro-optimization fact for interviews.
- **Infinite loop guard**: `while True:` with an internal `break` is a very common pattern, especially for input-validation loops:
```python
while True:
    val = input("Enter a positive number: ")
    if val.isdigit():
        break
```

### Interview Angles
- *"What does `for...else` do?"* — a genuinely favorite "gotcha" question to separate people who've memorized syntax from people who understand Python's design.
- *"How would you flatten a nested loop / avoid deep nesting?"* — mention early `continue`/`return` to reduce nesting depth (a general clean-code point, not Python-specific, but commonly asked).
- *"Why is `range()` preferred over building a list of numbers manually?"* — laziness / O(1) memory regardless of range size.
- *"What's the time complexity of your loop?"* — always be ready to reason about nested loops (`O(n^2)`), even in "basic" control flow questions — interviewers often pivot straight from syntax questions into complexity analysis.

---

## Quick-Fire Gotchas (rapid revision before an interview)

- `0.1 + 0.2 != 0.3` → floating point representation issue.
- `True + True == 2` → `bool` is a subclass of `int`.
- `int(-7 / 2) == -3` but `-7 // 2 == -4` → truncation vs floor division.
- `x = y = []` then mutating `x` also changes `y` → same object reference.
- `round(2.5) == 2` → banker's rounding, not "round half up."
- `"5" + 5` → `TypeError` (Python won't silently coerce types like JS does).
- `is` vs `==` → identity vs value; never use `is` for number/string value checks.
- `for` loop variables leak into the enclosing scope (no block scoping in Python).
- `and`/`or` return one of the actual operands, not necessarily `True`/`False`.

---

*Data Structures (Lists, Tuples, Dictionaries) intentionally excluded — saved for tomorrow's session.*
