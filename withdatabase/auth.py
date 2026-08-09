import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="auth"
    )

def add_score(name, score):
    conn = get_connection()
    cursor = conn.cursor()
    sql = 'INSERT INTO users (name, score) VALUES (%s, %s)'
    cursor.execute(sql, (name, score))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Name:{name}")
    print(f"Score:{score}")
    print(" ")

def view_nameAndScore():
    print("")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()
    cursor.close()
    print(" ")

if __name__ == "__main__":
    while True:
        print("1. Add Name and Score")
        print("2. View Name and Score")
        print("3. Exit the program")
        print(" ")
        user = input("Enter your choice: ")

        if user == "1":
            name = input("Enter your name: ")
            score = input("Enter your score: ")
            add_score(name, score)
        elif user == "2":
            view_nameAndScore()
        elif user == "3":
            exit()
        else:
            print("Invalid input")
            exit()



