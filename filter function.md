# filter() function

> where `map()` transforms every element, `filter()` interrogates every element and only keeps the ones that pass. same shape, opposite question.

---

## 1. what filter() does

- syntax: `filter(function, iterable)`
- runs `function` on every item in `iterable`, and keeps only the items where `function` returns a truthy value
- like `map()`, it returns a lazy **filter object** — wrap it in `list()` to actually see the result

```python
nums = [1, 2, 3, 4, 5, 6]
evens = filter(lambda x: x % 2 == 0, nums)
print(list(evens))   # [2, 4, 6]
```

- manual loop equivalent:

```python
evens = []
for x in nums:
    if x % 2 == 0:
        evens.append(x)
```

- `filter()` is that same logic collapsed into one line, once the condition is simple enough for a lambda

---

## 2. filter() with a named function

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

nums = list(range(1, 30))
primes = list(filter(is_prime, nums))
print(primes)   # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

- passing `is_prime` directly (no parentheses, no lambda) — `filter()` calls it on each element itself

---

## 3. filter() with None as the function

- a special case worth knowing: `filter(None, iterable)` removes every element that's falsy — `0`, `""`, `None`, `False`, empty lists, etc.

```python
values = [0, 1, "", "hi", None, "sonam", False, 42]
cleaned = list(filter(None, values))
print(cleaned)   # [1, 'hi', 'sonam', 42]
```

- a quick, idiomatic way to strip junk/empty values out of a list without writing a lambda for it

---

## 4. filter() vs list comprehension

```python
# filter()
list(filter(lambda x: x % 2 == 0, nums))

# list comprehension — same result, usually preferred in real code
[x for x in nums if x % 2 == 0]
```

- functionally identical — comprehension is generally considered the more Pythonic choice today, but `filter()` still appears often enough (and in interviews) that it's worth being fluent in both

---

## 5. chaining filter() and map() together

- since both return iterators, they compose naturally — filter first, then transform what survives

```python
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, nums)))
print(result)   # [4, 16, 36, 64, 100]
```

- reads inside-out: filter to evens first, *then* square what's left
- the list comprehension version of the same thing is usually easier to read at a glance:

```python
[x*x for x in nums if x % 2 == 0]
```

---

*filter() asks "does this belong?" for every element, one at a time, and only keeps the ones that say yes.*
