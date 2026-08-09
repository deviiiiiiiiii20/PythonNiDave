from unittest import result

import mysql.connector
from mysql.connector.aio import cursor

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="useraccount"
    )


def auth ():
    while True:
        print(" ")
        print("=" * 51)
        print("==================== WELCOME ======================")
        print("=" * 51)

        print("1. Login")
        print("2. Register")
        print("3. Logout")
        print("=" * 51)
        print(" ")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            login()
        elif choice == 2:
            register()
        elif choice == 3:
            exit()

def login():
    print(" ")
    print("=" * 51)
    username = (input(f"Enter your username: "))
    password = (input(f"Enter your password: "))

    conn = get_connection()
    cursor = conn.cursor()
    sql = "select * from userinfo where username = %s and password = %s"
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        menu(username, result)
    else:
        return False

def usernameExist(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select * from userinfo where username = %s", (username, ))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    return record is not None


def register():
    username = input("Username: ")

    if usernameExist(username):
        print("Username already taken. Try again.")
        return

    password = input("Password: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("insert into userinfo (username, password, balance) values (%s, %s, %s)", (username, password, 0))
    conn.commit()
    cursor.close()
    conn.close()
    print("Account created successfully!")


def checkBalance(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select balance from userinfo where username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        print("User not found.")
    else:
        print("=" * 50)
        print(f"Account name: {username}")
        print(f"Balance: {row[0]}")
        print("=" * 50)

def deposit(username, result):
    user_id = result[0]
    addDeposit = input("Enter your deposit amount: ")

    newBalance = addDeposit

    conn = get_connection()
    cursor = conn.cursor()
    sql = "update userinfo set balance = balance + %s where id = %s"
    cursor.execute(sql, (newBalance, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select balance from userinfo where id = %s", (user_id,))
    fBalance = cursor.fetchone()
    cursor.close()
    conn.close()
    print("=" * 50)
    print("Balace deposited successfully!")
    print(f"Updated balance: {fBalance[0]} ")
    print("=" * 50)

def withdraw(username, result):
    user_id = result[0]
    withdrawBalance = input("Enter your withdraw amount: ")

    conn = get_connection()
    cursor = conn.cursor()
    sql = "update userinfo set balance = balance - %s where id = %s"
    cursor.execute(sql, (withdrawBalance, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select balance from userinfo where id = %s", (user_id,))
    fBalance = cursor.fetchone()
    cursor.close()
    conn.close()
    print(" ")
    print("=" * 50)
    print("Withdraw successfully!")
    print(f"Withdrawed : {withdrawBalance} ")
    print(f"Updated balance: {fBalance[0]} ")
    print("=" * 50)


def menu(username, result):
    print(" ")
    print("=" * 50)
    print("====================== ATM =======================")
    print("=" * 50)

    while True:
        print(" ")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")
        print(" ")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            checkBalance(username)
        elif choice == 2:
            deposit(username, result)
        elif choice == 3:
            withdraw(username, result)
        elif choice == 4:
            auth()

if __name__ == "__main__":
    auth()
