# Practice 6 — Python File Handling and Built-in Functions

## Overview
Hands-on coverage of file I/O, directory management, and Python's core built-in functions.

## Repository Structure
```
Practice6/
├── file_handling/
│   ├── read_files.py          # read(), readline(), readlines(), pathlib
│   ├── write_files.py         # 'w', 'a', 'x' modes, writelines()
│   └── copy_delete_files.py   # shutil.copy/move/rmtree, safe deletion
├── directory_management/
│   ├── create_list_dirs.py    # mkdir, makedirs, listdir, os.walk, rglob
│   └── move_files.py          # bulk organiser, rename, batch rename
├── builtin_functions/
│   ├── map_filter_reduce.py   # map, filter, reduce, sorted, type conversion
│   └── enumerate_zip_examples.py  # enumerate, zip, zip_longest, any, all
└── README.md
```

## How to Run
```bash
# Run any script from inside its own folder:
cd file_handling
python read_files.py

cd ../directory_management
python create_list_dirs.py

cd ../builtin_functions
python map_filter_reduce.py
```
Requires Python 3.8+. No third-party packages needed.

## Topics Covered

### File Handling (`file_handling/`)
| Script | Concepts |
|---|---|
| `read_files.py` | `read()`, `readline()`, `readlines()`, line iteration, `pathlib.Path`, binary mode |
| `write_files.py` | Modes `w` `a` `x`, `write()`, `writelines()`, CSV output, `write_text()` |
| `copy_delete_files.py` | `shutil.copy/copy2/copyfile/move/copytree/rmtree`, `os.remove()`, `Path.unlink()`, timestamped backups |

### Directory Management (`directory_management/`)
| Script | Concepts |
|---|---|
| `create_list_dirs.py` | `os.mkdir/makedirs/listdir/getcwd/chdir/rmdir`, `Path.iterdir/rglob/glob`, find by extension, `os.path` utilities |
| `move_files.py` | `shutil.move()`, bulk file organiser by extension, `os.walk()`, `os.rename()`, batch rename |

### Built-in Functions (`builtin_functions/`)
| Script | Concepts |
|---|---|
| `map_filter_reduce.py` | `map()`, `filter()`, `reduce()`, `lambda`, `len/sum/min/max/abs/round()`, type conversion, `sorted()` |
| `enumerate_zip_examples.py` | `enumerate()`, `zip()`, `zip_longest()`, `dict(zip())`, unzipping, `any()`, `all()`, `isinstance()`, `type()` |

## Key Patterns to Remember

```python
# Read a file safely
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Write a file
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(["line1\n", "line2\n"])

# Append without overwriting
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("new entry\n")

# Create nested directories
from pathlib import Path
Path("a/b/c").mkdir(parents=True, exist_ok=True)

# Find all .py files recursively
py_files = list(Path(".").rglob("*.py"))

# map + filter + reduce pipeline
from functools import reduce
result = reduce(lambda a, b: a + b,
                filter(lambda x: x > 0,
                       map(lambda x: x * 2, [-1, 2, -3, 4])))

# enumerate + zip together
for i, (name, score) in enumerate(zip(names, scores), 1):
    print(f"{i}. {name}: {score}")
```

## Commit
```bash
git add .
git commit -m "Add Practice6 - file handling and built-in functions examples"
git push origin main
```
