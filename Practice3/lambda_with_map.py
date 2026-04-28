# ============================================================
# Lambda with map()
# map(function, iterable) applies a function to every item
# Returns a map object — convert to list to see results
# ============================================================

# Double every number in a list
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(f"Original: {numbers}")
print(f"Doubled:  {doubled}")   # [2, 4, 6, 8, 10]

# Square every number
squared = list(map(lambda x: x ** 2, numbers))
print(f"Squared:  {squared}")   # [1, 4, 9, 16, 25]

# Convert Celsius to Fahrenheit
celsius = [0, 20, 37, 100]
fahrenheit = list(map(lambda c: (c * 9/5) + 32, celsius))
print(f"\nCelsius:    {celsius}")
print(f"Fahrenheit: {fahrenheit}")  # [32.0, 68.0, 98.6, 212.0]

# Convert all strings to uppercase
words = ["hello", "world", "python", "lambda"]
uppercased = list(map(lambda w: w.upper(), words))
print(f"\nOriginal:   {words}")
print(f"Uppercased: {uppercased}")

# Get the length of each word
lengths = list(map(lambda w: len(w), words))
print(f"Lengths:    {lengths}")   # [5, 5, 6, 6]

# Apply map to a list of dictionaries
students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob",   "score": 72},
    {"name": "Charlie", "score": 91},
]

# Extract just the names
names = list(map(lambda s: s["name"], students))
print(f"\nStudent names: {names}")

# Add letter grade to each student
def add_grade(student):
    score = student["score"]
    grade = "A" if score >= 90 else "B" if score >= 80 else "C"
    return {**student, "grade": grade}

graded = list(map(add_grade, students))
print("\nStudents with grades:")
for s in graded:
    print(f"  {s['name']}: {s['score']} → {s['grade']}")

# map with two lists (zip-like behaviour)
prices = [100, 200, 300]
discounts = [0.1, 0.2, 0.15]
final_prices = list(map(lambda p, d: p * (1 - d), prices, discounts))
print(f"\nPrices:       {prices}")
print(f"Discounts:    {discounts}")
print(f"Final prices: {final_prices}")
