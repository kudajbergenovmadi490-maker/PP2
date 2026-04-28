# ============================================================
# Class Definition and Object Creation
# A class is a blueprint; an object is an instance of a class
# ============================================================

# Define a simple class
class Dog:
    """A simple class representing a dog."""

    # Class variable — shared by ALL instances
    species = "Canis familiaris"

    # Constructor — runs when object is created
    def __init__(self, name, breed, age):
        # Instance variables — unique to each object
        self.name = name
        self.breed = breed
        self.age = age

    # Instance method
    def bark(self):
        """Makes the dog bark."""
        print(f"{self.name} says: Woof!")

    def describe(self):
        """Prints a description of the dog."""
        print(f"{self.name} is a {self.age}-year-old {self.breed}.")

    def is_puppy(self):
        """Returns True if the dog is less than 2 years old."""
        return self.age < 2


# Create objects (instances) of the Dog class
dog1 = Dog("Rex", "German Shepherd", 3)
dog2 = Dog("Buddy", "Golden Retriever", 1)
dog3 = Dog("Max", "Bulldog", 5)

# Access instance variables
print("--- Instance Variables ---")
print(f"Name:  {dog1.name}")
print(f"Breed: {dog1.breed}")
print(f"Age:   {dog1.age}")

# Access class variable
print(f"\n--- Class Variable ---")
print(f"Species (via object): {dog1.species}")
print(f"Species (via class):  {Dog.species}")

# Call methods
print("\n--- Methods ---")
dog1.bark()
dog2.bark()
dog1.describe()
dog2.describe()

# Use a method that returns a value
print(f"\n--- is_puppy() ---")
print(f"Is {dog1.name} a puppy? {dog1.is_puppy()}")  # False (age=3)
print(f"Is {dog2.name} a puppy? {dog2.is_puppy()}")  # True  (age=1)

# Each object is independent
print(f"\n--- Objects are independent ---")
print(f"dog1: {dog1.name}, dog2: {dog2.name}, dog3: {dog3.name}")

# Check object type
print(f"\n--- isinstance() check ---")
print(f"dog1 is a Dog: {isinstance(dog1, Dog)}")  # True


# Another example: Book class
class Book:
    """Represents a book."""

    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def summary(self):
        print(f'"{self.title}" by {self.author} ({self.pages} pages)')

    def is_long(self):
        return self.pages > 300


print("\n--- Book class ---")
book1 = Book("Python Crash Course", "Eric Matthes", 544)
book2 = Book("The Alchemist", "Paulo Coelho", 197)

book1.summary()
book2.summary()
print(f"Is '{book1.title}' long? {book1.is_long()}")  # True
print(f"Is '{book2.title}' long? {book2.is_long()}")  # False
