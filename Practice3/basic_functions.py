# ============================================================
# Basic Functions
# Functions are reusable blocks of code defined with 'def'
# ============================================================

# Basic function with no parameters
def greet():
    """Prints a simple greeting message."""
    print("Hello, World!")

greet()  # Call the function

# Function with a parameter
def greet_user(name):
    """Greets a specific user by name."""
    print(f"Hello, {name}! Welcome.")

greet_user("Alice")
greet_user("Bob")

# Function that performs a calculation
def square(number):
    """Returns the square of a number."""
    return number ** 2

result = square(5)
print(f"\nSquare of 5: {result}")      # 25
print(f"Square of 9: {square(9)}")    # 81

# Function with multiple parameters
def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

print(f"\n3 + 7 = {add(3, 7)}")       # 10
print(f"10 + 25 = {add(10, 25)}")     # 35

# Function that checks a condition
def is_even(number):
    """Returns True if the number is even, False otherwise."""
    return number % 2 == 0

print(f"\nIs 4 even? {is_even(4)}")   # True
print(f"Is 7 even? {is_even(7)}")     # False

# Function that works with strings
def make_greeting(name, language="English"):
    """Creates a greeting in the specified language."""
    greetings = {
        "English": f"Hello, {name}!",
        "Spanish": f"Hola, {name}!",
        "French": f"Bonjour, {name}!",
        "Kazakh": f"Salam, {name}!",
    }
    return greetings.get(language, f"Hi, {name}!")

print(f"\n{make_greeting('Alice')}")
print(f"{make_greeting('Carlos', 'Spanish')}")
print(f"{make_greeting('Pierre', 'French')}")
print(f"{make_greeting('Amir', 'Kazakh')}")

# Calling functions inside other functions
def circle_area(radius):
    """Returns the area of a circle."""
    pi = 3.14159
    return pi * square(radius)   # reuses square() from above

print(f"\nArea of circle with radius 5: {circle_area(5):.2f}")
