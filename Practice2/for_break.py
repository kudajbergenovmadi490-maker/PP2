# ============================================================
# For Loop with Break
# break exits the loop early when a condition is met
# ============================================================

# Stop when we find a target
print("--- Find 'cherry' in list ---")
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

for fruit in fruits:
    if fruit == "cherry":
        print(f"Found it: {fruit}")
        break
    print(f"Not this one: {fruit}")

# Break in a number search
print("\n--- First number greater than 50 ---")
numbers = [12, 34, 67, 8, 99, 5]

for num in numbers:
    if num > 50:
        print(f"First number > 50 is: {num}")
        break

# Break in a string search
print("\n--- Stop at first digit in a string ---")
text = "Hello2World"

for char in text:
    if char.isdigit():
        print(f"Found digit: {char}")
        break
    print(f"  Letter: {char}")

# Nested loops with break (only breaks inner loop)
print("\n--- Break in nested loop ---")
for i in range(1, 4):
    print(f"Outer loop: i = {i}")
    for j in range(1, 4):
        if j == 2:
            print(f"  Breaking inner loop at j = {j}")
            break
        print(f"  Inner loop: j = {j}")

# Find first prime number after 10
print("\n--- First prime number after 10 ---")
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

for num in range(11, 100):
    if is_prime(num):
        print(f"First prime after 10: {num}")
        break  # 11 is prime

# Break with else (else does NOT run if break was used)
print("\n--- For-else with break ---")
search_list = [1, 2, 3, 4, 5]
target = 3

for item in search_list:
    if item == target:
        print(f"Found {target}!")
        break
else:
    print("Target not found.")  # won't print since break was hit
