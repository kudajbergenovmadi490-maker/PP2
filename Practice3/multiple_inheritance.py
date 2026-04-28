# ============================================================
# Multiple Inheritance
# A class can inherit from more than one parent class
# Syntax: class Child(Parent1, Parent2):
# ============================================================

# --- Basic multiple inheritance ---
class Flyable:
    """Mixin: gives flying ability."""

    def fly(self):
        print(f"{self.name} is flying! ✈️")

    def land(self):
        print(f"{self.name} has landed.")


class Swimmable:
    """Mixin: gives swimming ability."""

    def swim(self):
        print(f"{self.name} is swimming! 🏊")

    def dive(self):
        print(f"{self.name} dives underwater.")


class Animal:
    """Base animal class."""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        print(f"{self.name} is eating.")

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"


# Duck can fly AND swim
class Duck(Animal, Flyable, Swimmable):
    """Duck inherits from Animal, Flyable, and Swimmable."""

    def quack(self):
        print(f"{self.name} says: Quack! 🦆")


# Seagull can only fly
class Seagull(Animal, Flyable):
    """Seagull inherits from Animal and Flyable."""

    def screech(self):
        print(f"{self.name} screeches!")


# Fish can only swim
class Fish(Animal, Swimmable):
    """Fish inherits from Animal and Swimmable."""

    def blow_bubbles(self):
        print(f"{self.name} blows bubbles.")


print("--- Duck (Animal + Flyable + Swimmable) ---")
duck = Duck("Donald", 3)
duck.eat()       # from Animal
duck.fly()       # from Flyable
duck.swim()      # from Swimmable
duck.quack()     # own method

print("\n--- Seagull (Animal + Flyable) ---")
seagull = Seagull("Gull", 2)
seagull.fly()
seagull.land()
seagull.screech()

print("\n--- Fish (Animal + Swimmable) ---")
fish = Fish("Nemo", 1)
fish.swim()
fish.dive()
fish.blow_bubbles()

# MRO — Method Resolution Order
# Python uses C3 linearization to determine which method to call
print("\n--- Method Resolution Order (MRO) ---")
print(Duck.__mro__)


# --- Practical example: Role-based mixin pattern ---
class ReadMixin:
    """Gives read permission."""
    def read(self):
        print(f"{self.username} is reading data.")

class WriteMixin:
    """Gives write permission."""
    def write(self):
        print(f"{self.username} is writing data.")

class DeleteMixin:
    """Gives delete permission."""
    def delete(self):
        print(f"{self.username} is deleting data.")

class User:
    """Base user class."""
    def __init__(self, username):
        self.username = username

    def login(self):
        print(f"{self.username} logged in.")

# Different roles have different permissions
class Viewer(User, ReadMixin):
    """Can only read."""
    pass

class Editor(User, ReadMixin, WriteMixin):
    """Can read and write."""
    pass

class Admin(User, ReadMixin, WriteMixin, DeleteMixin):
    """Can do everything."""
    pass


print("\n--- Role-based mixin example ---")
viewer = Viewer("alice")
editor = Editor("bob")
admin  = Admin("charlie")

viewer.login()
viewer.read()

editor.login()
editor.read()
editor.write()

admin.login()
admin.read()
admin.write()
admin.delete()

# Check capabilities
print(f"\nCan viewer delete? {hasattr(viewer, 'delete')}")   # False
print(f"Can admin delete?  {hasattr(admin, 'delete')}")     # True
