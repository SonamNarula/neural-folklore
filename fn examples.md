# more function examples

> the definitions are easy — the muscle memory comes from writing enough small functions that the shape of them stops feeling foreign. this is that practice set.

---

## 1. checking primality

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

print(is_prime(29))   # True
print(is_prime(15))   # False
```

- returns early the moment a factor is found — no need to keep checking
- looping only up to `sqrt(n)` is the standard optimization, worth internalizing early

---

## 2. reversing a string

```python
def reverse_string(s):
    return s[::-1]

print(reverse_string("neural"))   # laruen
```

- slicing with a step of `-1` is the idiomatic Python way — no manual loop needed
- worth knowing the longer loop version too, since interviews sometimes ask for it without slicing:

```python
def reverse_string_manual(s):
    result = ""
    for ch in s:
        result = ch + result
    return result
```

---

## 3. factorial (iterative and recursive)

```python
def factorial_iter(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def factorial_rec(n):
    if n <= 1:
        return 1
    return n * factorial_rec(n - 1)

print(factorial_iter(5))   # 120
print(factorial_rec(5))    # 120
```

- same answer, two mindsets — iterative builds up, recursive breaks down
- recursion needs a **base case** (`n <= 1`) or it never stops calling itself

---

## 4. fibonacci with memoization

```python
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]

print(fib(30))   # 832040, instantly — plain recursion would take a while
```

- naive recursive fibonacci recomputes the same values over and over — memoization stores answers so each `n` is solved once
- a mutable default argument (`memo={}`) is normally something to avoid, but it's a common trick specifically for memoization since the dict persists across calls

---

## 5. a function that validates its own input

```python
def divide(a, b):
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b

try:
    print(divide(10, 0))
except ValueError as e:
    print(f"error: {e}")
```

- functions don't have to trust their inputs — raising early keeps bad values from silently corrupting output further down
- pairs naturally with `try`/`except` at the call site

---

## 6. helper functions composing into one solution

```python
def is_vowel(ch):
    return ch.lower() in "aeiou"

def count_vowels(s):
    return sum(1 for ch in s if is_vowel(ch))

print(count_vowels("Neural Folklore"))   # 7
```

- `count_vowels` doesn't know *how* `is_vowel` decides — it just trusts the answer
- this is the real payoff of functions: solve a small piece once, then stop thinking about it while building the bigger piece

---

*small functions, composed — that's most of programming once the syntax stops being the obstacle.*
