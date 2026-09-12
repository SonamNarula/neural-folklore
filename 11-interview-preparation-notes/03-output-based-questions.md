# 30 Tricky Python Output-Based Interview Questions

> Sharpen your mental execution trace: 30 non-trivial Python snippets with line-by-line mechanical explanations.

---

### Snippet 1
```python
nums = [1, 2, 3]
nums.append(nums)
print(len(nums), nums[3][3][0])
```
**Output:** `4 1`
**Explanation:** `nums` appends a reference to itself. Index 3 is `nums` itself. Traversing `nums[3][3]` navigates the cyclical reference back to `nums`, and index 0 is `1`.

---

### Snippet 2
```python
x = 5
def f(a=x):
    print(a)
x = 10
f()
```
**Output:** `5`
**Explanation:** Default parameter `a=x` evaluates at definition time when `x = 5`. Rebinding `x` later has no effect on `f`'s default argument tuple.

---

### Snippet 3
```python
print([i for i in range(5) if i == (i := 2)])
```
**Output:** `[2]`
**Explanation:** When `i=0`, `0 == 2` is False, but `i` is reassigned to 2 by walrus. In the next iteration, the loop advances to `i=1`, `1 == 2` is False. When `i=2`, `2 == 2` is True, yielding 2.

---

### Snippet 4
```python
a = (1, 2)
b = (1, 2)
print(a is b, [1, 2] is [1, 2])
```
**Output:** `True False` (in CPython compiler optimizations)
**Explanation:** Immutable constant tuples with primitive values are often folded and interned by the compiler to the same object. Dynamic lists are always distinct allocations.

---

### Snippet 5
```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)
print([f() for f in funcs])
```
**Output:** `[2, 2, 2]`
**Explanation:** Late binding in closures. All lambdas look up `i` in the enclosing scope after the loop finished at `i = 2`.

---

### Snippet 6
```python
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])
```
**Output:** `[0, 1, 2]`
**Explanation:** Early binding via default argument `i=i` captures the current value of `i` at each iteration.

---

### Snippet 7
```python
d = {True: "yes", 1: "no", 1.0: "maybe"}
print(len(d), d[True])
```
**Output:** `1 maybe`
**Explanation:** `True == 1 == 1.0` and all have identical hash values. They map to the same hash table entry; the final assignment `"maybe"` overwrites earlier values.

---

### Snippet 8
```python
def add(x, l=[]):
    l.append(x)
    return l

l1 = add(10)
l2 = add(20, [])
l3 = add(30)
print(l1, l2, l3)
```
**Output:** `[10, 30] [20] [10, 30]`
**Explanation:** `l1` and `l3` use the shared default list. `l2` passed an explicit new list `[]`.

---

### Snippet 9
```python
x = [1, 2, 3]
y = x[:]
x[0] = 99
print(x, y)
```
**Output:** `[99, 2, 3] [1, 2, 3]`
**Explanation:** `x[:]` creates a shallow copy. Mutating `x[0]` does not affect `y`.

---

### Snippet 10
```python
x = [[1, 2]]
y = x[:]
x[0][0] = 99
print(x, y)
```
**Output:** `[[99, 2]] [[99, 2]]`
**Explanation:** Slicing creates a shallow copy of the outer list, but the inner list reference is shared.

---

### Snippet 11
```python
print(round(2.5), round(3.5))
```
**Output:** `2 4`
**Explanation:** Python uses banker's rounding (round half to even). 2 is even; 4 is even.

---

### Snippet 12
```python
a = [1, 2]
a.extend("34")
print(a)
```
**Output:** `[1, 2, '3', '4']`
**Explanation:** Strings are iterables; `extend` unpacks each character individually.

---

### Snippet 13
```python
class A:
    x = 1
class B(A):
    pass
class C(A):
    pass

B.x = 2
A.x = 3
print(A.x, B.x, C.x)
```
**Output:** `3 2 3`
**Explanation:** `B.x = 2` creates an attribute on class `B`. `A.x = 3` updates class `A`. `C` inherits `x` from `A`, reflecting 3.

---

### Snippet 14
```python
val = None or [] or 0 or "winner" or False
print(val)
```
**Output:** `"winner"`
**Explanation:** `or` short-circuits on the first truthy value.

---

### Snippet 15
```python
val = [1] and {"a": 1} and (0,) and "done"
print(val)
```
**Output:** `"done"`
**Explanation:** `and` evaluates operands until encountering a falsy value or returns the last truthy operand. `(0,)` is a non-empty tuple (truthy).

---

### Snippet 16
```python
try:
    print(1)
except:
    print(2)
else:
    print(3)
finally:
    print(4)
```
**Output:**
```text
1
3
4
```
**Explanation:** No exception was raised, so `try`, `else`, and `finally` all execute in sequence.

---

### Snippet 17
```python
s = {1, 1.0, "1"}
print(len(s))
```
**Output:** `2`
**Explanation:** `1 == 1.0` and share the same hash, so they are deduplicated. `"1"` is a string and is preserved.

---

### Snippet 18
```python
x = (i for i in range(3))
print(list(x), list(x))
```
**Output:** `[0, 1, 2] []`
**Explanation:** Generators are single-use iterators. Once consumed by the first `list()`, the second call sees an exhausted iterator.

---

### Snippet 19
```python
print(bool([]) == False, bool(()) == False)
```
**Output:** `True True`
**Explanation:** Empty containers evaluate to `False` in boolean contexts.

---

### Snippet 20
```python
def f():
    x = 10
    def g():
        nonlocal x
        x += 5
    g()
    return x

print(f())
```
**Output:** `15`
**Explanation:** `nonlocal x` allows `g()` to rebind `x` in `f`'s enclosing scope.

---

### Snippet 21
```python
print(all([]), any([]))
```
**Output:** `True False`
**Explanation:** `all()` on an empty iterable returns `True` (vacuous truth). `any()` returns `False`.

---

### Snippet 22
```python
a = [1, 2, 3]
del a[1:2]
print(a)
```
**Output:** `[1, 3]`
**Explanation:** Slice `1:2` specifies index 1, which is deleted.

---

### Snippet 23
```python
x = [1, 2]
x *= 2
print(x)
```
**Output:** `[1, 2, 1, 2]`
**Explanation:** `*=` on lists concatenates the list with itself in-place.

---

### Snippet 24
```python
d = {"a": 1, "b": 2}
for k in d:
    d[k] = d[k] * 2
print(d["a"])
```
**Output:** `2`
**Explanation:** Mutating existing dictionary values during iteration is valid; adding or deleting keys is what raises `RuntimeError`.

---

### Snippet 25
```python
print(isinstance(lambda x: x, object))
```
**Output:** `True`
**Explanation:** Functions in Python are first-class objects inheriting from `object`.

---

### Snippet 26
```python
a = 10
b = a
a = 20
print(b)
```
**Output:** `10`
**Explanation:** Integers are immutable. Reassigning `a = 20` binds `a` to a new object; `b` still references `10`.

---

### Snippet 27
```python
t = (1,) * 3
print(t)
```
**Output:** `(1, 1, 1)`
**Explanation:** Repetition operator on a 1-element tuple creates a 3-element tuple.

---

### Snippet 28
```python
def f(x, y=None):
    if y is None:
        y = []
    y.append(x)
    return y

print(f(1), f(2))
```
**Output:** `[1] [2]`
**Explanation:** Proper sentinel pattern allocates a fresh list on every invocation.

---

### Snippet 29
```python
print(sum([True, True, False, True]))
```
**Output:** `3`
**Explanation:** `bool` is a subclass of `int` (`True == 1`, `False == 0`). `sum()` adds integers.

---

### Snippet 30
```python
print(type(1 / 1))
```
**Output:** `<class 'float'>`
**Explanation:** The `/` operator always performs true division and returns a `float` in Python 3, even for evenly divisible integers.
