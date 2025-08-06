import json
import os

def main():
    while True:
        print("========== Welcome to Library ==========")
        print("Enter '1' to go to user-interface.")
        print("Enter '2' to go to admin-page.")
        print("Enter '3' to exit system.")
        val = input("Enter your choice: ")

        if not val.isdigit():
            print("Error: Enter a valid input.")
            continue

        val = int(val)
        if val == 1:
            user_interface()
        elif val == 2:
            admin_page()
        elif val == 3:
            print("Thanks. Goodbye!")
            break
        else:
            print("Error: Enter a valid number.")

def load_data(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)
    with open(file, "r") as f:
        return json.load(f)

def saveData(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ USER SECTION ------------------

def user_interface():
    while True:
        print("Welcome to User Interface of Library")
        print("1. Login")
        print("2. Sign-Up (New User)")
        print("3. Exit")
        val = input("Enter your choice: ")

        if not val.isdigit():
            print("Error: Enter the correct value.")
            continue

        val = int(val)
        if val == 1:
            userLoginpage()
        elif val == 2:
            userSignuppage()
        elif val == 3:
            break
        else:
            print("Error: Enter the correct value.")

def userSignuppage():
    print("Welcome to Signup Page")
    data = load_data("userData.json")

    while True:
        id = input("Enter user-id: ").strip()
        if checkid(id, data):
            print("User-id already taken. Try another.")
        else:
            break

    password = input("Enter password: ")
    user = {
        "id": id,
        "password": password,
        "Book": []
    }

    data.append(user)
    saveData("userData.json", data)
    print("User registered successfully.")
    userLoginpage()

def checkid(id, data):
    for user in data:
        if user["id"] == id:
            return True
    return False

def userLoginpage():
    data = load_data("userData.json")
    print("User Login Page")
    id = input("Enter id: ")
    password = input("Enter password: ")

    for user in data:
        if user["id"] == id:
            if user["password"] == password:
                print("Login successful.")
                library(id)
                return
            else:
                print("Incorrect password.")
                return
    print("User ID not found.")

def library(id):
    while True:
        print("\nLibrary Menu")
        print("1. Borrow Book")
        print("2. Submit Book")
        print("3. Exit")
        val = input("Enter choice: ")

        if not val.isdigit():
            print("Invalid input.")
            continue

        val = int(val)
        if val == 1:
            borrow(id)
        elif val == 2:
            submit(id)
        elif val == 3:
            break
        else:
            print("Invalid choice.")

def borrow(id):
    dataBook = load_data("store.json")
    dataUser = load_data("userData.json")

    bookid = input("Enter book ID to borrow: ").strip()
    book_found = False

    for book in dataBook:
        if book["id"] == bookid and book["status"] == "available":
            book["status"] = "borrowed"
            book_found = True
            break

    if not book_found:
        print("Book not available.")
        return

    for user in dataUser:
        if user["id"] == id:
            user["Book"].append(bookid)
            break

    saveData("store.json", dataBook)
    saveData("userData.json", dataUser)
    print(f"Book {bookid} borrowed successfully.")

def submit(id):
    dataBook = load_data("store.json")
    dataUser = load_data("userData.json")

    bookid = input("Enter book ID to submit: ").strip()
    found = False

    for user in dataUser:
        if user["id"] == id:
            if bookid in user["Book"]:
                user["Book"].remove(bookid)
                found = True
                break

    if not found:
        print("Book not found in your account.")
        return

    for book in dataBook:
        if book["id"] == bookid:
            book["status"] = "available"
            break

    saveData("store.json", dataBook)
    saveData("userData.json", dataUser)
    print(f"Book {bookid} submitted successfully.")

# ------------------ ADMIN SECTION ------------------

def admin_page():
    while True:
        print("Welcome to Admin Page")
        print("1. Login")
        print("2. Sign-Up")
        print("3. Exit")
        val = input("Enter your choice: ")

        if not val.isdigit():
            print("Invalid input.")
            continue

        val = int(val)
        if val == 1:
            adminLogin_page()
        elif val == 2:
            adminSignup_page()
        elif val == 3:
            break
        else:
            print("Invalid option.")

def adminSignup_page():
    print("Admin Sign-Up Page")
    data = load_data("adminData.json")

    while True:
        admin_id = input("Enter admin ID: ").strip()
        if checkAdminid(admin_id):
            print("ID already registered. Try another.")
        else:
            break

    password = input("Enter password: ")
    admin = {
        "id": admin_id,
        "password": password
    }
    data.append(admin)
    saveData("adminData.json", data)
    print("Admin registered successfully.")
    adminLogin_page()

def checkAdminid(admin_id):
    data = load_data("adminData.json")
    for admin in data:
        if admin["id"] == admin_id:
            return True
    return False

def adminLogin_page():
    print("Admin Login Page")
    data = load_data("adminData.json")

    id = input("Enter admin ID: ")
    password = input("Enter password: ")

    for admin in data:
        if admin["id"] == id and admin["password"] == password:
            print("Login successful.")
            admin_panel()
            return
    print("Invalid credentials.")

def admin_panel():
    while True:
        print("\nAdmin Panel")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Exit")
        val = input("Enter your choice: ")

        if not val.isdigit():
            print("Invalid input.")
            continue

        val = int(val)
        if val == 1:
            add_book()
        elif val == 2:
            remove_book()
        elif val == 3:
            break
        else:
            print("Invalid option.")

def add_book():
    data = load_data("store.json")
    while True:
        book_id = input("Enter book ID (or type 'exit'): ").strip()
        if book_id.lower() == "exit":
            break
        book_name = input("Enter book name: ").strip()
        book = {
            "id": book_id,
            "name": book_name,
            "status": "available"
        }
        data.append(book)
        print(f"Book '{book_name}' added.")
    saveData("store.json", data)

def remove_book():
    data = load_data("store.json")
    while True:
        book_id = input("Enter book ID to remove (or type 'exit'): ").strip()
        if book_id.lower() == "exit":
            break
        found = False
        for book in data:
            if book["id"] == book_id:
                book["status"] = "removed"
                found = True
                print(f"Book '{book_id}' marked as removed.")
                break
        if not found:
            print("Book not found.")
    saveData("store.json", data)

# ------------------ MAIN ENTRY ------------------

if __name__ == "__main__":
    main()
