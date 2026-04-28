"""
map_filter_reduce.py
====================
Practice 6 — Built-in Functions
Demonstrates map(), filter(), reduce(), and related tools.

Covers:
  - map()         → apply a function to every element
  - filter()      → keep elements that satisfy a condition
  - reduce()      → fold a sequence into a single value
  - lambda        → anonymous functions used with the above
  - len(), sum(), min(), max()
  - Type conversion: int(), float(), str(), list(), tuple(), set()
  - sorted(), reversed(), abs(), round()
"""

from functools import reduce

# ─────────────────────────────────────────────────────────────────────────────
# SAMPLE DATA
# ─────────────────────────────────────────────────────────────────────────────

prices      = [29.99, 5.49, 14.99, 89.00, 3.25, 49.99, 0.99, 199.00]
temperatures = [22, -5, 37, 0, 15, -12, 28, 100, -3, 41]
words       = ["python", "FILE", "Handling", "REGEX", "builtin", "Practice"]
students    = [
    {"name": "Alice",   "score": 92, "grade": "A"},
    {"name": "Bob",     "score": 54, "grade": "F"},
    {"name": "Charlie", "score": 78, "grade": "B"},
    {"name": "Diana",   "score": 96, "grade": "A"},
    {"name": "Evan",    "score": 61, "grade": "D"},
    {"name": "Fiona",   "score": 83, "grade": "B"},
]

# ─────────────────────────────────────────────────────────────────────────────
# 1. map()  — transform every element
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print("1. map()  — transform every element")
print("=" * 60)

# 1a. Convert prices: add 12% tax
taxed = list(map(lambda p: round(p * 1.12, 2), prices))
print(f"  Original prices : {prices}")
print(f"  After 12% tax   : {taxed}")

# 1b. Normalise words to title case
titled = list(map(str.title, words))
print(f"\n  Original words  : {words}")
print(f"  Title-cased     : {titled}")

# 1c. Convert strings to integers (type conversion inside map)
str_nums = ["10", "20", "30", "40", "50"]
ints     = list(map(int, str_nums))
print(f"\n  String list : {str_nums}")
print(f"  Mapped int  : {ints}")

# 1d. Named function vs lambda
def celsius_to_fahrenheit(c: float) -> float:
    return round(c * 9 / 5 + 32, 1)

fahrenheit = list(map(celsius_to_fahrenheit, temperatures))
print(f"\n  °C : {temperatures}")
print(f"  °F : {fahrenheit}")

# 1e. map() over list of dicts — extract a field
names = list(map(lambda s: s["name"], students))
print(f"\n  Student names via map : {names}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. filter()  — keep elements that pass a test
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("2. filter()  — keep matching elements")
print("=" * 60)

# 2a. Keep expensive items (>= 50)
expensive = list(filter(lambda p: p >= 50, prices))
print(f"  Prices >= 50    : {expensive}")

# 2b. Positive temperatures only
positive_temps = list(filter(lambda t: t > 0, temperatures))
print(f"  Positive temps  : {positive_temps}")

# 2c. Students who passed (score >= 60)
passed = list(filter(lambda s: s["score"] >= 60, students))
print(f"\n  Passed students : {[s['name'] for s in passed]}")

# 2d. Words longer than 6 characters
long_words = list(filter(lambda w: len(w) > 6, words))
print(f"  Words > 6 chars : {long_words}")

# 2e. filter with a named function
def is_even(n: int) -> bool:
    return n % 2 == 0

evens = list(filter(is_even, range(1, 21)))
print(f"\n  Even numbers 1–20 : {evens}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. reduce()  — fold sequence to single value (from functools)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("3. reduce()  — fold to a single value")
print("=" * 60)

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 3a. Sum with reduce (equivalent to sum())
total = reduce(lambda acc, x: acc + x, nums)
print(f"  reduce(+) on {nums} = {total}")

# 3b. Product of all numbers
product = reduce(lambda acc, x: acc * x, nums)
print(f"  reduce(*) (factorial-like)   = {product}")

# 3c. Maximum using reduce
maximum = reduce(lambda a, b: a if a > b else b, nums)
print(f"  reduce(max)                  = {maximum}")

# 3d. Concatenate strings
words_list = ["Python", " is", " really", " fun", "!"]
sentence = reduce(lambda a, b: a + b, words_list)
print(f"  reduce(str concat)           = '{sentence}'")

# 3e. Reduce with initial value
total_with_start = reduce(lambda acc, x: acc + x, nums, 100)
print(f"  reduce(+, start=100)         = {total_with_start}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Combining map + filter + reduce (pipeline)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("4. Combined pipeline: map → filter → reduce")
print("=" * 60)

# Goal: sum of taxes on items that cost more than $10
result = reduce(
    lambda acc, p: acc + p,
    filter(
        lambda p: p > 10,
        map(lambda p: round(p * 0.12, 2), prices)   # 12% tax per item
    ),
    0,
)
print(f"  Prices                  : {prices}")
print(f"  Tax on items >$10 only  : {result:.2f}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. Aggregate built-ins: len, sum, min, max, abs, round
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("5. Aggregate built-ins: len, sum, min, max, abs, round")
print("=" * 60)

scores = [s["score"] for s in students]
print(f"  Scores       : {scores}")
print(f"  len()        : {len(scores)}")
print(f"  sum()        : {sum(scores)}")
print(f"  min()        : {min(scores)}")
print(f"  max()        : {max(scores)}")
print(f"  average      : {round(sum(scores) / len(scores), 2)}")

neg_vals = [-7, 3, -15, 42, -1]
print(f"\n  Values       : {neg_vals}")
print(f"  abs() map    : {list(map(abs, neg_vals))}")
print(f"  round(3.14159, 2) = {round(3.14159, 2)}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. Type conversion functions
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("6. Type conversion built-ins")
print("=" * 60)

print(f"  int('42')         = {int('42')}         type={type(int('42')).__name__}")
print(f"  int(3.9)          = {int(3.9)}          type={type(int(3.9)).__name__}")
print(f"  float('3.14')     = {float('3.14')}      type={type(float('3.14')).__name__}")
print(f"  str(100)          = {str(100)!r}       type={type(str(100)).__name__}")
print(f"  bool(0)           = {bool(0)}")
print(f"  bool('hello')     = {bool('hello')}")
print(f"  list((1,2,3))     = {list((1, 2, 3))}")
print(f"  tuple([1,2,3])    = {tuple([1, 2, 3])}")
print(f"  set([1,2,2,3,3])  = {set([1, 2, 2, 3, 3])}")
print(f"  list(map(int, ['1','2','3'])) = {list(map(int, ['1','2','3']))}")


# ─────────────────────────────────────────────────────────────────────────────
# 7. sorted() and reversed()
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("7. sorted() and reversed()")
print("=" * 60)

unsorted = [34, 1, 78, 12, 56, 3]
print(f"  Original           : {unsorted}")
print(f"  sorted()           : {sorted(unsorted)}")
print(f"  sorted(reverse=True): {sorted(unsorted, reverse=True)}")
print(f"  reversed() list    : {list(reversed(unsorted))}")

# Sort list of dicts by a key
by_score = sorted(students, key=lambda s: s["score"])
by_name  = sorted(students, key=lambda s: s["name"])
print(f"\n  Students by score  : {[s['name'] for s in by_score]}")
print(f"  Students by name   : {[s['name'] for s in by_name]}")
print(f"  Top scorer         : {max(students, key=lambda s: s['score'])['name']}")

print("\n✅  map_filter_reduce.py complete.")
