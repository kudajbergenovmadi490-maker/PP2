"""
PhoneBook application backed by PostgreSQL.
Practice 7 – psycopg2 CRUD demo
"""

import csv
import psycopg2
from connect import get_connection, create_table


# ──────────────────────────────────────────────
# INSERT
# ──────────────────────────────────────────────

def insert_from_csv(filepath: str) -> None:
    """Read a CSV file (first_name, phone) and insert all rows."""
    sql = """
        INSERT INTO phonebook (first_name, phone)
        VALUES (%s, %s)
        ON CONFLICT (phone) DO NOTHING;
    """
    inserted = 0
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [(row["first_name"].strip(), row["phone"].strip()) for row in reader]

    with get_connection() as conn:
        with conn.cursor() as cur:
            for row in rows:
                cur.execute(sql, row)
                if cur.rowcount:
                    inserted += 1
    print(f"CSV import done – {inserted} new row(s) inserted.")


def insert_from_console() -> None:
    """Ask the user for a name and phone, then insert."""
    first_name = input("Enter first name: ").strip()
    phone      = input("Enter phone number: ").strip()

    if not first_name or not phone:
        print("Name and phone cannot be empty.")
        return

    sql = """
        INSERT INTO phonebook (first_name, phone)
        VALUES (%s, %s)
        ON CONFLICT (phone) DO NOTHING;
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name, phone))
                if cur.rowcount:
                    print(f"Added: {first_name} – {phone}")
                else:
                    print("Phone already exists. Nothing inserted.")
    except psycopg2.Error as e:
        print(f"DB error: {e}")


# ──────────────────────────────────────────────
# UPDATE
# ──────────────────────────────────────────────

def update_contact() -> None:
    """Update a contact's first name or phone number."""
    phone = input("Enter the phone number of the contact to update: ").strip()

    print("What do you want to change?")
    print("  1 – First name")
    print("  2 – Phone number")
    choice = input("Choice: ").strip()

    if choice == "1":
        new_value = input("New first name: ").strip()
        sql = "UPDATE phonebook SET first_name = %s WHERE phone = %s;"
    elif choice == "2":
        new_value = input("New phone number: ").strip()
        sql = "UPDATE phonebook SET phone = %s WHERE phone = %s;"
    else:
        print("Invalid choice.")
        return

    if not new_value:
        print("Value cannot be empty.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_value, phone))
                if cur.rowcount:
                    print("Contact updated successfully.")
                else:
                    print("No contact found with that phone number.")
    except psycopg2.errors.UniqueViolation:
        print("That phone number already belongs to another contact.")
    except psycopg2.Error as e:
        print(f"DB error: {e}")


# ──────────────────────────────────────────────
# QUERY
# ──────────────────────────────────────────────

def query_contacts() -> None:
    """Query contacts with different filters."""
    print("Filter options:")
    print("  1 – All contacts")
    print("  2 – By first name (exact)")
    print("  3 – By first name (partial match)")
    print("  4 – By phone prefix")
    choice = input("Choice: ").strip()

    with get_connection() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                cur.execute("SELECT id, first_name, phone FROM phonebook ORDER BY first_name;")

            elif choice == "2":
                name = input("Enter first name: ").strip()
                cur.execute(
                    "SELECT id, first_name, phone FROM phonebook WHERE first_name = %s;",
                    (name,)
                )

            elif choice == "3":
                name = input("Enter partial name: ").strip()
                cur.execute(
                    "SELECT id, first_name, phone FROM phonebook WHERE first_name ILIKE %s;",
                    (f"%{name}%",)
                )

            elif choice == "4":
                prefix = input("Enter phone prefix (e.g. +7700): ").strip()
                cur.execute(
                    "SELECT id, first_name, phone FROM phonebook WHERE phone LIKE %s;",
                    (f"{prefix}%",)
                )

            else:
                print("Invalid choice.")
                return

            rows = cur.fetchall()

    if rows:
        print(f"\n{'ID':<5} {'First Name':<20} {'Phone'}")
        print("-" * 45)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]}")
        print(f"\n{len(rows)} record(s) found.")
    else:
        print("No contacts found.")


# ──────────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────────

def delete_contact() -> None:
    """Delete a contact by first name or phone number."""
    print("Delete by:")
    print("  1 – First name")
    print("  2 – Phone number")
    choice = input("Choice: ").strip()

    if choice == "1":
        value = input("Enter first name: ").strip()
        sql   = "DELETE FROM phonebook WHERE first_name = %s;"
    elif choice == "2":
        value = input("Enter phone number: ").strip()
        sql   = "DELETE FROM phonebook WHERE phone = %s;"
    else:
        print("Invalid choice.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (value,))
            deleted = cur.rowcount

    if deleted:
        print(f"Deleted {deleted} contact(s).")
    else:
        print("No matching contact found.")


# ──────────────────────────────────────────────
# MENU
# ──────────────────────────────────────────────

def main() -> None:
    create_table()
    print("PhoneBook initialized.\n")

    menu = {
        "1": ("Insert from CSV file",          insert_from_csv),
        "2": ("Insert from console",            insert_from_console),
        "3": ("Update a contact",               update_contact),
        "4": ("Query / search contacts",        query_contacts),
        "5": ("Delete a contact",               delete_contact),
        "0": ("Exit",                           None),
    }

    while True:
        print("\n===== PhoneBook Menu =====")
        for key, (label, _) in menu.items():
            print(f"  {key} – {label}")

        choice = input("Select option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            path = input("CSV file path [contacts.csv]: ").strip() or "contacts.csv"
            insert_from_csv(path)
        elif choice in menu:
            _, func = menu[choice]
            func()
        else:
            print("Unknown option, try again.")


if __name__ == "__main__":
    main()
