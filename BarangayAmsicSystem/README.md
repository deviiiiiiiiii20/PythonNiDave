# Barangay Amsic Complaint and Request Tracking System

A Python terminal (CLI) application with a MySQL database. It gives residents of
Barangay Amsic a **formal channel** to submit complaints/service requests and
receive a **tracking number**, and gives barangay staff a central place to review,
assign, update and monitor them. It does not replace Facebook or other channels,
emergency services, or any official decision-making. Scope: Barangay Amsic only.

> School project reference. The test accounts below are for DEVELOPMENT ONLY.

## Features
**Residents:** register, log in, submit a complaint (category, location, description),
get a tracking number (e.g. `AMS-00001`), view their own complaints, track one complaint,
view its update history, log out.

**Staff:** log in, view/search complaints (tracking number, category, status), view details,
assign to staff, update status, add remarks, view statistics, log out.
Every change is saved in `complaint_updates`, so the full history is kept.

## Technologies
Python 3, MySQL (XAMPP's MariaDB also works), `mysql-connector-python`, VS Code, Windows 11.

## Folder structure
```
BarangayAmsicSystem/
├── docs/                     (put System_Documentation.pdf here; see PROJECT_GUIDE.md)
├── src/
│   ├── main.py               menus and user interaction
│   ├── models.py             User, Resident, Staff, Complaint, ComplaintCount
│   ├── database.py           all MySQL code
│   └── utils.py              helper functions (validation, hashing, display)
├── schema.sql                database + tables + test data
├── requirements.txt
└── README.md
```

## Installation
1. Install **Python 3.10+** (tick "Add Python to PATH") and **VS Code**.
2. Install **XAMPP**, open the XAMPP Control Panel and click **Start** next to **MySQL**.
3. Open `http://localhost/phpmyadmin` -> **SQL** tab -> paste the whole `schema.sql` -> **Go**.
   (Run it once. To start over: `DROP DATABASE barangay_amsic;` then run it again.)
4. Open the `BarangayAmsicSystem` folder in VS Code, open a terminal and run:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.

## Database configuration
Open `src/database.py` and edit `DB_CONFIG`. XAMPP's `root` user has an empty password by default:
```python
DB_CONFIG = {"host": "localhost", "user": "root", "password": "", "database": "barangay_amsic"}
```
If your MySQL has a password, put it in `"password"`. Do not share a file containing a real password.
Set `DEBUG_MODE = True` in the same file to print full tracebacks for database errors.

## How to run
From the project folder (with the venv active):
```
python src/main.py
```

## Test accounts (DEVELOPMENT / TEST ONLY)
| Role     | Username  | Password      |
|----------|-----------|---------------|
| Staff    | staff1    | Staff123!     |
| Staff    | staff2    | Staff123!     |
| Resident | resident1 | Resident123!  |

Passwords are stored as PBKDF2 hashes (`salt$hash`), never as plain text. Residents created through
the Registration menu always get the `resident` role; staff accounts only exist through the database.
To create another staff account, generate a hash with:
```
python -c "import sys; sys.path.insert(0, 'src'); from utils import hash_password; print(hash_password('YourPassword1'))"
```
and INSERT it into `users` with `role = 'staff'`.

## How the system works
1. A resident registers and logs in, then submits a complaint -> the system saves it with status
   **Submitted**, creates `AMS-xxxxx`, and records the first history entry.
2. Staff review it, assign it (status **Assigned**), and change the status as work progresses
   (Under Review -> Assigned -> In Progress -> Resolved -> Closed). Resolved/Closed require remarks.
3. The resident tracks it with the tracking number and reads the history.

## Troubleshooting
| Message / problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'mysql'` | Activate the venv, then `pip install -r requirements.txt` |
| "Cannot connect to MySQL" | Start MySQL in XAMPP; check host/port in `DB_CONFIG` |
| "MySQL rejected the username/password" | Fix `user`/`password` in `DB_CONFIG` |
| "Database 'barangay_amsic' does not exist" | Run `schema.sql` |
| `python` not recognised | Reinstall Python with "Add to PATH", or use `py src/main.py` |
| Password typing shows nothing | Normal: the password is hidden while typing |
