# Efficient Algorithms

## Outline of an efficient algorithm

```
# define variables
for ...
    # efficient algorithm
# return answer
```

A loop in an efficient algorithm may contain the following:

1. Updates a variable's value using other variables
2. Arithmetic operations related to variable updates
3. if commands that affect the variable updates

But the loop may not contain:

1. Other loops that go through the input
2. Slow operations that process the input (`count or slice operations`)
3. Slow function calls (for example `max`, `min`, and `sum` applied to the whole input)

A major challenge in the design of many algorithms is to figure out how to implement the algorithm so that the loop contains only efficient code. We will next see examples of how to achieve this.

### 1. Example: Stock trading

> You are given the price of a stock for nn days. Your task is figure out the highest profit you could have made if you had bought the stock on one day and sold it on another day.

> Consider the following situation:

| Day   | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- |
| Price | 3   | 7   | 5   | 1   | 4   | 6   | 2   | 3   |

> Here the highest profit is 6 – 1 = 5, achieved by buying on day 3 and selling on day 5.

> Solution

```python
def brute_force_best_profit(prices: list[int]):
    n = len(prices)
    max_profit = 0

    for i in range(n-1):
        for j in range(i + 1, n):
            profit = prices[j] - prices[i]
            max_profit = max(profit, max_profit)

    return max_profit

print(brute_force_best_profit([3, 7, 5, 1, 4, 6, 2, 3]))
```

The above approach is an O(n2) solution. We can instead use a single loop using the following solution. The profit on any given day can be maximized if we bought the stock on a day with the minimum price on any of the preceding days.

```python
def single_loop_best_profit(prices: list[int]):
    n = len(prices)
    max_profit = 0

    for i in range(n):
        min_buy = min(prices[0: i+1])
        max_profit = max(max_profit, prices[i] - min_buy)

    return max_profit
```

The above solution has one loop, but it is still not efficient since the min function call is an O(n) call. The above solution as well is an O(n2) solution.

We can fix the problem as follows:

```python
def better_single_loop_solution(prices: list[int]):
    n = len(prices)
    max_profit = 0
    min_buy = prices[0]

    for i in range(1, n):
        min_buy = min(prices[i], min_buy)
        max_profit = max(max_profit, prices[i] - min_buy)

    return max_profit

```

Now the value of the variable `min_buy` is not computed from scratch each time, but instead each new value is computed efficiently from the previous one. With this modification, each round of the loop needs only _O(1)_ time and the time complexity of the whole algorithm is _O(n)_, making it efficient.

Notice that the function `min` can be slow or fast. Computing the smallest value on a long list is slow, but computing the smaller of two values is fast.

I tested the time taken by the brute force algorithm and the best algo using the below code:

```python
n = random.randint(9000, 10000)
prices = [random.randint(1, 1000) for _ in range(n)]

start = time.time()
result_brute = brute_force_best_profit(prices)
end = time.time()

print("Time taken by brute force algo: ", end - start, "seconds")

start = time.time()
result_fast = better_single_loop_solution(prices)
end = time.time()

print("Time taken by fast algo: ", end - start, "seconds")
```

The results for the above code test is:

> Time taken by brute force algo: 2.6276752948760986 seconds

> Time taken by fast algo: 0.000762939453125 seconds

### 2. Example: Bit String

> You are given a bit string consisting of the characters `0` and `1`. How many ways can you select two positions in the bit string so that the left position contains the bit `0` and the right position contains the bit `1`?

> Consider the following situation:

| Position | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   |
| -------- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bit      | 0   | 1   | 0   | 0   | 1   | 0   | 1   | 1   |

> Here there are 12 such pairs of positions.

A straightforward solution is to iterate through all possible pairs of positions and count the number of times with 0 on the left and 1 on the right:

```python
def count_ways(bits):
    n = len(bits)
    result = 0
    for i in range(n):
        for j in range(i + 1, n):
            if bits[i] == '0' and bits[j] == '1':
                result += 1
    return result
```

Again, the algorithm is too slow as its time complexity is _O(n2)_.

Let us think about how we could solve the task with a single loop. As with the stock trading problem, a good approach is to consider all pairs ending at the current position simultaneously. More precisely, at a position i, we need an efficient way of counting the pairs with a bit 1 at position i and a bit 0 at a position before i.

If the bit at position i is 0, the count is obviously 0. If the bit at position i is 1, we need to know how many of the preceding positions contain a 0 bit. We get this number efficiently by keeping track of the number of 0 bits seen so far. Here is an implementation of this idea:

```python
def count_ways(bits):
    n = len(bits)
    result = 0
    zeros = 0
    for i in range(len(bits)):
        if bits[i] == '0':
            zeros += 1
        if bits[i] == '1':
            result += zeros
    return result
```

The code executed within the loop depends on whether the bit at the current position is 0 or 1. If the bit is 0, we increment the variable zeros that stores the number of zeros seen so far. If the bit is 1, we add the value zeros to the variable result, corresponding to the desired pairs with i as the right position.

The algorithm has a single loop that scans through the input, and the code inside the loop needs _O(1)_ time. Thus the algorithm is efficient as it runs in _O(n)_ time.

### 3. Example: List Splitting

> You are given a list containing nn integers. Your task is to count how many ways one can split the list into two parts so that both parts have the same total sum of elements.

> Consider the following example list:
> |Position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
> |----------|---|---|---|---|---|---|---|---|
> |Number | 1 | -1 | 1 | -1 | 1 | -1 | 1 | -1 |

> Here the number of ways is 3. We can split the list between positions 1 and 2, between positions 3 and 4, and between positions 5 and 6.

Here is a straightforward algorithm for the task:

```python
def count_splits(numbers):
    n = len(numbers)
    result = 0
    for i in range(n - 1):
        left_sum = sum(numbers[0:i+1])
        right_sum = sum(numbers[i+1:])
        if left_sum == right_sum:
            result += 1
    return result
```

The above algorithm gies through all the ways of splitting the list into two parts and calculates the sum for both parts of the list. This is an O(n2) solution.

The left sum calculation can be reduced by storing it in a variable and increasing it everytime we iterate through an element.

It will be something like this:

```python
def count_splits(numbers):
    n = len(numbers)
    result = 0
    left_sum = 0
    for i in range(n - 1):
        left_sum += numbers[i]
        right_sum = sum(numbers[i+1:])
        if left_sum == right_sum:
            result += 1
    return result
```

This is still not fast enough, because computing `right_sum` is still slow, and the trick we used for `left_sum` does not work for `right_sum`, because the list is processed in `left-to-right order`. Even with the faster computation of `left_sum`, the time complexity is still _O(n2)_.

For further improvement, we can utilize the following observation: If we know the sum of the whole list in addition to `left_sum`, we can compute `right_sum` efficiently:

```python
def count_splits(numbers):
    n = len(numbers)
    result = 0
    left_sum = 0
    total_sum = sum(numbers)
    for i in range(n - 1):
        left_sum += numbers[i]
        right_sum = total_sum - left_sum
        if left_sum == right_sum:
            result += 1
    return result

```

Since the total sum does not change during the loop, we can compute it into the variable `total_sum` before the loop. This takes _O(n)_ time but it is done only once. Then, inside the loop, `right_sum` can be computed as the difference `total_sum - left_sum`. The total time complexity of the obtained algorithm is _O(n)_.

### 4, Example: Sublists

> You are given a list containing nn integers. How many ways can we choose a sublist that contains exactly two distinct integers?

> For example, the list `[1,2,3,3,2,2,4,2]` has `14` such sublists.

My brute force approach:

```python
def count_lists(numbers: list[int]) -> int:
    n = len(numbers)
    result = 0

    for i in range(n - 1):
        map = {numbers[i]: 1}
        key_count = 1

        for j in range(i + 1, n):
            if numbers[j] not in map:
                map[numbers[j]] = 1
                key_count += 1

            if key_count > 2:
                break

            if key_count == 2:
                result += 1

    return result
```

I'll explain the approach step by step, show why the variables a and b work, and walk through the sample to make the logic and the updates clear.

High-level goal

- We want the number of contiguous sublists (subarrays) that contain exactly two distinct integers.
- Instead of enumerating all sublists, we scan once from left to right and for each end index i count how many valid sublists end exactly at i. Summing those counts gives the total.

Key observation

- Fix an end index i. Any sublist that ends at i and contains exactly two distinct values must start somewhere to the left of i. If we can locate the earliest possible start position for sublists that still have exactly those two values, then the number of valid starts is (latest allowed start index) − (earliest excluded index). The algorithm keeps enough information to compute that quickly.

What the variables a and b mean (intuition + invariant)

- a: the last index before i where the value changed (i.e., the index of the most recent occurrence of the "other" value when looking left from i). More precisely, after processing position i, a points to the index of the most recent element that is not equal to numbers[i] and that occurs immediately before the current block of equal numbers ending at i.
- b: the index of the last change before a — i.e., the most recent index strictly left of a where a different value appears (so b points to an occurrence of a third distinct value).

Invariant maintained for each i (after performing the update for i):

- The values at indices in (b, a] and in (a, i] together cover at most two distinct values: one value appears in (a, i] (the value numbers[i]) and the other value appears in (b, a] (the other value). Index b is the last index strictly to the left such that numbers[b] is different from both of those two values (or b = -1 when no third value exists yet).
- Any sublist that ends at i and uses exactly those two values must start at some index s with b < s ≤ a. So the count of valid sublists ending at i equals a − b.

Why the count of valid sublists ending at i equals a − b

- Consider the block structure looking left from i:
  - (a, i] is a contiguous block of the same value numbers[i] (could be length ≥ 1).
  - (b, a] is a block (maybe not strictly contiguous in values but contains only one other value when we consider the two-value window) that contains the other value used in valid sublists ending at i.
- If we want exactly two distinct values in a sublist ending at i, the sublist must include at least one element from (a, i] (to include numbers[i]) and at least one element from (b, a] (to include the other value). That forces the start index s to be > b (so it does not include the disallowed third value at b or earlier) and ≤ a (so the sublist includes at least one element from the other-value region). Therefore s can be any integer in {b+1, b+2, ..., a} — exactly a − b choices.

Edge cases:

- If b = −1, that means there is no earlier third distinct value — starts s can be 0..a so there are a − (−1) = a+1 starts.
- If a = −1 (meaning we have not yet seen a change from the previous element when i is at 0), then a − b is 0 and there are no valid sublists ending at that position (correct since we need two distinct values).

How a and b are updated when we move i to i+1
We only need to update when numbers[i] ≠ numbers[i−1] (a new run begins). Two cases:

1. numbers[i] ≠ numbers[a] (i.e., numbers[i] introduces a value different from the current "other" value that was stored at a)

   - This means the pair of values that might be in sublists ending at i is changing: the new value numbers[i] together with the previous run's value numbers[i−1] are the current two values, and the previous other value (which was equal to numbers[a]) becomes a third distinct value and must move into b.
   - We set b = a (the previous a becomes the index of a third value), then set a = i − 1 (the boundary between the two current values is at i − 1).
   - After this, the allowed starts for sublists ending at i are in (b, a] — i.e., a − b choices.

2. numbers[i] == numbers[a]
   - This means the new element numbers[i] matches the previous "other" value (the value that lived at a). So the two values usable for sublists ending at i are unchanged: numbers[i] and the value in (b, a].
   - We just move a forward to i − 1 (since the last boundary between the two values moves right), but b stays the same.
   - Allowed starts remain (b, a] which updated because a moved to i−1; count = a − b.

Why we compare numbers[i] to numbers[a] rather than numbers[i−1] or something else

- numbers[i−1] tells us whether the run of equal values changed at i. If numbers[i] == numbers[i−1], we are still in the same run and nothing about the two-value window changes — count at i just increases by the same increment as at i−1. Only when numbers[i] differs from numbers[i−1] does the composition of the last two runs change and we may need to move a or b.
- numbers[a] is the value of the other value in the two-value window (the value in the run directly left of the current run). If numbers[i] equals numbers[a], then numbers[i] is not introducing a new third value and only the boundary a moves. If numbers[i] differs from numbers[a], a third value is introduced, so b must be moved to track the previous second value.

Step-by-step walkthrough of the sample [1,2,3,3,2,2,4,2]
Start with a = b = −1, result = 0.
We run i from 1 to 7 and update as described. I'll show the important steps and counts:

i = 1: numbers[1] = 2, numbers[0] = 1 → change

- numbers[1] != numbers[a] (a = −1 means no value stored → treat as different)
- b = a = −1, a = i−1 = 0
- count ending at 1: a − b = 0 − (−1) = 1 → result += 1
  i = 2: numbers[2] = 3, numbers[1] = 2 → change
- numbers[2] != numbers[a] (numbers[a]=numbers[0]=1, 3 != 1) → case 1
- b = a = 0, a = 1
- count ending at 2: a − b = 1 − 0 = 1 → result += 1
  i = 3: numbers[3] = 3, numbers[2] = 3 → no change
- no update of a,b
- a − b = 1 − 0 = 1 → result += 1
  i = 4: numbers[4] = 2, numbers[3] = 3 → change
- numbers[4] != numbers[a] (numbers[a]=numbers[1]=2; 2 == 2 → equal) → case 2
- a = i − 1 = 3, b stays 0
- count: a − b = 3 − 0 = 3 → result += 3
  i = 5: numbers[5] = 2, numbers[4] = 2 → no change
- a − b = 3 − 0 = 3 → result += 3
  i = 6: numbers[6] = 4, numbers[5] = 2 → change
- numbers[6] != numbers[a] (numbers[a]=numbers[3]=3; 4 != 3) → case 1
- b = a = 3, a = 5
- count: a − b = 5 − 3 = 2 → result += 2
  i = 7: numbers[7] = 2, numbers[6] = 4 → change
- numbers[7] != numbers[a]? numbers[a]=numbers[5]=2; 2 == 2 → case 2
- a = i − 1 = 6, b stays 3
- count: a − b = 6 − 3 = 3 → result += 3

The counts per index (as given) are: [0,1,1,1,3,3,2,3] and their sum is 14.

Why initialization with a = b = −1 works

- a = −1 means "no previous boundary stored yet"; when we encounter the first change at i = 1, we treat numbers[i] != numbers[a] so we set a = 0 and b remains −1. The arithmetic a − b handles the "count of starts" correctly because with b = −1 it becomes a + 1 which counts starts from index 0.

Correctness argument (compact)

- For each i, the algorithm maintains the invariant that b is the last index to the left that contains a value different from both numbers[i] and the value in (a, i], so every start s that produces exactly two distinct values and ends at i must satisfy b < s ≤ a. Conversely, any s in (b, a] will produce a sublist ending at i with exactly two distinct values (because it includes the two runs on the right and excludes any third value at b or before). So the number of valid starts is exactly a − b. The update rules ensure the invariant is maintained when we extend i by one.

Complexity

- Single pass over the list, O(n) time and O(1) extra space.

Short intuition summary

- Keep track of the last border between the two values (a) and the previous border (b). For each end i, the valid starts are exactly those after the last forbidden index b and up to the border a, giving a − b sublists. Update a and b only when a new run begins, using whether the new run's value equals the former "other" value to decide whether the third-value pointer b must move.

```python
def count_lists(numbers: list[int]) -> int:
    n = len(numbers)
    a = b = -1
    result = 0
    for i in range(1, n):
        if numbers[i] != numbers[i - 1]:
            if numbers[i] != numbers[a]:
                b = a
            a = i - 1
        result += a - b
    return result
```
