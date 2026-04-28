# ============================================================
# Inheritance Basics
# A child class inherits attributes and methods from a parent class
# Syntax: class Child(Parent):
# ============================================================

# --- Parent class ---
class Animal:
    """Base class for all animals."""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        print(f"{self.name} is eating.")

    def sleep(self):
        print(f"{self.name} is sleeping.")

    def describe(self):
        print(f"Animal: {self.name}, Age: {self.age}")

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name}, age={self.age})"


# --- Child classes ---
class Dog(Animal):
    """Dog inherits from Animal and adds dog-specific behavior."""

    def __init__(self, name, age, breed):
        super().__init__(name, age)   # call parent __init__
        self.breed = breed            # dog-specific attribute

    def bark(self):
        print(f"{self.name} says: Woof!")

    def fetch(self):
        print(f"{self.name} fetches the ball!")


class Cat(Animal):
    """Cat inherits from Animal and adds cat-specific behavior."""

    def __init__(self, name, age, indoor):
        super().__init__(name, age)
        self.indoor = indoor  # True if indoor cat

    def meow(self):
        print(f"{self.name} says: Meow!")

    def purr(self):
        print(f"{self.name} is purring...")

    def describe(self):
        # Override parent's describe()
        location = "indoor" if self.indoor else "outdoor"
        print(f"Cat: {self.name}, Age: {self.age}, {location}")


class Bird(Animal):
    """Bird inherits from Animal."""

    def __init__(self, name, age, can_fly=True):
        super().__init__(name, age)
        self.can_fly = can_fly

    def chirp(self):
        print(f"{self.name} chirps!")

    def fly(self):
        if self.can_fly:
            print(f"{self.name} is flying!")
        else:
            print(f"{self.name} cannot fly.")


# --- Using the classes ---
print("--- Creating animals ---")
dog = Dog("Rex", 3, "German Shepherd")
cat = Cat("Whiskers", 5, indoor=True)
bird = Bird("Tweety", 2)
penguin = Bird("Pingu", 4, can_fly=False)

# Inherited methods
print("\n--- Inherited methods ---")
dog.eat()      # from Animal
cat.sleep()    # from Animal
bird.eat()     # from Animal

# Own methods
print("\n--- Own methods ---")
dog.bark()
dog.fetch()
cat.meow()
cat.purr()
bird.chirp()
bird.fly()
penguin.fly()

# describe() — overridden in Cat
print("\n--- describe() ---")
dog.describe()      # uses Animal's describe
cat.describe()      # uses Cat's overridden describe

# isinstance() and issubclass()
print("\n--- Type checking ---")
print(f"dog is Animal? {isinstance(dog, Animal)}")   # True
print(f"dog is Dog?    {isinstance(dog, Dog)}")      # True
print(f"dog is Cat?    {isinstance(dog, Cat)}")      # False
print(f"Dog is subclass of Animal? {issubclass(Dog, Animal)}")  # True

print(f"\n{dog}")
print(f"{cat}")
print(f"{penguin}")
