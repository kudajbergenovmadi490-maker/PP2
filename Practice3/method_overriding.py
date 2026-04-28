# ============================================================
# Method Overriding
# A child class redefines a method from the parent class
# The child's version takes priority over the parent's
# ============================================================

# --- Base class ---
class Employee:
    """Represents a general employee."""

    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def calculate_pay(self):
        """Default pay calculation — just base salary."""
        return self.base_salary

    def work(self):
        """Default work description."""
        print(f"{self.name} is working.")

    def describe(self):
        pay = self.calculate_pay()
        print(f"{self.name} ({self.__class__.__name__}) — Pay: ${pay:,.2f}")


# --- Child classes with overridden methods ---
class Manager(Employee):
    """Manager gets a bonus on top of base salary."""

    def __init__(self, name, base_salary, bonus):
        super().__init__(name, base_salary)
        self.bonus = bonus

    def calculate_pay(self):
        """Overrides: base salary + bonus."""
        return self.base_salary + self.bonus

    def work(self):
        """Overrides: manager has different work."""
        print(f"{self.name} is managing the team and attending meetings.")


class SalesEmployee(Employee):
    """Sales employee earns commission on sales."""

    def __init__(self, name, base_salary, sales_amount, commission_rate):
        super().__init__(name, base_salary)
        self.sales_amount = sales_amount
        self.commission_rate = commission_rate

    def calculate_pay(self):
        """Overrides: base salary + commission."""
        commission = self.sales_amount * self.commission_rate
        return self.base_salary + commission

    def work(self):
        """Overrides: sales-specific work."""
        print(f"{self.name} is calling clients and closing deals.")


class Intern(Employee):
    """Intern earns 60% of base salary."""

    def calculate_pay(self):
        """Overrides: interns get 60% of base."""
        return self.base_salary * 0.6

    def work(self):
        """Overrides: intern activities."""
        print(f"{self.name} is learning and assisting the team.")


# --- Demonstrate method overriding ---
employees = [
    Employee("Alice", 5000),
    Manager("Bob", 6000, 1500),
    SalesEmployee("Charlie", 3000, 20000, 0.05),
    Intern("Diana", 3000),
]

print("--- Employee Pay Calculations ---")
for emp in employees:
    emp.work()          # each class has its own work() version
    emp.describe()      # calls overridden calculate_pay() internally
    print()

# Polymorphism — same method name, different behavior
print("--- Polymorphism Demo ---")
print("Calling calculate_pay() on each employee:")
for emp in employees:
    print(f"  {emp.name}: ${emp.calculate_pay():,.2f}")


# --- Overriding __str__ and __repr__ ---
class Product:
    """Product with overridden string methods."""

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        """Human-readable string (used by print())."""
        return f"{self.name} — ${self.price:.2f} ({self.stock} in stock)"

    def __repr__(self):
        """Developer-friendly representation."""
        return f"Product(name={self.name!r}, price={self.price}, stock={self.stock})"


class DiscountedProduct(Product):
    """Overrides __str__ to show the discount."""

    def __init__(self, name, price, stock, discount):
        super().__init__(name, price, stock)
        self.discount = discount

    def final_price(self):
        return self.price * (1 - self.discount)

    def __str__(self):
        """Override: show original price and discounted price."""
        return (f"{self.name} — ~~${self.price:.2f}~~ "
                f"→ ${self.final_price():.2f} ({int(self.discount*100)}% off)")


print("\n--- Overriding __str__ ---")
p1 = Product("Keyboard", 80, 15)
p2 = DiscountedProduct("Mouse", 50, 8, 0.20)

print(p1)   # uses Product's __str__
print(p2)   # uses DiscountedProduct's __str__
print(repr(p1))
