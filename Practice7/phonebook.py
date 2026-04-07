import csv
import psycopg2
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_from_csv():
    filename = input("Enter CSV file name [contacts.csv]: ")
    if filename == "":
        filename = "contacts.csv"

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["first_name"].strip()
            phone = row["phone"].strip()
            cur.execute("""
                INSERT INTO phonebook (first_name, phone)
                VALUES (%s, %s)
                ON CONFLICT (phone) DO NOTHING;
            """, (name, phone))

    conn.commit()
    print("CSV data inserted!")
    cur.close()
    conn.close()

def insert_from_console():
    name = input("Enter first name: ")
    phone = input("Enter phone number: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO phonebook (first_name, phone)
        VALUES (%s, %s)
        ON CONFLICT (phone) DO NOTHING;
    """, (name, phone))
    conn.commit()
    print("Contact added!")
    cur.close()
    conn.close()

def update_contact():
    phone = input("Enter phone of contact to update: ")
    print("What to update?  1 - name   2 - phone")
    choice = input("Your choice: ")

    if choice == "1":
        new_value = input("New name: ")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE phonebook SET first_name = %s WHERE phone = %s;", (new_value, phone))
    elif choice == "2":
        new_value = input("New phone: ")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s;", (new_value, phone))
    else:
        print("Wrong choice.")
        return

    conn.commit()
    print("Contact updated!")
    cur.close()
    conn.close()

def search_contacts():
    print("Search by:  1 - all   2 - name   3 - partial name   4 - phone prefix")
    choice = input("Your choice: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        cur.execute("SELECT * FROM phonebook ORDER BY first_name;")
    elif choice == "2":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s;", (name,))
    elif choice == "3":
        name = input("Enter part of name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s;", ("%" + name + "%",))
    elif choice == "4":
        prefix = input("Enter phone prefix: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s;", (prefix + "%",))
    else:
        print("Wrong choice.")
        cur.close()
        conn.close()
        return

    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()

def delete_contact():
    print("Delete by:  1 - name   2 - phone")
    choice = input("Your choice: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s;", (name,))
    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s;", (phone,))
    else:
        print("Wrong choice.")
        cur.close()
        conn.close()
        return

    conn.commit()
    print("Contact deleted!")
    cur.close()
    conn.close()

create_table()
print("PhoneBook ready!")

while True:
    print("\n--- PhoneBook Menu ---")
    print("1 - Insert from CSV file")
    print("2 - Insert from console")
    print("3 - Update a contact")
    print("4 - Search contacts")
    print("5 - Delete a contact")
    print("0 - Exit")

    choice = input("Choose: ")

    if choice == "1":
        insert_from_csv()
    elif choice == "2":
        insert_from_console()
    elif choice == "3":
        update_contact()
    elif choice == "4":
        search_contacts()
    elif choice == "5":
        delete_contact()
    elif choice == "0":
        print("Bye!")
        break
    else:
        print("Wrong choice, try again.")
