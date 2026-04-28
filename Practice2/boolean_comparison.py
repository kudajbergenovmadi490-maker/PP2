# ============================================================
# Booleans as Comparison Results
# Comparison operators always return True or False
# ============================================================

a = 10
b = 20

print("--- Comparison Operators ---")
print(a == b)   # False - equal to
print(a != b)   # True  - not equal to
print(a > b)    # False - greater than
print(a < b)    # True  - less than
print(a >= 10)  # True  - greater than or equal to
print(b <= 20)  # True  - less than or equal to

# Comparing strings
print("\n--- String Comparisons ---")
name1 = "Alice"
name2 = "Bob"
print(name1 == name2)   # False
print(name1 < name2)    # True  - alphabetical order (A < B)
print("apple" == "apple")  # True

# Comparing different types
print("\n--- Comparing with numbers ---")
print(1 == 1.0)    # True  - int and float can be equal
print(1 == True)   # True  - True equals 1
print(0 == False)  # True  - False equals 0

# Using comparisons in variables
print("\n--- Storing comparison results ---")
age = 18
is_adult = age >= 18
print("Is adult:", is_adult)  # True

score = 75
passed = score >= 60
print("Passed exam:", passed)  # True

temperature = -5
is_freezing = temperature < 0
print("Is freezing:", is_freezing)  # True
