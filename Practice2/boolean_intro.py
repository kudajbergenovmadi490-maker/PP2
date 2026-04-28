# ============================================================
# Boolean Introduction
# Booleans represent one of two values: True or False
# ============================================================

# Basic boolean values
is_python_fun = True
is_sky_green = False

print("Is Python fun?", is_python_fun)       # True
print("Is the sky green?", is_sky_green)     # False

# bool() function - evaluate any value as boolean
print("\n--- bool() function examples ---")
print(bool(1))        # True  - non-zero numbers are True
print(bool(0))        # False - zero is False
print(bool("Hello"))  # True  - non-empty strings are True
print(bool(""))       # False - empty string is False
print(bool([1, 2]))   # True  - non-empty list is True
print(bool([]))       # False - empty list is False
print(bool(None))     # False - None is always False

# isinstance() to check boolean type
x = True
print("\n--- isinstance() check ---")
print(isinstance(x, bool))  # True - x is a boolean

# Booleans are also integers (True == 1, False == 0)
print("\n--- Booleans as integers ---")
print(True + True)    # 2
print(True + False)   # 1
print(False + False)  # 0
print(True * 5)       # 5
