"""
Practice 8 – PhoneBook with PostgreSQL Functions & Stored Procedures
"""

import psycopg2
from connect import get_connection


# ── helpers ──────────────────────────────────────────────────

def print_rows(rows: list) -> None:
    if not rows:
        print("  (no records)")
        return
    print(f"\n  {'ID':<5} {'First Name':<20} {'Phone'}")
    print("  " + "-" * 42)
    for r in rows:
        print(f"  {r[0]:<5} {r[1]:<20} {r[2]}")
    print(f"\n  {len(rows)} record(s).")


# ── 1. Pattern search (calls function) ───────────────────────

def search_by_pattern() -> None:
    pattern = input("Enter search pattern (name or phone): ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
            print_rows(cur.fetchall())


# ── 2. Upsert single contact (calls procedure) ───────────────

def upsert_contact() -> None:
    name  = input("First name: ").strip()
    phone = input("Phone (+7XXXXXXXXXX): ").strip()
    if not name or not phone:
        print("Name and phone cannot be empty.")
        return
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
    print("Done.")


# ── 3. Bulk insert with validation (calls procedure) ─────────

def bulk_insert() -> None:
    print("Enter contacts one per line as  name,phone")
    print("Type END on a blank line to finish.\n")
    names, phones = [], []
    while True:
        line = input("  > ").strip()
        if line.upper() == "END" or line == "":
            break
        parts = line.split(",", 1)
        if len(parts) != 2:
            print("  Bad format, skipping:", line)
            continue
        names.append(parts[0].strip())
        phones.append(parts[1].strip())

    if not names:
        print("Nothing to insert.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL bulk_insert_contacts(%s::varchar[], %s::varchar[]);",
                (names, phones)
            )
            # Read invalid rows from temp table (same session / connection)
            cur.execute("SELECT first_name, phone, reason FROM invalid_contacts;")
            bad = cur.fetchall()

    if bad:
        print(f"\n  ⚠  {len(bad)} invalid row(s) were NOT inserted:")
        print(f"  {'Name':<20} {'Phone':<18} {'Reason'}")
        print("  " + "-" * 55)
        for b in bad:
            print(f"  {b[0]:<20} {b[1]:<18} {b[2]}")
    else:
        print("All rows inserted / updated successfully.")


# ── 4. Paginated query (calls function) ──────────────────────

def paginated_query() -> None:
    try:
        limit  = int(input("Rows per page [5]: ").strip() or 5)
        offset = int(input("Offset (skip rows) [0]: ").strip() or 0)
    except ValueError:
        print("Please enter valid numbers.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_page(%s, %s);",
                (limit, offset)
            )
            print_rows(cur.fetchall())


# ── 5. Delete by name or phone (calls procedure) ─────────────

def delete_contact() -> None:
    print("Delete by:  1 – name   2 – phone")
    choice = input("Choice: ").strip()
    if choice == "1":
        value = input("First name: ").strip()
        by    = "name"
    elif choice == "2":
        value = input("Phone: ").strip()
        by    = "phone"
    else:
        print("Invalid choice.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s, %s);", (value, by))
    print("Delete executed.")


# ── menu ──────────────────────────────────────────────────────

def main() -> None:
    menu = {
        "1": ("Search contacts by pattern",          search_by_pattern),
        "2": ("Upsert contact (insert or update)",   upsert_contact),
        "3": ("Bulk insert with validation",         bulk_insert),
        "4": ("Paginated query",                     paginated_query),
        "5": ("Delete contact by name or phone",     delete_contact),
        "0": ("Exit",                                None),
    }

    print("PhoneBook – Practice 8 (Functions & Procedures)")
    while True:
        print("\n===== Menu =====")
        for k, (label, _) in menu.items():
            print(f"  {k} – {label}")
        choice = input("Select: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()
