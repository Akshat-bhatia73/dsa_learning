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

| Position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|----------|---|---|---|---|---|---|---|---|
| Bit | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 1 |

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