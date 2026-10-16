# Project Guide: Barangay Amsic Complaint and Request Tracking System

This file covers the non-code parts: architecture, setup, the outline for
`System_Documentation.pdf`, class diagram, ERD, course requirement mapping,
test steps, common errors and the final checklist.

---

## PART 1 - Project architecture

```
 main.py  (menus, input, flow)
    |  calls
    +--> utils.py     helpers: validation, hashing, table printing
    +--> models.py    OOP objects: User, Resident, Staff, Complaint, ComplaintCount
    +--> database.py  ONLY place with SQL -> MySQL (barangay_amsic)
                         |
                         +--> imports models.py (status list) and utils.py (hashing, tracking number)
```
- `main.py` never contains SQL; it calls functions such as `add_complaint()`.
- `models.py` imports nothing from the other project files (no circular imports).
- Query results are returned as **dictionaries**; `from_dict()` turns them into objects.

## PART 2 - Folder structure

```
BarangayAmsicSystem/
├── docs/
│   ├── PROJECT_GUIDE.md          (this file)
│   └── System_Documentation.pdf  (you create it from Part 11)
├── src/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   └── utils.py
├── schema.sql
├── requirements.txt
└── README.md
```
Create the folders in VS Code (New Folder) or in a terminal:
`mkdir BarangayAmsicSystem`, `cd BarangayAmsicSystem`, `mkdir src docs`.

## PART 3 - MySQL installation / setup (Windows 11)

1. Install XAMPP, open the Control Panel, click **Start** for **MySQL** (Apache is only needed for phpMyAdmin).
2. Open `http://localhost/phpmyadmin` -> **SQL** tab -> paste all of `schema.sql` -> **Go**.
3. Check that database `barangay_amsic` has three tables: `users`, `complaints`, `complaint_updates`.
4. If your `root` account has a password, set it in `DB_CONFIG` in `src/database.py`.

Why indexes? An index lets MySQL find rows without reading the whole table:
`username` (login), `tracking_number` (tracking), `user_id` (a resident's complaints),
`status` (search/statistics), `assigned_staff_id`, and `complaint_id` in `complaint_updates` (history).

Parts 4-10 (schema.sql, requirements.txt, models.py, database.py, utils.py, main.py, README.md) are the project files themselves.

---

## PART 11 - Outline for `System_Documentation.pdf`

1. **Title** - Proposed Barangay Complaint and Request Tracking System for Barangay Amsic.
2. **System Overview** - CLI system (Python + MySQL) that records, tracks and reports complaints/requests.
3. **Problem Statement** - Complaints and requests are scattered across Facebook posts, messages and verbal reports. Residents cannot tell if their concern was formally received, who handles it, or its status; staff find it hard to organize and monitor them. (Officials not responding is *not* the problem.)
4. **Objectives** - Provide a formal submission channel with tracking numbers; let staff assign, update and monitor; keep a history; show basic statistics.
5. **Scope and Limitations** - Barangay Amsic only. Does not replace Facebook, emergency services or legal decisions; does not guarantee resolution or judge validity; not real-time.
6. **Users** - Resident; Staff.
7. **System Features** - resident and staff features listed in the README.
8. **System Architecture** - Part 1 above (four modules + MySQL).
9. **Class Diagram Explanation** - Part 12 below.
10. **Database Design** - three tables, InnoDB, foreign keys, indexes, hashed passwords.
11. **ERD Explanation** - Part 13 below.
12. **Table Descriptions** - field-by-field from `schema.sql` (include `position` and the nullable `staff_id`).
13. **Python Concepts Demonstrated** - Part 14 table (variables, strings, ints, floats, booleans, lists, dicts, casting, f-strings, functions, loops, try/except, imports).
14. **OOP Concepts** - classes, constructors, inheritance, `super()`, properties, class/static methods, dunder methods.
15. **System Flow** - Start -> Main menu -> Register/Login/Exit -> role check -> Resident or Staff menu -> actions -> Logout -> Main menu -> Exit. Resident: submit, view, track, updates. Staff: view, search, details, assign, status, remarks, statistics.
16. **Testing** - table from Part 16 (test, input, expected, result).
17. **Known Limitations** - no admin screen (staff accounts are created in the database); no password reset; no complaint deletion/editing; no notifications; single barangay; console only; input is not logged.
18. **Conclusion** - The system gives residents a formal, trackable channel and gives staff an organized record, while demonstrating Python and OOP concepts.

## PART 12 - Class diagram explanation

```
          User
         /    \
   Resident   Staff

   Complaint        ComplaintCount
```
- **User (parent):** `user_id`, `full_name` (property), `username`, `role`; class variable `VALID_ROLES`; `from_dict()`, `__str__`, `__repr__`, `__eq__`, `__hash__`.
- **Resident (child):** inherits the above, adds `address`; calls `super().__init__()` with role `"resident"`.
- **Staff (child):** inherits the above, adds `position`; role `"staff"`. Staff does **not** inherit from Resident.
- **Complaint (separate):** `complaint_id`, `tracking_number`, `user_id`, `category`, `location`, `description`, `status` (property, stored in `_status`), `assigned_staff_id`, `created_at`, `updated_at`. Methods: `update_status()`, `assign_staff()`, `add_remark()`, `is_open()`, `display_summary()`. Class variables `VALID_STATUSES`, `OPEN_STATUSES`, `CATEGORIES`. Static `validate_status()`, class `from_dict()`. Dunder: `__str__`, `__repr__`, `__eq__`, `__hash__`, `__len__`.
- **ComplaintCount (helper):** a label plus a number; `__add__` adds counts.

## PART 13 - ERD explanation

```
USERS (user_id PK) --1:M--> COMPLAINTS (complaint_id PK) --1:M--> COMPLAINT_UPDATES (update_id PK)
```
- `users.user_id` - primary key.
- `complaints.user_id` - FK -> `users.user_id` (the resident who submitted it).
- `complaints.assigned_staff_id` - FK -> `users.user_id`, nullable (the staff handling it). A staff member can have many complaints.
- `complaint_updates.complaint_id` - FK -> `complaints.complaint_id` (one complaint, many updates).
- `complaint_updates.staff_id` - FK -> `users.user_id`, nullable (NULL for the resident's own "Submitted" record).

---

## PART 14 - Course requirement mapping

| Requirement | File | Example |
|---|---|---|
| Classes | models.py | `class User`, `Resident`, `Staff`, `Complaint`, `ComplaintCount` |
| Constructor / `self` / instance variables | models.py | `Complaint.__init__`, `self.tracking_number` |
| Class variables | models.py | `Complaint.VALID_STATUSES`, `Complaint.CATEGORIES`, `User.VALID_ROLES` |
| Instance methods | models.py | `Complaint.update_status()`, `assign_staff()`, `display_summary()` |
| Inheritance | models.py | `class Resident(User)`, `class Staff(User)` |
| `super()` | models.py | `super().__init__(user_id, full_name, username, "resident")` |
| Encapsulation / `@property` / setter | models.py | `Complaint.status` + `_status`; `User.full_name` |
| Class method | models.py | `from_dict()` (builds an object from a DB row; `cls` makes subclasses build themselves) |
| Static method | models.py | `Complaint.validate_status()` (needs no `self`/`cls`) |
| `__str__` | models.py | `str(complaint)` -> `AMS-00001 \| Streetlights \| Submitted` |
| `__repr__` | models.py | `repr(complaint)` -> `Complaint(complaint_id=1, ...)` |
| `__eq__` (+ `__hash__`) | models.py | complaints equal when tracking numbers match; users when `user_id` matches |
| `__len__` | models.py / main.py | `len(draft)` checks the description length in `submit_complaint_flow` |
| `__add__` | models.py / main.py | `ComplaintCount.__add__`, used in `statistics_flow` to total open complaints |
| Variables, strings, ints, booleans | all files | `attempts = 0`, `is_valid`, `tracking_number` |
| Floats | main.py | `rate = finished / total * 100`, shown with `:.1f` |
| Lists | models.py / main.py | `Complaint.CATEGORIES`, `table_rows` |
| Dictionaries | database.py | `DB_CONFIG`, `SEARCH_CLAUSES`, rows from `cursor(dictionary=True)`, `get_statistics()` |
| Type casting | utils.py | `int(raw_text)` in `safe_int_input`; `str(text)` in `_shorten` |
| f-strings | all files | `f"AMS-{complaint_id:05d}"` |
| Functions / parameters / return | utils.py | `hash_password(password, salt=None)` |
| `*args` | utils.py / main.py | `display_messages(*messages)`, `run_safely(action, *args)` |
| `**kwargs` | utils.py / main.py | `create_log_message(**kwargs)` (called in assign/status flows); `connect(**DB_CONFIG)` is dictionary unpacking |
| if / elif / else | main.py | menu choices in `resident_menu`, `staff_menu` |
| for | main.py / utils.py | `show_history`, `print_table`, `choose_from_list` |
| while | main.py / utils.py | menu loops, `login_flow`, `safe_int_input` |
| `range()` | utils.py | `range(min_value, max_value + 1)` in `safe_int_input` |
| break / continue | main.py | `register_flow` (`continue` on bad input, `break` when valid); menus `break` on logout |
| pass | database.py | empty class body of `DatabaseError` |
| try / except | utils.py / database.py / main.py | `int()` conversion; `mysql.connector.Error`; `except DatabaseError` |
| imports / modules | main.py | `from database import ...`, `from models import ...` |
| MySQL | database.py | `import mysql.connector`, `get_connection()` |
| SQL INSERT | database.py | `register_resident`, `add_complaint` |
| SQL SELECT | database.py | `_fetch_all`, `get_complaint_by_tracking`, `get_statistics` (`COUNT`, `GROUP BY`) |
| SQL UPDATE | database.py | `update_complaint_status`, `assign_complaint` |
| SQL DELETE | - | not implemented on purpose (see conflicts below) |
| Transactions | database.py | `connection.commit()` / `connection.rollback()` |
| Indexes | schema.sql | `UNIQUE KEY` on username and tracking_number; `KEY idx_complaints_status`, ... |
| Password hashing | utils.py | `hashlib.pbkdf2_hmac` in `hash_password` |

**Lists and dictionaries with MySQL:** MySQL stores the permanent data. Python lists/dictionaries only hold
temporary data: category/status lists, query results (list of dict rows), and the statistics dictionary. Nothing replaces MySQL.

**Conflicts / decisions to mention to your instructor:**
- **DELETE:** your spec says "if necessary" and also "do not delete previous history". No feature needs it, so no DELETE exists. If your course requires one, add a function that deletes a *test* user only.
- **`__add__`:** adding two complaints makes no sense, so it lives in the small `ComplaintCount` class, where adding counts is natural.
- **`users.position`:** the spec gives `Staff` a `position` attribute, so the `users` table has a nullable `position` column.
- **`complaint_updates.staff_id` is nullable:** the first "Submitted" record is created by the resident, not staff.
- **Tracking number:** a temporary unique value is inserted, then replaced by `AMS-` + the new ID inside the same transaction.
- **Not included:** the optional `Rejected` status and an `admin` role, to keep the project simple.

## PART 15 - Step-by-step run

1. Start MySQL in XAMPP. 2. Run `schema.sql` in phpMyAdmin. 3. Open the folder in VS Code.
4. `python -m venv venv` 5. `venv\Scripts\activate` 6. `pip install -r requirements.txt`
7. Check `DB_CONFIG` in `src/database.py`. 8. `python src/main.py`

## PART 16 - How to test every major feature

| # | Test | Steps | Expected |
|---|---|---|---|
| 1 | Invalid menu input | Main menu: type `abc`, then `9` | Messages, menu stays |
| 2 | Register | Option 1, new username, password with letter+number | "Registration successful" |
| 3 | Duplicate username | Register `resident1` | "already taken" |
| 4 | Weak password | `short1` | Rejected (min 8 chars) |
| 5 | Wrong login | Login with wrong password | "Invalid username or password."; 3 failures return to main menu |
| 6 | Resident login | `resident1` / `Resident123!` | Resident menu |
| 7 | Submit | Option 1, pick category, location, 10+ char description | Tracking number `AMS-0000x` |
| 8 | View my complaints | Option 2 | Only your complaints |
| 9 | Privacy | Log in as a new resident, track `AMS-00001` | "not found in your account" |
| 10 | Track | Option 3 with your number (lower case works) | Full details |
| 11 | History | Option 4 | Submitted entry (plus later updates) |
| 12 | Staff login | `staff1` / `Staff123!` | Staff dashboard |
| 13 | View/search | Options 1 and 2 (tracking, category, status) | Tables |
| 14 | Details | Option 3 | Details and history |
| 15 | Assign | Option 4, choose staff | Status Assigned, history entry |
| 16 | Update status | Option 5 -> In Progress, then Resolved | Resolved requires remarks |
| 17 | Remarks | Option 6 | New history entry |
| 18 | Statistics | Option 7 | Counts, open total, rate |
| 19 | Resident sees updates | Log in as the resident, option 4 | New history visible |
| 20 | No MySQL | Stop MySQL, run program | Clear connection error, no crash |

## PART 17 - Common errors and fixes

| Error | Meaning / fix |
|---|---|
| `ModuleNotFoundError: No module named 'mysql'` | Package not installed in the active environment: activate venv, `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'models'` | Run from the project folder with `python src/main.py` |
| `mysql.connector.errors.DatabaseError / InterfaceError` | MySQL not running, wrong host/user/password; shown as a friendly message |
| `ProgrammingError: 1146` | Table missing: run `schema.sql` |
| `ValueError: Invalid complaint status.` | A status outside `Complaint.VALID_STATUSES` was assigned |
| `ValueError: invalid literal for int()` | Non-number typed; `safe_int_input` catches it |
| `TypeError: ... missing 1 required positional argument` | A call has the wrong number of arguments; read the traceback line |
| `AttributeError: 'NoneType' object has no attribute ...` | A query returned `None` (nothing found) and the code used it anyway |
| `KeyError: 'xyz'` | A dictionary key (column name) is misspelled or not selected in the SQL |

**Reading a traceback:** read from the bottom up. The last line is the error type and message; the lines above
show the file and line number where it happened. Set `DEBUG_MODE = True` in `database.py` to see tracebacks for database errors
(the friendly error is still raised with `from error`, so the original cause is preserved).

## PART 18 - Final code review checklist

- [x] Imports resolve (`database` -> `models`, `utils`; `main` -> all three; `models` imports nothing local).
- [x] Every called function exists; every SQL column exists in `schema.sql`.
- [x] All SQL uses `%s` parameters; fixed SQL text is the only thing concatenated.
- [x] Residents only query by their own `user_id` (`get_complaint_by_tracking(tracking, user_id)`).
- [x] Every status change/assignment/remark writes a `complaint_updates` row in the same transaction as the update.
- [x] Passwords are PBKDF2-hashed; input is hidden; login errors do not reveal which part was wrong.
- [x] Menus loop and recover from invalid input; database errors do not crash the program.
- [x] Tested end to end against MariaDB 10.11 (the engine XAMPP uses) on Linux with scripted input: registration, validation, login and lockout, submit, track, resident isolation, search, assign, status updates, required remarks, history and statistics. Not run on Windows 11/XAMPP itself, so do the Part 16 checks once on your machine.
