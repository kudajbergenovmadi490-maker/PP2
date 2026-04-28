# ============================================================
# *args and **kwargs in depth
# Flexible functions that accept any number of arguments
# ============================================================

# --- *args: variable positional arguments ---
def multiply_all(*args):
    """Multiplies all given numbers together."""
    result = 1
    for num in args:
        result *= num
    return result

print("--- *args examples ---")
print(multiply_all(2, 3))           # 6
print(multiply_all(2, 3, 4))        # 24
print(multiply_all(1, 2, 3, 4, 5)) # 120

# *args with a required argument
def introduce(greeting, *names):
    """Greets multiple names with one greeting."""
    for name in names:
        print(f"{greeting}, {name}!")

print("\n--- *args with required arg ---")
introduce("Hello", "Alice", "Bob", "Charlie")
introduce("Hi", "Zara")

# --- **kwargs: variable keyword arguments ---
def build_html_tag(tag, **attributes):
    """Builds an HTML tag string from keyword arguments."""
    attrs = " ".join(f'{k}="{v}"' for k, v in attributes.items())
    return f"<{tag} {attrs}>" if attrs else f"<{tag}>"

print("\n--- **kwargs examples ---")
print(build_html_tag("a", href="https://python.org", target="_blank"))
print(build_html_tag("img", src="photo.jpg", alt="A photo", width="200"))
print(build_html_tag("div"))

# **kwargs: building dynamic settings
def configure_app(**settings):
    """Applies application settings from keyword arguments."""
    print("\nApp Configuration:")
    defaults = {"debug": False, "theme": "light", "language": "en"}
    defaults.update(settings)   # override with provided settings
    for key, value in defaults.items():
        print(f"  {key}: {value}")

configure_app(debug=True, theme="dark", max_users=100)

# --- Passing *args and **kwargs to another function ---
def log(*args, **kwargs):
    """Wrapper that logs and then calls print."""
    print("[LOG]", *args, **kwargs)

log("Hello", "World", sep="-", end="!\n")

# --- Unpacking lists/dicts into function calls ---
def add_three(a, b, c):
    """Adds three numbers."""
    return a + b + c

numbers = [1, 2, 3]
print(f"\nUnpacking list: {add_three(*numbers)}")  # 6

values = {"a": 10, "b": 20, "c": 30}
print(f"Unpacking dict: {add_three(**values)}")    # 60

# --- Combining *args and **kwargs ---
def flexible_function(*args, **kwargs):
    """Accepts absolutely any arguments."""
    print(f"\nPositional args: {args}")
    print(f"Keyword args:    {kwargs}")
    print(f"Total arguments: {len(args) + len(kwargs)}")

flexible_function(1, 2, 3, name="Alice", city="Almaty", active=True)
