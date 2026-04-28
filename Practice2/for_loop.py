# ============================================================
# For Loop
# Iterates over a sequence (list, tuple, string, range, etc.)
# ============================================================

# Loop through a list
print("--- Loop through a list ---")
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Loop through a string (character by character)
print("\n--- Loop through a string ---")
for letter in "Python":
    print(letter, end=" ")
print()  # newline

# Loop with range()
print("\n--- range(5): 0 to 4 ---")
for i in range(5):
    print(i, end=" ")
print()

print("\n--- range(1, 6): 1 to 5 ---")
for i in range(1, 6):
    print(i, end=" ")
print()

print("\n--- range(0, 10, 2): even numbers ---")
for i in range(0, 10, 2):
    print(i, end=" ")
print()

print("\n--- range(10, 0, -2): counting down by 2 ---")
for i in range(10, 0, -2):
    print(i, end=" ")
print()

# Loop through a tuple
print("\n--- Loop through a tuple ---")
colors = ("red", "green", "blue")
for color in colors:
    print(f"Color: {color}")

# Loop through a dictionary
print("\n--- Loop through a dictionary ---")
student = {"name": "Alice", "age": 20, "grade": "A"}
for key in student:
    print(f"{key}: {student[key]}")

# Loop with items()
print("\n--- Loop with .items() ---")
for key, value in student.items():
    print(f"  {key} → {value}")

# Loop with enumerate() - get index and value
print("\n--- enumerate() for index + value ---")
animals = ["cat", "dog", "bird"]
for index, animal in enumerate(animals):
    print(f"  [{index}] {animal}")

# Nested for loops - multiplication table
print("\n--- Multiplication table (1-3) ---")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i*j}", end="   ")
    print()  # newline after each row

# Loop to compute sum
print("\n--- Sum of a list ---")
numbers = [10, 20, 30, 40, 50]
total = 0
for num in numbers:
    total += num
print(f"Sum: {total}")  # 150
