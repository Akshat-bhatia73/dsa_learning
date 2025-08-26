# Hashing

## Set

The Python data structure `set`, based on hashing, maintains a set of elements. The operations on the data structure include:

- `add`
- `in`
- `remove`

The data structure is implemented so that all of the above operations take O(1) time.

**Example**

```python
numbers = set()

numbers.add(1)
numbers.add(2)
numbers.add(3)

print(numbers) # {1, 2, 3}
```

#### List vs set

A list and a set are similar data structures in that both maintain a collection of elements and support additions and removals. However, there are significant differences in their efficiency and other properties.

**Efficiency**

Adding an element to a list is efficient, but finding an element and removing it can be slow.

With a set, adding elements, finding elements and removing elements are all efficient operations.

| Operations | List | Set  |
| ---------- | ---- | ---- |
| Add        | O(1) | O(1) |
| Find       | O(n) | O(1) |
| Remove     | O(n) | O(1) |

**Indexing**

In a list, elements can be accessed using an index.
A set does not support indexing.

## Dictionary

The python data stucture `dict` or dictionary is based on hashing and stores key-value pairs. The idea is that we can use the key to retrieve the associated value.

A dictionary can be seen as a generalization of a list: In a list, keys are the indices _0...n_, while in dictionary, keys can be arbitrary objects.

Adding, accessing and removing data using a key takse _O(1)_ time.

### Using a dictionary

We will next take a look at three common ways to use a dictionary in algorithm design.

**Has an element occured**

A dictionary can be used similarly to a set to keep track of elements that have been seen:

```python
seen = {}
for x in items:
    seen[x] = True
```

This code has approximately the same functionality as the following code:

```python
seen = set()
for x in items:
    seen.add(x)
```

Indeed, a set can be seen as a special case of a dictionary, where each key is associated with the value `True` (or any fixed value).

**Counting occurrences**

A common use of dictionaries is counting element occurrences:

```python
count = {}
for x in items:
    if x not in count:
        count[x] = 0
    count[x] += 1
```

This code counts the number of occurrences of each element using the dictionary count. If the element is not yet in the dictionary, the code adds the element as a key with the initial count of zero as the associated value. Then the count is incremented by one for every occurrence of the element.

**Position of occurrence**

In some algorithms, it is useful to keep track of where each element has occurred.

```python
pos = {}
for i, x in enumerate(items):
    pos[x] = i
```

Here the dictionary pos stores the index of the most recent occurrence of each element. Using the function enumerate, the code iterates through the list items so that in each round i is the index of an element and x is the element itself.

## How does hashing work?

The Python data structures of this chapter, `set` and `dict`, are based on hashing and a data structure called `hash table`. In Python, hash table is implemented using open hashing.

### Hash table

A hash table consists of _N_ locations indexed 0, 1, _N_-1. Each element has a specific location in the hash table based on its hash value.

A hash function determines the location of an element in the hash table. The function tales an element _x_ as a parameter and returns an integer _h(x)_ as the `hash value` of the element _x_. The location of _x_ in the hash table is _h(x)_ mod _N_, i.e., the remainder from dividing _h(x)_ by _N_.

When the element is added to the hash table, it will be inserted at the location _h(x)_ mod _N_. Similarly, when checking if the hash table contains the element _x_, it will be searched at the location _h(x)_ mod _N_.

**Example**

Consider an example, where N = 10 and h(x) = 7x. We will store the elements of the set {2, 4, 5, 9, 18, 30} into the hash table. We obtain the following locations for the elements:

| Element | Location          |
| ------- | ----------------- |
| 2       | 7 x 2 mod 10 = 4  |
| 4       | 7 x 4 mod 10 = 8  |
| 5       | 7 x 5 mod 10 = 5  |
| 9       | 7 x 9 mod 10 = 3  |
| 18      | 7 x 18 mod 10 = 6 |
| 30      | 7 x 30 mod 10 = 0 |

Thus the hash table as follows after the additions:

| Location | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   |
| -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Elements | 30  | -   | -   | 9   | 2   | 5   | 18  | -   | 4   | -   |

When we want to check if the hash table contains an element x, we search for it at the location 7x mod 10. For example, we will search for the element 4 at the location 7x4 mod 10 = 8.

**Collisions**

A collision is a situation, where two elements have the same location in the hash table. An implementation of a hash table has to be prepared for collisions, because the size N of the hash table is typically much smaller than the number of possible element values.

For example, if we add the elements 4 and 14 into our example hash table, both will be assigned to the location 8, because 7x4 mod 10 = 7x14 mod 10 = 8.

There are two commonly used techniques for handling collisions:

- Chaining: Each hash table location contains a list that stores all the elements assigned to that location.
- Open addressing: Each location contains at most one element. The location of an element x is determined by using has function p(x, i) with a second parameter i so that we can try different choices i = 0, 1, 2, .... until an unoccupied location is found.

**Efficiency**

A hash table operates efficiently if the elements are fairly evenly distributed over the whole hash table. The distribution is determined by the hash table size and the choice of the hash function.

Chaining is efficient if each location contains only a small number of elements. Then the lists are short and the list operations are fast.

Open addressing is efficient if a small number of tries is sufficient for finding a location of an element, i.e., only a few calls to the function p(x, i) is needed.

However, in the worst case, a hash table can become slow and the operations can take O(n) time. For example, this happend with chaining if every element is assigned into a same location.

[Python dict implementaion](https://github.com/python/cpython/blob/main/Objects/dictobject.c)

Python has a built-in function hash that is used for computing a hash value for an object. Python calls this function to determine the location of the object in a hash table. The function can be tested as follows:

```
> hash(42)
42
> hash(10**100)
910685213754167845
> hash("apina")
4992529190565255982
```

As the above shows, in Python, the hash value of a small integer is the integer itself. Otherwise, the hash values are random looking numbers.

The Python data structures based on hashing are usually efficient, and you can assume that an addition, access or removal takes O(1) time. However, there is a possiblity that hashing is slow if the input chosen in a specific way.

### Slow hashing

Operations on data structures based on hashing are usually efficient, but it is possible for the operations to be slow due to collisions. We will next see how the Python dictionary becomes slow, when the keys stored there are chosen in a specific way.

In order to choose the keys, we need to know the exact implementation of the dictionary. The relevant aspect of the implementation are the hash function, the hash table size and the collision handling.

**Hash function**

The Python hash function hash is implemented differently for different data types. For small enough integers, the hash value is simply the integer itself:

```
> hash(42)
42
> hash(123)
123
> hash(1337)
1337
```

We will use small integers as keys, so that we can assume the above hash function.

**Hash table size**

The has table size N of the python dictionary is initially 8. The hash table is implemented so that at most 2/3rd of the locations are occupied. If this limit is exceeded, the size of the hash table is doubled.

The following code illustrates this:

```python
import sys

n = 1000

numbers = {}
old_size = 0

for i in range(n):
    new_size = sys.getsizeof(numbers)

    if new_size != old_size:
        print(len(numbers), sys.getsizeof(numbers))
        old_size = new_size

    numbers[i] = True
```

The code creates a dictionary numbers and adds elements to it one at a time. When the memory usage of the hash table changes, the code prints out the number of elements and the memory usage of the hash table. The output of the code is as follows:

```
0 64
1 232
6 360
11 640
22 1176
43 2272
86 4696
171 9312
342 18520
683 36960
```

For example, the size of the hash table increases when the element count reaches 6, and then the hash table size increases from 8 to 16. The size increases, because the ratio 6/8 exceeds the limit 2/3. The size increases again when the element count reaches 1111, because 11/16 exceeds 2/3, and then the new size is 32.

**Handling collisions**
The following code shows how the Python dictionary chooses the location in the hash table for the pair (key, value):

```python
index = hash(key) % N
perturb = hash(key)
while True:
    if not table[index]:
        table[index] = (key, value)
        break
    perturb = perturb >> 5
    index = (5 * index + 1 + perturb) % N
```

Notice that this is not the actual code implementing the dictionary (Python is implemented in the C language), but this code shows the idea.

The variable index is the location in the hash table and its initial value is computed with the formula `hash(key) % N`. If the location index is occupied, the next location to try is computed with the formula `(5 * index + 1 + perturb) % N`. This continues until an unoccupied location is found.

The purpose of the variable perturb is to make collisions less likely. It affects the location formula for the first few tries. The initial value of perturb is the hash value of the key, and in each round its new value is computed as `perturb >> 5`. This bit shift operation corresponds to dividing by 32 and rounding down.

**Constructing the input**

Now we know enough about the Python dictionary implementation, and we can design an input that makes the dictionary operations slow. The idea is to use keys that collide with each other and cause the hash table operations slow down. The following code constructs such an input:

```python
def find(table, key):
    N = len(table)
    index = hash(key) % N
    perturb = hash(key)
    count = 0
    while True:
        count += 1
        if not table[index]:
            return index, count
        perturb = perturb >> 5
        index = (5 * index + 1 + perturb) % N

n = 100000
chain_len = 50000
threshold = 5000

N = 2**18
table = [None] * N
keys = []

key = 1
for i in range(chain_len):
    keys.append(key)
    key = (5 * key + 1) % N

key = chain_len
while len(keys) < n:
    index, count = find(table, key)
    if count > threshold:
        table[index] = True
        keys.append(key)
    key += 1
```

The code creates an input of n keys. The hash table size N is chosen accordingly so that the limit of 2/3 is not exceeded. The list keys stores the chosen keys.

First, the code adds keys that form a chain of length chain_len. The first key in the chain is 1 and the other keys in the chain are computed iteratively with the formula `key = (5 * key + 1) % N`. The chain is designed so that once the sequence of locations tried for a given key gets locked on the chain, it will stay locked on the chain until the end of the chain. Then the code adds the remaining keys so that each key added causes at least threshold steps along the chain before an unoccupied location is found. This makes their addition to the dictionary slow.

### Which objects can be hashed?

The following code does not work in Python:

```python
lists = set()
lists.add([1, 2, 3]) # TypeError: unhashable type 'list'
```

It is not possible to compute a hash value for a list
A basic principle in Python is that hash value can only be computed for an immutable object. A list is not immutable, because we can change the list with operations like append, and thus hashing a list is not possible.

Immutable objects in Python include, numbers, strings and tuples consisting of immutable objects. For example, the following code works, because a tuple of numbers is immutable:

```python
lists = set()
lists.add((1, 2, 3))
```

### Hashing for you rown class

If you define for your own class, you can apply hashing to it by defining the following methods:

- `**hash**~: returns the hash value of the object (the function hash calls this method)
- `__eq__`: compares if two objects have identical content

```python
class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
```

With these definitions, the following code works as expected:

```python
locations = set()
locations.add(Location(1, 2))
locations.add(Location(3, -5))
locations.add(Location(1, 4))
```
