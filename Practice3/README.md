# Practice 3: Python Functions and Object-Oriented Programming

## Overview
This practice covers Python functions, lambda expressions, and object-oriented programming (OOP) concepts including classes, inheritance, and method overriding.

## Project Structure
```
Practice-03/
├── functions/
│   ├── basic_functions.py       # Function definition, calling, docstrings
│   ├── function_arguments.py    # Positional, default, keyword, *args, **kwargs
│   ├── return_values.py         # Single, multiple, and no return values
│   └── args_kwargs.py           # Deep dive into *args and **kwargs
├── lambda/
│   ├── lambda_basics.py         # Lambda syntax and basic usage
│   ├── lambda_with_map.py       # map() for transformation
│   ├── lambda_with_filter.py    # filter() for selection
│   └── lambda_with_sorted.py    # sorted() with custom key
├── classes/
│   ├── class_definition.py      # Class blueprint, object creation
│   ├── init_method.py           # __init__ constructor, computed attrs
│   ├── class_methods.py         # Instance methods, __str__
│   └── class_variables.py       # Class vs instance variables, @classmethod, @staticmethod
├── inheritance/
│   ├── inheritance_basics.py    # Parent/child class relationships
│   ├── super_function.py        # super() to call parent methods
│   ├── method_overriding.py     # Polymorphism, overriding __str__
│   └── multiple_inheritance.py  # Multiple parents, mixins, MRO
└── README.md
```

## Key Concepts

### Functions
| Concept | Syntax |
|---------|--------|
| Define | `def func(args): ...` |
| Positional args | `func(a, b)` |
| Default args | `def func(x, y=10)` |
| *args | `def func(*args)` — tuple of extra positionals |
| **kwargs | `def func(**kwargs)` — dict of extra keywords |
| Return | `return value` |

### Lambda
| Usage | Example |
|-------|---------|
| Basic | `lambda x: x * 2` |
| Two args | `lambda a, b: a + b` |
| With map | `list(map(lambda x: x**2, nums))` |
| With filter | `list(filter(lambda x: x > 0, nums))` |
| With sorted | `sorted(items, key=lambda x: x['score'])` |

### OOP
| Concept | Description |
|---------|-------------|
| Class | Blueprint for objects |
| Object | Instance of a class |
| `__init__` | Constructor, runs at creation |
| `self` | Reference to the current object |
| Class variable | Shared by all instances |
| Instance variable | Unique per object |
| Inheritance | `class Child(Parent)` |
| `super()` | Calls the parent's method |
| Override | Redefine parent method in child |

## How to Run
```bash
python functions/basic_functions.py
python lambda/lambda_with_map.py
python classes/class_methods.py
python inheritance/multiple_inheritance.py
```
