# Python — Data Structures + Functions

Covers: Lists & List Comprehension, Tuples, Dictionaries, Real World Use Cases of Lists, Functions (Getting Started, Lambda, Map, Filter).

---

## 1. Lists and List Comprehension

### What is a List?
- A list is an **ordered, mutable** collection — order of insertion is preserved, and you can modify/add/remove items after creation.
- Duplicates are allowed, and a single list can technically hold mixed types (though it's better practice to avoid that).

```python
fruits = ["apple", "banana", "mango"]
mixed = [1, "hello", 3.14, True]   # mixed types allowed, but avoid unless needed
```

### Common Operations
```python
fruits.append("orange")       # add at the end
fruits.insert(1, "kiwi")       # insert at a specific index
fruits.remove("banana")        # remove by value (first match)
fruits.pop()                    # remove & return last element
fruits.pop(0)                   # remove & return by index
fruits.sort()                   # sort in-place
fruits.sort(reverse=True)       # descending
sorted(fruits)                  # returns a NEW sorted list, original untouched
len(fruits)                     # length
fruits[1:3]                     # slicing — start to end-1
fruits[::-1]                    # reverse the whole list (slicing trick)
```

**Important distinction**: `.sort()` modifies the list **in-place** and returns `None`. `sorted()` returns a **new list**, leaving the original unchanged.
> *Hinglish note: Isko yaad rakhne ka simple tarika — `sort()` khud list ko badal deta hai (kuch return nahi karta), `sorted()` ek naya list banake deta hai. Agar tune `x = fruits.sort()` likha, to `x` mein `None` aayega — ye ek bahut common mistake hai.*

### List Comprehension
- A compact way to build a list, instead of writing a full `for` loop.
- General syntax: `[expression for item in iterable if condition]`

```python
squares = [x**2 for x in range(10)]
# equivalent to:
squares = []
for x in range(10):
    squares.append(x**2)
```

```python
evens = [x for x in range(20) if x % 2 == 0]      # filter only even numbers
names_upper = [name.upper() for name in fruits]    # transform each element
pairs = [(x, y) for x in range(3) for y in range(3)]   # nested loop version
```

**With if/else** (conditional expression inside comprehension):
```python
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
```
> *Hinglish note: Jab if-else dono ho, order thoda alag ho jaata hai — pehle `expression if condition else expression2`, phir `for`. Jab sirf filter karna ho (else na ho), to `if` sabse aakhir mein aata hai.*

### Tips & Tricks
- List comprehensions are generally **faster** than an equivalent explicit loop, since the looping happens internally at the C level.
- Avoid deeply nested comprehensions (3+ levels) — readability suffers; a normal loop is better there.
- Interview favorite: *"List comprehension vs generator expression?"* — comprehension uses `[]` and builds the entire list in memory immediately; a generator uses `()` and produces values lazily (one at a time), which is more memory-efficient for large data.
```python
gen = (x**2 for x in range(10))   # generator expression, uses ()
```

---

## 2. Tuples In Python

### What is a Tuple?
- A tuple is also an ordered collection, similar to a list — except it's **immutable**: once created, you cannot add, remove, or modify its elements.

```python
point = (10, 20)
single = (5,)          # single-element tuple — comma is required, else it's just an int
empty = ()
```

### Operations
```python
point[0]              # indexing works just like lists
point.count(10)        # how many times a value appears
point.index(20)         # find index of a value
x, y = point            # tuple unpacking
```

### Why does immutability matter?
- Because tuples are immutable, they're **hashable** — so they can be used as dictionary keys or set elements, unlike lists.
```python
locations = {(28.7, 77.1): "Delhi", (19.0, 72.8): "Mumbai"}
```
- Tuples are also slightly **faster** and safer than lists when the data is meant to stay fixed (e.g., coordinates, RGB values) — immutability protects against accidental modification.
> *Hinglish note: Simple rule — data change hona hai to List use karo, data fixed/constant rehna hai to Tuple. Tuple thoda lightweight bhi hota hai memory ke hisaab se.*

### Interview Angle
- *"List vs Tuple — when would you use which?"* → Mutable data → List; fixed/constant data → Tuple.
- *"Tuples are immutable, so how does `t = t + (4,)` work?"* → It creates a **new** tuple; the original isn't modified — the variable `t` just gets rebound to point to the new object.

---

## 3. Dictionaries In Python

### What is a Dictionary?
- A collection of key-value pairs. Every key must be **unique**, and keys must be **hashable/immutable** (str, int, tuple — not list).
- Since Python 3.7+, dictionaries maintain **insertion order** — iteration order matches the order items were added.

```python
student = {"name": "Sonam", "age": 21, "branch": "CSE"}
```

### Common Operations
```python
student["college"] = "JECRC"      # add a new key / update existing
del student["age"]                 # delete a key
student.get("age", "N/A")          # safe access — returns default instead of erroring
student.pop("branch")               # remove & return the value
student.keys()                      # all keys
student.values()                    # all values
student.items()                     # (key, value) pairs
"name" in student                    # membership check (checks keys by default)
```

**Important**: `student["age"]` raises a **KeyError** if the key doesn't exist. Use `.get()` when you're not sure a key exists — it won't crash your program.
> *Hinglish note: Jab pakka na ho key hai ya nahi, hamesha `.get()` use karo — direct `[]` access se crash ho sakta hai agar key missing hui.*

### Dictionary Comprehension
```python
squares_dict = {x: x**2 for x in range(5)}
# {0:0, 1:1, 2:4, 3:9, 4:16}

filtered = {k: v for k, v in student.items() if v is not None}
```

### Iterating
```python
for key, value in student.items():
    print(key, "→", value)
```

### Interview Angle
- *"Why must dictionary keys be hashable?"* → Internally a dictionary is a **hash table** — a key's hash determines where its value is stored. A mutable object's hash could change if its content changes, breaking the lookup, so mutable types aren't allowed as keys.
- *"Time complexity of dictionary lookup?"* → Average case **O(1)** — this is the main reason dictionaries are much faster than a list's `in` check (`O(n)`).

---

## 4. Real World Use Cases of Lists

- **To-do lists / task queues**: `append()` to add a new task, `pop(0)` or `pop()` to remove a completed one.
- **Stack implementation**: `append()` = push, `pop()` = pop — a list already behaves like a stack (LIFO).
- **Queue-like behavior**: `pop(0)` can simulate FIFO, though for large data `collections.deque` is better — a list's `pop(0)` is O(n), while deque's is O(1).
- **Data collection/records**: student marks, sensor readings, form responses — sequential data to be processed later.
- **Data preprocessing pipelines**: using list comprehension to clean/filter/transform raw data before using it further (this pattern shows up constantly in your AI+ML roadmap too — e.g., loading a CSV row into a list and processing it).
- **Batch processing**: splitting/iterating over a large dataset in chunks via a list.

---

## 5. Functions In Python

### Getting Started With Functions
- A function is a reusable block of code — instead of repeating the same logic, define it once and call it as many times as needed.

```python
def greet(name):
    return f"Hello, {name}!"

greet("Sonam")     # "Hello, Sonam!"
```

### Default Arguments
```python
def greet(name="Guest"):
    return f"Hello, {name}!"

greet()            # "Hello, Guest!"
```

### Positional vs Keyword Arguments
```python
def add(a, b):
    return a + b

add(3, 5)             # positional
add(a=3, b=5)          # keyword — order doesn't matter
add(b=5, a=3)          # also valid
```

### `*args` and `**kwargs`
- Used when you don't know in advance how many arguments will be passed.
```python
def total(*args):            # args becomes a tuple
    return sum(args)
total(1, 2, 3, 4)              # 10

def show_info(**kwargs):      # kwargs becomes a dict
    for k, v in kwargs.items():
        print(k, v)
show_info(name="Sonam", age=21)
```

### Return vs Print
- **Common beginner mistake**: `print()` only displays something on screen — it does NOT give you the function's actual output to use elsewhere. `return` sends a value back that you can store or use further.
```python
def add_wrong(a, b):
    print(a + b)     # no return — function returns None

result = add_wrong(2, 3)   # result = None !!
```
> *Hinglish note: `print()` sirf dikhata hai, `return` value ko wapas bhejta hai jisse aage use kar sako. Ye confusion beginners mein bahut common hai.*

### Interview Angle
- *"Local vs global scope?"* → A variable defined inside a function is local to that function. To modify a global variable from inside a function, you need the `global` keyword.
```python
count = 0
def increment():
    global count
    count += 1
```
- *"Mutable default argument gotcha?"* → A classic trick question:
```python
def add_item(item, items=[]):     # DANGER — default list is created only ONCE
    items.append(item)
    return items

add_item(1)     # [1]
add_item(2)     # [1, 2]  — expected [2], but the old list is being reused!
```
  Fix: use `None` as default and create the list inside:
```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```
> *Hinglish note: Ye gotcha isliye hota hai kyunki default argument sirf ek baar, function define hote waqt banta hai — har call pe naya nahi banta. Isliye mutable default (list/dict) hamesha risky hai.*

---

## 6. Lambda Function In Python

- A lambda is an **anonymous (unnamed) function**, written in a single line — convenient when the function is small and won't be reused elsewhere.

```python
square = lambda x: x ** 2
square(5)          # 25

add = lambda a, b: a + b
add(3, 4)           # 7
```

- Normal function vs lambda — same thing, different style:
```python
def square(x):
    return x ** 2

square = lambda x: x ** 2    # equivalent, written in one line
```

### Where is it commonly used?
- Most often inside `sort()`, `map()`, `filter()` as the **key** or **transformation function**, where a small throwaway function is needed.
```python
students = [("Sonam", 21), ("Riya", 19), ("Aman", 22)]
students.sort(key=lambda x: x[1])     # sort by age
```

### Interview Angle
- *"Can a lambda contain multiple statements?"* → No, a lambda only allows a **single expression** — no separate statements like `if`/`for`/`print`. For complex logic, use a normal `def` function.
- *"Should lambdas be overused?"* → Keep them for simple cases only — if a lambda starts getting complicated, a named function is more readable and maintainable.
> *Hinglish note: Lambda ko chhoti-chhoti cheezon ke liye use karo — agar lambda padhne mein hi confusing lagne lage, seedha normal function likh do.*

---

## 7. Map Function In Python

- `map()` applies a function to **every element of an iterable**, and returns a new map object (an iterator).

```python
nums = [1, 2, 3, 4]
squared = list(map(lambda x: x**2, nums))
# [1, 4, 9, 16]
```

- Works with a normal function too, not just lambdas:
```python
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

temps = [0, 20, 30, 100]
list(map(celsius_to_fahrenheit, temps))
```

- Can take **multiple iterables** at once:
```python
a = [1, 2, 3]
b = [10, 20, 30]
list(map(lambda x, y: x + y, a, b))    # [11, 22, 33]
```

### Important Point
- `map()` is **lazy** — it doesn't compute the result immediately. Values are generated only when you consume it (via `list()` or a loop). Printing it directly shows `<map object at 0x...>` rather than the actual values.
> *Hinglish note: Isliye `map()` ka result seedha print karoge to values nahi dikhengi, ek object reference dikhega — `list()` mein wrap karna padta hai actual values dekhne ke liye.*

---

## 8. Filter Function In Python

- `filter()` selects elements from an iterable based on a condition function (one that returns `True`/`False`) — only elements that satisfy the condition are kept.

```python
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
# [2, 4, 6]
```

```python
words = ["hi", "hello", "hey", "goodbye"]
short_words = list(filter(lambda w: len(w) <= 3, words))
# ["hi", "hey"]
```

- Works with a normal function too:
```python
def is_adult(age):
    return age >= 18

ages = [12, 20, 15, 25]
list(filter(is_adult, ages))    # [20, 25]
```

### Map vs Filter vs List Comprehension — when to use which?
- `map()` → **transforms** each element.
- `filter()` → **selects** elements matching a condition.
- List comprehension → can do both at once, and is usually considered more **readable/Pythonic**:
```python
list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))
# vs (more readable):
[x**2 for x in nums if x % 2 == 0]
```

### Interview Angle
- *"map()/filter() vs comprehension — what would you prefer?"* → Modern Python generally favors comprehensions for simple cases due to readability, but `map`/`filter` are still useful when passing an already-defined function by name, or when following a functional-programming style.
- *"Why are map()/filter() lazy?"* → For memory efficiency — the entire result isn't built in memory at once for large data; values are generated element-by-element as needed.
> *Hinglish note: Simple rule of thumb — agar list comprehension se same kaam ek line mein readable ho raha hai, usko prefer karo. map/filter tab useful hain jab function pehle se defined hai ya functional style follow karni ho.*

---

*Notes cover: Section 3 (Lists, Tuples, Dictionaries, Real World List Use Cases) + Section 4 (Functions, Lambda, Map, Filter).*
