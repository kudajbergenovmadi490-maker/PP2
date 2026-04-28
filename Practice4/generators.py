# ============================================================
# Iterators and Generators
# ============================================================

# --- ITERATORS ---
# An iterator is any object with __iter__() and __next__() methods

# Built-in iterators
print("=== ITERATORS ===")

# iter() and next()
my_list = [10, 20, 30, 40]
iterator = iter(my_list)          # create iterator from list

print("--- iter() and next() ---")
print(next(iterator))   # 10
print(next(iterator))   # 20
print(next(iterator))   # 30
print(next(iterator))   # 40
# next(iterator)        # would raise StopIteration

# Loop through an iterator
print("\n--- Loop through iterator ---")
fruits = ("apple", "banana", "cherry")
fruit_iter = iter(fruits)

for fruit in fruit_iter:
    print(f"  {fruit}")

# Strings are iterable too
print("\n--- String iterator ---")
char_iter = iter("Python")
for char in char_iter:
    print(char, end=" ")
print()

# --- CREATE A CUSTOM ITERATOR ---
print("\n--- Custom Iterator class ---")

class CountUp:
    """Counts up from start to end."""

    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self     # the object itself is the iterator

    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


counter = CountUp(1, 5)
for num in counter:
    print(num, end=" ")
print()

# Custom iterator: Fibonacci sequence
print("\n--- Fibonacci Iterator ---")

class Fibonacci:
    """Generates Fibonacci numbers up to a limit."""

    def __init__(self, limit):
        self.limit = limit
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.a > self.limit:
            raise StopIteration
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        return value


fib = Fibonacci(100)
print("Fibonacci up to 100:", list(fib))


# ============================================================
# GENERATORS
# A generator function uses 'yield' instead of 'return'
# It returns a generator object — lazy evaluation (one item at a time)
# ============================================================

print("\n=== GENERATORS ===")

# Basic generator function
def count_up(start, end):
    """Generator that counts from start to end."""
    current = start
    while current <= end:
        yield current       # pauses here, returns value, resumes on next()
        current += 1

print("--- Basic generator ---")
gen = count_up(1, 5)
print(type(gen))            # <class 'generator'>
print(next(gen))            # 1
print(next(gen))            # 2

print("\nAll values via for loop:")
for val in count_up(1, 5):
    print(val, end=" ")
print()

# Generator for squares
def squares(n):
    """Yields squares of numbers from 1 to n."""
    for i in range(1, n + 1):
        yield i ** 2

print("\n--- Squares generator ---")
print(list(squares(8)))    # [1, 4, 9, 16, 25, 36, 49, 64]

# Generator for Fibonacci
def fibonacci(limit):
    """Yields Fibonacci numbers up to limit."""
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b

print("\n--- Fibonacci generator ---")
print(list(fibonacci(200)))

# Generator — memory efficient (doesn't build full list)
def large_range(n):
    """Generator version of range — never stores all values."""
    i = 0
    while i < n:
        yield i
        i += 1

print("\n--- Memory-efficient generator ---")
gen = large_range(1_000_000)
print(f"Generator object (no memory used yet): {gen}")
print(f"First 5 values: {[next(gen) for _ in range(5)]}")

# Generator Expressions (like list comprehensions but lazy)
print("\n--- Generator Expressions ---")
# List comprehension — builds full list immediately
list_comp = [x ** 2 for x in range(10)]

# Generator expression — lazy, one item at a time
gen_exp = (x ** 2 for x in range(10))

print(f"List:      {list_comp}")
print(f"Generator: {gen_exp}")
print(f"As list:   {list(gen_exp)}")

# Chaining generators
def evens(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

def squared(gen):
    for val in gen:
        yield val ** 2

print("\n--- Chained generators (even squares up to 20) ---")
pipeline = squared(evens(20))
print(list(pipeline))
