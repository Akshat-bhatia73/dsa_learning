def bubble_sort(arr: list[int]) -> list[int]:
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            """If no swap has happend in the current iteration, the array has been sorted completely. No need to continue"""
            break

    return arr


def insertion_sort_for_loop(arr: list[int]) -> list[int]:
    n = len(arr)

    if len(arr) <= 1:
        return arr

    for i in range(1, n):
        key = arr[i]

        for j in range(i - 1, -1, -1):
            if key <= arr[j]:
                print("Swapping {a} and {b}".format(a=arr[j], b=arr[j + 1]))
                arr[j + 1], arr[j] = arr[j], arr[j + 1]
            else:
                break

        print("Array after pass {i} : {arr}".format(i=i, arr=arr))
    return arr


def insertion_sort_while_loop(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

    return arr


def selection_sort(arr: list[int]) -> list[int]:
    n = len(arr)

    for i in range(0, n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr


def counting_sort(arr: list[int]) -> list[int]:
    n = len(arr)

    # find the maximum element
    maxval = max(arr)

    # create and initialize count array
    count = [0] * (maxval + 1)

    # count frequency of each element
    for num in arr:
        count[num] += 1

    # compute prefix sum
    # This will actually tell us at what index will the particular value end.
    for i in range(1, maxval + 1):
        count[i] += count[i - 1]
        # count[i] becomes the last index on which this value will be present in the sorted array

    # build output array
    ans = [0] * n
    for i in range(n - 1, -1, -1):
        val = arr[i]
        ans[count[val] - 1] = val
        count[val] -= 1

    return ans


# print(bubble_sort([12, 11, 13, 5, 6]))
# print(insertion_sort_for_loop([12, 11, 13, 5, 6]))
# print(insertion_sort_while_loop([12, 11, 13, 5, 6]))
print(counting_sort([5, 6, 12, 11, 13, 5, 6]))
