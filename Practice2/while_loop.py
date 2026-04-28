# ============================================================
# While Loop
# Repeats a block of code as long as condition is True
# ============================================================

# Basic while loop - counting up
print("--- Counting from 1 to 5 ---")
i = 1
while i <= 5:
    print(i)
    i += 1   # IMPORTANT: always update the variable to avoid infinite loop

# Countdown
print("\n--- Countdown ---")
count = 5
while count > 0:
    print(count)
    count -= 1
print("Liftoff! 🚀")

# Sum of numbers from 1 to 10
print("\n--- Sum 1 to 10 ---")
total = 0
n = 1
while n <= 10:
    total += n
    n += 1
print(f"Sum = {total}")  # 55

# While loop with user-like input simulation
print("\n--- Password check simulation ---")
correct_password = "python123"
attempts = 0
max_attempts = 3
password = ""

passwords_to_try = ["wrong1", "wrong2", "python123"]  # simulating input

while password != correct_password and attempts < max_attempts:
    password = passwords_to_try[attempts]
    attempts += 1
    if password == correct_password:
        print(f"Access granted on attempt {attempts}!")
    else:
        print(f"Wrong password. Attempt {attempts}/{max_attempts}")

# Collecting items in a list using while
print("\n--- Building a list with while ---")
numbers = []
x = 1
while x <= 5:
    numbers.append(x * x)  # add squares
    x += 1
print("Squares:", numbers)  # [1, 4, 9, 16, 25]

# While with else clause
print("\n--- While with else ---")
num = 1
while num <= 3:
    print(f"  num = {num}")
    num += 1
else:
    print("Loop finished! (else block runs when condition becomes False)")
