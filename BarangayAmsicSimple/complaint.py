from utils import format_date


class Complaint:
    VALID_STATUSES = ["Submitted", "Under Review", "Assigned",
                      "In Progress", "Resolved", "Closed"]
    CATEGORIES = ["Road/Infrastructure", "Streetlights", "Waste Collection",
                  "Water-related Concern", "Environmental Concern",
                  "Noise Complaint", "Stray Animals", "Community Safety",
                  "Barangay Service Request", "Other"]

    def __init__(self, complaint_id, tracking_number, category, location,
                 description, status):
        self.complaint_id = complaint_id
        self.tracking_number = tracking_number
        self.category = category
        self.location = location
        self.description = description
        self._status = "Submitted"
        self.status = status
        self.assigned_staff_id = None
        self.assigned_staff_name = None
        self.resident_name = None
        self.created_at = None
        self.updated_at = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        if Complaint.validate_status(new_status):
            self._status = new_status

    @staticmethod
    def validate_status(status):
        return status in Complaint.VALID_STATUSES

    @classmethod
    def from_row(cls, row):
        complaint = cls(row["complaint_id"], row["tracking_number"],
                        row["category"], row["location"],
                        row["description"], row["status"])
        complaint.assigned_staff_id = row["assigned_staff_id"]
        complaint.assigned_staff_name = row["assigned_staff_name"]
        complaint.resident_name = row["resident_name"]
        complaint.created_at = row["created_at"]
        complaint.updated_at = row["updated_at"]
        return complaint

    def update_status(self, new_status):
        self.status = new_status

    def show_details(self):
        print()
        print("Tracking Number :", self.tracking_number)
        print("Resident        :", self.resident_name)
        print("Category        :", self.category)
        print("Location        :", self.location)
        print("Description     :", self.description)
        print("Status          :", self.status)
        if self.assigned_staff_name is None:
            print("Assigned Staff  : Not yet assigned")
        else:
            print("Assigned Staff  :", self.assigned_staff_name)
        print("Date Submitted  :", format_date(self.created_at))
        print("Last Updated    :", format_date(self.updated_at))

    def __str__(self):
        return self.tracking_number + " | " + self.category + " | " + self.status

    def __repr__(self):
        return f"Complaint({self.complaint_id}, {self.tracking_number})"

    def __eq__(self, other):
        return self.tracking_number == other.tracking_number
