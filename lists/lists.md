# List

The memory of a computer consists of a sequence of memory locations capable of storing data. Each memory location has an address that can be used for access. When a program is executed, the data it processes is stored in the memory.

The elements of the list are stored in cosecutive memory locations, which makes it easy to determine the location of a given list element. The memory address of an element is obtained by adding the element index to the address of the first element.

```python
a = 1
b = 2
c = [1, 2, 3, 4, 5]
d = 99
```

|100|101|102|103|104|105|106|107|108|109|110|
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 1 | 2 | 3 | 4 | 5 | 0 | 0 | 0 | 99 |
| a | b | c |  |   |   |   |   |   |   | d |

The list occupies _**more memory**_ than is needed for its current elements. The reason for extra memory is to prepare for possible addition of new elements to the list. Thus the list has two sizes: the number of elements(here 5) and the number of memory locations reserved for the list(here 8).

## List Operations
- O(1): Accessing an element by index
- O(n): Searching for an element, inserting an element at the beginning or in the middle


`len(list)` function takes O(1) time, because the length is stored in memory with the list

The `append` method can take O(1) time or O(n) time depending on whether the list has enough reserved memory for the new element. If there is enough memory, the new element is added in O(1) time. If there is not enough memory, a new larger memory block is allocated, the elements are copied to the new block, and the new element is added, which takes O(n) time.

The worst time complexity is O(n), it can be shown that the average case time complexity os O(1) with an apprppriate method of memory reservation. One such method is to `double` the reserved memory aea whenever more memory is needed.

### 1. The setting

A **dynamic array** (like Python’s `list` or Java’s `ArrayList`) stores elements in a contiguous memory block.
When adding a new element:

* If there’s unused capacity → **O(1)**, because you just put the element in the next slot.
* If it’s full → **O(n)** in worst case, because a larger block must be allocated and all elements copied.

To avoid constant reallocations, the array **grows by a fixed factor** (commonly ×2).

---

### 2. The doubling scenario

Let’s say the array doubles its capacity each time it’s full:

Example growth:

```
Capacity: 1   2   4   8   16   ...   n
```

Each time capacity is exceeded:

* Allocate new block (size doubled)
* Copy all old elements into it

---

### 3. Where the sequence comes from

When the array reaches **n elements**, the past copy operations looked like this:

* Most recent reallocation: copied **n** elements
* Before that: copied **n/2** elements
* Before that: copied **n/4** elements
* … and so on, down to copying 1 element the first time it grew.

So, **total elements moved over lifetime**:

```
n + n/2 + n/4 + n/8 + ...
```

This is a **geometric series** with sum:

```
S = n * (1 + 1/2 + 1/4 + 1/8 + ...)
```

The series converges to **2n**, so:

```
Total moves < 2n  ⇒  O(n) total copying work
```

---

### 4. Why average cost per insert is O(1)

We inserted **n elements** in total.
Copying work = **O(n)** total.
Thus:

```
O(n) total / n insertions = O(1) amortized per insertion
```

Meaning: most insertions are constant time, with rare expensive insertions.

---

### 5. Generalizing with factor c > 1

If instead of doubling, you grow by multiplying capacity by a constant **c** each time (e.g., c=1.5), the copies look like:

```
n + n/c + n/c² + n/c³ + ...
```

This is another geometric series:

```
Sum = n * (1 + 1/c + 1/c² + ...)
    = n * [1 / (1 - 1/c)]
```

Since c > 1, the sum is proportional to n ⇒ **O(n)** total.

---

### 6. Tradeoff controlled by c

* Larger **c** → fewer reallocations and copies, but wastes more unused capacity.
* Smaller **c** → less unused memory, but more frequent costly reallocations.

---

If you want, I can also show you **exactly why n + n/2 + n/4 + ... < 2n** without skipping steps. That’s the core mathematical bound in the proof.

## Python Implementation

We can study the memore use of a python list with the following code:

```python
import sys
numbers = []
old_size = 0

for i in range(n):
    new_size = sys.getsizeof(numbers)
    
    if new_size != old_size:
        print(len(numbers), new_size)
        old_size = new_size
    
    numbers.append(1)
```

The `getsizeof` function returns the memory used by the given object in bytes. The code creates a list and then adds elements to the list one at a time. Whenever the memory usage changes, the code prints out the length and memory use of the list.

The code returns the following:
```
0 56
1 88
5 120
9 184
17 248
25 312
33 376
41 472
53 568
65 664
77 792
93 920
```

This shows that an empty list requires 56 bytes of memory, and that each additional element needs 8 bytes. The memory usage grows when the number of elements grows to 1, 5, 9, 17, 25, etc.. For example, when the element count reaches 17, the new memory usage is 248 bytes and there is room for (248 - 56) / 8 = 24 elements. Thus the next expansion happens when the element count reaches 25.

[List implementation in python](https://github.com/python/cpython/blob/0a9b339363a59be1249189c767ed6f46fd71e1c7/Objects/listobject.c#L72)

## References and copying

In Python, lists and other data structures are accesses through references. Assigning a list to a variable only copies the reference, not the contents of the list.

```python
a = [1, 2, 3, 4]
b = a
a.append(5)

print(a) # [1, 2, 3, 4, 5]
print(b) # [1, 2, 3, 4, 5]
```

For copying contents, we can use the method copy

```python
a = [1, 2, 3, 4]
b = a.copy()
a.append(5)

print(a) # [1, 2, 3, 4, 5]
print(b) # [1, 2, 3, 4]
```

Efficiency: copying a reference `O(1)` | copying the contents `O(n)`

### Side effects of functions

When a functions is given a data structure as a parameter, only a reference is copied. Then the function can cause side effects, if it changes the contents of the data structure.

## Slicing and concatenation

The Python slice operator ([:]) creates a new list that contains a copy of a segment of the given list

The operator needs `O(n)` time because it copis the contents from the old list to the new list.

We can use slice to copy the whole list too(`result = numbers[:] ~ result = numbers.copy()`)

Concatenation also creates a new list, so it also takes `O(n)` time, because the operator copies the elements from the original to the new list.

## Lists in other languages

The list described in this chapter is more generally known as an array list or a dynamic array.

In low level languages (such as C++ and Java), the basic data structure is usually the array. Like a list, an array is a sequence of consecutive elements that can be accessed with indexing. However, an array is assigned a fixed memory area when it is created and its size cannot be changed later. When a variable size is required, these languages have other data structures.

In C++ the data structure `std::vector` implements a list:

```cpp
std::vector<int> numbers;

numbers.push_back(1);
numbers.push_back(2);
numbers.push_back(3);
```

And in Java, the data structure `ArrayList` implements a list:
```java
ArrayList<Integer> numbers = new ArrayList<>();

numbers.add(1);
numbers.add(2);
numbers.add(3);
```

In JavaScript, the basic data structure is called `Array`, but it is really a list since its size can be changed:
```javascript
numbers = [];

numbers.push(1);
numbers.push(2);
numbers.push(3);
```