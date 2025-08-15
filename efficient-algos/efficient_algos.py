import random
import time

"""
> You are given the price of a stock for nn days. Your task is figure out the highest profit you could have made if you had bought the stock on one day and sold it on another day.

> Consider the following situation:

| Day | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Price | 3 | 7 | 5 | 1 | 4 | 6 | 2 |3 |

> Here the highest profit is 6 – 1 = 5, achieved by buying on day 3 and selling on day 5.
"""


def brute_force_best_profit(prices: list[int]):
    """
    Brute force function to calculate max profit between two trading days.
    This is an O(n2) approach
    """
    n = len(prices)
    max_profit = 0

    for i in range(n - 1):
        for j in range(i + 1, n):
            profit = prices[j] - prices[i]
            max_profit = max(profit, max_profit)

    return max_profit


def single_loop_best_profit(prices: list[int]):
    """
    The highest profit can be earned by buying when the price was minimum on a preceding day.
    This can be done using a single loop.
    """
    n = len(prices)
    max_profit = 0

    for i in range(n):
        min_buy = min(prices[0 : i + 1])
        max_profit = max(max_profit, prices[i] - min_buy)

    return max_profit


def better_single_loop_solution(prices: list[int]):
    """
    Similar to the solution above but without calculating min for the complete preceding list in each iteration, we save the min buy price while iterating through the array.

    This is an O(n) solution.
    """
    n = len(prices)
    max_profit = 0
    min_buy = prices[0]

    for i in range(1, n):
        min_buy = min(prices[i], min_buy)
        max_profit = max(max_profit, prices[i] - min_buy)

    return max_profit


"""
> You are given a bit string consisting of the characters `0` and `1`. How many ways can you select two positions in the bit string so that the left position contains the bit `0` and the right position contains the bit `1`?

> Consider the following situation:

| Position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|----------|---|---|---|---|---|---|---|---|
| Bit | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 1 |

> Here there are 12 such pairs of positions.
"""


def brute_force_bit(bits: list[str]):
    n = len(bits)
    result = 0

    for i in range(n - 1):
        if bits[i] == "1":
            continue
        for j in range(i + 1, n):
            if bits[i] == "0" and bits[j] == "1":
                result += 1

    return result


def efficient_bits(bits: list[str]):
    zeroes = 0
    result = 0

    for bit in bits:
        if bit == "1":
            result += zeroes

        else:
            zeroes += 1

    return result


"""
> You are given a list containing nn integers. Your task is to count how many ways one can split the list into two parts so that both parts have the same total sum of elements.

> Consider the following example list:
|Position |	0 |	1 |	2 |	3 |	4 |	5 |	6 |	7 |
|----------|---|---|---|---|---|---|---|---|
|Number | 1 | -1 | 1 |	-1 | 1 | -1 | 1 | -1 |

> Here the number of ways is 3. We can split the list between positions 1 and 2, between positions 3 and 4, and between positions 5 and 6.
"""


def brute_force_count_splits(numbers: list[int]) -> int:
    n = len(numbers)
    result = 0
    for i in range(n - 1):
        left_sum = sum(numbers[0 : i + 1])
        right_sum = sum(numbers[i + 1 :])
        if left_sum == right_sum:
            result += 1
    return result


def slightly_better_brute_force_count_splits(numbers: list[int]) -> int:
    n = len(numbers)
    result = 0
    left_sum = 0
    for i in range(n - 1):
        left_sum += numbers[i]
        right_sum = sum(numbers[i + 1 :])
        if left_sum == right_sum:
            result += 1
    return result


def my_efficient_solution_count_splits(numbers: list[int]) -> int:
    n = len(numbers)
    result = 0

    total_sum = sum(numbers)
    left_sum = 0
    for i in range(n - 1):
        left_sum += numbers[i]
        total_sum -= numbers[i]

        if total_sum == left_sum:
            result += 1

    return result


def calculate_time(exec, variable):
    start_time = time.time()
    result = exec(variable)
    end_time = time.time()

    print("Result: ", result)

    print(
        "Total time taken to execute: ",
        exec.__name__,
        " ",
        end_time - start_time,
        end="\n",
    )


def brue_force_count_sublists(numbers: list[int]) -> int:
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


def efficient_count_lists(numbers: list[int]) -> int:
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


n = random.randint(10000, 20000)

numbers = [random.randint(1000, 1006) for _ in range(n)]

calculate_time(brue_force_count_sublists, variable=numbers)
calculate_time(efficient_count_lists, variable=numbers)
