# ============================================================
# Lambda with sorted()
# sorted(iterable, key=function) sorts by a custom criterion
# The key function extracts the comparison value from each item
# ============================================================

# Sort numbers (default — no lambda needed)
numbers = [5, 2, 8, 1, 9, 3]
print(f"Original:       {numbers}")
print(f"Sorted asc:     {sorted(numbers)}")
print(f"Sorted desc:    {sorted(numbers, reverse=True)}")

# Sort strings by length
words = ["banana", "apple", "kiwi", "strawberry", "fig"]
by_length = sorted(words, key=lambda w: len(w))
print(f"\nWords:          {words}")
print(f"By length:      {by_length}")

# Sort strings by last character
by_last = sorted(words, key=lambda w: w[-1])
print(f"By last char:   {by_last}")

# Sort strings alphabetically (case-insensitive)
mixed_case = ["Banana", "apple", "Cherry", "date"]
by_alpha = sorted(mixed_case, key=lambda w: w.lower())
print(f"\nMixed case:     {mixed_case}")
print(f"Case-insens.:   {by_alpha}")

# Sort list of tuples by second element
points = [(1, 5), (3, 2), (2, 8), (4, 1)]
by_y = sorted(points, key=lambda p: p[1])
print(f"\nPoints:         {points}")
print(f"By Y value:     {by_y}")

# Sort list of dictionaries by a field
students = [
    {"name": "Charlie", "score": 91, "age": 22},
    {"name": "Alice",   "score": 85, "age": 20},
    {"name": "Bob",     "score": 72, "age": 21},
    {"name": "Diana",   "score": 91, "age": 19},
]

by_score = sorted(students, key=lambda s: s["score"], reverse=True)
print("\nStudents sorted by score (descending):")
for s in by_score:
    print(f"  {s['name']}: {s['score']}")

by_name = sorted(students, key=lambda s: s["name"])
print("\nStudents sorted by name:")
for s in by_name:
    print(f"  {s['name']}")

# Sort by multiple keys (score desc, then name asc)
multi_sort = sorted(students, key=lambda s: (-s["score"], s["name"]))
print("\nSorted by score desc, then name asc:")
for s in multi_sort:
    print(f"  {s['name']}: {s['score']}")

# Sort words by number of vowels
def count_vowels(word):
    return sum(1 for c in word if c in "aeiou")

fruits = ["apple", "fig", "strawberry", "orange", "kiwi"]
by_vowels = sorted(fruits, key=lambda w: count_vowels(w), reverse=True)
print(f"\nFruits by vowel count (desc): {by_vowels}")
