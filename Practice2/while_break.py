# ============================================================
# While Loop with Break
# break exits the loop immediately, even if condition is True
# ============================================================

# Basic break example
print("--- Break when i equals 3 ---")
i = 1
while i <= 10:
    if i == 3:
        print("Found 3! Breaking out of loop.")
        break
    print(i)
    i += 1
# Output: 1, 2, then breaks

# Searching in a list
print("\n--- Search with break ---")
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
target = "cherry"
position = -1

i = 0
while i < len(fruits):
    if fruits[i] == target:
        position = i
        print(f"Found '{target}' at index {position}")
        break   # no need to keep searching
    i += 1

if position == -1:
    print(f"'{target}' not found.")

# ATM simulation - break when user wants to quit
print("\n--- ATM balance check simulation ---")
balance = 1000
transactions = [200, 150, 700, 50]  # simulated withdrawals
index = 0

while True:   # infinite loop - only exits via break
    if index >= len(transactions):
        print("No more transactions.")
        break

    amount = transactions[index]
    if amount > balance:
        print(f"Insufficient funds for withdrawal of {amount}. Exiting.")
        break

    balance -= amount
    print(f"Withdrew {amount}. Remaining balance: {balance}")
    index += 1

# Find first number divisible by both 3 and 7
print("\n--- Find first number divisible by 3 and 7 ---")
num = 1
while num <= 1000:
    if num % 3 == 0 and num % 7 == 0:
        print(f"First number divisible by both 3 and 7: {num}")
        break
    num += 1

# Break with else (else does NOT run when break is used)
print("\n--- Break with else ---")
i = 1
while i <= 5:
    if i == 3:
        print(f"Breaking at i={i}")
        break
    print(f"i = {i}")
    i += 1
else:
    print("This will NOT print because we broke out")
