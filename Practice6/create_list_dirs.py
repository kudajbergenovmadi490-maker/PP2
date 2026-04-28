"""
create_list_dirs.py
===================
Practice 6 — Directory Management
Demonstrates creating, navigating, inspecting, and removing directories.

Covers:
  - os.mkdir(), os.makedirs()
  - os.listdir(), os.getcwd(), os.chdir()
  - os.rmdir(), shutil.rmtree()
  - pathlib.Path: mkdir(), iterdir(), rglob(), glob()
  - Finding files by extension
"""

import os
import shutil
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────────────────────────────────────────

BASE = Path("dir_demo")
if BASE.exists():
    shutil.rmtree(BASE)   # clean start

# ─────────────────────────────────────────────────────────────────────────────
# 1. os.mkdir()  — create a SINGLE directory
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 55)
print("1. os.mkdir()  — single directory")
print("=" * 55)

os.mkdir(BASE)
print(f"  Created       : {BASE}")
print(f"  Exists?       : {BASE.exists()}")
print(f"  Is directory? : {BASE.is_dir()}")

# Trying to create it again raises FileExistsError
try:
    os.mkdir(BASE)
except FileExistsError as e:
    print(f"  Expected error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. os.makedirs()  — create NESTED directories in one call
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("2. os.makedirs()  — nested directories")
print("=" * 55)

nested = BASE / "projects" / "python" / "practice6"
os.makedirs(nested, exist_ok=True)   # exist_ok=True avoids error if exists
print(f"  Created nested path: {nested}")

# pathlib equivalent
docs_path = BASE / "docs" / "api" / "v1"
docs_path.mkdir(parents=True, exist_ok=True)
print(f"  Created via pathlib: {docs_path}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Populate with sample files
# ─────────────────────────────────────────────────────────────────────────────

sample_files = {
    BASE / "README.md"                          : "# Project README\n",
    BASE / "projects" / "python" / "main.py"    : "print('Hello')\n",
    BASE / "projects" / "python" / "utils.py"   : "def helper(): pass\n",
    BASE / "projects" / "python" / "data.csv"   : "id,name\n1,Alice\n",
    BASE / "projects" / "python" / "practice6" / "notes.txt": "Practice notes\n",
    BASE / "docs" / "api" / "v1" / "index.html" : "<html></html>\n",
    BASE / "docs" / "api" / "v1" / "style.css"  : "body {}\n",
    BASE / "docs" / "changelog.txt"             : "v1.0 - initial\n",
}
for path, text in sample_files.items():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
print(f"\n  Created {len(sample_files)} sample files.")


# ─────────────────────────────────────────────────────────────────────────────
# 4. os.getcwd() and os.chdir()  — current working directory
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("4. os.getcwd() and os.chdir()")
print("=" * 55)

original_cwd = os.getcwd()
print(f"  CWD before chdir : {original_cwd}")

os.chdir(BASE)
print(f"  CWD after chdir  : {os.getcwd()}")

os.chdir(original_cwd)       # always restore!
print(f"  CWD restored to  : {os.getcwd()}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. os.listdir()  — list contents of a directory
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("5. os.listdir()  — list directory contents")
print("=" * 55)

entries = os.listdir(BASE)
print(f"  Contents of '{BASE}': {entries}")

# Separate files and directories
files = [e for e in entries if (BASE / e).is_file()]
dirs  = [e for e in entries if (BASE / e).is_dir()]
print(f"  Files : {files}")
print(f"  Dirs  : {dirs}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. pathlib iterdir()  — iterate directory contents
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("6. pathlib iterdir()  — iterate contents")
print("=" * 55)

print(f"  Direct children of '{BASE}':")
for item in sorted(BASE.iterdir()):
    kind = "DIR " if item.is_dir() else "FILE"
    print(f"    [{kind}] {item.name}")


# ─────────────────────────────────────────────────────────────────────────────
# 7. pathlib rglob()  — recursive search (all files)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("7. pathlib rglob('*')  — all files recursively")
print("=" * 55)

all_files = sorted(p for p in BASE.rglob("*") if p.is_file())
print(f"  Total files found: {len(all_files)}")
for f in all_files:
    print(f"    {f.relative_to(BASE)}")


# ─────────────────────────────────────────────────────────────────────────────
# 8. Find files by extension
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("8. Find files by extension")
print("=" * 55)

for ext in (".py", ".txt", ".csv", ".html", ".css", ".md"):
    matches = list(BASE.rglob(f"*{ext}"))
    print(f"  {ext:6}  →  {[f.name for f in matches]}")


# ─────────────────────────────────────────────────────────────────────────────
# 9. os.path utilities
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("9. os.path  — path utilities")
print("=" * 55)

sample = str(BASE / "projects" / "python" / "main.py")
print(f"  Path          : {sample}")
print(f"  basename      : {os.path.basename(sample)}")
print(f"  dirname       : {os.path.dirname(sample)}")
print(f"  splitext      : {os.path.splitext(sample)}")
print(f"  isfile        : {os.path.isfile(sample)}")
print(f"  isdir         : {os.path.isdir(sample)}")
print(f"  getsize       : {os.path.getsize(sample)} bytes")
print(f"  join example  : {os.path.join('dir', 'sub', 'file.txt')}")


# ─────────────────────────────────────────────────────────────────────────────
# 10. os.rmdir() and shutil.rmtree()
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("10. Removing directories")
print("=" * 55)

empty_dir = BASE / "empty_dir"
empty_dir.mkdir()
os.rmdir(empty_dir)           # only works on EMPTY directories
print(f"  os.rmdir() removed empty dir:  exists={empty_dir.exists()}")

# Trying to rmdir a non-empty directory raises OSError
try:
    os.rmdir(BASE / "projects")
except OSError as e:
    print(f"  os.rmdir() on non-empty dir: {type(e).__name__}")

# shutil.rmtree — remove directory and ALL contents
shutil.rmtree(BASE)
print(f"  shutil.rmtree() removed '{BASE}': exists={BASE.exists()}")


print("\n✅  create_list_dirs.py complete.")
