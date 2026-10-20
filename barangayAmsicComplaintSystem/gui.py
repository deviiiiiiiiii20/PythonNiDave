
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import database
import utils
from complaint import Complaint
from user import Resident, Staff


def say(message):
    messagebox.showinfo("Barangay Amsic", message)


def complaints_text(rows):
    if len(rows) == 0:
        return "No complaints found."
    text = ""
    for row in rows:
        complaint = Complaint.from_row(row)
        text += str(complaint) + "\n"
        text += "   Resident: " + str(complaint.resident_name) + "\n"
        if complaint.assigned_staff_name is None:
            text += "   Assigned: -\n"
        else:
            text += "   Assigned: " + complaint.assigned_staff_name + "\n"
        text += "   Date: " + utils.format_date(complaint.created_at) + "\n\n"
    return text


def details_text(complaint):
    text = "Tracking Number: " + complaint.tracking_number + "\n"
    text += "Resident: " + str(complaint.resident_name) + "\n"
    text += "Category: " + complaint.category + "\n"
    text += "Location: " + complaint.location + "\n"
    text += "Description: " + complaint.description + "\n"
    text += "Status: " + complaint.status + "\n"
    if complaint.assigned_staff_name is None:
        text += "Assigned Staff: Not yet assigned\n"
    else:
        text += "Assigned Staff: " + complaint.assigned_staff_name + "\n"
    text += "Date Submitted: " + utils.format_date(complaint.created_at) + "\n"
    text += "Last Updated: " + utils.format_date(complaint.updated_at) + "\n"
    return text


def history_text(complaint_id, tracking_number):
    history = database.get_history(complaint_id)
    text = "Tracking Number: " + tracking_number + "\n\nHistory:\n"
    for update in history:
        text += "\n" + update["status"] + "\n"
        text += "   Date/time: " + utils.format_date(update["created_at"]) + "\n"
        if update["staff_name"] is None:
            text += "   Updated by: Resident\n"
        else:
            text += "   Updated by: " + update["staff_name"] + "\n"
        text += "   Remarks: " + str(update["remarks"]) + "\n"
    return text


class BarangayGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Barangay Amsic Complaint and Request Tracking System")
        self.window.geometry("900x580")
        self.user = None
        self.content = None
        self.output = None
        self.show_login()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def make_title(self, text):
        tk.Label(self.content, text=text, font=("Arial", 14, "bold")).pack(anchor="w", pady=5)

    def make_form(self):
        form = tk.Frame(self.content)
        form.pack(anchor="w", pady=5)
        return form

    def add_entry(self, form, label_text, row, width=40):
        tk.Label(form, text=label_text).grid(row=row, column=0, sticky="e", padx=5, pady=4)
        entry = tk.Entry(form, width=width)
        entry.grid(row=row, column=1, sticky="w", pady=4)
        return entry

    def add_box(self, form, label_text, row, values):
        tk.Label(form, text=label_text).grid(row=row, column=0, sticky="e", padx=5, pady=4)
        box = ttk.Combobox(form, values=values, state="readonly", width=37)
        box.grid(row=row, column=1, sticky="w", pady=4)
        return box

    def make_output(self):
        holder = tk.Frame(self.content)
        holder.pack(fill="both", expand=True, pady=10)
        scrollbar = tk.Scrollbar(holder)
        scrollbar.pack(side="right", fill="y")
        output = tk.Text(holder, height=15, width=70, state="disabled",
                         yscrollcommand=scrollbar.set)
        output.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=output.yview)
        self.output = output

    def set_output(self, text):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", text)
        self.output.config(state="disabled")

    def make_dashboard(self, title, buttons):
        self.clear_window()
        left = tk.Frame(self.window, bg="#dddddd", width=220)
        left.pack(side="left", fill="y")
        tk.Label(left, text=title, font=("Arial", 12, "bold"), bg="#dddddd").pack(pady=10)
        tk.Label(left, text=self.user.full_name, bg="#dddddd").pack(pady=5)
        for button in buttons:
            tk.Button(left, text=button[0], width=22, command=button[1]).pack(pady=4, padx=10)
        self.content = tk.Frame(self.window)
        self.content.pack(side="left", fill="both", expand=True, padx=15, pady=10)

    def make_tracking_form(self, title, button_text, command):
        self.clear_content()
        self.make_title(title)
        form = self.make_form()
        self.tracking_entry = self.add_entry(form, "Tracking number:", 0, 25)
        tk.Button(form, text=button_text, command=command).grid(row=0, column=2, padx=10)
        self.make_output()

    def show_login(self):
        self.clear_window()
        frame = tk.Frame(self.window)
        frame.pack(pady=70)
        tk.Label(frame, text="BARANGAY AMSIC COMPLAINT SYSTEM",
                 font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        self.username_entry = self.add_entry(frame, "Username:", 1, 30)
        self.password_entry = self.add_entry(frame, "Password:", 2, 30)
        self.password_entry.config(show="*")
        tk.Button(frame, text="Login", width=20, command=self.do_login).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Register as Resident", width=20,
                  command=self.show_register).grid(row=4, column=0, columnspan=2)

    def do_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if username == "" or password == "":
            say("Please type your username and password.")
            return

        row = database.login(username, utils.hash_password(password))
        if row is None:
            say("Wrong username or password.")
            return

        if row["role"] == "resident":
            self.user = Resident(row["user_id"], row["full_name"],
                                 row["username"], row["address"])
            self.show_resident_menu()
        elif row["role"] == "staff":
            self.user = Staff(row["user_id"], row["full_name"],
                              row["username"], row["position"])
            self.show_staff_menu()

    def show_register(self):
        self.clear_window()
        frame = tk.Frame(self.window)
        frame.pack(pady=40)
        tk.Label(frame, text="RESIDENT REGISTRATION",
                 font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=15)
        self.name_entry = self.add_entry(frame, "Full name:", 1, 30)
        self.address_entry = self.add_entry(frame, "Address:", 2, 30)
        self.username_entry = self.add_entry(frame, "Username:", 3, 30)
        self.password_entry = self.add_entry(frame, "Password:", 4, 30)
        self.confirm_entry = self.add_entry(frame, "Confirm password:", 5, 30)
        self.password_entry.config(show="*")
        self.confirm_entry.config(show="*")
        tk.Button(frame, text="Register", width=20, command=self.do_register).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Back to Login", width=20, command=self.show_login).grid(row=7, column=0, columnspan=2)

    def do_register(self):
        full_name = self.name_entry.get().strip()
        address = self.address_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        if full_name == "" or address == "":
            say("Please fill in your full name and address.")
            return
        if len(username) < 4 or " " in username:
            say("Username must be at least 4 characters and have no spaces.")
            return
        if database.username_exists(username):
            say("That username is already taken.")
            return
        if len(password) < 8:
            say("Password must be at least 8 characters.")
            return
        if password != confirm:
            say("Passwords do not match.")
            return

        database.register_resident(full_name, address, username, utils.hash_password(password))
        say("Registration successful! You can now log in.")
        self.show_login()

    def logout(self):
        self.user = None
        self.show_login()

    def show_change_password(self):
        self.clear_content()
        self.make_title("Change Password")
        form = self.make_form()
        self.old_password_entry = self.add_entry(form, "Old password:", 0, 30)
        self.new_password_entry = self.add_entry(form, "New password:", 1, 30)
        self.confirm_new_entry = self.add_entry(form, "Confirm new password:", 2, 30)
        self.old_password_entry.config(show="*")
        self.new_password_entry.config(show="*")
        self.confirm_new_entry.config(show="*")
        tk.Button(form, text="Change Password", width=20,
                  command=self.change_password_clicked).grid(row=3, column=1, sticky="w", pady=10)

    def change_password_clicked(self):
        old_password = self.old_password_entry.get().strip()
        new_password = self.new_password_entry.get().strip()
        confirm = self.confirm_new_entry.get().strip()

        if old_password == "" or new_password == "" or confirm == "":
            say("Please fill in all the password fields.")
            return
        if database.login(self.user.username, utils.hash_password(old_password)) is None:
            say("Old password is wrong.")
            return
        if len(new_password) < 8:
            say("New password must be at least 8 characters.")
            return
        if new_password == old_password:
            say("New password must be different from the old password.")
            return
        if new_password != confirm:
            say("New passwords do not match.")
            return

        database.change_password(self.user.user_id, utils.hash_password(new_password))
        say("Password changed successfully!")
        self.show_change_password()

    def show_resident_menu(self):
        buttons = [
            ("Submit Complaint/Request", self.show_submit),
            ("View My Complaints", self.show_my_complaints),
            ("Track Complaint", self.show_track),
            ("View Complaint Updates", self.show_updates),
            ("Change Password", self.show_change_password),
            ("Logout", self.logout),
        ]
        self.make_dashboard("RESIDENT MENU", buttons)
        self.make_title("Welcome, " + self.user.full_name)

    def show_submit(self):
        self.clear_content()
        self.make_title("Submit Complaint / Request")
        form = self.make_form()
        self.category_box = self.add_box(form, "Category:", 0, Complaint.CATEGORIES)
        self.location_entry = self.add_entry(form, "Location:", 1)
        tk.Label(form, text="Description:").grid(row=2, column=0, sticky="ne", padx=5, pady=4)
        self.description_box = tk.Text(form, height=6, width=40)
        self.description_box.grid(row=2, column=1, sticky="w", pady=4)
        tk.Button(form, text="Submit", width=15, command=self.save_complaint).grid(row=3, column=1, sticky="w", pady=10)

    def save_complaint(self):
        category = self.category_box.get()
        location = self.location_entry.get().strip()
        description = self.description_box.get("1.0", "end").strip()

        if category == "" or location == "" or description == "":
            say("Please choose a category and fill in the location and description.")
            return
        if len(description) < 10:
            say("Please write at least 10 characters in the description.")
            return

        tracking_number = database.add_complaint(self.user.user_id, category, location, description)
        say("Complaint submitted successfully!\n\nTracking Number: " + tracking_number)
        self.show_submit()

    def show_my_complaints(self):
        self.clear_content()
        self.make_title("My Complaints")
        self.make_output()
        rows = database.get_my_complaints(self.user.user_id)
        self.set_output(complaints_text(rows))

    def show_track(self):
        self.make_tracking_form("Track Complaint", "Track", self.track_complaint)

    def track_complaint(self):
        tracking_number = self.tracking_entry.get().strip().upper()
        if tracking_number == "":
            say("Please type a tracking number.")
            return
        row = database.find_my_complaint(tracking_number, self.user.user_id)
        if row is None:
            say("Complaint not found in your account.")
            return
        self.set_output(details_text(Complaint.from_row(row)))

    def show_updates(self):
        self.make_tracking_form("Complaint Updates", "View", self.view_updates)

    def view_updates(self):
        tracking_number = self.tracking_entry.get().strip().upper()
        if tracking_number == "":
            say("Please type a tracking number.")
            return
        row = database.find_my_complaint(tracking_number, self.user.user_id)
        if row is None:
            say("Complaint not found in your account.")
            return
        self.set_output(history_text(row["complaint_id"], row["tracking_number"]))


    def show_staff_menu(self):
        buttons = [
            ("View All Complaints", self.show_all),
            ("Search Complaint", self.show_search),
            ("View Complaint Details", self.show_details),
            ("Assign Complaint", self.show_assign),
            ("Update Complaint Status", self.show_update_status),
            ("Add Remarks", self.show_remarks),
            ("View Statistics", self.show_statistics),
            ("Change Password", self.show_change_password),
            ("Logout", self.logout),
        ]
        self.make_dashboard("STAFF DASHBOARD", buttons)
        self.make_title("Welcome, " + self.user.full_name)

    def show_all(self):
        self.clear_content()
        self.make_title("All Complaints")
        self.make_output()
        self.set_output(complaints_text(database.get_all_complaints()))

    def show_search(self):
        self.clear_content()
        self.make_title("Search Complaint")
        form = self.make_form()
        self.search_entry = self.add_entry(form, "Tracking number:", 0, 25)
        tk.Button(form, text="Search", command=self.search_tracking).grid(row=0, column=2, padx=10)
        self.search_category_box = self.add_box(form, "Category:", 1, Complaint.CATEGORIES)
        tk.Button(form, text="Search", command=self.search_category).grid(row=1, column=2, padx=10)
        self.search_status_box = self.add_box(form, "Status:", 2, Complaint.VALID_STATUSES)
        tk.Button(form, text="Search", command=self.search_status).grid(row=2, column=2, padx=10)
        self.make_output()

    def search_tracking(self):
        text = self.search_entry.get().strip().upper()
        if text == "":
            say("Please type a tracking number.")
            return
        self.set_output(complaints_text(database.search_by_tracking(text)))

    def search_category(self):
        category = self.search_category_box.get()
        if category == "":
            say("Please choose a category.")
            return
        self.set_output(complaints_text(database.search_by_category(category)))

    def search_status(self):
        status = self.search_status_box.get()
        if status == "":
            say("Please choose a status.")
            return
        self.set_output(complaints_text(database.search_by_status(status)))

    def show_details(self):
        self.make_tracking_form("Complaint Details", "View", self.view_details)

    def view_details(self):
        tracking_number = self.tracking_entry.get().strip().upper()
        if tracking_number == "":
            say("Please type a tracking number.")
            return
        row = database.find_complaint(tracking_number)
        if row is None:
            say("Complaint not found.")
            return
        complaint = Complaint.from_row(row)
        text = details_text(complaint) + "\n" + history_text(complaint.complaint_id, complaint.tracking_number)
        self.set_output(text)

    def show_assign(self):
        self.clear_content()
        self.make_title("Assign Complaint")
        form = self.make_form()
        self.tracking_entry = self.add_entry(form, "Tracking number:", 0)

        self.staff_list = database.get_staff_list()
        names = []
        for member in self.staff_list:
            names.append(member["full_name"] + " - " + str(member["position"]))
        self.staff_box = self.add_box(form, "Assign to:", 1, names)

        self.remarks_entry = self.add_entry(form, "Remarks (optional):", 2)
        tk.Button(form, text="Assign", width=15, command=self.assign_clicked).grid(row=3, column=1, sticky="w", pady=10)

    def assign_clicked(self):
        tracking_number = self.tracking_entry.get().strip().upper()
        index = self.staff_box.current()
        if tracking_number == "" or index == -1:
            say("Please type a tracking number and choose a staff member.")
            return
        row = database.find_complaint(tracking_number)
        if row is None:
            say("Complaint not found.")
            return
        complaint = Complaint.from_row(row)
        if complaint.status == "Resolved" or complaint.status == "Closed":
            say("This complaint is already finished and cannot be assigned.")
            return

        chosen = self.staff_list[index]
        remarks = "Assigned to " + chosen["full_name"] + "."
        extra = self.remarks_entry.get().strip()
        if extra != "":
            remarks = remarks + " " + extra

        database.assign_complaint(complaint.complaint_id, chosen["user_id"], self.user.user_id, remarks)
        say("Complaint assigned successfully.")
        self.show_assign()

    def show_update_status(self):
        self.clear_content()
        self.make_title("Update Complaint Status")
        form = self.make_form()
        self.tracking_entry = self.add_entry(form, "Tracking number:", 0)
        self.status_box = self.add_box(form, "New status:", 1, Complaint.VALID_STATUSES)
        self.remarks_entry = self.add_entry(form, "Remarks:", 2)
        tk.Label(form, text="(Remarks are required for Resolved and Closed)").grid(row=3, column=1, sticky="w")
        tk.Button(form, text="Update", width=15, command=self.update_clicked).grid(row=4, column=1, sticky="w", pady=10)

    def update_clicked(self):
        tracking_number = self.tracking_entry.get().strip().upper()
        new_status = self.status_box.get()
        remarks = self.remarks_entry.get().strip()
        if tracking_number == "" or new_status == "":
            say("Please type a tracking number and choose a status.")
            return
        row = database.find_complaint(tracking_number)
        if row is None:
            say("Complaint not found.")
            return
        complaint = Complaint.from_row(row)
        if new_status == complaint.status:
            say("The complaint already has that status.")
            return
        if new_status == "Assigned" and complaint.assigned_staff_id is None:
            say("Please use Assign Complaint first.")
            return
        if (new_status == "Resolved" or new_status == "Closed") and remarks == "":
            say("Please type remarks for Resolved or Closed.")
            return
        if remarks == "":
            remarks = "Status changed to " + new_status + "."

        complaint.update_status(new_status)
        database.update_status(complaint.complaint_id, complaint.status, self.user.user_id, remarks)
        say("Status updated successfully.")
        self.show_update_status()

    def show_remarks(self):
        self.clear_content()
        self.make_title("Add Remarks")
        form = self.make_form()
        self.tracking_entry = self.add_entry(form, "Tracking number:", 0)
        self.remarks_entry = self.add_entry(form, "Remarks:", 1)
        tk.Button(form, text="Save", width=15, command=self.remarks_clicked).grid(row=2, column=1, sticky="w", pady=10)

    def remarks_clicked(self):
        tracking_number = self.tracking_entry.get().strip().upper()
        remarks = self.remarks_entry.get().strip()
        if tracking_number == "" or remarks == "":
            say("Please type a tracking number and your remarks.")
            return
        row = database.find_complaint(tracking_number)
        if row is None:
            say("Complaint not found.")
            return
        complaint = Complaint.from_row(row)
        database.add_remark(complaint.complaint_id, self.user.user_id, complaint.status, remarks)
        say("Remarks saved.")
        self.show_remarks()

    def show_statistics(self):
        self.clear_content()
        self.make_title("Complaint Statistics")
        self.make_output()
        stats = database.get_statistics(Complaint.VALID_STATUSES)
        text = "Total Complaints: " + str(stats["Total"]) + "\n\n"
        for status in Complaint.VALID_STATUSES:
            text += status + ": " + str(stats[status]) + "\n"
        if stats["Total"] > 0:
            finished = stats["Resolved"] + stats["Closed"]
            percent = finished / stats["Total"] * 100
            text += "\nResolved/Closed: " + str(round(percent, 1)) + " %\n"
        self.set_output(text)


if __name__ == "__main__":
    window = tk.Tk()
    app = BarangayGUI(window)
    window.mainloop()
