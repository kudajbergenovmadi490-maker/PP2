# ============================================================
# Instance Methods
# Functions defined inside a class that operate on objects
# Always take 'self' as the first parameter
# ============================================================

class BankAccount:
    """A simple bank account class demonstrating various methods."""

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []

    # Method that modifies state
    def deposit(self, amount):
        """Adds money to the account."""
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.balance += amount
        self.transactions.append(f"+${amount}")
        print(f"Deposited ${amount}. New balance: ${self.balance}")

    # Method that modifies state with validation
    def withdraw(self, amount):
        """Removes money from the account if funds are sufficient."""
        if amount <= 0:
            print("Withdrawal must be positive.")
            return
        if amount > self.balance:
            print(f"Insufficient funds. Balance: ${self.balance}")
            return
        self.balance -= amount
        self.transactions.append(f"-${amount}")
        print(f"Withdrew ${amount}. New balance: ${self.balance}")

    # Method that returns a value
    def get_balance(self):
        """Returns the current balance."""
        return self.balance

    # Method that prints a summary
    def show_history(self):
        """Prints transaction history."""
        print(f"\nTransaction history for {self.owner}:")
        if not self.transactions:
            print("  No transactions yet.")
        for t in self.transactions:
            print(f"  {t}")
        print(f"  Current balance: ${self.balance}")

    # Method that calls other methods
    def transfer(self, other_account, amount):
        """Transfers money to another BankAccount."""
        print(f"\nTransferring ${amount} from {self.owner} to {other_account.owner}...")
        self.withdraw(amount)
        other_account.deposit(amount)

    # String representation method
    def __str__(self):
        """Returns a readable string when print() is called on the object."""
        return f"BankAccount(owner={self.owner}, balance=${self.balance})"


print("--- BankAccount demo ---")
acc1 = BankAccount("Alice", 500)
acc2 = BankAccount("Bob", 200)

acc1.deposit(300)
acc1.withdraw(100)
acc1.withdraw(1000)   # should fail
acc1.transfer(acc2, 150)

acc1.show_history()
acc2.show_history()

# Using __str__
print(f"\n{acc1}")
print(f"{acc2}")

# Accessing methods dynamically
print(f"\nAlice's balance via method: ${acc1.get_balance()}")


# Another example: Temperature class
class Temperature:
    """Stores temperature in Celsius and converts to other units."""

    def __init__(self, celsius):
        self.celsius = celsius

    def to_fahrenheit(self):
        return (self.celsius * 9/5) + 32

    def to_kelvin(self):
        return self.celsius + 273.15

    def describe(self):
        if self.celsius < 0:
            condition = "freezing"
        elif self.celsius < 20:
            condition = "cold"
        elif self.celsius < 30:
            condition = "comfortable"
        else:
            condition = "hot"
        return f"{self.celsius}°C is {condition}"

    def __str__(self):
        return (f"{self.celsius}°C = "
                f"{self.to_fahrenheit():.1f}°F = "
                f"{self.to_kelvin():.2f}K")


print("\n--- Temperature class ---")
t1 = Temperature(0)
t2 = Temperature(37)
t3 = Temperature(100)

for t in [t1, t2, t3]:
    print(t)
    print(f"  → {t.describe()}")
