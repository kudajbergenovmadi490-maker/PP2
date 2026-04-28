# ============================================================
# While Loop with Continue
# continue skips the rest of the current iteration
# and jumps back to the condition check
# ============================================================

# Skip number 3
print("--- Skip 3 while counting to 5 ---")
i = 0
while i < 5:
    i += 1
    if i == 3:
        continue    # skip printing 3
    print(i)
# Output: 1, 2, 4, 5

# Print only even numbers
print("\n--- Print only even numbers up to 10 ---")
n = 0
while n < 10:
    n += 1
    if n % 2 != 0:
        continue    # skip odd numbers
    print(n)
# Output: 2, 4, 6, 8, 10

# Skip negative numbers in a list
print("\n--- Skip negative numbers ---")
numbers = [5, -3, 8, -1, 0, 12, -7, 4]
index = 0
total = 0

while index < len(numbers):
    num = numbers[index]
    index += 1
    if num < 0:
        print(f"  Skipping negative: {num}")
        continue
    total += num
    print(f"  Adding: {num}, running total: {total}")

print(f"Sum of non-negative numbers: {total}")

# Skip vowels in a string
print("\n--- Print consonants only ---")
word = "python"
vowels = "aeiou"
i = 0

while i < len(word):
    letter = word[i]
    i += 1
    if letter in vowels:
        continue    # skip vowels
    print(letter, end=" ")
print()  # newline

# Continue with a counter (difference from break)
print("\n--- Continue doesn't stop the loop ---")
i = 0
skipped = 0
processed = 0

while i < 10:
    i += 1
    if i % 3 == 0:
        skipped += 1
        continue     # skips multiples of 3
    processed += 1

print(f"Processed: {processed}, Skipped: {skipped}")  # 7 processed, 3 skipped
