# Master Python & AI Systems Cheat Sheet

> High-density reference containing Big-O complexity tables, slicing formulas, built-in library methods, and ML tensor operations.

---

## 1. Built-in Data Structure Complexities

| Operation | `list` | `collections.deque` | `set` | `dict` |
| :--- | :--- | :--- | :--- | :--- |
| **Index Access** | $O(1)$ | $O(N)$ | N/A | N/A |
| **Append (End)** | $O(1)$ amortized | $O(1)$ | N/A | N/A |
| **Prepend (Start)**| $O(N)$ | $O(1)$ | N/A | N/A |
| **Pop (End)** | $O(1)$ | $O(1)$ | N/A | N/A |
| **Pop (Start)** | $O(N)$ | $O(1)$ | N/A | N/A |
| **Search / `in`** | $O(N)$ | $O(N)$ | $O(1)$ avg | $O(1)$ avg |
| **Insert / Delete**| $O(N)$ | $O(N)$ (middle) | $O(1)$ avg | $O(1)$ avg |

---

## 2. Sequence Slicing Syntax
`sequence[start:stop:step]`
- `s[::-1]`: Reverse sequence
- `s[::2]`: Every second element
- `s[:5]`: First 5 elements
- `s[-3:]`: Last 3 elements
- `s[1:-1]`: All elements except first and last

---

## 3. Bitwise Operators Reference
- `x & y`: Bitwise AND (masking)
- `x | y`: Bitwise OR (combining flags)
- `x ^ y`: Bitwise XOR (find single non-duplicate)
- `~x`: Bitwise NOT (`-x - 1`)
- `x << k`: Left shift ($x \cdot 2^k$)
- `x >> k`: Right shift ($x // 2^k$)

---

## 4. PyTorch / NumPy Tensor Cheatsheet
```python
# NumPy / PyTorch Tensor Reshaping:
# arr.reshape(-1, dim)       # Infer dimension dynamically
# arr.unsqueeze(0) / arr[None, :] # Add batch dimension
# arr.squeeze()              # Remove single-dimensional entries
# arr.transpose(0, 1) / arr.T# Swap axes
# arr.contiguous()           # Ensure contiguous memory buffer
# arr.detach().cpu().numpy() # Transfer tensor from GPU autograd graph to NumPy
```

---

## 5. String Manipulation & Regex Cheatsheet
```python
# Methods:
# s.strip() / s.lower() / s.replace("old", "new")
# " ".join(list_of_strings)
# s.split(",") / s.rsplit(",", maxsplit=1)

# Regex (re module):
# re.sub(pattern, replacement, text)
# re.findall(pattern, text)
# re.compile(r"...") # Precompile for 10x throughput in loops!
```
