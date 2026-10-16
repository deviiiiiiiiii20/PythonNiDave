"""main.py - entry point and terminal menus of the
Barangay Amsic Complaint and Request Tracking System.

Run from the project folder with:  python src/main.py
"""

from database import (
    DatabaseError,
    add_complaint,
    add_remark,
    assign_complaint,
    authenticate_user,
    check_connection,
    get_all_complaints,
    get_complaint_by_tracking,
    get_complaint_history,
    get_complaints_by_user,
    get_staff_list,
    get_statistics,
    register_resident,
    search_complaints,
    update_complaint_status,
    username_exists,
)
from models import Complaint, ComplaintCount, Resident, Staff
from utils import (
    choose_from_list,
    create_log_message,
    display_header,
    display_messages,
    format_date,
    get_non_empty_input,
    get_optional_input,
    get_password_input,
    pause_screen,
    print_table,
    safe_int_input,
    validate_password,
    validate_username,
)

MAX_LOGIN_ATTEMPTS = 3
MIN_DESCRIPTION_LENGTH = 10
REMARKS_REQUIRED_STATUSES = ["Resolved", "Closed"]  # staff must explain these


# ----------------------------------------------------------------------
# Small shared helpers
# ----------------------------------------------------------------------
def run_safely(action, *args):
    """Run a menu action and show database problems as simple messages.

    *args passes along whatever the action needs (a resident, a staff
    member, or nothing) so one helper works for every menu option.
    """
    try:
        action(*args)
    except DatabaseError as error:
        print(f"\n[ERROR] {error}")
    pause_screen()


def ask_tracking_number():
    return get_non_empty_input("Enter tracking number (e.g. AMS-00001): ").upper()


def show_history(complaint_id, tracking_number):
    """Print every update saved in complaint_updates for one complaint."""
    history = get_complaint_history(complaint_id)
    print(f"\nTracking Number: {tracking_number}")
    print("\nHistory:")
    if not history:
        print("No updates recorded yet.")
        return
    for entry in history:  # one block per history record
        print(f"\n{entry['status']}")
        print(f"  Date/time : {format_date(entry['created_at'], include_time=True)}")
        print(f"  Updated by: {entry['staff_name'] or 'Resident'}")
        print(f"  Remarks   : {entry['remarks'] or '-'}")


def show_complaint_details(row):
    """Show the full details of a complaint row using the Complaint class."""
    complaint = Complaint.from_dict(row)
    display_messages("", "-" * 40)
    complaint.display_summary()
    print(f"Date Submitted  : {format_date(complaint.created_at, include_time=True)}")
    print(f"Last Updated    : {format_date(complaint.updated_at, include_time=True)}")
    return complaint


# ----------------------------------------------------------------------
# Registration and login
# ----------------------------------------------------------------------
def register_flow():
    display_header("RESIDENT REGISTRATION")
    full_name = get_non_empty_input("Full name: ", 100)
    address = get_non_empty_input("Address: ", 255)

    while True:  # keep asking until the username is valid and free
        username = get_non_empty_input("Username: ", 50)
        is_valid, message = validate_username(username)
        if not is_valid:
            print(message)
            continue
        if username_exists(username):
            print("That username is already taken. Please choose another.")
            continue
        break

    while True:  # keep asking until the password is valid and confirmed
        password = get_password_input("Password: ")
        is_valid, message = validate_password(password)
        if not is_valid:
            print(message)
            continue
        confirm_password = get_password_input("Confirm password: ")
        if confirm_password != password:
            print("Passwords do not match. Please try again.")
            continue
        break

    register_resident(full_name, address, username, password)
    print("\nRegistration successful! You can now log in.")


def login_flow():
    display_header("LOGIN")
    attempts = 0
    user_row = None
    while attempts < MAX_LOGIN_ATTEMPTS:
        username = get_non_empty_input("Username: ")
        password = get_password_input("Password: ")
        user_row = authenticate_user(username, password)
        if user_row is None:
            attempts += 1
            # Same message for a wrong username or a wrong password.
            print("Invalid username or password.")
            continue
        break

    if user_row is None:
        print("Too many failed attempts. Returning to the main menu.")
        return

    print(f"\nWelcome, {user_row['full_name']}!")
    if user_row["role"] == "resident":
        resident_menu(Resident.from_dict(user_row))
    elif user_row["role"] == "staff":
        staff_menu(Staff.from_dict(user_row))
    else:
        print("This account has an unknown role. Please contact the administrator.")


# ----------------------------------------------------------------------
# Resident features
# ----------------------------------------------------------------------
def submit_complaint_flow(resident):
    display_header("SUBMIT COMPLAINT / REQUEST")
    category = choose_from_list("Select a category:", Complaint.CATEGORIES)
    location = get_non_empty_input("Location: ", 255)

    while True:
        description = get_non_empty_input("Description: ")
        # A temporary Complaint object lets us use len() (Complaint.__len__).
        draft = Complaint(None, "PENDING", resident.user_id, category,
                          location, description)
        if len(draft) < MIN_DESCRIPTION_LENGTH:
            print(f"Please describe it in at least {MIN_DESCRIPTION_LENGTH} characters.")
            continue
        break

    tracking_number = add_complaint(resident.user_id, category, location, description)
    print("\nComplaint submitted successfully!")
    print(f"Tracking Number: {tracking_number}")
    print("Please keep this number to track your complaint.")


def view_my_complaints_flow(resident):
    display_header("MY COMPLAINTS")
    rows = get_complaints_by_user(resident.user_id)  # only this resident's rows
    if not rows:
        print("You have not submitted any complaints yet.")
        return
    table_rows = []
    for row in rows:
        table_rows.append([
            row["tracking_number"], row["category"], row["status"],
            format_date(row["created_at"]),
        ])
    print_table(["Tracking No.", "Category", "Status", "Date"], table_rows)


def track_complaint_flow(resident):
    display_header("TRACK COMPLAINT")
    tracking_number = ask_tracking_number()
    row = get_complaint_by_tracking(tracking_number, resident.user_id)
    if row is None:
        print("No complaint with that tracking number was found in your account.")
        return
    show_complaint_details(row)


def view_updates_flow(resident):
    display_header("COMPLAINT UPDATES")
    tracking_number = ask_tracking_number()
    row = get_complaint_by_tracking(tracking_number, resident.user_id)
    if row is None:
        print("No complaint with that tracking number was found in your account.")
        return
    show_history(row["complaint_id"], row["tracking_number"])


def resident_menu(resident):
    while True:
        display_header("RESIDENT MENU")
        display_messages(
            "1. Submit Complaint/Request",
            "2. View My Complaints",
            "3. Track Complaint",
            "4. View Complaint Updates",
            "5. Logout",
        )
        choice = safe_int_input("\nEnter choice: ", 1, 5)

        if choice == 1:
            run_safely(submit_complaint_flow, resident)
        elif choice == 2:
            run_safely(view_my_complaints_flow, resident)
        elif choice == 3:
            run_safely(track_complaint_flow, resident)
        elif choice == 4:
            run_safely(view_updates_flow, resident)
        else:
            print("You have been logged out.")
            break


# ----------------------------------------------------------------------
# Staff features
# ----------------------------------------------------------------------
def print_staff_complaint_table(rows):
    if not rows:
        print("No complaints found.")
        return
    table_rows = []
    for row in rows:
        table_rows.append([
            row["tracking_number"], row["resident_name"], row["category"],
            row["status"], format_date(row["created_at"]),
            row["assigned_staff_name"] or "-",
        ])
    print_table(
        ["Tracking No.", "Resident", "Category", "Status",
         "Date Submitted", "Assigned Staff"],
        table_rows,
    )


def view_all_complaints_flow():
    display_header("ALL COMPLAINTS")
    print_staff_complaint_table(get_all_complaints())


def search_complaint_flow():
    display_header("SEARCH COMPLAINT")
    display_messages(
        "1. By tracking number", "2. By category", "3. By status", "4. Back"
    )
    choice = safe_int_input("\nEnter choice: ", 1, 4)

    if choice == 1:
        value = get_non_empty_input("Tracking number (full or partial): ").upper()
        rows = search_complaints("tracking_number", value)
    elif choice == 2:
        value = choose_from_list("Select a category:", Complaint.CATEGORIES)
        rows = search_complaints("category", value)
    elif choice == 3:
        value = choose_from_list("Select a status:", Complaint.VALID_STATUSES)
        rows = search_complaints("status", value)
    else:
        return
    print()
    print_staff_complaint_table(rows)


def find_complaint_row():
    """Ask for a tracking number and return the row (or None with a message)."""
    row = get_complaint_by_tracking(ask_tracking_number())
    if row is None:
        print("No complaint found with that tracking number.")
    return row


def view_details_flow():
    display_header("COMPLAINT DETAILS")
    row = find_complaint_row()
    if row is None:
        return
    show_complaint_details(row)
    show_history(row["complaint_id"], row["tracking_number"])


def assign_complaint_flow(staff):
    display_header("ASSIGN COMPLAINT")
    row = find_complaint_row()
    if row is None:
        return
    complaint = show_complaint_details(row)
    if complaint.status in REMARKS_REQUIRED_STATUSES:
        print("\nThis complaint is already resolved/closed and cannot be assigned.")
        return

    staff_list = get_staff_list()
    print("\nAvailable staff:")
    for number, member in enumerate(staff_list, start=1):
        print(f"  {number}. {member['full_name']} - {member['position'] or 'Staff'}")
    picked = staff_list[safe_int_input("Select staff: ", 1, len(staff_list)) - 1]

    extra_remarks = get_optional_input("Remarks (optional): ")
    remarks = f"Assigned to {picked['full_name']}."
    if extra_remarks:
        remarks += f" {extra_remarks}"

    complaint.assign_staff(picked["user_id"], picked["full_name"])
    assign_complaint(complaint.complaint_id, picked["user_id"],
                     staff.user_id, remarks)
    print("\nComplaint assigned successfully.")
    print(create_log_message(
        action="Assigned", tracking_number=complaint.tracking_number,
        staff=picked["full_name"], status=complaint.status,
    ))


def update_status_flow(staff):
    display_header("UPDATE COMPLAINT STATUS")
    row = find_complaint_row()
    if row is None:
        return
    complaint = show_complaint_details(row)

    new_status = choose_from_list("Select the new status:", Complaint.VALID_STATUSES)
    if new_status == complaint.status:
        print("The complaint already has that status.")
        return
    if new_status == "Assigned" and complaint.assigned_staff_id is None:
        print("Please use 'Assign Complaint' to choose who handles it.")
        return

    if new_status in REMARKS_REQUIRED_STATUSES:
        remarks = get_non_empty_input("Remarks (required): ")
    else:
        remarks = get_optional_input("Remarks (optional): ")
    remarks = remarks or f"Status changed to {new_status}."

    try:
        complaint.update_status(new_status, remarks)  # validates the status
    except ValueError as error:
        print(f"Could not update: {error}")
        return

    update_complaint_status(complaint.complaint_id, complaint.status,
                            staff.user_id, remarks)
    print("\nStatus updated successfully.")
    print(create_log_message(
        action="Status updated", tracking_number=complaint.tracking_number,
        new_status=complaint.status, by=staff.full_name,
    ))


def add_remarks_flow(staff):
    display_header("ADD REMARKS")
    row = find_complaint_row()
    if row is None:
        return
    complaint = show_complaint_details(row)
    remarks = get_non_empty_input("Remarks: ")
    complaint.add_remark(remarks)
    add_remark(complaint.complaint_id, staff.user_id, remarks)
    print("\nRemarks saved to the complaint history.")


def statistics_flow():
    display_header("COMPLAINT STATISTICS")
    statistics = get_statistics()  # dictionary: {'Total': 25, 'Submitted': 3, ...}
    print(f"Total Complaints: {statistics['Total']}")
    for status in Complaint.VALID_STATUSES:
        print(f"{status}: {statistics[status]}")

    # ComplaintCount.__add__ adds the counts of all still-open statuses.
    open_total = ComplaintCount("Open complaints")
    for status in Complaint.OPEN_STATUSES:
        open_total = open_total + ComplaintCount(status, statistics[status])
    print(f"\n{open_total}")

    if statistics["Total"] > 0:
        finished = statistics["Resolved"] + statistics["Closed"]
        rate = finished / statistics["Total"] * 100  # float result
        print(f"Resolved/Closed rate: {rate:.1f}%")


def staff_menu(staff):
    while True:
        display_header("STAFF DASHBOARD")
        display_messages(
            "1. View All Complaints",
            "2. Search Complaint",
            "3. View Complaint Details",
            "4. Assign Complaint",
            "5. Update Complaint Status",
            "6. Add Remarks",
            "7. View Statistics",
            "8. Logout",
        )
        choice = safe_int_input("\nEnter choice: ", 1, 8)

        if choice == 1:
            run_safely(view_all_complaints_flow)
        elif choice == 2:
            run_safely(search_complaint_flow)
        elif choice == 3:
            run_safely(view_details_flow)
        elif choice == 4:
            run_safely(assign_complaint_flow, staff)
        elif choice == 5:
            run_safely(update_status_flow, staff)
        elif choice == 6:
            run_safely(add_remarks_flow, staff)
        elif choice == 7:
            run_safely(statistics_flow)
        else:
            print("You have been logged out.")
            break


# ----------------------------------------------------------------------
# Program start
# ----------------------------------------------------------------------
def main():
    try:
        check_connection()
    except DatabaseError as error:
        print(f"[ERROR] {error}")
        return

    while True:
        display_header("BARANGAY AMSIC COMPLAINT SYSTEM")
        display_messages("1. Resident Registration", "2. Login", "3. Exit")
        choice = safe_int_input("\nEnter choice: ", 1, 3)

        if choice == 1:
            run_safely(register_flow)
        elif choice == 2:
            run_safely(login_flow)
        else:
            print("Thank you for using the system. Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped.")
