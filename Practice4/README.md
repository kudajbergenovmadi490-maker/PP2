# Practice 4: Python Advanced Topics — Iterators, Dates, Math, and JSON

## Overview
This practice covers advanced Python concepts: iterators and generators, working with dates and times, mathematical operations, and JSON handling.

## Project Structure
```
Practice4/
├── generators.py       # Iterators, iter(), next(), custom iterators, generators, yield
├── dates.py            # datetime module, formatting, timedelta, calendar
├── math.py             # Built-in math functions + math module + random module
├── json.py             # json.loads(), json.dumps(), reading/writing JSON files
├── sample-data.json    # Sample company data for JSON exercises
└── README.md
```

## Topics Covered

### Iterators (`generators.py`)
| Concept | Description |
|---------|-------------|
| `iter(obj)` | Creates an iterator from an iterable |
| `next(it)` | Gets the next item from an iterator |
| `__iter__()` | Makes a class iterable |
| `__next__()` | Returns next value; raises StopIteration when done |
| `yield` | Turns a function into a generator |
| Generator expression | `(x**2 for x in range(10))` — lazy evaluation |

### Dates (`dates.py`)
| Concept | Example |
|---------|---------|
| Today's date | `date.today()` |
| Current datetime | `datetime.now()` |
| Specific date | `date(2025, 6, 15)` |
| Format date | `dt.strftime("%Y-%m-%d")` |
| Parse string | `datetime.strptime(s, "%Y-%m-%d")` |
| Date arithmetic | `date.today() + timedelta(days=7)` |
| Difference | `end_date - start_date` → timedelta |

### Math (`math.py`)
| Function | Description |
|----------|-------------|
| `min()`, `max()` | Smallest / largest value |
| `abs()` | Absolute value |
| `round(x, n)` | Round to n decimal places |
| `pow(x, y)` | x to the power of y |
| `math.sqrt(x)` | Square root |
| `math.ceil(x)` | Round up |
| `math.floor(x)` | Round down |
| `math.pi`, `math.e` | Mathematical constants |
| `random.random()` | Float between 0.0 and 1.0 |
| `random.randint(a, b)` | Integer between a and b |
| `random.choice(seq)` | Random item from sequence |
| `random.shuffle(lst)` | Shuffle list in place |
| `random.sample(seq, k)` | k unique random items |

### JSON (`json.py`)
| Function | Description |
|----------|-------------|
| `json.loads(string)` | Parse JSON string → Python object |
| `json.dumps(obj)` | Convert Python object → JSON string |
| `json.load(file)` | Read JSON from file object |
| `json.dump(obj, file)` | Write JSON to file object |

#### Python ↔ JSON Type Mapping
| Python | JSON |
|--------|------|
| `dict` | `{}` object |
| `list` | `[]` array |
| `str` | string |
| `int`, `float` | number |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

## How to Run
```bash
python generators.py
python dates.py
python math.py
python json.py
```
