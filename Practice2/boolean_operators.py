# ============================================================
# Boolean Operators: and, or, not
# Used to combine or invert boolean expressions
# ============================================================

# --- AND operator ---
# Returns True only if BOTH conditions are True
print("--- AND operator ---")
print(True and True)    # True
print(True and False)   # False
print(False and True)   # False
print(False and False)  # False

age = 25
has_license = True
can_drive = age >= 18 and has_license
print("\nCan drive:", can_drive)  # True

# --- OR operator ---
# Returns True if AT LEAST ONE condition is True
print("\n--- OR operator ---")
print(True or True)     # True
print(True or False)    # True
print(False or True)    # True
print(False or False)   # False

is_weekend = False
is_holiday = True
can_rest = is_weekend or is_holiday
print("Can rest today:", can_rest)  # True

# --- NOT operator ---
# Inverts the boolean value
print("\n--- NOT operator ---")
print(not True)    # False
print(not False)   # True

is_raining = False
should_go_outside = not is_raining
print("Should go outside:", should_go_outside)  # True

# --- Combining operators ---
print("\n--- Combined operators ---")
x = 15
# x is between 10 and 20
result = x > 10 and x < 20
print("x is between 10 and 20:", result)  # True

# More complex logic
username = "admin"
password = "1234"
is_valid = username == "admin" and password == "1234"
print("Login valid:", is_valid)  # True

score = 45
grade = "A" if score >= 90 else "pass" if score >= 60 else "fail"
print("Grade:", grade)  # fail

# Short-circuit evaluation
print("\n--- Short-circuit evaluation ---")
# Python stops evaluating as soon as result is determined
print(False and (1/0))  # False - doesn't evaluate (1/0) !
print(True or (1/0))   # True  - doesn't evaluate (1/0)
