import mysql.connector
import random


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="appointment_system"
    )

def add_appointment():
    name = input("Enter your name: ")
    place = input("Enter the place of meeting: ")
    date = input("Enter the date of meeting: ")
    time = input("Enter the time of meeting: ")

    ref_number = str(random.randint(0, 999)).zfill(3)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('insert into user (name, place, date, time, ref_number) values (%s, %s, %s, %s, %s)', (name, place, date, time, ref_number))
    conn.commit()
    cursor.close()
    conn.close()
    print(" ")
    print("=" * 51)
    print("Appointment successfully saved.")
    print(f"Your reference number is: {ref_number}")
    print("Please remember this number — you'll need it to check your appointment.")
    print("=" * 51)

def check_appointment():
    ref_number = input("Enter your reference number: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('select * from user where ref_number = %s', (ref_number,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        print("Appointment found:")
        appointment(ref_number)
    else:
        print("No appointment found with that reference number.")


def appointment(ref_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('select name from user where ref_number = %s', (ref_number,))
    name = cursor.fetchone()[0]

    cursor.execute('select place from user where ref_number = %s', (ref_number,))
    place = cursor.fetchone()[0]

    cursor.execute('select time from user where ref_number = %s', (ref_number,))
    time = cursor.fetchone()[0]

    cursor.execute('select date from user where ref_number = %s', (ref_number,))
    date = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    print(" ")
    print("=" * 51)
    print("========= YOUR APPOINTMENT INFORMATION ============")
    print("=" * 51)
    print(f"Name: {name}")
    print(f"Place: {place}")
    print(f"Time: {time}")
    print(f"Date: {date}")
    print("=" * 51)


def useSystem():
    print(" ")
    print("=" * 51)
    print("==================== WELCOME ======================")
    print("=" * 51)
    while True:
        print(" ")
        print("1. Add appointment")
        print("2. Check appointment")
        print("3. Remove appointment")
        print("4. Update appointment")
        print("5. Exit")

        user = input("Enter your choice: ")
        if user == '1':
            add_appointment()
        elif user == '2':
            check_appointment()
        elif user == '3':
            ...
        elif user == '4':
            ...
        elif user == '5':
            exit()

if __name__ == "__main__":
    useSystem()