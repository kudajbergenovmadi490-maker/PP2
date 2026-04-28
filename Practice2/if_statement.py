# ============================================================
# If Statement
# Executes a block of code only if the condition is True
# ============================================================

# Basic if statement
temperature = 30

if temperature > 25:
    print("It's hot outside!")  # This runs because 30 > 25

# If with multiple lines in block
age = 20

if age >= 18:
    print("You are an adult.")
    print("You can vote.")
    print("You can drive.")

# If with a number
balance = 1000

if balance > 0:
    print("\nYour account has a positive balance:", balance)

# If with a string check
name = "Alice"

if name == "Alice":
    print("Hello, Alice! Welcome back.")

# If with boolean variable
is_logged_in = True

if is_logged_in:
    print("\nUser is logged in. Showing dashboard...")

# If with membership check (in operator)
fruits = ["apple", "banana", "cherry"]

if "banana" in fruits:
    print("Banana is in the list!")

# If with length check
password = "mypassword123"

if len(password) >= 8:
    print("\nPassword length is valid.")

# Nested if statement
score = 85

if score >= 60:
    print("\nYou passed the exam.")
    if score >= 90:
        print("Excellent! Grade: A")
    if score >= 75:
        print("Good job! Grade: B")
