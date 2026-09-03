# Python Fundamentals — Notes

Covers: Variables, Data Types, Operators, Control Flow, and core Data Structures (Lists, Tuples, Dictionaries).

---

## 1. Variables in Python

- A variable is a name that refers to a value stored in memory. Python is **dynamically typed** — you don't declare a type, it's inferred at assignment.

```python
name = "Sonam"        # str
age = 21               # int
gpa = 8.7               # float
is_student = True      # bool
```

- **Rules for naming variables**
  - Must start with a letter or underscore (`_`), not a digit.
  - Can contain letters, digits, underscores.
  - Case-sensitive (`Age` ≠ `age`).
  - Cannot be a reserved keyword (`if`, `for`, `class`, etc.).

- **Multiple assignment**
```python
a, b, c = 1, 2, 3
x = y = z = 0          # all point to the same value initially
```

- **Dynamic typing** — a variable can be reassigned to a different type:
```python
val = 10
val = "now a string"   # perfectly valid
```

- **Variable scope** (preview — covered in depth with functions):
  - Local: defined inside a function.
  - Global: defined at the top level of a script/module.

- **Memory model**: variables are references (names) pointing to objects, not containers holding values directly. This matters later with mutable vs immutable types.

---

## 2. Basic Data Types in Python

| Type | Example | Notes |
|---|---|---|
| `int` | `10`, `-5` | Arbitrary precision (no overflow like C++) |
| `float` | `3.14`, `2.0` | Double-precision floating point |
| `str` | `"hello"` | Immutable sequence of characters |
| `bool` | `True`, `False` | Subclass of `int` (`True == 1`) |
| `complex` | `2 + 3j` | Rarely used in general programming |
| `NoneType` | `None` | Represents "no value" |

- **Type checking & conversion**
```python
type(10)          # <class 'int'>
int("5")          # 5
float("3.14")     # 3.14
str(100)          # "100"
bool(0)           # False
```

- **Truthy / Falsy values**
  - Falsy: `0`, `0.0`, `""`, `[]`, `{}`, `()`, `None`, `False`
  - Everything else is truthy.

- **Mutable vs Immutable**
  - Immutable: `int`, `float`, `str`, `bool`, `tuple`
  - Mutable: `list`, `dict`, `set`

---

## 3. Operators in Python

### Arithmetic Operators
| Operator | Meaning | Example |
|---|---|---|
| `+` | Addition | `5 + 2 → 7` |
| `-` | Subtraction | `5 - 2 → 3` |
| `*` | Multiplication | `5 * 2 → 10` |
| `/` | Division (float) | `5 / 2 → 2.5` |
| `//` | Floor division | `5 // 2 → 2` |
| `%` | Modulus | `5 % 2 → 1` |
| `**` | Exponent | `5 ** 2 → 25` |

### Comparison Operators
`==`, `!=`, `>`, `<`, `>=`, `<=` → always return `bool`.

### Logical Operators
`and`, `or`, `not` — short-circuit evaluation applies (e.g., in `a and b`, `b` isn't evaluated if `a` is falsy).

### Assignment Operators
`=`, `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`

### Identity vs Membership vs Equality
```python
a is b        # checks if same object in memory
a == b        # checks if values are equal
x in [1,2,3]  # membership check
```

- **Common gotcha**: `is` compares identity, `==` compares value. Small integers and short strings may be cached (interned) by CPython, so `is` can behave inconsistently — always use `==` for value comparison.

---

## 4. Control Flow

### 4.1 Conditional Statements
```python
if condition1:
    # block
elif condition2:
    # block
else:
    # block
```
- Indentation (not braces) defines blocks — standard is 4 spaces.
- Ternary/conditional expression: `x = a if condition else b`

### 4.2 Loops

**`for` loop** — iterates over a sequence (list, string, range, etc.)
```python
for i in range(5):      # 0,1,2,3,4
    print(i)

for ch in "abc":
    print(ch)
```

**`while` loop** — runs while condition is `True`
```python
i = 0
while i < 5:
    print(i)
    i += 1
```

**Loop control statements**
- `break` — exits the loop entirely.
- `continue` — skips to the next iteration.
- `pass` — does nothing, acts as a placeholder.
- `else` on a loop — executes if the loop completes *without* hitting `break`.

```python
for i in range(5):
    if i == 3:
        break
else:
    print("Loop finished without break")   # won't print here
```

---

## 5. Data Structures Using Python

### 5.1 Lists
- Ordered, **mutable**, allows duplicates, can hold mixed types.

```python
nums = [1, 2, 3, 4]
nums.append(5)          # add to end
nums.insert(0, 0)       # insert at index
nums.remove(3)          # remove by value
nums.pop()              # remove & return last element
nums.sort()             # sort in place
nums.reverse()          # reverse in place
len(nums)               # length
nums[1:3]               # slicing
```

**List Comprehension** — compact way to build lists.
```python
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
pairs = [(x, y) for x in range(3) for y in range(3)]
```
General form: `[expression for item in iterable if condition]`

### 5.2 Tuples
- Ordered, **immutable**, allows duplicates.

```python
t = (1, 2, 3)
single = (5,)            # comma needed for single-element tuple
t[0]                      # indexing works like lists
t.count(2)                # count occurrences
t.index(3)                # find index of value
```
- Use tuples for fixed collections (e.g., coordinates) — faster and safer than lists since they can't be accidentally modified.
- **Tuple unpacking**:
```python
x, y = (10, 20)
```

### 5.3 Dictionaries
- Unordered (insertion-ordered since Python 3.7+), **mutable**, key-value pairs, keys must be unique & hashable (immutable types).

```python
person = {"name": "Sonam", "age": 21}
person["college"] = "JECRC"     # add/update
del person["age"]               # delete a key
person.get("age", "N/A")        # safe access with default
person.keys()                   # dict_keys view
person.values()                 # dict_values view
person.items()                  # dict_items view (key, value pairs)
```

**Dictionary Comprehension**
```python
squares_dict = {x: x**2 for x in range(5)}
```

**Iterating a dictionary**
```python
for key, value in person.items():
    print(key, value)
```

### 5.4 Real-World Use Cases of Lists
- Storing collections of records (e.g., student marks, to-do items).
- Queues/stacks (using `append`/`pop`).
- Data preprocessing pipelines (filtering, transforming with comprehensions).
- Representing rows of tabular data before converting to structured formats (e.g., DataFrames).

---

## Quick Reference: List vs Tuple vs Dict

| Feature | List | Tuple | Dict |
|---|---|---|---|
| Mutable | ✅ | ❌ | ✅ |
| Ordered | ✅ | ✅ | ✅ (3.7+) |
| Duplicates allowed | ✅ | ✅ | Keys: ❌ / Values: ✅ |
| Syntax | `[]` | `()` | `{}` |
| Use case | Dynamic collections | Fixed/constant data | Key-value lookups |

---

*Notes compiled from course progress: Section 1 (Introduction) through Section 3 (Data Structures Using Python).*
