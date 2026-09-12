# 25 Classic Python Interview Traps and Gotchas

> Python includes several counter-intuitive behaviors arising from dynamic pointer bindings, late-binding closures, integer caching, and default argument evaluation.

---

## Trap 1: The Mutable Default Argument
```python
def append_to(element, target=[]):
    target.append(element)
    return target

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2]  <- TRAP! Default list is shared across calls!
```
**Why:** Default arguments are evaluated once at function definition time, not at invocation time.
**Fix:** Use `None` as sentinel: `def append_to(element, target=None): target = [] if target is None else target`.

---

## Trap 2: Late-Binding Closures in Loops
```python
multipliers = [lambda x: x * i for i in range(3)]
print([m(2) for m in multipliers])  # [4, 4, 4] <- TRAP! Not [0, 2, 4]!
```
**Why:** Closures look up `i` in the enclosing scope when called, at which point the loop has finished and `i = 2`.
**Fix:** Bind early via default arg: `[lambda x, i=i: x * i for i in range(3)]`.

---

## Trap 3: Small Integer Caching (-5 to 256)
```python
a = 256
b = 256
print(a is b)  # True

x = 257
y = 257
print(x is y)  # False <- TRAP!
```
**Why:** CPython pre-allocates global singletons for integers from -5 to 256. Beyond this range, distinct heap objects are allocated.

---

## Trap 4: Modifying a List While Iterating
```python
nums = [1, 2, 3, 4]
for n in nums:
    if n % 2 == 0:
        nums.remove(n)
print(nums)  # [1, 3] (Worked by coincidence)

nums = [1, 2, 2, 3]
for n in nums:
    if n == 2:
        nums.remove(n)
print(nums)  # [1, 2, 3] <- TRAP! Second '2' was skipped due to index shift!
```
**Fix:** Iterate over a copy: `for n in nums[:]:` or use list comprehension.

---

## Trap 5: The Shallow 2D Matrix Multiplication Trap
```python
matrix = [[0] * 3] * 3
matrix[0][0] = 1
print(matrix)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] <- TRAP! Mutated all 3 rows!
```
**Why:** `* 3` replicates the outer list with 3 references to the **exact same inner list**.
**Fix:** Use comprehension: `[[0] * 3 for _ in range(3)]`.

---

## Trap 6: Chained Comparison Surprises
```python
print(False == False in [False])  # True <- TRAP!
```
**Why:** Evaluated as `(False == False) and (False in [False])`. Both evaluate to `True`.

---

## Trap 7: Tuple Containing Mutable Elements
```python
t = (1, 2, [3, 4])
try:
    t[2] += [5]
except TypeError:
    pass
print(t)  # (1, 2, [3, 4, 5]) <- TRAP! Mutated despite raising TypeError!
```
**Why:** `+=` calls `__iadd__` on the list, modifying it in-place. Python then tries to reassign the result to `t[2]`, raising `TypeError` because tuples reject assignment.

---

## Trap 8: Variable Leaks in List Comprehensions (Walrus Operator)
```python
# Standard comprehension variables are scoped:
[x for x in range(3)]
# print(x) -> NameError

# But Walrus operator leaks into enclosing scope:
[y := z for z in range(3)]
print(y)  # 2 <- TRAP! Leaked into outer scope!
```

---

## Trap 9: String `split()` Without Arguments vs `split(" ")`
```python
s = "  a   b  "
print(s.split())     # ['a', 'b']
print(s.split(" ")) # ['', '', 'a', '', '', 'b', '', ''] <- TRAP!
```

---

## Trap 10: `bool()` on Non-Empty Strings
```python
print(bool("False"))  # True <- TRAP! Any non-empty string is truthy!
```

---

## Trap 11: `isinstance()` vs `type()`
```python
print(type(True) == int)        # False
print(isinstance(True, int))    # True <- TRAP! bool is a subclass of int!
```

---

## Trap 12: `finally` Block Overriding `return`
```python
def check():
    try:
        return "try"
    finally:
        return "finally"

print(check())  # "finally" <- TRAP! Finally overwrote try return!
```

---

## Trap 13: Floats and IEEE 754 Representation
```python
print(0.1 + 0.2 == 0.3)  # False <- TRAP! 0.30000000000000004
```
**Fix:** `math.isclose(0.1 + 0.2, 0.3)`.

---

## Trap 14: Class Attributes Shadowed by Instance Attributes
```python
class Node:
    count = 0

n1 = Node()
n2 = Node()
n1.count += 1
print(n1.count, n2.count, Node.count)  # 1 0 0 <- TRAP! n1 created an instance variable!
```

---

## Trap 15: In-Place Mutation with List `+=` vs `+`
```python
a = [1]
b = a
a += [2]       # In-place mutation (b reflects [1, 2])

x = [1]
y = x
x = x + [2]    # Allocates NEW list (y remains [1])
```

---

## Trap 16: `is` Comparison on Floats
```python
a = float("nan")
print(a == a)  # False <- TRAP! NaN does not equal itself!
print(a is a)  # True  (Same memory address)
```

---

## Trap 17: Bare `except:` Swallowing KeyboardInterrupt
```python
# ANTI-PATTERN:
# try: ... except: pass  <- TRAP! Prevents Ctrl+C from stopping execution!
```

---

## Trap 18: UnboundLocalError When Shadowing Globals
```python
x = 10
def f():
    # print(x)
    x = 20  # Assigning anywhere in function makes x local for entire scope!
# Calling f() raises UnboundLocalError on print(x)!
```

---

## Trap 19: Dict Keys Overwriting Equivalent Types
```python
d = {}
d[1] = "int"
d[1.0] = "float"
d[True] = "bool"
print(len(d), d[1])  # 1 'bool' <- TRAP! 1, 1.0, and True share identical hash and equality!
```

---

## Trap 20: Calling `next()` on an Exhausted Generator
```python
gen = (x for x in [1])
next(gen)
# next(gen) -> Raises StopIteration! Once exhausted, generators cannot be reset!
```

---

## Trap 21: Overwriting Built-ins Silently
```python
list = [1, 2, 3]  # Shadows built-in list constructor!
# list("abc") -> TypeError: 'list' object is not callable
```

---

## Trap 22: String Concatenation in Loops ($O(N^2)$)
```python
s = ""
for tok in ["a", "b", "c"]:
    s += tok  # Re-allocates new string on every step!
# Fix: "".join(...)
```

---

## Trap 23: Decorator Name Loss Without `@wraps`
```python
def dec(fn):
    def wrapper(): return fn()
    return wrapper

@dec
def greet(): pass
print(greet.__name__)  # 'wrapper' <- TRAP! Lost function identity!
```

---

## Trap 24: Sorting Heterogeneous Lists in Python 3
```python
# [1, "2"].sort() -> TypeError: '<' not supported between instances of 'str' and 'int'
# Python 3 strictly prohibits comparison between incompatible types!
```

---

## Trap 25: Generator Expressions in Multiple Passes
```python
data = (x for x in range(3))
sum1 = sum(data)
sum2 = sum(data)
print(sum1, sum2)  # 3 0 <- TRAP! Second sum is 0 because generator was exhausted!
```
