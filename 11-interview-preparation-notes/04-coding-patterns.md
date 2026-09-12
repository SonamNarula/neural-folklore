# High-Frequency Coding Patterns for Technical Interviews

> Master the 5 universal coding patterns: Two Pointers, Sliding Window, Fast & Slow Pointers, Monotonic Stack, and Top-K with Heaps.

---

## Pattern 1: Two Pointers (Sorted Arrays)

**When to Use:** Input is sorted, looking for pairs, partitions, or reversing sequences in $O(N)$ time and $O(1)$ space.

### Implementation: Two Sum on Sorted Array
```python
def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int] | None:
    left, right = 0, len(nums) - 1
    while left < right:
        curr_sum = nums[left] + nums[right]
        if curr_sum == target:
            return (left, right)
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    return None

print(two_sum_sorted([2, 7, 11, 15], 9))  # (0, 1)
```

---

## Pattern 2: Sliding Window (Dynamic Size)

**When to Use:** Substrings or contiguous subarrays satisfying a condition (e.g. longest substring without repeating characters).

### Implementation: Longest Substring Without Repeating Characters
```python
def length_of_longest_substring(s: str) -> int:
    char_index_map = {}
    max_len = 0
    left = 0

    for right, char in enumerate(s):
        if char in char_index_map and char_index_map[char] >= left:
            left = char_index_map[char] + 1

        char_index_map[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len

print(length_of_longest_substring("abcabcbb"))  # 3 ("abc")
```

---

## Pattern 3: Fast and Slow Pointers (Cycle Detection)

**When to Use:** Detecting cycles in linked lists or state sequences (Floyd's Tortoise and Hare).

### Implementation: Cycle Detection
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def has_cycle(head: ListNode | None) -> bool:
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

---

## Pattern 4: Monotonic Stack (Next Greater Element)

**When to Use:** Finding the next greater or smaller element in $O(N)$ time instead of $O(N^2)$.

### Implementation: Daily Temperatures
```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    ans = [0] * n
    stack = []  # Stores indices: Monotonically decreasing stack

    for curr_idx, curr_temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < curr_temp:
            prev_idx = stack.pop()
            ans[prev_idx] = curr_idx - prev_idx
        stack.append(curr_idx)

    return ans

print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))
# [1, 1, 4, 2, 1, 1, 0, 0]
```

---

## Pattern 5: Top-K Elements with Min-Heap

**When to Use:** Extracting the top $K$ largest elements from a stream or list in $O(N \log K)$ time.

### Implementation: Top-K Frequent Elements
```python
import heapq
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    # Maintain a min-heap of size K: (frequency, num)
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)

    return [num for freq, num in heap]

print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))  # [2, 1]
```
