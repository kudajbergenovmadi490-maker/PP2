# ============================================================
# super() Function
# Calls methods from the parent class
# Avoids hardcoding the parent class name
# ============================================================

# --- Basic super() in __init__ ---
class Vehicle:
    """Base class for vehicles."""

    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        print(f"  [Vehicle.__init__ called: {make} {model}]")

    def start(self):
        print(f"{self.make} {self.model} engine started.")

    def stop(self):
        print(f"{self.make} {self.model} engine stopped.")

    def info(self):
        return f"{self.year} {self.make} {self.model}"


class Car(Vehicle):
    """A car with additional car-specific attributes."""

    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)    # call parent __init__
        self.num_doors = num_doors
        print(f"  [Car.__init__ called: {num_doors} doors]")

    def info(self):
        # Extend parent's info() using super()
        base_info = super().info()
        return f"{base_info} ({self.num_doors}-door)"


class ElectricCar(Car):
    """An electric car — extends Car which extends Vehicle."""

    def __init__(self, make, model, year, num_doors, battery_kw):
        super().__init__(make, model, year, num_doors)  # calls Car.__init__
        self.battery_kw = battery_kw
        print(f"  [ElectricCar.__init__ called: {battery_kw}kW battery]")

    def info(self):
        base_info = super().info()   # calls Car's info()
        return f"{base_info} [Electric, {self.battery_kw}kW]"

    def charge(self):
        print(f"Charging {self.make} {self.model}... 🔋")


print("--- Creating Car ---")
car = Car("Toyota", "Camry", 2022, 4)
print(f"\n{car.info()}")
car.start()

print("\n--- Creating ElectricCar (3-level hierarchy) ---")
tesla = ElectricCar("Tesla", "Model 3", 2023, 4, 75)
print(f"\n{tesla.info()}")
tesla.start()    # inherited from Vehicle (through Car)
tesla.charge()   # own method

# super() in methods (not just __init__)
class Shape:
    """Base shape class."""

    def __init__(self, color):
        self.color = color

    def area(self):
        return 0

    def describe(self):
        print(f"Shape — Color: {self.color}, Area: {self.area():.2f}")


class Circle(Shape):
    """A circle."""

    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def describe(self):
        super().describe()   # call parent describe
        print(f"  → Circle with radius {self.radius}")


class Square(Shape):
    """A square."""

    def __init__(self, color, side):
        super().__init__(color)
        self.side = side

    def area(self):
        return self.side ** 2

    def describe(self):
        super().describe()
        print(f"  → Square with side {self.side}")


print("\n--- super() in methods ---")
shapes = [
    Circle("red", 5),
    Square("blue", 4),
    Circle("green", 3),
]

for shape in shapes:
    shape.describe()
    print()
