
import database
import utils
from complaint import Complaint
from user import Resident, Staff


def show_complaints(rows):
    if len(rows) == 0:
        print("No complaints found.")
        return
    for row in rows:
        complaint = Complaint.from_row(row)
        print()
        print(complaint)
        print("   Resident:", complaint.resident_name)
        if complaint.assigned_staff_name is None:
            print("   Assigned: -")
        else:
            print("   Assigned:", complaint.assigned_staff_name)
        print("   Date:", utils.format_date(complaint.created_at))


def show_history(complaint_id, tracking_number):
    history = database.get_history(complaint_id)
    print()
    print("Tracking Number:", tracking_number)
    print("History:")
    for update in history:
        print()
        print(update["status"])
        print("   Date/time:", utils.format_date(update["created_at"]))
        if update["staff_name"] is None:
            print("   Updated by: Resident")
        else:
            print("   Updated by:", update["staff_name"])
        print("   Remarks:", update["remarks"])


# ---------------- registration and login ----------------
def register():
    utils.show_header("RESIDENT REGISTRATION")
    full_name = utils.get_text("Full name: ")
    address = utils.get_text("Address: ")

    while True:
        username = utils.get_text("Username: ")
        if len(username) < 4 or " " in username:
            print("Username must be at least 4 characters and have no spaces.")
            continue
        if database.username_exists(username):
            print("That username is already taken.")
            continue
        break

    while True:
        password = utils.get_text("Password (at least 8 characters): ")
        if len(password) < 8:
            print("Password is too short.")
            continue
        confirm = utils.get_text("Confirm password: ")
        if confirm != password:
            print("Passwords do not match.")
            continue
        break

    database.register_resident(full_name, address, username, utils.hash_password(password))
    print("Registration successful! You can now log in.")


def login():
    utils.show_header("LOGIN")
    attempts = 0
    while attempts < 3:
        username = utils.get_text("Username: ")
        password = utils.get_text("Password: ")
        row = database.login(username, utils.hash_password(password))

        if row is None:
            attempts += 1
            print("Wrong username or password.")
            continue

        print("Welcome,", row["full_name"])
        if row["role"] == "resident":
            resident = Resident(row["user_id"], row["full_name"],
                                row["username"], row["address"])
            resident_menu(resident)
        elif row["role"] == "staff":
            staff = Staff(row["user_id"], row["full_name"],
                          row["username"], row["position"])
            staff_menu(staff)
        return

    print("Too many wrong attempts.")


# ---------------- resident ----------------
def submit_complaint(resident):
    utils.show_header("SUBMIT COMPLAINT / REQUEST")
    category = utils.choose_from_list("Select a category:", Complaint.CATEGORIES)
    location = utils.get_text("Location: ")

    while True:
        description = utils.get_text("Description: ")
        if len(description) < 10:
            print("Please write at least 10 characters.")
            continue
        break

    tracking_number = database.add_complaint(resident.user_id, category, location, description)
    print()
    print("Complaint submitted successfully!")
    print("Tracking Number:", tracking_number)


def view_my_complaints(resident):
    utils.show_header("MY COMPLAINTS")
    rows = database.get_my_complaints(resident.user_id)
    show_complaints(rows)


def track_complaint(resident):
    utils.show_header("TRACK COMPLAINT")
    tracking_number = utils.get_text("Tracking number (example AMS-00001): ").upper()
    row = database.find_my_complaint(tracking_number, resident.user_id)
    if row is None:
        print("Complaint not found in your account.")
        return
    complaint = Complaint.from_row(row)
    complaint.show_details()


def view_updates(resident):
    utils.show_header("COMPLAINT UPDATES")
    tracking_number = utils.get_text("Tracking number (example AMS-00001): ").upper()
    row = database.find_my_complaint(tracking_number, resident.user_id)
    if row is None:
        print("Complaint not found in your account.")
        return
    show_history(row["complaint_id"], row["tracking_number"])


def resident_menu(resident):
    while True:
        utils.show_header("RESIDENT MENU")
        print("1. Submit Complaint/Request")
        print("2. View My Complaints")
        print("3. Track Complaint")
        print("4. View Complaint Updates")
        print("5. Logout")
        choice = utils.get_number("Enter choice: ", 1, 5)

        if choice == 1:
            submit_complaint(resident)
            utils.pause()
        elif choice == 2:
            view_my_complaints(resident)
            utils.pause()
        elif choice == 3:
            track_complaint(resident)
            utils.pause()
        elif choice == 4:
            view_updates(resident)
            utils.pause()
        else:
            print("You are logged out.")
            break


# ---------------- staff ----------------
def view_all_complaints():
    utils.show_header("ALL COMPLAINTS")
    rows = database.get_all_complaints()
    show_complaints(rows)


def search_complaint():
    utils.show_header("SEARCH COMPLAINT")
    print("1. By tracking number")
    print("2. By category")
    print("3. By status")
    print("4. Back")
    choice = utils.get_number("Enter choice: ", 1, 4)

    if choice == 1:
        text = utils.get_text("Tracking number (full or part): ").upper()
        rows = database.search_by_tracking(text)
    elif choice == 2:
        category = utils.choose_from_list("Select a category:", Complaint.CATEGORIES)
        rows = database.search_by_category(category)
    elif choice == 3:
        status = utils.choose_from_list("Select a status:", Complaint.VALID_STATUSES)
        rows = database.search_by_status(status)
    else:
        return
    show_complaints(rows)


def view_details():
    utils.show_header("COMPLAINT DETAILS")
    tracking_number = utils.get_text("Tracking number: ").upper()
    row = database.find_complaint(tracking_number)
    if row is None:
        print("Complaint not found.")
        return
    complaint = Complaint.from_row(row)
    complaint.show_details()
    show_history(complaint.complaint_id, complaint.tracking_number)


def assign_complaint(staff):
    utils.show_header("ASSIGN COMPLAINT")
    tracking_number = utils.get_text("Tracking number: ").upper()
    row = database.find_complaint(tracking_number)
    if row is None:
        print("Complaint not found.")
        return
    complaint = Complaint.from_row(row)
    complaint.show_details()

    if complaint.status == "Resolved" or complaint.status == "Closed":
        print("This complaint is already finished and cannot be assigned.")
        return

    staff_list = database.get_staff_list()
    print()
    print("Available staff:")
    number = 1
    for member in staff_list:
        print(f"{number}. {member['full_name']} - {member['position']}")
        number += 1
    choice = utils.get_number("Select staff: ", 1, len(staff_list))
    chosen = staff_list[choice - 1]

    extra = input("Remarks (optional): ").strip()
    remarks = "Assigned to " + chosen["full_name"] + "."
    if extra != "":
        remarks = remarks + " " + extra

    database.assign_complaint(complaint.complaint_id, chosen["user_id"], staff.user_id, remarks)
    print("Complaint assigned successfully.")


def update_complaint_status(staff):
    utils.show_header("UPDATE COMPLAINT STATUS")
    tracking_number = utils.get_text("Tracking number: ").upper()
    row = database.find_complaint(tracking_number)
    if row is None:
        print("Complaint not found.")
        return
    complaint = Complaint.from_row(row)
    complaint.show_details()

    new_status = utils.choose_from_list("Select the new status:", Complaint.VALID_STATUSES)
    if new_status == complaint.status:
        print("The complaint already has that status.")
        return
    if new_status == "Assigned" and complaint.assigned_staff_id is None:
        print("Please use Assign Complaint first.")
        return

    # remarks are required when the complaint is finished
    if new_status == "Resolved" or new_status == "Closed":
        remarks = utils.get_text("Remarks (required): ")
    else:
        remarks = input("Remarks (optional): ").strip()
        if remarks == "":
            remarks = "Status changed to " + new_status + "."

    complaint.update_status(new_status)
    database.update_status(complaint.complaint_id, complaint.status, staff.user_id, remarks)
    print("Status updated successfully.")


def add_remarks(staff):
    utils.show_header("ADD REMARKS")
    tracking_number = utils.get_text("Tracking number: ").upper()
    row = database.find_complaint(tracking_number)
    if row is None:
        print("Complaint not found.")
        return
    complaint = Complaint.from_row(row)
    remarks = utils.get_text("Remarks: ")
    database.add_remark(complaint.complaint_id, staff.user_id, complaint.status, remarks)
    print("Remarks saved.")


def view_statistics():
    utils.show_header("COMPLAINT STATISTICS")
    stats = database.get_statistics(Complaint.VALID_STATUSES)
    print("Total Complaints:", stats["Total"])
    for status in Complaint.VALID_STATUSES:
        print(f"{status}: {stats[status]}")

    if stats["Total"] > 0:
        finished = stats["Resolved"] + stats["Closed"]
        percent = finished / stats["Total"] * 100
        print()
        print("Resolved/Closed:", round(percent, 1), "%")


def staff_menu(staff):
    while True:
        utils.show_header("STAFF DASHBOARD")
        print("1. View All Complaints")
        print("2. Search Complaint")
        print("3. View Complaint Details")
        print("4. Assign Complaint")
        print("5. Update Complaint Status")
        print("6. Add Remarks")
        print("7. View Statistics")
        print("8. Logout")
        choice = utils.get_number("Enter choice: ", 1, 8)

        if choice == 1:
            view_all_complaints()
            utils.pause()
        elif choice == 2:
            search_complaint()
            utils.pause()
        elif choice == 3:
            view_details()
            utils.pause()
        elif choice == 4:
            assign_complaint(staff)
            utils.pause()
        elif choice == 5:
            update_complaint_status(staff)
            utils.pause()
        elif choice == 6:
            add_remarks(staff)
            utils.pause()
        elif choice == 7:
            view_statistics()
            utils.pause()
        else:
            print("You are logged out.")
            break


# ---------------- main menu ----------------
def main():
    while True:
        utils.show_header("BARANGAY AMSIC COMPLAINT SYSTEM")
        print("1. Resident Registration")
        print("2. Login")
        print("3. Exit")
        choice = utils.get_number("Enter choice: ", 1, 3)

        if choice == 1:
            register()
            utils.pause()
        elif choice == 2:
            login()
            utils.pause()
        else:
            print("Thank you for using the system. Goodbye!")
            break


main()
