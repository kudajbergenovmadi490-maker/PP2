# ============================================================
# Short Hand If / Ternary Operator
# Write if-else in a single line
# Syntax: value_if_true if condition else value_if_false
# ============================================================

# Basic ternary
age = 20
status = "adult" if age >= 18 else "minor"
print("Status:", status)  # adult

# Even or odd
number = 14
parity = "even" if number % 2 == 0 else "odd"
print(f"\n{number} is {parity}")  # even

# Max of two numbers
a = 55
b = 99
maximum = a if a > b else b
print(f"\nMax of {a} and {b} is: {maximum}")  # 99

# Absolute value (without abs())
x = -7
absolute = x if x >= 0 else -x
print(f"\nAbsolute value of {x} is: {absolute}")  # 7

# Short-hand if (one-liner without else)
# Only runs if condition is True
temperature = 35
if temperature > 30: print("\nIt's a hot day!")  # prints

# Nested ternary (use carefully - can reduce readability)
score = 85
grade = "A" if score >= 90 else ("B" if score >= 80 else "C")
print(f"\nScore {score} → Grade: {grade}")  # B (85 is not >=90 but >=80)

# Using ternary in f-strings
items = 1
print(f"\nYou have {items} {'item' if items == 1 else 'items'} in your cart.")

# Ternary with function call
def greet(name):
    return f"Hello, {name}!"

user = "Alice"
message = greet(user) if user else "Hello, stranger!"
print(f"\n{message}")  # Hello, Alice!

# Ternary to set default value
user_input = ""
display_name = user_input if user_input else "Anonymous"
print(f"\nDisplay name: {display_name}")  # Anonymous
