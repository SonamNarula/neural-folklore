# functions in python

> a function is just a named piece of behaviour — you write the logic once, then summon it by name whenever you need it. everything below builds on that one idea.

---

## 1. introduction to functions

- a function is a reusable block of code that runs only when it's called
- exists to avoid repeating the same logic — write once, reuse everywhere
- makes code modular: each function does one job, and the program becomes a collection of small, readable pieces
- two kinds:
  - **built-in functions** — already given to you (`print()`, `len()`, `type()`, `sum()`, etc.)
  - **user-defined functions** — the ones you write yourself for your own logic
- benefits worth remembering:
  - reusability — call it 100 times, write it once
  - readability — `is_prime(n)` reads better than 8 raw lines of loop logic sitting in the middle of a script
  - easier debugging — a bug lives inside one function, not scattered across the file

---

## 2. defining functions

- a function is defined using the `def` keyword, followed by a name, parentheses, and a colon
- the body is indented — Python uses indentation instead of `{ }` to mark scope

```python
def greet():
    print("hey, welcome back")
```

- naming rules follow normal variable rules: no spaces, can't start with a digit, case-sensitive
- convention: lowercase with underscores — `calculate_area`, not `CalculateArea`
- a function that's defined but never called simply sits there — defining is not the same as running

---

## 3. calling functions

- to actually run a function, you write its name followed by `()`
- until it's called, the code inside never executes — Python just registers that the function exists

```python
def greet():
    print("hey, welcome back")

greet()   # this is the call — output happens only now
```

- a function can be called as many times as needed, from anywhere below its definition
- one function can call another function inside it — this is normal and common

```python
def square(n):
    return n * n

def sum_of_squares(a, b):
    return square(a) + square(b)   # square() called from inside another function

print(sum_of_squares(2, 3))   # 13
```

---

## 4. function parameters

- parameters are placeholders listed inside the `()` at definition time — they let a function accept input
- arguments are the actual values you pass in when calling the function
- a function can take any number of parameters, separated by commas

```python
def add(a, b):
    return a + b

print(add(4, 5))   # 4 and 5 are arguments, mapped to a and b
```

- Python matches arguments to parameters **positionally** by default — order matters
- you can override that using **keyword arguments**, passing `name=value` so order stops mattering

```python
def introduce(name, age):
    print(f"{name} is {age} years old")

introduce(age=21, name="sonam")   # works fine, order doesn't matter here
```

---

## 5. default parameters

- a parameter can be given a default value in the definition — used only when the caller doesn't supply one
- lets a function stay flexible without forcing every call site to pass every argument

```python
def greet(name, greeting="hello"):
    print(f"{greeting}, {name}")

greet("sonam")                 # hello, sonam
greet("sonam", "good morning") # good morning, sonam
```

- rule: parameters with default values must come **after** the non-default ones in the definition — Python won't let a default parameter sit before a required one
- useful whenever a function has one "usual" value but occasionally needs to be overridden

---

## 6. variable-length arguments

- sometimes you don't know in advance how many arguments will be passed — Python handles this with `*args` and `**kwargs`

**`*args`** — collects any number of *positional* arguments into a tuple

```python
def total(*args):
    return sum(args)

print(total(1, 2, 3, 4))   # 10
```

**`**kwargs`** — collects any number of *keyword* arguments into a dictionary

```python
def show_profile(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

show_profile(name="sonam", role="dsa captain")
```

- naming `args`/`kwargs` is just convention — the `*` and `**` are what actually matter
- order in a definition, if combined: normal params → `*args` → default params → `**kwargs`

---

## 7. return statement

- `return` sends a value back to wherever the function was called from, and immediately ends the function's execution
- without a `return`, a function implicitly returns `None`
- `print()` only *displays* a value — it doesn't hand it back for further use. `return` is what makes a function's output usable elsewhere in the program

```python
def square(n):
    return n * n

result = square(5)   # result now holds 25, usable further down
print(result * 2)    # 50
```

- a function can return multiple values at once — Python packs them into a tuple automatically

```python
def min_max(nums):
    return min(nums), max(nums)

low, high = min_max([4, 1, 9, 2])
```

- anything written after a `return` inside the same block never executes — it's dead code

---

*seven ideas, one thread: define once, call anywhere, pass what changes, get something back.*
