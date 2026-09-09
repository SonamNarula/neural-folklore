# lambda functions

> a lambda is a function stripped down to just the part that matters — the expression. no name, no `def`, no `return` keyword, gone the moment it's used unless you deliberately keep it.

---

## 1. what a lambda is

- an **anonymous function** — defined without `def` and without a name, using the `lambda` keyword
- syntax: `lambda arguments: expression`
- the expression is evaluated and returned automatically — no `return` keyword needed, and there can only be one expression, not a block of statements

```python
square = lambda x: x * x
print(square(5))   # 25
```

- functionally the same as:

```python
def square(x):
    return x * x
```

- the difference isn't power, it's intent — a lambda says "this is small and disposable," a `def` says "this is a real, named piece of logic"

---

## 2. multiple arguments

- a lambda can take more than one argument, comma-separated, same as a normal function

```python
add = lambda a, b: a + b
print(add(3, 4))   # 7

full_name = lambda first, last: f"{first} {last}"
print(full_name("sonam", "narula"))
```

---

## 3. why lambdas exist — using them inline

- their real use case is being passed *into* other functions, on the spot, without cluttering the code with a separate named function you'll never reuse

```python
nums = [5, 2, 9, 1, 7]
nums.sort(key=lambda x: -x)   # sort descending, without writing a separate function
print(nums)   # [9, 7, 5, 2, 1]
```

- `sorted()` with a custom key is the classic use case:

```python
students = [("aman", 82), ("sonam", 91), ("riya", 76)]
top_first = sorted(students, key=lambda s: s[1], reverse=True)
print(top_first)   # sorted by score, highest first
```

---

## 4. conditional logic inside a lambda

- a lambda can hold a ternary expression, since a ternary is still just one expression

```python
check = lambda n: "even" if n % 2 == 0 else "odd"
print(check(7))   # odd
```

---

## 5. where lambdas stop being a good idea

- if the logic needs more than one line, a loop, or multiple statements — that's a `def`, not a lambda, no exceptions
- a lambda assigned to a variable and reused repeatedly is really just a `def` in disguise, and should probably become one — readability drops fast once a lambda gets nested or chained
- rule of thumb: lambda for a one-off throwaway used *inside* another call (`sort`, `map`, `filter`); `def` for anything that has a name worth remembering

```python
# fine — quick, inline, disposable
sorted(nums, key=lambda x: abs(x))

# not fine — this deserved to be a real function
process = lambda x: x**2 if x > 0 else -x**2 if x < 0 else 0
```

---

*a lambda is a function with its name filed off — useful exactly until you find yourself wanting to give it one.*
