# ============================================================
# Lambda with filter()
# filter(function, iterable) keeps items where function returns True
# Returns a filter object — convert to list to see results
# ============================================================

# Keep only even numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Numbers: {numbers}")
print(f"Evens:   {evens}")    # [2, 4, 6, 8, 10]

# Keep only positive numbers
mixed = [-5, -3, 0, 2, 7, -1, 9, 4]
positives = list(filter(lambda x: x > 0, mixed))
print(f"\nMixed:     {mixed}")
print(f"Positives: {positives}")   # [2, 7, 9, 4]

# Keep words longer than 4 characters
words = ["hi", "hello", "python", "cat", "programming", "dog"]
long_words = list(filter(lambda w: len(w) > 4, words))
print(f"\nWords:      {words}")
print(f"Long words: {long_words}")  # ['hello', 'python', 'programming']

# Filter students who passed (score >= 60)
students = [
    {"name": "Alice",   "score": 85},
    {"name": "Bob",     "score": 42},
    {"name": "Charlie", "score": 91},
    {"name": "Diana",   "score": 55},
    {"name": "Eve",     "score": 78},
]

passed = list(filter(lambda s: s["score"] >= 60, students))
print("\nStudents who passed:")
for s in passed:
    print(f"  {s['name']}: {s['score']}")

# Filter out None values from a list
data = [1, None, 3, None, 5, None, 7]
clean = list(filter(lambda x: x is not None, data))
print(f"\nWith None:    {data}")
print(f"Without None: {clean}")  # [1, 3, 5, 7]

# Filter strings that start with a specific letter
fruits = ["apple", "avocado", "banana", "apricot", "blueberry", "cherry"]
a_fruits = list(filter(lambda f: f.startswith("a"), fruits))
print(f"\nFruits starting with 'a': {a_fruits}")

# Combine filter and map
numbers = list(range(1, 21))
# First filter: keep even numbers, then map: square them
even_squares = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))
print(f"\nSquares of even numbers (1-20): {even_squares}")
