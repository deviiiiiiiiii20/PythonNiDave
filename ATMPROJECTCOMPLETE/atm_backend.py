import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="useraccount"
    )

def do_login(username, password):
    """Returns the full user row if credentials match, otherwise None."""
    conn = get_connection()
    cursor = conn.cursor()
    sql = "select * from userinfo where username = %s and password = %s"
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def username_exists(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select * from userinfo where username = %s", (username,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    return record is not None


def do_register(username, password):
    """Returns True if the account was created, False if username is taken."""
    if username_exists(username):
        return False

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "insert into userinfo (username, password, balance) values (%s, %s, %s)",
        (username, password, 0)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True


def get_balance(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select balance from userinfo where id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0] if row else None


def do_deposit(user_id, amount):
    """Adds amount to the user's balance and returns the new balance."""
    conn = get_connection()
    cursor = conn.cursor()
    sql = "update userinfo set balance = balance + %s where id = %s"
    cursor.execute(sql, (amount, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return get_balance(user_id)


def do_withdraw(user_id, amount):
    """
    Attempts to withdraw amount from the user's balance.
    Returns a tuple: (new_balance, error_message)
    - On success: (new_balance, None)
    - On failure: (None, "reason it failed")
    """
    balance = get_balance(user_id)
    if amount <= 0:
        return None, "Withdraw amount must be greater than 0."
    if amount > balance:
        return None, "Insufficient balance!"

    conn = get_connection()
    cursor = conn.cursor()
    sql = "update userinfo set balance = balance - %s where id = %s"
    cursor.execute(sql, (amount, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return get_balance(user_id), None