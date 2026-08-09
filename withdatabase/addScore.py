import mysql.connector
from mysql.connector.aio import cursor
from mysql.connector.constants import flag_is_set


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="auth"
    )

def login():
    name = input("Enter your username: ")
    password = input("Enter your password: ")

    conn = get_connection()
    cursor = conn.cursor()
    sql = "select * from users where name = %s && password =%s"
    cursor.execute(sql, (name, password))
    result = cursor.fetchone()
    conn.close()
    cursor.close()

    if result:
        user_id = result[0]  # extract the actual id from the row
        addScore = int(input("Add a score: "))

        conn = get_connection()
        cursor = conn.cursor()
        sql = "select score from users where id = %s"
        cursor.execute(sql, (user_id,))
        current_score = cursor.fetchone()[0]

        new_score = addScore

        sql = "update users set score = score + %s where id = %s"
        cursor.execute(sql, (new_score, user_id))
        conn.commit()
        cursor.close()
        conn.close()

        conn = get_connection()
        cursor = conn.cursor()
        sql = "select score from users where id = %s"
        cursor.execute(sql, (user_id,))
        score1 = cursor.fetchone()[0]


        print("Score added successfully.")
        print(" ")
        print("Updated score")
        print(f"{name}'s score is {score1}")

    else:
        print("Name or password is incorrect.")
        return False



if __name__ == "__main__":
    while True:
        print("1. Login")
        print("2. Create")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            login()
        elif choice == "2":
            ...
        elif choice == "3":
            break
        else:
            print("Invalid option, try again.")
