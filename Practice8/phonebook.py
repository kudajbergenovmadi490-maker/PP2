import psycopg2
from connect import get_connection


# --- Search contacts by name or phone ---
def search_contacts():
    pattern = input("Enter name or phone to search: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")
    cur.close()
    conn.close()


# --- Insert or update a contact ---
def upsert_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
    conn.commit()
    print("Done!")
    cur.close()
    conn.close()


# --- Insert many contacts at once ---
def bulk_insert():
    names = []
    phones = []
    print("Enter contacts as: name,phone")
    print("Type 'end' to stop.")
    while True:
        line = input("Enter contact: ")
        if line.lower() == "end":
            break
        parts = line.split(",")
        if len(parts) == 2:
            names.append(parts[0].strip())
            phones.append(parts[1].strip())
        else:
            print("Wrong format! Use: name,phone")

    if not names:
        print("No contacts entered.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL bulk_insert_contacts(%s::varchar[], %s::varchar[]);", (names, phones))
    cur.execute("SELECT * FROM invalid_contacts;")
    bad_rows = cur.fetchall()
    conn.commit()

    if bad_rows:
        print("These contacts were NOT inserted:")
        for row in bad_rows:
            print(row)
    else:
        print("All contacts inserted!")

    cur.close()
    conn.close()


# --- Show contacts with pagination ---
def paginated_query():
    limit = int(input("How many rows per page? "))
    offset = int(input("Skip how many rows? "))
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_page(%s, %s);", (limit, offset))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")
    cur.close()
    conn.close()


# --- Delete a contact ---
def delete_contact():
    print("Delete by: 1 - name   2 - phone")
    choice = input("Your choice: ")
    if choice == "1":
        value = input("Enter name: ")
        by_what = "name"
    elif choice == "2":
        value = input("Enter phone: ")
        by_what = "phone"
    else:
        print("Wrong choice.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s, %s);", (value, by_what))
    conn.commit()
    print("Deleted!")
    cur.close()
    conn.close()


# --- Main menu ---
while True:
    print("\n--- PhoneBook Menu ---")
    print("1 - Search contacts")
    print("2 - Add or update contact")
    print("3 - Bulk insert contacts")
    print("4 - Show contacts (with pagination)")
    print("5 - Delete contact")
    print("0 - Exit")

    choice = input("Choose: ")

    if choice == "1":
        search_contacts()
    elif choice == "2":
        upsert_contact()
    elif choice == "3":
        bulk_insert()
    elif choice == "4":
        paginated_query()
    elif choice == "5":
        delete_contact()
    elif choice == "0":
        print("Bye!")
        break
    else:
        print("Wrong choice, try again.")
