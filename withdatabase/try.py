import mysql.connector

# --- Connect to the database ---
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # default XAMPP MySQL user
        password="",       # default XAMPP MySQL password is blank
        database="school"  # change this to your actual database name
    )

# --- Add a student ---
def add_student(name, age):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO students (name, age) VALUES (%s, %s)"
    cursor.execute(sql, (name, age))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Added: {name}, {age}")

# --- View all students ---
def view_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn.close()

# --- Example usage ---
if __name__ == "__main__":
    add_student("Juan Dela Cruz", 20)
    view_students()




