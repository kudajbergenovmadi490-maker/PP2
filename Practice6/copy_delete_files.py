"""
copy_delete_files.py
====================
Practice 6 — File Handling
Demonstrates copying, backing up, and safely deleting files using
os, shutil, and pathlib.

Covers:
  - shutil.copy(), shutil.copy2(), shutil.copyfile()
  - shutil.move()
  - os.remove() / Path.unlink()
  - Safe deletion with existence checks
  - Automated backup with timestamps
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# SETUP — working directories and a sample file
# ─────────────────────────────────────────────────────────────────────────────

BASE    = Path("demo_workspace")
SRC_DIR = BASE / "source"
DST_DIR = BASE / "destination"
BAK_DIR = BASE / "backups"

for d in (SRC_DIR, DST_DIR, BAK_DIR):
    d.mkdir(parents=True, exist_ok=True)

original = SRC_DIR / "report.txt"
original.write_text(
    "Monthly Sales Report\n"
    "====================\n"
    "Q1: 120,000\n"
    "Q2: 135,000\n"
    "Q3: 142,000\n"
    "Q4: 158,000\n"
    f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}\n",
    encoding="utf-8",
)
print(f"✅  Setup complete. Working directory: {BASE.resolve()}\n")


# ─────────────────────────────────────────────────────────────────────────────
# 1. shutil.copyfile()  — content only, no metadata
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 55)
print("1. shutil.copyfile()  — content only")
print("=" * 55)

dest1 = DST_DIR / "report_copyfile.txt"
shutil.copyfile(original, dest1)
print(f"  Source      : {original}")
print(f"  Destination : {dest1}")
print(f"  Exists?     : {dest1.exists()}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. shutil.copy()  — content + permissions
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("2. shutil.copy()  — content + permissions")
print("=" * 55)

dest2 = DST_DIR / "report_copy.txt"
shutil.copy(original, dest2)
print(f"  Copied to   : {dest2}")
print(f"  Permissions : {oct(dest2.stat().st_mode)}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. shutil.copy2()  — content + permissions + timestamps
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("3. shutil.copy2()  — content + permissions + timestamps")
print("=" * 55)

dest3 = DST_DIR / "report_copy2.txt"
shutil.copy2(original, dest3)
src_mtime = datetime.fromtimestamp(original.stat().st_mtime)
dst_mtime = datetime.fromtimestamp(dest3.stat().st_mtime)
print(f"  Copied to       : {dest3}")
print(f"  Source mtime    : {src_mtime:%Y-%m-%d %H:%M:%S}")
print(f"  Dest mtime      : {dst_mtime:%Y-%m-%d %H:%M:%S}")
print(f"  Timestamps match: {abs((src_mtime - dst_mtime).total_seconds()) < 2}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Automated backup with timestamp in filename
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("4. Automated timestamped backup")
print("=" * 55)

def backup_file(src: Path, backup_dir: Path) -> Path:
    """Copy src to backup_dir with a timestamp suffix."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{src.stem}_{timestamp}{src.suffix}"
    dest = backup_dir / backup_name
    shutil.copy2(src, dest)
    return dest

backup_path = backup_file(original, BAK_DIR)
print(f"  Original : {original}")
print(f"  Backup   : {backup_path}")
print(f"  All backups in '{BAK_DIR}':")
for f in BAK_DIR.iterdir():
    print(f"    {f.name}  ({f.stat().st_size} bytes)")


# ─────────────────────────────────────────────────────────────────────────────
# 5. shutil.move()  — move (rename) a file
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("5. shutil.move()  — move / rename a file")
print("=" * 55)

temp_file = SRC_DIR / "temp_data.txt"
temp_file.write_text("Temporary data.\n", encoding="utf-8")

moved_file = DST_DIR / "moved_data.txt"
shutil.move(str(temp_file), str(moved_file))

print(f"  Source exists after move : {temp_file.exists()}")    # False
print(f"  Dest   exists after move : {moved_file.exists()}")   # True


# ─────────────────────────────────────────────────────────────────────────────
# 6. Safe file deletion  — os.remove() and Path.unlink()
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("6. Safe file deletion")
print("=" * 55)

# Method A — os.remove() with existence check
target_a = DST_DIR / "report_copyfile.txt"
if os.path.exists(target_a):
    os.remove(target_a)
    print(f"  ✅  os.remove()  deleted: {target_a.name}")
else:
    print(f"  ⚠️   '{target_a.name}' not found — skipped.")

# Method B — Path.unlink(missing_ok=True)  (Python 3.8+)
target_b = DST_DIR / "report_copy.txt"
target_b.unlink(missing_ok=True)
print(f"  ✅  unlink(missing_ok=True) deleted: {target_b.name}")

# Method C — try/except for fine-grained error handling
target_c = DST_DIR / "does_not_exist.txt"
try:
    os.remove(target_c)
except FileNotFoundError:
    print(f"  ⚠️   '{target_c.name}' not found — caught FileNotFoundError.")
except PermissionError:
    print(f"  ❌  Permission denied deleting '{target_c.name}'.")


# ─────────────────────────────────────────────────────────────────────────────
# 7. Copy and delete an entire directory  — shutil.copytree / rmtree
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("7. Copy & delete entire directory tree")
print("=" * 55)

tree_src = BASE / "tree_source"
tree_src.mkdir(exist_ok=True)
(tree_src / "a.txt").write_text("A", encoding="utf-8")
(tree_src / "b.txt").write_text("B", encoding="utf-8")
sub = tree_src / "subdir"
sub.mkdir(exist_ok=True)
(sub / "c.txt").write_text("C", encoding="utf-8")

tree_dst = BASE / "tree_copy"
if tree_dst.exists():
    shutil.rmtree(tree_dst)

shutil.copytree(tree_src, tree_dst)
print(f"  Copied '{tree_src}' → '{tree_dst}'")
print(f"  Files in copy: {[str(p.relative_to(tree_dst)) for p in tree_dst.rglob('*') if p.is_file()]}")

shutil.rmtree(tree_src)
print(f"  Deleted source tree '{tree_src}': exists={tree_src.exists()}")


# ─────────────────────────────────────────────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────────────────────────────────────────────

shutil.rmtree(BASE)
print(f"\n🧹  Cleaned up entire '{BASE}' workspace.")
print("\n✅  copy_delete_files.py complete.")
