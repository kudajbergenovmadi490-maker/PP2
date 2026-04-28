"""
read_files.py
=============
Practice 6 — File Handling
Demonstrates every way to READ files in Python.

Covers:
  - open() modes: 'r', 'rb'
  - read(), readline(), readlines()
  - Iterating line-by-line
  - Context manager: with statement
  - pathlib.Path for cross-platform paths
"""

from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# SETUP — create a sample file to read
# ─────────────────────────────────────────────────────────────────────────────

SAMPLE_FILE = Path("sample.txt")

SAMPLE_FILE.write_text(
    "Line 1: Python file handling\n"
    "Line 2: Reading files is easy\n"
    "Line 3: Use 'with' for safety\n"
    "Line 4: pathlib makes paths simple\n"
    "Line 5: Always close your files!\n",
    encoding="utf-8",
)
print(f"✅  Created '{SAMPLE_FILE}' for reading demos.\n")


# ─────────────────────────────────────────────────────────────────────────────
# 1. read()  — reads the ENTIRE file as one string
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 55)
print("1. read()  — entire file as a single string")
print("=" * 55)

with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
    content = f.read()

print(repr(content))          # show escape characters
print(f"\nCharacter count: {len(content)}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. readline()  — reads ONE line at a time
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("2. readline()  — one line per call")
print("=" * 55)

with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
    first  = f.readline()
    second = f.readline()

print(f"First  line : {first.rstrip()}")
print(f"Second line : {second.rstrip()}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. readlines()  — returns a LIST of all lines
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("3. readlines()  — all lines as a list")
print("=" * 55)

with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Type    : {type(lines)}")
print(f"Count   : {len(lines)} lines")
for i, line in enumerate(lines, 1):
    print(f"  [{i}] {line.rstrip()}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Iterate line-by-line  — most memory-efficient method
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("4. Iterate line-by-line (most memory-efficient)")
print("=" * 55)

with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        print(f"  Line {line_num}: {line.rstrip()}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. read(n)  — read only N characters
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("5. read(n)  — partial read (first 20 characters)")
print("=" * 55)

with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
    chunk = f.read(20)
    rest  = f.read(20)

print(f"First 20 chars : {repr(chunk)}")
print(f"Next  20 chars : {repr(rest)}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. pathlib  — modern cross-platform approach
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("6. pathlib.Path  — cross-platform file reading")
print("=" * 55)

p = Path(SAMPLE_FILE)
print(f"  Path object   : {p}")
print(f"  Absolute path : {p.resolve()}")
print(f"  File name     : {p.name}")
print(f"  Stem          : {p.stem}")
print(f"  Suffix        : {p.suffix}")
print(f"  Exists?       : {p.exists()}")
print(f"  Size (bytes)  : {p.stat().st_size}")
print(f"\n  Content via pathlib.read_text():")
print(p.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────────────────────────────────────
# 7. Binary mode  'rb'
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 55)
print("7. Binary mode 'rb'  — reads bytes")
print("=" * 55)

with open(SAMPLE_FILE, "rb") as f:
    raw_bytes = f.read(30)

print(f"First 30 bytes : {raw_bytes}")
print(f"Type           : {type(raw_bytes)}")


# ─────────────────────────────────────────────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────────────────────────────────────────────

SAMPLE_FILE.unlink()
print(f"\n🧹  Cleaned up '{SAMPLE_FILE}'.")
print("\n✅  read_files.py complete.")
