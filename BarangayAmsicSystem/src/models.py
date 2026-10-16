"""models.py - the OOP classes of the system.

User
├── Resident
└── Staff
Complaint        (separate class)
ComplaintCount   (small helper class that makes __add__ meaningful)
"""


class User:
    """Parent class: attributes every user has."""

    VALID_ROLES = ["resident", "staff"]  # class variable shared by all users

    def __init__(self, user_id, full_name, username, role):
        self.user_id = user_id
        self.full_name = full_name  # goes through the property setter below
        self.username = username
        self.role = role

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        if not value or not value.strip():
            raise ValueError("Full name cannot be empty.")
        self._full_name = value.strip()

    @classmethod
    def from_dict(cls, data):
        """Build an object from a database row (dictionary).

        A class method is used because it creates a NEW object and needs
        the class (cls) - so Resident.from_dict() builds a Resident.
        """
        return cls(data["user_id"], data["full_name"], data["username"], data["role"])

    def __str__(self):
        return f"{self.full_name} ({self.role})"

    def __repr__(self):
        return (
            f"User(user_id={self.user_id!r}, full_name={self.full_name!r}, "
            f"username={self.username!r}, role={self.role!r})"
        )

    def __eq__(self, other):
        """Two users are the same person if they have the same user_id."""
        if not isinstance(other, User):
            return NotImplemented
        return self.user_id == other.user_id

    def __hash__(self):
        # Python removes __hash__ when __eq__ is defined, so we add it back.
        return hash(self.user_id)


class Resident(User):
    """A resident of Barangay Amsic."""

    def __init__(self, user_id, full_name, username, address):
        super().__init__(user_id, full_name, username, "resident")
        self.address = address

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["user_id"], data["full_name"], data["username"],
            data.get("address") or "",
        )

    def __str__(self):
        return f"{super().__str__()} - {self.address}"


class Staff(User):
    """A barangay staff member."""

    def __init__(self, user_id, full_name, username, position):
        super().__init__(user_id, full_name, username, "staff")
        self.position = position

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["user_id"], data["full_name"], data["username"],
            data.get("position") or "Barangay Staff",
        )

    def __str__(self):
        return f"{super().__str__()} - {self.position}"


class Complaint:
    """A complaint or service request submitted by a resident."""

    VALID_STATUSES = [
        "Submitted", "Under Review", "Assigned",
        "In Progress", "Resolved", "Closed",
    ]
    OPEN_STATUSES = ["Submitted", "Under Review", "Assigned", "In Progress"]
    CATEGORIES = [
        "Road/Infrastructure", "Streetlights", "Waste Collection",
        "Water-related Concern", "Environmental Concern", "Noise Complaint",
        "Stray Animals", "Community Safety", "Barangay Service Request", "Other",
    ]

    def __init__(self, complaint_id, tracking_number, user_id, category,
                 location, description, status="Submitted",
                 assigned_staff_id=None, created_at=None, updated_at=None,
                 resident_name=None, assigned_staff_name=None):
        self.complaint_id = complaint_id
        self.tracking_number = tracking_number
        self.user_id = user_id
        self.category = category
        self.location = location
        self.description = description
        self.status = status  # uses the validating setter below
        self.assigned_staff_id = assigned_staff_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.resident_name = resident_name
        self.assigned_staff_name = assigned_staff_name
        self.remarks = []  # temporary list of remarks added in this session

    # --- encapsulation: _status is "protected", accessed via a property ---
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not Complaint.validate_status(value):
            raise ValueError("Invalid complaint status.")
        self._status = value

    @staticmethod
    def validate_status(status):
        """Return True if the status is allowed.

        A static method is used because it needs neither self (one specific
        complaint) nor cls - it only checks a value against the valid list.
        """
        return status in Complaint.VALID_STATUSES

    @classmethod
    def from_dict(cls, data):
        """Create a Complaint from a database row (dictionary)."""
        return cls(
            data["complaint_id"], data["tracking_number"], data["user_id"],
            data["category"], data["location"], data["description"],
            data["status"], data.get("assigned_staff_id"),
            data.get("created_at"), data.get("updated_at"),
            data.get("resident_name"), data.get("assigned_staff_name"),
        )

    # --- behaviour ---
    def update_status(self, new_status, remarks=""):
        """Change the status (validated by the setter) and remember the remark."""
        self.status = new_status
        if remarks:
            self.add_remark(remarks)

    def assign_staff(self, staff_id, staff_name):
        """Assign the complaint to a staff member and mark it Assigned."""
        self.assigned_staff_id = staff_id
        self.assigned_staff_name = staff_name
        self.status = "Assigned"

    def add_remark(self, remark):
        self.remarks.append(remark)

    def is_open(self):
        return self.status in Complaint.OPEN_STATUSES

    def display_summary(self):
        """Print the main details of the complaint."""
        print(f"Tracking Number : {self.tracking_number}")
        if self.resident_name:
            print(f"Resident        : {self.resident_name}")
        print(f"Category        : {self.category}")
        print(f"Location        : {self.location}")
        print(f"Description     : {self.description}")
        print(f"Status          : {self.status}")
        print(f"Assigned Staff  : {self.assigned_staff_name or 'Not yet assigned'}")

    # --- dunder methods ---
    def __str__(self):
        return f"{self.tracking_number} | {self.category} | {self.status}"

    def __repr__(self):
        return (
            f"Complaint(complaint_id={self.complaint_id!r}, "
            f"tracking_number={self.tracking_number!r}, status={self.status!r})"
        )

    def __eq__(self, other):
        """Complaints are equal when they have the same tracking number."""
        if not isinstance(other, Complaint):
            return NotImplemented
        return self.tracking_number == other.tracking_number

    def __hash__(self):
        return hash(self.tracking_number)

    def __len__(self):
        """Length of the description (used to check it is detailed enough)."""
        return len(self.description)


class ComplaintCount:
    """A labelled count, e.g. ('Resolved', 5).

    __add__ is meaningful here: the statistics page adds the counts of
    several statuses to get the total of OPEN complaints.
    """

    def __init__(self, label, count=0):
        self.label = label
        self.count = count

    def __add__(self, other):
        if not isinstance(other, ComplaintCount):
            return NotImplemented
        return ComplaintCount(self.label, self.count + other.count)

    def __str__(self):
        return f"{self.label}: {self.count}"

    def __repr__(self):
        return f"ComplaintCount(label={self.label!r}, count={self.count!r})"
