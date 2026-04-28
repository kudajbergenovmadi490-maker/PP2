"""
enumerate_zip_examples.py
=========================
Practice 6 — Built-in Functions
Demonstrates enumerate(), zip(), and paired/indexed iteration patterns.

Covers:
  - enumerate()    → (index, value) pairs
  - zip()          → combine multiple iterables
  - zip_longest()  → zip with unequal lengths
  - dict(zip())    → build dictionaries
  - any(), all()   → boolean aggregation
  - isinstance(), type()  → type checking
"""

from itertools import zip_longest

# ─────────────────────────────────────────────────────────────────────────────
# SAMPLE DATA
# ─────────────────────────────────────────────────────────────────────────────

fruits   = ["apple", "banana", "cherry", "date", "elderberry"]
prices   = [1.20, 0.50, 2.50, 3.00, 4.75]
in_stock = [True, True, False, True, False]

days     = ["Mon", "Tue", "Wed", "Thu", "Fri"]
temps_am = [12, 15, 9, 18, 22]
temps_pm = [18, 20, 14, 25, 27]

students = ["Alice", "Bob", "Charlie", "Diana", "Evan"]
scores   = [92, 54, 78, 96, 61]
grades   = ["A", "F", "B", "A", "D"]


# ─────────────────────────────────────────────────────────────────────────────
# 1. enumerate()  — index + value pairs
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print("1. enumerate()  — index + value pairs")
print("=" * 60)

# 1a. Basic usage (default start=0)
print("  Basic enumerate (start=0):")
for idx, fruit in enumerate(fruits):
    print(f"    [{idx}] {fruit}")

# 1b. Custom start index
print("\n  enumerate(start=1)  — 1-based numbering:")
for num, fruit in enumerate(fruits, start=1):
    print(f"    {num}. {fruit}")

# 1c. Practical: numbered receipt lines
print("\n  Numbered receipt output:")
items  = ["Milk", "Bread", "Eggs", "Butter"]
item_prices = [480, 350, 890, 620]
total  = 0
for i, (item, price) in enumerate(zip(items, item_prices), 1):
    total += price
    print(f"    {i:>2}. {item:<10}  {price:>6} ₸")
print(f"    {'':>4} {'TOTAL':<10}  {total:>6} ₸")

# 1d. Use enumerate to find index of an element
target = "cherry"
for i, f in enumerate(fruits):
    if f == target:
        print(f"\n  '{target}' found at index {i}")
        break


# ─────────────────────────────────────────────────────────────────────────────
# 2. zip()  — combine multiple iterables
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("2. zip()  — pair up multiple iterables")
print("=" * 60)

# 2a. Two lists
print("  zip(fruits, prices):")
for fruit, price in zip(fruits, prices):
    print(f"    {fruit:<12} ${price:.2f}")

# 2b. Three lists — fruit catalogue with stock status
print("\n  zip(fruits, prices, in_stock):")
for fruit, price, stock in zip(fruits, prices, in_stock):
    status = "✅ In stock" if stock else "❌ Out of stock"
    print(f"    {fruit:<12} ${price:.2f}  {status}")

# 2c. zip stops at the SHORTEST iterable
long_list  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
short_list = ["a", "b", "c"]
zipped = list(zip(long_list, short_list))
print(f"\n  zip stops at shortest: {zipped}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. zip_longest()  — zip with unequal lengths (pads with fill value)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("3. zip_longest()  — handle unequal lengths")
print("=" * 60)

long_zip = list(zip_longest(long_list, short_list, fillvalue="N/A"))
print(f"  zip_longest result: {long_zip}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. dict(zip())  — build dictionaries from two lists
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("4. dict(zip())  — create dict from two lists")
print("=" * 60)

fruit_prices  = dict(zip(fruits, prices))
student_scores = dict(zip(students, scores))
student_grades = dict(zip(students, grades))

print(f"  Fruit price dict   : {fruit_prices}")
print(f"  Student score dict : {student_scores}")
print(f"  Student grade dict : {student_grades}")

# Lookup
print(f"\n  Price of 'date'  : ${fruit_prices.get('date', 'N/A'):.2f}")
print(f"  Alice's score    : {student_scores['Alice']}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. Combining enumerate + zip
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("5. enumerate + zip combined  — weather table")
print("=" * 60)

print(f"  {'#':<4} {'Day':<6} {'AM °C':>7} {'PM °C':>7} {'Diff':>6}")
print("  " + "-" * 34)
for i, (day, am, pm) in enumerate(zip(days, temps_am, temps_pm), 1):
    diff = pm - am
    print(f"  {i:<4} {day:<6} {am:>7} {pm:>7} {diff:>+6}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. Unzipping — zip(*zipped) reverses zip
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("6. Unzipping  — zip(*zipped)")
print("=" * 60)

pairs = [(1, "a"), (2, "b"), (3, "c"), (4, "d")]
nums, letters = zip(*pairs)

print(f"  Pairs   : {pairs}")
print(f"  Nums    : {nums}")
print(f"  Letters : {letters}")


# ─────────────────────────────────────────────────────────────────────────────
# 7. any() and all()  — boolean aggregation
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("7. any() and all()  — boolean aggregation")
print("=" * 60)

print(f"  In-stock flags   : {in_stock}")
print(f"  any(in_stock)    : {any(in_stock)}   ← at least one is True")
print(f"  all(in_stock)    : {all(in_stock)}  ← all must be True")

all_passed  = all(s >= 60 for s in scores)
any_failed  = any(s < 60 for s in scores)
any_perfect = any(s == 100 for s in scores)

print(f"\n  Scores           : {scores}")
print(f"  all passed(>=60) : {all_passed}")
print(f"  any failed(<60)  : {any_failed}")
print(f"  any perfect(100) : {any_perfect}")


# ─────────────────────────────────────────────────────────────────────────────
# 8. Type checking: type(), isinstance()
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("8. type() and isinstance()  — type checking")
print("=" * 60)

mixed = [42, 3.14, "hello", True, [1, 2], {"key": "val"}, (1,), None]

for val in mixed:
    print(f"  {str(val):<20}  type={type(val).__name__:<10} "
          f"  is int? {isinstance(val, int):<6} "
          f"  is str? {isinstance(val, str)}")

# isinstance allows checking multiple types at once
print(f"\n  isinstance checks with tuple of types:")
for val in mixed:
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        print(f"    {val} is numeric (int or float, not bool)")


# ─────────────────────────────────────────────────────────────────────────────
# 9. Practical: zipped student report card
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("9. Practical: Full student report card")
print("=" * 60)

print(f"  {'No.':<5} {'Name':<10} {'Score':>7} {'Grade':>7} {'Status':>10}")
print("  " + "-" * 44)
for i, (name, score, grade) in enumerate(zip(students, scores, grades), 1):
    status = "PASS" if score >= 60 else "FAIL"
    marker = "⭐" if score >= 90 else ""
    print(f"  {i:<5} {name:<10} {score:>7} {grade:>7} {status:>10} {marker}")

avg = sum(scores) / len(scores)
print(f"\n  Class average : {avg:.1f}")
print(f"  Highest score : {max(scores)} ({students[scores.index(max(scores))]})")
print(f"  Lowest  score : {min(scores)} ({students[scores.index(min(scores))]})")
print(f"  Pass rate     : {sum(1 for s in scores if s >= 60)}/{len(scores)}")

print("\n✅  enumerate_zip_examples.py complete.")
