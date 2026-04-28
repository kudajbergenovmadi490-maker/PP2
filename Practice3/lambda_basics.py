# ============================================================
# Lambda Basics
# Anonymous functions written in one line
# Syntax: lambda arguments: expression
# ============================================================

# Regular function vs lambda
def square_regular(x):
    return x ** 2

square_lambda = lambda x: x ** 2

print("--- Regular vs Lambda ---")
print(f"Regular: {square_regular(5)}")   # 25
print(f"Lambda:  {square_lambda(5)}")    # 25

# Lambda with one argument
double = lambda x: x * 2
print(f"\nDouble 7: {double(7)}")         # 14

# Lambda with two arguments
add = lambda a, b: a + b
print(f"3 + 4 = {add(3, 4)}")            # 7

multiply = lambda a, b: a * b
print(f"6 x 7 = {multiply(6, 7)}")       # 42

# Lambda with three arguments
volume = lambda l, w, h: l * w * h
print(f"\nBox volume (3x4x5): {volume(3, 4, 5)}")  # 60

# Lambda with a conditional expression
is_even = lambda n: "even" if n % 2 == 0 else "odd"
print(f"\n10 is {is_even(10)}")  # even
print(f"7 is {is_even(7)}")     # odd

# Lambda returning a string
greet = lambda name: f"Hello, {name}!"
print(f"\n{greet('Alice')}")     # Hello, Alice!

# Lambda called immediately (IIFE style)
result = (lambda x, y: x ** y)(2, 10)
print(f"\n2^10 = {result}")      # 1024

# Storing lambdas in a dictionary (dispatch table)
print("\n--- Lambda dispatch table ---")
operations = {
    "add":      lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide":   lambda a, b: a / b if b != 0 else "Error",
}

for op_name, op_func in operations.items():
    print(f"  10 {op_name} 3 = {op_func(10, 3)}")
