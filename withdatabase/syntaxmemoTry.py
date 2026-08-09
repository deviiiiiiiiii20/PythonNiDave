import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="auth"
    )

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    conn = get_connection()
    cursor = conn.cursor()
    sql = "select * from account where username = %s && password = %s"
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()
    conn.close()
    cursor.close()


    if result:
        print("Logged in successfully.")
        print(f"Welcome {username}!")
        return True
    else:
        print("Incorrect username or password.")
        return False

def username_exists(username):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "select * from account where username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    conn.close()
    cursor = conn.close()
    return result is not None

def register():
    username = input("Choose your username: ")

    if username_exists(username):
        print("Username already exists.")
        return

    password = input("Set your password: ")

    conn = get_connection()
    cursor = conn.cursor()
    sql = "insert into account (username, password) values (%s, %s)"
    cursor.execute(sql, (username, password))
    conn.commit()
    conn.close()
    cursor.close()
    print("Account created successfully.")

def view():
    print("This is the list of Usernames.")
    conn = get_connection()
    cursor = conn.cursor()
    sql = "select * from account"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)
    conn.close()
    cursor.close()


if __name__ == "__main__":

    while True:
        print("1. Login")
        print("2. Register")
        print("3. View")
        print("4. Exit")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            login()
        elif choice == 2:
            register()
        elif choice == 3:
            view()
        elif choice == 4:
            exit()
        else:
            print("Invalid choice.")
