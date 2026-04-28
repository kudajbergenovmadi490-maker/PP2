# ============================================================
# For Loop with Continue
# continue skips the current iteration and moves to the next
# ============================================================

# Skip a specific value
print("--- Skip banana ---")
fruits = ["apple", "banana", "cherry", "date"]

for fruit in fruits:
    if fruit == "banana":
        print("  (skipping banana)")
        continue
    print(f"I like {fruit}")

# Print only even numbers using continue
print("\n--- Even numbers from 1 to 10 ---")
for i in range(1, 11):
    if i % 2 != 0:
        continue   # skip odd numbers
    print(i, end=" ")
print()

# Skip negative numbers, sum only positives
print("\n--- Sum only positive numbers ---")
data = [5, -3, 8, -1, 12, -7, 4, 0]
total = 0

for num in data:
    if num <= 0:
        continue   # skip zero and negatives
    total += num
    print(f"  + {num}")

print(f"Sum of positives: {total}")

# Skip items that don't meet a condition
print("\n--- Print names longer than 4 characters ---")
names = ["Ali", "Alice", "Bob", "Charlie", "Li", "Sophia"]

for name in names:
    if len(name) <= 4:
        continue
    print(name)

# Continue in a grade filter
print("\n--- Students who passed (score >= 60) ---")
students = [
    ("Alice", 85),
    ("Bob", 42),
    ("Charlie", 91),
    ("Diana", 55),
    ("Eve", 78),
]

for name, score in students:
    if score < 60:
        continue   # skip failed students
    print(f"  {name}: {score} — PASSED ✓")

# Continue vs break comparison
print("\n--- Continue (process all) vs Break (stop at 3) ---")
print("Continue:")
for i in range(1, 6):
    if i == 3:
        continue
    print(i, end=" ")
print()

print("Break:")
for i in range(1, 6):
    if i == 3:
        break
    print(i, end=" ")
print()
# Continue: 1 2 4 5 | Break: 1 2
