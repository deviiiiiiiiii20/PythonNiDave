"""database.py - everything that talks to MySQL.

All queries use %s placeholders (parameterized queries), so user input is
never glued into the SQL text. Rows come back as dictionaries.
"""

import traceback
import uuid

import mysql.connector
from mysql.connector import errorcode

from models import Complaint
from utils import generate_tracking_number, hash_password, verify_password

# >>> CHANGE THE PASSWORD HERE if your MySQL/XAMPP root account has one <<<
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "barangay_amsic",
}

# Set to True while developing to print the full traceback of database errors.
DEBUG_MODE = False

INITIAL_STATUS = "Submitted"

# Fixed (not user-typed) SQL text shared by several queries.
COMPLAINT_SELECT = """
    SELECT c.complaint_id, c.tracking_number, c.user_id, c.category,
           c.location, c.description, c.status, c.assigned_staff_id,
           c.created_at, c.updated_at,
           r.full_name AS resident_name,
           s.full_name AS assigned_staff_name
    FROM complaints AS c
    JOIN users AS r ON c.user_id = r.user_id
    LEFT JOIN users AS s ON c.assigned_staff_id = s.user_id
"""

# Search types map to fixed WHERE clauses (the value is still a %s parameter).
SEARCH_CLAUSES = {
    "tracking_number": "WHERE c.tracking_number LIKE %s",
    "category": "WHERE c.category = %s",
    "status": "WHERE c.status = %s",
}


class DatabaseError(Exception):
    """A friendly error that main.py can show to the user."""

    pass  # empty class body: Exception already does everything we need


# ----------------------------------------------------------------------
# Connection and error helpers
# ----------------------------------------------------------------------
def get_connection():
    """Open and return a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


def _friendly_message(error):
    """Translate a MySQL error number into a simple message."""
    if error.errno == 2003:
        return "Cannot connect to MySQL. Is MySQL (XAMPP) running?"
    if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        return "MySQL rejected the username/password. Check DB_CONFIG in database.py."
    if error.errno == errorcode.ER_BAD_DB_ERROR:
        return "Database 'barangay_amsic' does not exist. Run schema.sql first."
    if error.errno == errorcode.ER_NO_SUCH_TABLE:
        return "A table is missing. Run schema.sql first."
    if error.errno == errorcode.ER_DUP_ENTRY:
        return "That value already exists (for example, the username is taken)."
    if error.errno == errorcode.ER_NO_REFERENCED_ROW_2:
        return "Invalid reference: the related user or complaint does not exist."
    return f"Database error: {error.msg}"


def _raise_database_error(error):
    """Show the traceback in debug mode, then raise a friendly DatabaseError."""
    if DEBUG_MODE:
        traceback.print_exc()
    raise DatabaseError(_friendly_message(error)) from error


def _close(cursor, connection):
    """Close the cursor and connection if they were opened."""
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()


def _fetch_all(query, params=()):
    """Run a SELECT and return a list of dictionaries."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchall()
    except mysql.connector.Error as error:
        _raise_database_error(error)
    finally:
        _close(cursor, connection)


def _fetch_one(query, params=()):
    """Run a SELECT and return one dictionary (or None)."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchone()
    except mysql.connector.Error as error:
        _raise_database_error(error)
    finally:
        _close(cursor, connection)


def _rollback(connection):
    if connection is not None and connection.is_connected():
        connection.rollback()


def check_connection():
    """Raise DatabaseError if the database cannot be reached."""
    connection = None
    try:
        connection = get_connection()
    except mysql.connector.Error as error:
        _raise_database_error(error)
    finally:
        _close(None, connection)


# ----------------------------------------------------------------------
# Users
# ----------------------------------------------------------------------
def username_exists(username):
    row = _fetch_one(
        "SELECT COUNT(*) AS total FROM users WHERE username = %s", (username,)
    )
    return row["total"] > 0


def register_resident(full_name, address, username, password):
    """INSERT a new resident (role is always 'resident'). Returns the new user_id."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO users (full_name, username, password_hash, role, address)
            VALUES (%s, %s, %s, 'resident', %s)
            """,
            (full_name, username, hash_password(password), address),
        )
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as error:
        _rollback(connection)
        _raise_database_error(error)
    finally:
        _close(cursor, connection)


def authenticate_user(username, password):
    """Return the user's row (without the hash) if the login is correct, else None."""
    row = _fetch_one(
        """
        SELECT user_id, full_name, username, password_hash, role, address, position
        FROM users
        WHERE username = %s
        """,
        (username,),
    )
    if row is None or not verify_password(password, row["password_hash"]):
        return None
    del row["password_hash"]  # never pass the hash around
    return row


def get_staff_list():
    return _fetch_all(
        """
        SELECT user_id, full_name, position
        FROM users
        WHERE role = 'staff'
        ORDER BY full_name
        """
    )


# ----------------------------------------------------------------------
# Complaints (read)
# ----------------------------------------------------------------------
def get_complaints_by_user(user_id):
    """Only the complaints of ONE resident."""
    return _fetch_all(
        COMPLAINT_SELECT
        + " WHERE c.user_id = %s ORDER BY c.created_at DESC, c.complaint_id DESC",
        (user_id,),
    )


def get_all_complaints():
    return _fetch_all(
        COMPLAINT_SELECT + " ORDER BY c.created_at DESC, c.complaint_id DESC"
    )


def get_complaint_by_tracking(tracking_number, user_id=None):
    """Find one complaint. If user_id is given, it must belong to that resident."""
    if user_id is None:
        return _fetch_one(
            COMPLAINT_SELECT + " WHERE c.tracking_number = %s", (tracking_number,)
        )
    return _fetch_one(
        COMPLAINT_SELECT + " WHERE c.tracking_number = %s AND c.user_id = %s",
        (tracking_number, user_id),
    )


def search_complaints(search_type, value):
    """Search by 'tracking_number' (partial match), 'category' or 'status'."""
    if search_type not in SEARCH_CLAUSES:
        raise ValueError(f"Unknown search type: {search_type}")
    if search_type == "tracking_number":
        value = f"%{value}%"  # still passed as a parameter, not joined into SQL
    return _fetch_all(
        COMPLAINT_SELECT + " " + SEARCH_CLAUSES[search_type]
        + " ORDER BY c.created_at DESC, c.complaint_id DESC",
        (value,),
    )


def get_complaint_history(complaint_id):
    return _fetch_all(
        """
        SELECT u.update_id, u.status, u.remarks, u.created_at,
               s.full_name AS staff_name
        FROM complaint_updates AS u
        LEFT JOIN users AS s ON u.staff_id = s.user_id
        WHERE u.complaint_id = %s
        ORDER BY u.created_at, u.update_id
        """,
        (complaint_id,),
    )


# ----------------------------------------------------------------------
# Complaints (write) - each one is a transaction: commit or rollback
# ----------------------------------------------------------------------
def add_complaint(user_id, category, location, description):
    """INSERT a complaint, create its tracking number and first history record."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # The tracking number needs the new ID, so we insert a temporary
        # unique value first and replace it right away (same transaction).
        temporary_number = "TMP-" + uuid.uuid4().hex[:20]
        cursor.execute(
            """
            INSERT INTO complaints
                (tracking_number, user_id, category, location, description, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (temporary_number, user_id, category, location, description,
             INITIAL_STATUS),
        )
        complaint_id = cursor.lastrowid
        tracking_number = generate_tracking_number(complaint_id)

        cursor.execute(
            "UPDATE complaints SET tracking_number = %s WHERE complaint_id = %s",
            (tracking_number, complaint_id),
        )
        cursor.execute(
            """
            INSERT INTO complaint_updates (complaint_id, staff_id, status, remarks)
            VALUES (%s, NULL, %s, %s)
            """,
            (complaint_id, INITIAL_STATUS, "Complaint submitted by resident."),
        )
        connection.commit()
        return tracking_number
    except mysql.connector.Error as error:
        _rollback(connection)
        _raise_database_error(error)
    finally:
        _close(cursor, connection)


def update_complaint_status(complaint_id, new_status, staff_id, remarks):
    """UPDATE the status and INSERT a history record (old history is kept)."""
    if not Complaint.validate_status(new_status):
        raise ValueError("Invalid complaint status.")
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE complaints
            SET status = %s, updated_at = NOW()
            WHERE complaint_id = %s
            """,
            (new_status, complaint_id),
        )
        cursor.execute(
            """
            INSERT INTO complaint_updates (complaint_id, staff_id, status, remarks)
            VALUES (%s, %s, %s, %s)
            """,
            (complaint_id, staff_id, new_status, remarks),
        )
        connection.commit()
    except mysql.connector.Error as error:
        _rollback(connection)
        _raise_database_error(error)
    finally:
        _close(cursor, connection)


def assign_complaint(complaint_id, assigned_staff_id, acting_staff_id, remarks):
    """Assign a complaint, set its status to Assigned and record the history."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE complaints
            SET assigned_staff_id = %s, status = 'Assigned', updated_at = NOW()
            WHERE complaint_id = %s
            """,
            (assigned_staff_id, complaint_id),
        )
        cursor.execute(
            """
            INSERT INTO complaint_updates (complaint_id, staff_id, status, remarks)
            VALUES (%s, %s, 'Assigned', %s)
            """,
            (complaint_id, acting_staff_id, remarks),
        )
        connection.commit()
    except mysql.connector.Error as error:
        _rollback(connection)
        _raise_database_error(error)
    finally:
        _close(cursor, connection)


def add_remark(complaint_id, staff_id, remarks):
    """Save a remark in the history using the complaint's current status."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT status FROM complaints WHERE complaint_id = %s", (complaint_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise DatabaseError("Complaint not found.")
        cursor.execute(
            """
            INSERT INTO complaint_updates (complaint_id, staff_id, status, remarks)
            VALUES (%s, %s, %s, %s)
            """,
            (complaint_id, staff_id, row["status"], remarks),
        )
        cursor.execute(
            "UPDATE complaints SET updated_at = NOW() WHERE complaint_id = %s",
            (complaint_id,),
        )
        connection.commit()
    except mysql.connector.Error as error:
        _rollback(connection)
        _raise_database_error(error)
    finally:
        _close(cursor, connection)


# ----------------------------------------------------------------------
# Statistics
# ----------------------------------------------------------------------
def get_statistics():
    """Return a dictionary such as {'Total': 25, 'Submitted': 3, ...}."""
    total_row = _fetch_one("SELECT COUNT(*) AS total FROM complaints")
    rows = _fetch_all(
        "SELECT status, COUNT(*) AS total FROM complaints GROUP BY status"
    )

    statistics = {"Total": total_row["total"]}
    for status in Complaint.VALID_STATUSES:  # start every status at 0
        statistics[status] = 0
    for row in rows:
        statistics[row["status"]] = row["total"]
    return statistics
