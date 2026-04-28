# ============================================================
# Return Values
# Functions can return single values, multiple values, or None
# ============================================================

# Return a single value
def fahrenheit_to_celsius(f):
    """Converts Fahrenheit to Celsius."""
    return (f - 32) * 5 / 9

temp_c = fahrenheit_to_celsius(98.6)
print(f"98.6°F = {temp_c:.2f}°C")  # 37.00°C

# Return a boolean
def is_palindrome(text):
    """Returns True if the text is a palindrome."""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

print(f"\n'racecar' is palindrome: {is_palindrome('racecar')}")    # True
print(f"'hello' is palindrome: {is_palindrome('hello')}")          # False
print(f"'A man a plan a canal Panama': {is_palindrome('A man a plan a canal Panama')}")  # True

# Return multiple values (as a tuple)
def min_max(numbers):
    """Returns both the minimum and maximum of a list."""
    return min(numbers), max(numbers)

data = [4, 7, 1, 9, 3, 8, 2]
minimum, maximum = min_max(data)
print(f"\nData: {data}")
print(f"Min: {minimum}, Max: {maximum}")

# Return a list
def get_evens(numbers):
    """Returns a list of even numbers from the input list."""
    return [n for n in numbers if n % 2 == 0]

evens = get_evens([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(f"\nEven numbers: {evens}")  # [2, 4, 6, 8, 10]

# Return a dictionary
def get_stats(numbers):
    """Returns a dictionary of statistics for a list of numbers."""
    return {
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "average": sum(numbers) / len(numbers),
    }

stats = get_stats([10, 20, 30, 40, 50])
print("\nStatistics:")
for key, value in stats.items():
    print(f"  {key}: {value}")

# Early return (guard clause pattern)
def safe_divide(a, b):
    """Divides a by b, returns None if b is zero."""
    if b == 0:
        print("Error: Cannot divide by zero!")
        return None     # early return
    return a / b

print(f"\n10 / 2 = {safe_divide(10, 2)}")   # 5.0
print(f"10 / 0 = {safe_divide(10, 0)}")     # None

# Function with no return (implicitly returns None)
def log_message(msg):
    """Logs a message (returns nothing)."""
    print(f"[LOG] {msg}")

result = log_message("System started")
print(f"Return value: {result}")  # None
