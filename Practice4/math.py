# ============================================================
# Python Math and Random Modules
# ============================================================

import math
import random

print("=== BUILT-IN MATH FUNCTIONS ===")

# min() and max()
print("\n--- min() and max() ---")
numbers = [4, 7, 1, 9, 3, 8, 2, 6, 5]
print(f"Numbers: {numbers}")
print(f"min: {min(numbers)}")    # 1
print(f"max: {max(numbers)}")    # 9
print(f"min(3, 1, 4, 1, 5): {min(3, 1, 4, 1, 5)}")
print(f"max(3, 1, 4, 1, 5): {max(3, 1, 4, 1, 5)}")

# min/max with key
words = ["banana", "fig", "strawberry", "kiwi"]
print(f"\nShortest word: {min(words, key=len)}")   # fig
print(f"Longest word:  {max(words, key=len)}")     # strawberry

# abs()
print("\n--- abs() ---")
print(f"abs(-7):   {abs(-7)}")     # 7
print(f"abs(3.14): {abs(3.14)}")   # 3.14
print(f"abs(-0.5): {abs(-0.5)}")   # 0.5

# round()
print("\n--- round() ---")
print(f"round(3.7):    {round(3.7)}")      # 4
print(f"round(3.2):    {round(3.2)}")      # 3
print(f"round(3.14159, 2): {round(3.14159, 2)}")  # 3.14
print(f"round(2.5):    {round(2.5)}")      # 2 (banker's rounding)
print(f"round(3.5):    {round(3.5)}")      # 4

# pow()
print("\n--- pow() ---")
print(f"pow(2, 10): {pow(2, 10)}")    # 1024
print(f"pow(3, 3):  {pow(3, 3)}")     # 27
print(f"2 ** 10:    {2 ** 10}")        # same as pow(2, 10)
print(f"pow(2, 10, 1000): {pow(2, 10, 1000)}")  # modular: 1024 % 1000 = 24

# sum()
print("\n--- sum() ---")
print(f"sum([1..5]): {sum([1, 2, 3, 4, 5])}")    # 15
print(f"sum with start: {sum([1, 2, 3], 10)}")    # 16


print("\n=== MATH MODULE ===")

# Square root
print("\n--- math.sqrt() ---")
print(f"sqrt(16):  {math.sqrt(16)}")    # 4.0
print(f"sqrt(2):   {math.sqrt(2):.6f}") # 1.414213...
print(f"sqrt(144): {math.sqrt(144)}")   # 12.0

# Ceiling and floor
print("\n--- math.ceil() and math.floor() ---")
x = 4.3
print(f"x = {x}")
print(f"  ceil:  {math.ceil(x)}")    # 5 — round UP
print(f"  floor: {math.floor(x)}")   # 4 — round DOWN

y = -2.7
print(f"y = {y}")
print(f"  ceil:  {math.ceil(y)}")    # -2
print(f"  floor: {math.floor(y)}")   # -3

# Trigonometry
print("\n--- Trigonometry ---")
angle_deg = 45
angle_rad = math.radians(angle_deg)   # convert degrees to radians

print(f"Angle: {angle_deg}°  =  {angle_rad:.4f} radians")
print(f"sin(45°): {math.sin(angle_rad):.4f}")   # ~0.7071
print(f"cos(45°): {math.cos(angle_rad):.4f}")   # ~0.7071
print(f"tan(45°): {math.tan(angle_rad):.4f}")   # ~1.0

# Logarithms
print("\n--- Logarithms ---")
print(f"log(math.e):    {math.log(math.e):.4f}")    # natural log → 1.0
print(f"log(100, 10):   {math.log(100, 10):.4f}")   # log base 10 → 2.0
print(f"log2(1024):     {math.log2(1024):.4f}")      # log base 2 → 10.0
print(f"log10(1000):    {math.log10(1000):.4f}")     # log base 10 → 3.0

# Constants
print("\n--- Math constants ---")
print(f"math.pi:  {math.pi}")     # 3.14159...
print(f"math.e:   {math.e}")      # 2.71828...
print(f"math.tau: {math.tau}")    # 6.28318... (2 * pi)
print(f"math.inf: {math.inf}")    # infinity
print(f"math.nan: {math.nan}")    # not a number

# Other useful functions
print("\n--- Other math functions ---")
print(f"factorial(6):  {math.factorial(6)}")   # 720
print(f"gcd(48, 18):   {math.gcd(48, 18)}")    # 6
print(f"isnan(nan):    {math.isnan(math.nan)}") # True
print(f"isinf(inf):    {math.isinf(math.inf)}") # True
print(f"hypot(3, 4):   {math.hypot(3, 4)}")    # 5.0 (Pythagorean)


print("\n=== RANDOM MODULE ===")

random.seed(42)   # seed for reproducibility in examples

# random() — float between 0.0 and 1.0
print("\n--- random.random() ---")
for _ in range(4):
    print(f"  {random.random():.4f}")

# randint() — integer between a and b (inclusive)
print("\n--- random.randint() ---")
print(f"Die roll: {random.randint(1, 6)}")
print(f"Die roll: {random.randint(1, 6)}")
print(f"Lottery:  {random.randint(1, 49)}")

# randrange() — like range but random
print("\n--- random.randrange() ---")
print(f"Even number 0-10: {random.randrange(0, 11, 2)}")

# choice() — pick one random item from a sequence
print("\n--- random.choice() ---")
colors = ["red", "green", "blue", "yellow", "purple"]
print(f"Random color: {random.choice(colors)}")
print(f"Random color: {random.choice(colors)}")

# choices() — pick multiple items (with replacement)
print("\n--- random.choices() ---")
print(f"3 random colors: {random.choices(colors, k=3)}")

# sample() — pick multiple items WITHOUT replacement
print("\n--- random.sample() ---")
print(f"3 unique colors: {random.sample(colors, 3)}")

deck = list(range(1, 53))
hand = random.sample(deck, 5)
print(f"5-card hand: {hand}")

# shuffle() — shuffle a list IN PLACE
print("\n--- random.shuffle() ---")
cards = ["A", "K", "Q", "J", "10"]
print(f"Before: {cards}")
random.shuffle(cards)
print(f"After:  {cards}")

# uniform() — float between a and b
print("\n--- random.uniform() ---")
print(f"Random float 1.0-5.0: {random.uniform(1.0, 5.0):.4f}")
