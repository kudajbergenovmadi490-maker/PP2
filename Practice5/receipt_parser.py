"""
receipt_parser.py
=================
Practice 5 — Python Regular Expressions
Parses a raw receipt text file and extracts structured data using the `re` module.

Demonstrates:
  - re.search()   → find the FIRST match of a pattern
  - re.findall()  → find ALL matches of a pattern
  - re.split()    → split a string by a pattern
  - re.sub()      → substitute / replace pattern occurrences
  - re.match()    → match a pattern at the START of a string
  - Metacharacters: . * + ? ^ $ [] | () \
  - Special sequences: \d \w \s \D \W \S
  - Quantifiers: {n}, {n,}, {n,m}
  - Flags: re.IGNORECASE, re.MULTILINE
"""

import re
import json


# ─────────────────────────────────────────────────────────────────────────────
# 0.  LOAD THE RAW FILE
# ─────────────────────────────────────────────────────────────────────────────

with open("raw.txt", "r", encoding="utf-8") as f:
    raw = f.read()

print("=" * 60)
print("RAW RECEIPT FILE LOADED")
print("=" * 60)
print(raw)


# ─────────────────────────────────────────────────────────────────────────────
# 1.  EXTRACT ALL PRICES  (re.findall)
# ─────────────────────────────────────────────────────────────────────────────
# Pattern breakdown:
#   \d+       → one or more digits (integer part)
#   \.        → literal dot (decimal separator)
#   \d{2}     → exactly two digits (cents)
#   -?        → optional leading minus sign (for discounts)

print("\n" + "=" * 60)
print("SECTION 1 — re.findall()  |  Extract ALL prices")
print("=" * 60)

price_pattern = r"-?\d+\.\d{2}"
all_prices_raw = re.findall(price_pattern, raw)
print(f"Raw price strings found : {all_prices_raw}")

# Convert to floats and filter meaningful values (ignore tiny noise)
all_prices = [float(p) for p in all_prices_raw]
print(f"Converted to floats     : {all_prices}")

# Demonstrate findall with a different pattern — find quantities (x1, x2, …)
qty_pattern = r"x\d+"
quantities = re.findall(qty_pattern, raw)
print(f"\nQuantities found (x\\d+) : {quantities}")


# ─────────────────────────────────────────────────────────────────────────────
# 2.  FIND PRODUCT NAMES  (re.findall with groups)
# ─────────────────────────────────────────────────────────────────────────────
# Each item line looks like:
#   "1. Whole Milk 1L              x2   480.00"
# Pattern:
#   ^\d+\.\s+   → line start, item number, dot, whitespace
#   ([A-Za-z].+?) → capture group: product name (starts with a letter)
#   \s{2,}      → two or more spaces separate name from quantity/price

print("\n" + "=" * 60)
print("SECTION 2 — re.findall() with groups  |  Product names")
print("=" * 60)

item_pattern = r"^\d+\.\s+([A-Za-z][^\n]+?)\s{2,}x\d+"
items = re.findall(item_pattern, raw, re.MULTILINE)
print("Product names extracted:")
for i, name in enumerate(items, 1):
    print(f"  {i:>2}. {name}")


# ─────────────────────────────────────────────────────────────────────────────
# 3.  EXTRACT ITEM DETAILS (name, qty, price) — re.findall with multiple groups
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("SECTION 3 — re.findall() multi-group  |  Full item rows")
print("=" * 60)

full_item_pattern = r"^\d+\.\s+([A-Za-z][^\n]+?)\s{2,}x(\d+)\s+([\d.]+)"
item_rows = re.findall(full_item_pattern, raw, re.MULTILINE)

print(f"{'#':<4} {'Product':<30} {'Qty':>4} {'Unit Price':>12} {'Line Total':>12}")
print("-" * 65)
parsed_items = []
for idx, (name, qty, price) in enumerate(item_rows, 1):
    qty_int   = int(qty)
    unit_price = float(price) / qty_int   # price shown is already the line total
    line_total = float(price)
    parsed_items.append({
        "name"      : name.strip(),
        "quantity"  : qty_int,
        "unit_price": round(unit_price, 2),
        "line_total": line_total,
    })
    print(f"{idx:<4} {name.strip():<30} {qty_int:>4} {unit_price:>12.2f} {line_total:>12.2f}")


# ─────────────────────────────────────────────────────────────────────────────
# 4.  CALCULATE TOTALS  (re.search for labelled amounts)
# ─────────────────────────────────────────────────────────────────────────────
# re.search() scans the whole string and returns the FIRST match object.

print("\n" + "=" * 60)
print("SECTION 4 — re.search()  |  Labelled financial figures")
print("=" * 60)

def extract_amount(label: str, text: str) -> float | None:
    """Search for a labelled amount, e.g. 'SUBTOTAL:   9830.00'."""
    # re.IGNORECASE so 'Subtotal' and 'SUBTOTAL' both match
    pattern = rf"{re.escape(label)}\s*:?\s*(-?[\d,]+\.\d{{2}})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return float(match.group(1).replace(",", ""))
    return None

subtotal = extract_amount("SUBTOTAL", raw)
discount = extract_amount("DISCOUNT", raw)
tax      = extract_amount("TAX",      raw)
total    = extract_amount("TOTAL",    raw)

print(f"  Subtotal : {subtotal:>10.2f}")
print(f"  Discount : {discount:>10.2f}")
print(f"  Tax      : {tax:>10.2f}")
print(f"  TOTAL    : {total:>10.2f}")

# Verify calculated total
calc_total = round((subtotal or 0) + (discount or 0) + (tax or 0), 2)
print(f"\n  Cross-check (subtotal + discount + tax) = {calc_total:.2f}")
print(f"  Matches receipt total? {'✅ YES' if calc_total == total else '❌ NO'}")


# ─────────────────────────────────────────────────────────────────────────────
# 5.  DATE & TIME  (re.search)
# ─────────────────────────────────────────────────────────────────────────────
# Date pattern: DD/MM/YYYY
#   \d{2}\/\d{2}\/\d{4}
# Time pattern: HH:MM:SS
#   \d{2}:\d{2}:\d{2}

print("\n" + "=" * 60)
print("SECTION 5 — re.search()  |  Date and Time")
print("=" * 60)

date_match = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", raw)
time_match = re.search(r"\b(\d{2}:\d{2}:\d{2})\b", raw)

receipt_date = date_match.group(1) if date_match else "NOT FOUND"
receipt_time = time_match.group(1) if time_match else "NOT FOUND"
print(f"  Date : {receipt_date}")
print(f"  Time : {receipt_time}")


# ─────────────────────────────────────────────────────────────────────────────
# 6.  PAYMENT METHOD  (re.search + re.IGNORECASE flag)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("SECTION 6 — re.search() + re.IGNORECASE  |  Payment info")
print("=" * 60)

pay_match  = re.search(r"Payment Method:\s*(.+)", raw, re.IGNORECASE)
card_match = re.search(r"Card Number:\s*(.+)",    raw, re.IGNORECASE)
auth_match = re.search(r"Authorization:\s*(.+)",  raw, re.IGNORECASE)

payment_method = pay_match.group(1).strip()  if pay_match  else "N/A"
card_number    = card_match.group(1).strip() if card_match else "N/A"
auth_code      = auth_match.group(1).strip() if auth_match else "N/A"

print(f"  Payment Method : {payment_method}")
print(f"  Card Number    : {card_number}")
print(f"  Authorization  : {auth_code}")


# ─────────────────────────────────────────────────────────────────────────────
# 7.  STORE INFO & RECEIPT NUMBER  (re.search / re.findall)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("SECTION 7 — re.search()  |  Store and Receipt metadata")
print("=" * 60)

# Phone: +7 (727) 123-45-67  → international format
phone_match   = re.search(r"Tel:\s*(\+[\d\s\(\)\-]+)", raw)
receipt_match = re.search(r"RECEIPT\s*#\s*:\s*(\d+)", raw, re.IGNORECASE)
cashier_match = re.search(r"Cashier:\s*([A-Za-z\s.]+?)\s{2,}", raw)
points_match  = re.search(r"Total Loyalty Points:\s*(\d+)", raw, re.IGNORECASE)

print(f"  Phone           : {phone_match.group(1).strip()  if phone_match   else 'N/A'}")
print(f"  Receipt #       : {receipt_match.group(1)        if receipt_match else 'N/A'}")
print(f"  Cashier         : {cashier_match.group(1).strip() if cashier_match else 'N/A'}")
print(f"  Loyalty Points  : {points_match.group(1)         if points_match  else 'N/A'}")


# ─────────────────────────────────────────────────────────────────────────────
# 8.  re.split()  — Split the receipt into sections
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("SECTION 8 — re.split()  |  Split receipt into sections")
print("=" * 60)

# Split wherever there is a line of dashes (------ …) or equals (====== …)
sections = re.split(r"[-=]{6,}\n", raw)
sections = [s.strip() for s in sections if s.strip()]
print(f"Number of sections found: {len(sections)}\n")
for i, sec in enumerate(sections, 1):
    preview = sec[:60].replace("\n", " | ")
    print(f"  Section {i}: {preview} …")

# Split a single line by whitespace (classic tokenising example)
sample_line = "Whole Milk 1L              x2   480.00"
tokens = re.split(r"\s{2,}", sample_line)   # split on 2+ spaces
print(f"\n  Tokenising sample line by \\s{{2,}}:")
print(f"  Input  : {repr(sample_line)}")
print(f"  Tokens : {tokens}")


# ─────────────────────────────────────────────────────────────────────────────
# 9.  re.sub()  — Clean / redact / transform text
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("SECTION 9 — re.sub()  |  Text substitution examples")
print("=" * 60)

# 9a. Redact the card number digits that are shown
redacted = re.sub(r"\*{4}", "[REDACTED]", raw)
card_line_match = re.search(r"Card Number:.+", redacted)
print(f"  Redacted card line : {card_line_match.group() if card_line_match else 'N/A'}")

# 9b. Normalise all prices to use a comma decimal separator (EU style)
eu_style = re.sub(r"(\d)\.(\d{2})\b", r"\1,\2", raw)
price_lines = re.findall(r"TOTAL.+", eu_style, re.IGNORECASE)
print(f"  EU-style totals    : {price_lines}")

# 9c. Remove all separator lines (====…  or ----…) to get clean content
clean = re.sub(r"^[-=]{4,}\s*$", "", raw, flags=re.MULTILINE)
clean = re.sub(r"\n{3,}", "\n\n", clean)   # collapse multiple blank lines
line_count_before = raw.count("\n")
line_count_after  = clean.count("\n")
print(f"  Lines before cleanup : {line_count_before}")
print(f"  Lines after cleanup  : {line_count_after}")


# ─────────────────────────────────────────────────────────────────────────────
# 10.  re.match()  — Match at the BEGINNING of a string
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("SECTION 10 — re.match()  |  Match at string start")
print("=" * 60)

test_strings = [
    "480.00 — this is a price at the start",
    "Whole Milk 1L              x2   480.00",
    "25/04/2025 is a date at the start",
    "x3 quantity at the start",
]
pattern = r"\d{2}/\d{2}/\d{4}"   # date pattern
print(f"  Pattern: r'{pattern}'")
for s in test_strings:
    m = re.match(pattern, s)
    print(f"  {'MATCH  ' if m else 'no match'} ← \"{s[:50]}\"")


# ─────────────────────────────────────────────────────────────────────────────
# 11.  METACHARACTERS & SPECIAL SEQUENCES  — Quick reference demos
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("SECTION 11 — Metacharacters & Special Sequences demo")
print("=" * 60)

demos = [
    (r"\d+",        "One or more digits",          "Price: 9830.00"),
    (r"\D+",        "One or more NON-digits",      "Price: 9830.00"),
    (r"\w+",        "Word characters [a-zA-Z0-9_]","Fresh Mart 2025"),
    (r"\W+",        "NON-word characters",          "Fresh Mart 2025"),
    (r"\s+",        "Whitespace",                   "  TOTAL:  10458.40  "),
    (r"\S+",        "NON-whitespace",               "  TOTAL:  10458.40  "),
    (r"^\w+",       "Word at line START (^)",       "RECEIPT #: 00847261"),
    (r"\d{4}$",     "4 digits at line END ($)",     "Card: **** 7842"),
    (r"[A-Z]{2,}",  "2+ uppercase letters",         "TOTAL DISCOUNT TAX"),
    (r"(CARD|CASH)", "CARD or CASH  ( | )",         "Payment Method: KASPI CARD"),
    (r"\bMilk\b",   "Word boundary \\b",            "Whole Milk 1L — Milky Way"),
]

for pat, desc, text in demos:
    found = re.findall(pat, text, re.IGNORECASE)
    print(f"  Pattern {pat!r:<20} | {desc:<35} | found: {found}")


# ─────────────────────────────────────────────────────────────────────────────
# 12.  QUANTIFIERS — {n}, {n,}, {n,m}
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("SECTION 12 — Quantifiers  {n}, {n,}, {n,m}")
print("=" * 60)

sample = "1 12 123 1234 12345 123456"
for pat in [r"\d{3}", r"\d{3,}", r"\d{3,5}"]:
    found = re.findall(pat, sample)
    print(f"  r'{pat}'  →  {found}")


# ─────────────────────────────────────────────────────────────────────────────
# 13.  STRUCTURED OUTPUT — JSON
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("SECTION 13 — Structured JSON output")
print("=" * 60)

receipt_json = {
    "store": {
        "name"   : "SUPERMARKET FRESH MART",
        "address": "123 Main Street, Almaty",
        "phone"  : phone_match.group(1).strip() if phone_match else None,
        "website": "www.freshmart.kz",
    },
    "transaction": {
        "receipt_number": receipt_match.group(1)         if receipt_match else None,
        "date"          : receipt_date,
        "time"          : receipt_time,
        "cashier"       : cashier_match.group(1).strip() if cashier_match else None,
    },
    "items": parsed_items,
    "financials": {
        "subtotal"     : subtotal,
        "discount"     : discount,
        "tax"          : tax,
        "total"        : total,
    },
    "payment": {
        "method"       : payment_method,
        "card_number"  : card_number,
        "authorization": auth_code,
    },
    "loyalty": {
        "points_earned": int(re.search(r"Points Earned:\s*(\d+)", raw).group(1)),
        "points_total" : int(points_match.group(1)) if points_match else None,
    },
}

print(json.dumps(receipt_json, indent=4, ensure_ascii=False))

# Save JSON to file
with open("parsed_receipt.json", "w", encoding="utf-8") as jf:
    json.dump(receipt_json, jf, indent=4, ensure_ascii=False)
print("\n✅  Parsed receipt saved to parsed_receipt.json")


# ─────────────────────────────────────────────────────────────────────────────
# 14.  SUMMARY TABLE
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("SUMMARY — Functions used in this script")
print("=" * 60)
summary = [
    ("re.findall()",  "Extracted all prices, quantities, product names"),
    ("re.search()",   "Found date, time, totals, payment info, store data"),
    ("re.split()",    "Split receipt into sections; tokenised item lines"),
    ("re.sub()",      "Redacted card number; EU-style prices; cleaned text"),
    ("re.match()",    "Tested whether strings START with a specific pattern"),
    ("re.MULTILINE",  "Enabled ^ / $ to match per-line in findall calls"),
    ("re.IGNORECASE", "Case-insensitive search for labels like 'total'"),
    ("Groups ()",     "Captured named sub-patterns inside larger patterns"),
    ("\\d \\w \\s",    "Digit / word-char / whitespace special sequences"),
    ("{n,m}",         "Matched exact / minimum / ranged character counts"),
]
for fn, desc in summary:
    print(f"  {fn:<20} {desc}")

print("\n" + "=" * 60)
print("Practice 5 — receipt_parser.py  complete ✅")
print("=" * 60)
