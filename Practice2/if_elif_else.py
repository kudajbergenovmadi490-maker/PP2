# ============================================================
# If-Elif-Else Statement
# Tests multiple conditions one by one
# ============================================================

# Grade classification
score = 78

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"       # This matches (78 >= 70)
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score} → Grade: {grade}")  # Grade: C

# Day of the week
day_number = 3  # 1=Monday, 7=Sunday

if day_number == 1:
    day_name = "Monday"
elif day_number == 2:
    day_name = "Tuesday"
elif day_number == 3:
    day_name = "Wednesday"   # This matches
elif day_number == 4:
    day_name = "Thursday"
elif day_number == 5:
    day_name = "Friday"
elif day_number == 6:
    day_name = "Saturday"
elif day_number == 7:
    day_name = "Sunday"
else:
    day_name = "Invalid day"

print(f"\nDay {day_number} is: {day_name}")  # Wednesday

# BMI classification
bmi = 22.5

print("\n--- BMI Classification ---")
if bmi < 18.5:
    category = "Underweight"
elif bmi < 25:
    category = "Normal weight"    # This matches
elif bmi < 30:
    category = "Overweight"
else:
    category = "Obese"

print(f"BMI: {bmi} → Category: {category}")  # Normal weight

# Traffic light
light = "yellow"

print("\n--- Traffic Light ---")
if light == "green":
    print("Go!")
elif light == "yellow":
    print("Slow down!")    # This runs
elif light == "red":
    print("Stop!")
else:
    print("Unknown signal.")

# Age group classification
age = 35

print("\n--- Age Group ---")
if age < 13:
    group = "Child"
elif age < 18:
    group = "Teenager"
elif age < 60:
    group = "Adult"       # This matches
else:
    group = "Senior"

print(f"Age {age} → Group: {group}")
