"""
move_files.py
=============
Practice 6 — Directory Management
Demonstrates moving and organising files between directories.

Covers:
  - shutil.move()
  - Bulk file organisation by extension
  - Renaming files with os.rename() and Path.rename()
  - Walking a directory tree with os.walk()
"""

import os
import shutil
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# SETUP — create a messy download folder to organise
# ─────────────────────────────────────────────────────────────────────────────

BASE      = Path("organiser_demo")
DOWNLOADS = BASE / "downloads"
DOWNLOADS.mkdir(parents=True, exist_ok=True)

messy_files = {
    "report_2025.pdf"    : "PDF content",
    "holiday_photo.jpg"  : "JPEG content",
    "budget.xlsx"        : "Excel content",
    "notes.txt"          : "Text content",
    "presentation.pptx"  : "PPT content",
    "beach.png"          : "PNG content",
    "invoice_001.pdf"    : "PDF content",
    "code_snippet.py"    : "Python code",
    "music.mp3"          : "Audio content",
    "lecture.mp4"        : "Video content",
    "archive.zip"        : "ZIP content",
    "data.csv"           : "CSV content",
}

for name, content in messy_files.items():
    (DOWNLOADS / name).write_text(content, encoding="utf-8")

print(f"✅  Created {len(messy_files)} mixed files in '{DOWNLOADS}'")
print(f"  Files: {sorted(f.name for f in DOWNLOADS.iterdir())}\n")


# ─────────────────────────────────────────────────────────────────────────────
# 1. shutil.move()  — move a single file
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 55)
print("1. shutil.move()  — move a single file")
print("=" * 55)

docs_dir = BASE / "documents"
docs_dir.mkdir(exist_ok=True)

src  = DOWNLOADS / "notes.txt"
dest = docs_dir / "notes.txt"
shutil.move(str(src), str(dest))

print(f"  Moved: {src.name}")
print(f"  From : {src.parent}")
print(f"  To   : {dest.parent}")
print(f"  Still in downloads? {src.exists()}")
print(f"  In documents?       {dest.exists()}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Bulk organise by file extension
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("2. Bulk file organiser by extension")
print("=" * 55)

EXTENSION_MAP = {
    ".pdf"  : "Documents/PDFs",
    ".docx" : "Documents/Word",
    ".xlsx" : "Documents/Excel",
    ".pptx" : "Documents/PowerPoint",
    ".csv"  : "Documents/Data",
    ".txt"  : "Documents/Text",
    ".jpg"  : "Media/Images",
    ".jpeg" : "Media/Images",
    ".png"  : "Media/Images",
    ".mp3"  : "Media/Audio",
    ".mp4"  : "Media/Video",
    ".py"   : "Code/Python",
    ".zip"  : "Archives",
}

organised = BASE / "organised"
moved_count = 0
skipped = []

for file in list(DOWNLOADS.iterdir()):
    if not file.is_file():
        continue
    ext = file.suffix.lower()
    folder_name = EXTENSION_MAP.get(ext, "Other")
    target_dir  = organised / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file), str(target_dir / file.name))
    moved_count += 1
    print(f"  {file.name:<25} → {folder_name}/")

print(f"\n  Total files moved: {moved_count}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. os.walk()  — walk the entire organised tree
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("3. os.walk()  — walk organised directory tree")
print("=" * 55)

for root, dirs, files in os.walk(organised):
    depth = Path(root).relative_to(organised).parts
    indent = "  " * len(depth)
    print(f"{indent}📁 {Path(root).name}/")
    for file in files:
        print(f"{indent}  📄 {file}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. os.rename()  — rename a file in-place
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("4. os.rename() and Path.rename()  — rename files")
print("=" * 55)

pdf_dir  = organised / "Documents" / "PDFs"
old_name = pdf_dir / "report_2025.pdf"
new_name = pdf_dir / "annual_report_2025.pdf"

if old_name.exists():
    os.rename(old_name, new_name)
    print(f"  os.rename(): '{old_name.name}' → '{new_name.name}'")

# pathlib rename — also works cross-folder on same filesystem
invoice  = pdf_dir / "invoice_001.pdf"
renamed  = pdf_dir / "invoice_PAID_001.pdf"
if invoice.exists():
    invoice.rename(renamed)
    print(f"  Path.rename(): '{invoice.name}' → '{renamed.name}'")

print(f"  PDFs now: {[f.name for f in pdf_dir.iterdir()]}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. Batch rename  — add a prefix to all images
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("5. Batch rename  — prefix all images with '2025_'")
print("=" * 55)

images_dir = organised / "Media" / "Images"
for img in list(images_dir.iterdir()):
    if img.is_file() and not img.name.startswith("2025_"):
        new = img.parent / f"2025_{img.name}"
        img.rename(new)
        print(f"  Renamed: {img.name} → {new.name}")


# ─────────────────────────────────────────────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────────────────────────────────────────────

shutil.rmtree(BASE)
print(f"\n🧹  Removed demo workspace '{BASE}'.")
print("\n✅  move_files.py complete.")
