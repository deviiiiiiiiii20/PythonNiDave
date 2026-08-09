import mysql.connector
import hashlib

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="auth"
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def username_exists(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM account WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def register():
    username = input("Choose a username: ")

    if username_exists(username):
        print("Username already taken. Try again.")
        return

    password = input("Choose a password: ")
    hashed = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO account (username, password) VALUES (%s, %s)"
    cursor.execute(sql, (username, hashed))
    conn.commit()
    cursor.close()
    conn.close()
    print("Account created successfully!")

def login():
    username = input("Username: ")
    password = input("Password: ")
    hashed = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM account WHERE username == %s AND password == %s"
    cursor.execute(sql, (username, hashed))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        print(f"Welcome back, {username}!")
        return True
    else:
        print("Incorrect username or password.")
        return False

def view_usernames():
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT username FROM account"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()
    cursor.close()


if __name__ == "__main__":
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. View usernames")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            login()
        elif choice == "2":
            register()
        elif choice == "3":
            view_usernames()
        elif choice == "4":
            break
        else:
            print("Invalid option, try again.")


