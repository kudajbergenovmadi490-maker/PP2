# ============================================================
# The __init__() Method (Constructor)
# Automatically called when a new object is created
# Used to initialize instance variables
# ============================================================

# Basic __init__ with required parameters
class Person:
    """Represents a person."""

    def __init__(self, name, age):
        self.name = name
        self.age = age
        print(f"  [Person created: {self.name}]")

    def introduce(self):
        print(f"Hi, I'm {self.name} and I'm {self.age} years old.")


print("--- Creating Person objects ---")
p1 = Person("Alice", 25)
p2 = Person("Bob", 30)
p1.introduce()
p2.introduce()


# __init__ with default parameters
class Car:
    """Represents a car with some optional attributes."""

    def __init__(self, make, model, year, color="white", mileage=0):
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage

    def describe(self):
        print(f"{self.year} {self.color} {self.make} {self.model} — {self.mileage} km")

    def drive(self, km):
        self.mileage += km
        print(f"Drove {km} km. Total: {self.mileage} km")


print("\n--- Car class with defaults ---")
car1 = Car("Toyota", "Camry", 2022)               # uses defaults
car2 = Car("BMW", "M3", 2023, "black", 5000)      # all provided

car1.describe()
car2.describe()
car1.drive(150)
car1.describe()


# __init__ with computed attributes
class Rectangle:
    """A rectangle that computes area and perimeter automatically."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Computed in __init__ — derived attributes
        self.area = width * height
        self.perimeter = 2 * (width + height)

    def describe(self):
        print(f"Rectangle {self.width}x{self.height}: "
              f"area={self.area}, perimeter={self.perimeter}")


print("\n--- Rectangle with computed attrs ---")
r1 = Rectangle(5, 3)
r2 = Rectangle(10, 4)
r1.describe()
r2.describe()


# __init__ with a list attribute (mutable default — done safely)
class ShoppingCart:
    """A shopping cart that starts empty."""

    def __init__(self, owner):
        self.owner = owner
        self.items = []     # safe: create new list per instance

    def add_item(self, item, price):
        self.items.append({"item": item, "price": price})

    def total(self):
        return sum(i["price"] for i in self.items)

    def show(self):
        print(f"\n{self.owner}'s cart:")
        for entry in self.items:
            print(f"  {entry['item']}: ${entry['price']}")
        print(f"  Total: ${self.total()}")


print("\n--- ShoppingCart ---")
cart1 = ShoppingCart("Alice")
cart2 = ShoppingCart("Bob")

cart1.add_item("Python Book", 30)
cart1.add_item("Keyboard", 80)
cart2.add_item("Mouse", 25)

cart1.show()
cart2.show()
