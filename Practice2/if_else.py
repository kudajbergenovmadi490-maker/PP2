# ============================================================
# If-Else Statement
# Executes one block if condition is True, another if False
# ============================================================

# Basic if-else
age = 15

if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")   # This runs because 15 < 18

# Checking even or odd
number = 7

if number % 2 == 0:
    print(f"\n{number} is even.")
else:
    print(f"\n{number} is odd.")  # This runs

# Login check
username = "user123"
correct_username = "admin"

if username == correct_username:
    print("\nAccess granted!")
else:
    print("\nAccess denied! Wrong username.")  # This runs

# Temperature check
temp = -5

if temp >= 0:
    print("\nWater is liquid.")
else:
    print("\nWater is frozen! Temperature is below 0.")  # Runs

# Checking if a list is empty
shopping_cart = []

if shopping_cart:
    print("\nYou have items in your cart.")
else:
    print("\nYour shopping cart is empty.")  # This runs

# Grade check
score = 72

if score >= 60:
    result = "PASS"
else:
    result = "FAIL"

print(f"\nScore: {score} — Result: {result}")  # PASS

# Max of two numbers (without using max())
a = 42
b = 17

if a > b:
    maximum = a
else:
    maximum = b

print(f"\nThe maximum of {a} and {b} is: {maximum}")  # 42
