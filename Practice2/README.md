# Practice 2: Python Control Flow Basics

## Overview
This practice covers Python control flow structures including boolean values, conditionals, and loops.

## Project Structure
```
Practice2/
├── boolean/
│   ├── boolean_intro.py        # Boolean values, bool(), isinstance()
│   ├── boolean_comparison.py   # Comparison operators (==, !=, >, <, >=, <=)
│   └── boolean_operators.py    # Logical operators (and, or, not)
├── if_else/
│   ├── if_statement.py         # Basic if, nested if
│   ├── if_else.py              # If-else examples
│   ├── if_elif_else.py         # Multiple conditions with elif
│   └── short_hand_if.py        # Ternary operator (one-line if-else)
├── loops/
│   ├── while_loop.py           # While loop basics
│   ├── while_break.py          # While loop with break
│   ├── while_continue.py       # While loop with continue
│   ├── for_loop.py             # For loop with lists, range, dict, enumerate
│   ├── for_break.py            # For loop with break
│   └── for_continue.py         # For loop with continue
└── README.md
```

## Topics Covered

### Boolean Values
- `True` and `False` literals
- `bool()` function to evaluate truthiness
- Booleans as integers (True=1, False=0)

### Comparison Operators
| Operator | Meaning |
|----------|---------|
| `==` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |

### Boolean Operators
| Operator | Description |
|----------|-------------|
| `and` | True if BOTH conditions are True |
| `or` | True if AT LEAST ONE condition is True |
| `not` | Inverts the boolean value |

### Conditional Statements
- `if` — basic conditional
- `if-else` — two-way branch
- `if-elif-else` — multi-way branch
- Ternary: `value_if_true if condition else value_if_false`

### Loops
- `while` — repeats while condition is True
- `for` — iterates over a sequence
- `break` — exits the loop immediately
- `continue` — skips current iteration, continues loop
- `else` on loops — runs if loop completed without `break`

## How to Run
```bash
python boolean/boolean_intro.py
python if_else/if_elif_else.py
python loops/for_loop.py
# etc.
```
