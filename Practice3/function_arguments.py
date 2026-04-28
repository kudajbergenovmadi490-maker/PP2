# ============================================================
# Function Arguments
# Positional, keyword, default, *args, **kwargs
# ============================================================

# --- Positional Arguments ---
# Must be passed in the correct order
def describe_pet(animal, name):
    """Describes a pet using positional arguments."""
    print(f"I have a {animal} named {name}.")

describe_pet("dog", "Rex")      # positional order matters
describe_pet("cat", "Whiskers")

# --- Default Arguments ---
# Have a fallback value if not provided
def power(base, exponent=2):
    """Raises base to the given exponent (default is 2)."""
    return base ** exponent

print(f"\n2^3 = {power(2, 3)}")   # 8  — exponent provided
print(f"5^2 = {power(5)}")        # 25 — uses default exponent=2
print(f"3^4 = {power(3, 4)}")     # 81

# --- Keyword Arguments ---
# Pass by name, order doesn't matter
def create_profile(name, age, city):
    """Prints a user profile."""
    print(f"\nName: {name}, Age: {age}, City: {city}")

create_profile(name="Alice", age=25, city="Almaty")
create_profile(city="London", name="Bob", age=30)  # order doesn't matter

# --- *args (Arbitrary Positional Arguments) ---
# Accepts any number of positional arguments as a tuple
def total(*numbers):
    """Returns the sum of any number of arguments."""
    print(f"  Arguments received: {numbers}")
    return sum(numbers)

print(f"\nTotal: {total(1, 2, 3)}")           # 6
print(f"Total: {total(10, 20, 30, 40, 50)}") # 150
print(f"Total: {total(5)}")                   # 5

# --- **kwargs (Arbitrary Keyword Arguments) ---
# Accepts any number of keyword arguments as a dictionary
def print_info(**details):
    """Prints all keyword arguments as key-value pairs."""
    print("\nUser Details:")
    for key, value in details.items():
        print(f"  {key}: {value}")

print_info(name="Charlie", age=22, country="Kazakhstan", hobby="coding")

# --- Combining all argument types ---
def mixed_args(required, default="hello", *args, **kwargs):
    """Demonstrates all argument types together."""
    print(f"\nRequired: {required}")
    print(f"Default:  {default}")
    print(f"*args:    {args}")
    print(f"**kwargs: {kwargs}")

mixed_args("must_have", "world", 1, 2, 3, color="blue", size="large")
