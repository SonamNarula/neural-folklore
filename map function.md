# map() function

> `map()` takes a function and a sequence, and applies that function to every single element — no loop written by hand. it's the "do this to everything" tool.

---

## 1. what map() does

- syntax: `map(function, iterable)`
- applies `function` to every item in `iterable`, one at a time, and returns a **map object** — a lazy iterator, not a list
- to actually see the results, wrap it in `list()`, `tuple()`, or iterate over it directly

```python
nums = [1, 2, 3, 4]
squared = map(lambda x: x * x, nums)
print(list(squared))   # [1, 4, 9, 16]
```

- this replaces the manual loop version:

```python
squared = []
for x in nums:
    squared.append(x * x)
```

- both do the same thing — `map()` is just the one-line version once the transformation is simple enough to fit in a lambda

---

## 2. map() with a named function

- the function passed in doesn't have to be a lambda — any function that takes one argument works

```python
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

temps = [0, 20, 37, 100]
converted = list(map(celsius_to_fahrenheit, temps))
print(converted)   # [32.0, 68.0, 98.6, 212.0]
```

---

## 3. map() over multiple iterables

- `map()` can take more than one iterable — the function then needs that many arguments, and it pairs up elements positionally

```python
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
print(sums)   # [11, 22, 33]
```

- stops as soon as the shorter iterable runs out, if the lengths don't match

---

## 4. map() vs list comprehension

- both do the same job — `map()` is arguably faster for simple cases, list comprehension is usually considered more readable in Python

```python
# map()
list(map(lambda x: x * x, nums))

# list comprehension — same result
[x * x for x in nums]
```

- most Python style guides lean toward list comprehensions for anything with a condition attached, since `map()` combined with `filter()` and a lambda gets hard to read fast:

```python
# gets messy
list(map(lambda x: x*x, filter(lambda x: x % 2 == 0, nums)))

# reads better
[x*x for x in nums if x % 2 == 0]
```

- `map()` is still worth knowing well — it shows up constantly in interview answers and in codebases that lean functional

---

## 5. a practical use — converting input types

- a very common real-world one-liner: converting a line of space-separated numbers into a list of ints

```python
line = "3 1 4 1 5 9"
nums = list(map(int, line.split()))
print(nums)   # [3, 1, 4, 1, 5, 9]
```

- this exact pattern shows up constantly in competitive programming input parsing

---

*map() answers one question: "what does this look like after I apply f to every element?" — nothing more, nothing less.*
