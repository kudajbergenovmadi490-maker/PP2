"""
write_files.py
==============
Practice 6 — File Handling
Demonstrates writing and appending to files in Python.

Covers:
  - open() modes: 'w' (write), 'a' (append), 'x' (exclusive create)
  - write(), writelines()
  - Context manager (with statement)
  - pathlib.Path.write_text()
  - Verifying file contents after write
"""

from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Mode 'w'  — write (creates or OVERWRITES the file)
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 55)
print("1. Mode 'w'  — write (create / overwrite)")
print("=" * 55)

notes_file = OUTPUT_DIR / "notes.txt"

with open(notes_file, "w", encoding="utf-8") as f:
    f.write("=== My Study Notes ===\n")
    f.write("Topic: Python File Handling\n")
    f.write("Date: 2025-04-25\n")

print(f"  Written to: {notes_file}")
print(f"  Content:\n{notes_file.read_text(encoding='utf-8')}")

# Overwrite demo — 'w' wipes previous content
with open(notes_file, "w", encoding="utf-8") as f:
    f.write("=== Overwritten Content ===\n")
    f.write("The previous text is gone.\n")

print(f"  After overwrite:\n{notes_file.read_text(encoding='utf-8')}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. writelines()  — write a list of strings at once
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 55)
print("2. writelines()  — write a list of lines")
print("=" * 55)

shopping_file = OUTPUT_DIR / "shopping_list.txt"
items = [
    "1. Milk\n",
    "2. Eggs\n",
    "3. Bread\n",
    "4. Butter\n",
    "5. Cheese\n",
]

with open(shopping_file, "w", encoding="utf-8") as f:
    f.writelines(items)

print(f"  Written {len(items)} items to: {shopping_file}")
print(f"  Content:\n{shopping_file.read_text(encoding='utf-8')}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Mode 'a'  — append (adds to end, never overwrites)
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 55)
print("3. Mode 'a'  — append")
print("=" * 55)

log_file = OUTPUT_DIR / "app.log"

# First write
with open(log_file, "w", encoding="utf-8") as f:
    f.write("[2025-04-25 08:00:00] Application started\n")

# Append entries
log_entries = [
    "[2025-04-25 08:01:15] User logged in\n",
    "[2025-04-25 08:05:43] File uploaded\n",
    "[2025-04-25 08:10:02] User logged out\n",
]

for entry in log_entries:
    with open(log_file, "a", encoding="utf-8") as f:   # opens fresh each time
        f.write(entry)

print(f"  Log file content ({log_file}):")
for line in log_file.read_text(encoding="utf-8").splitlines():
    print(f"  | {line}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Mode 'x'  — exclusive create (fails if file exists)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("4. Mode 'x'  — exclusive create (error if exists)")
print("=" * 55)

new_file = OUTPUT_DIR / "new_file.txt"
new_file.unlink(missing_ok=True)   # ensure it doesn't exist

try:
    with open(new_file, "x", encoding="utf-8") as f:
        f.write("Created fresh with mode 'x'.\n")
    print(f"  ✅  Created: {new_file}")
except FileExistsError:
    print(f"  ❌  '{new_file}' already exists — 'x' mode refused.")

# Try again → should raise FileExistsError
try:
    with open(new_file, "x", encoding="utf-8") as f:
        f.write("This should fail.\n")
except FileExistsError as e:
    print(f"  ❌  Second attempt raised: {type(e).__name__}: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. pathlib shorthand — write_text() and read_text()
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("5. pathlib.write_text() / read_text()")
print("=" * 55)

config_file = OUTPUT_DIR / "config.txt"
config_file.write_text(
    "[settings]\n"
    "theme = dark\n"
    "language = en\n"
    "font_size = 14\n",
    encoding="utf-8",
)
print(f"  Written via write_text(): {config_file}")
print(f"  Read back via read_text():\n{config_file.read_text(encoding='utf-8')}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. Writing structured data  — CSV-style
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 55)
print("6. Writing structured CSV-style data")
print("=" * 55)

students = [
    ("Alice",   92, "A"),
    ("Bob",     78, "B"),
    ("Charlie", 85, "B+"),
    ("Diana",   96, "A+"),
    ("Evan",    61, "D"),
]

csv_file = OUTPUT_DIR / "students.csv"

with open(csv_file, "w", encoding="utf-8") as f:
    f.write("name,score,grade\n")           # header
    for name, score, grade in students:
        f.write(f"{name},{score},{grade}\n")

print(f"  CSV written to: {csv_file}")
print(f"  Content:\n{csv_file.read_text(encoding='utf-8')}")


# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY — File modes cheat sheet
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 55)
print("SUMMARY — File mode cheat sheet")
print("=" * 55)
modes = [
    ("r",  "Read only (default). Error if file missing."),
    ("w",  "Write. Creates file; OVERWRITES if exists."),
    ("a",  "Append. Creates file; adds to end if exists."),
    ("x",  "Exclusive create. Error if file already exists."),
    ("rb", "Read binary (images, PDFs, etc.)."),
    ("wb", "Write binary."),
    ("r+", "Read AND write (file must exist)."),
    ("w+", "Write AND read (overwrites existing)."),
]
for mode, desc in modes:
    print(f"  {mode!r:<6}  {desc}")

print("\n✅  write_files.py complete.")
