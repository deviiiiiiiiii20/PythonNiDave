
import mysql.connector
from utils import make_tracking_number


HOST = "localhost"
USER = "root"
PASSWORD = ""
DATABASE = "barangay_amsic"


base_sql = """
    select c.complaint_id, c.tracking_number, c.user_id, c.category,
           c.location, c.description, c.status, c.assigned_staff_id,
           c.created_at, c.updated_at,
           r.full_name as resident_name,
           s.full_name as assigned_staff_name
    from complaints c
    join users r on c.user_id = r.user_id
    left join users s on c.assigned_staff_id = s.user_id
"""


def get_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )



def username_exists(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select * from users where username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row is not None


def register_resident(full_name, address, username, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """insert into users (full_name, username, password_hash, role, address)
             values (%s, %s, %s, 'resident', %s)"""
    cursor.execute(sql, (full_name, username, password_hash, address))
    conn.commit()
    cursor.close()
    conn.close()


def login(username, password_hash):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "select * from users where username = %s and password_hash = %s"
    cursor.execute(sql, (username, password_hash))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_staff_list():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select user_id, full_name, position from users where role = 'staff'")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_my_complaints(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(base_sql + " where c.user_id = %s order by c.complaint_id desc", (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_all_complaints():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(base_sql + " order by c.complaint_id desc")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def find_my_complaint(tracking_number, user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = base_sql + " where c.tracking_number = %s and c.user_id = %s"
    cursor.execute(sql, (tracking_number, user_id))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def find_complaint(tracking_number):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(base_sql + " where c.tracking_number = %s", (tracking_number,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def search_by_tracking(text):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = base_sql + " where c.tracking_number like %s order by c.complaint_id desc"
    cursor.execute(sql, ("%" + text + "%",))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def search_by_category(category):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = base_sql + " where c.category = %s order by c.complaint_id desc"
    cursor.execute(sql, (category,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def search_by_status(status):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = base_sql + " where c.status = %s order by c.complaint_id desc"
    cursor.execute(sql, (status,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_history(complaint_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """select u.status, u.remarks, u.created_at, s.full_name as staff_name
             from complaint_updates u
             left join users s on u.staff_id = s.user_id
             where u.complaint_id = %s
             order by u.update_id"""
    cursor.execute(sql, (complaint_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def add_complaint(user_id, category, location, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("select max(complaint_id) from complaints")
    biggest = cursor.fetchone()[0]
    if biggest is None:
        biggest = 0
    tracking_number = make_tracking_number(biggest + 1)

    sql = """insert into complaints
             (tracking_number, user_id, category, location, description, status)
             values (%s, %s, %s, %s, %s, 'Submitted')"""
    cursor.execute(sql, (tracking_number, user_id, category, location, description))
    complaint_id = cursor.lastrowid

    sql = """insert into complaint_updates (complaint_id, staff_id, status, remarks)
             values (%s, NULL, 'Submitted', 'Complaint submitted by resident.')"""
    cursor.execute(sql, (complaint_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return tracking_number


def assign_complaint(complaint_id, assigned_staff_id, staff_id, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """update complaints
             set assigned_staff_id = %s, status = 'Assigned', updated_at = NOW()
             where complaint_id = %s"""
    cursor.execute(sql, (assigned_staff_id, complaint_id))
    sql = """insert into complaint_updates (complaint_id, staff_id, status, remarks)
             values (%s, %s, 'Assigned', %s)"""
    cursor.execute(sql, (complaint_id, staff_id, remarks))
    conn.commit()
    cursor.close()
    conn.close()


def update_status(complaint_id, new_status, staff_id, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "update complaints set status = %s, updated_at = NOW() where complaint_id = %s"
    cursor.execute(sql, (new_status, complaint_id))
    sql = """insert into complaint_updates (complaint_id, staff_id, status, remarks)
             values (%s, %s, %s, %s)"""
    cursor.execute(sql, (complaint_id, staff_id, new_status, remarks))
    conn.commit()
    cursor.close()
    conn.close()


def add_remark(complaint_id, staff_id, current_status, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """insert into complaint_updates (complaint_id, staff_id, status, remarks)
             values (%s, %s, %s, %s)"""
    cursor.execute(sql, (complaint_id, staff_id, current_status, remarks))
    cursor.execute("update complaints set updated_at = NOW() where complaint_id = %s", (complaint_id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_statistics(statuses):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("select count(*) from complaints")
    stats = {"Total": cursor.fetchone()[0]}

    for status in statuses:
        cursor.execute("select count(*) from complaints where status = %s", (status,))
        stats[status] = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return stats
